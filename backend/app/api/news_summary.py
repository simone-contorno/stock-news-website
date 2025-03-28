from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..db.database import get_db
from ..db.models import Stock, StockNews, StockPrice
from ..services.ai_service import generate_news_summary
from ..services.stock_service import get_stock_data
from ..services.news_service import get_stock_news

router = APIRouter()

@router.get("/stocks/{symbol}/news-summary")
async def get_stock_news_summary(symbol: str, period: str = "7d", date: str = None, db: Session = Depends(get_db)):
    # Verify stock exists
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Get news data with better error handling
    try:
        news_data = get_stock_news(symbol, period, date)
        
        # Handle different response statuses for news
        if news_data["status"] == "error":
            raise HTTPException(status_code=500, detail=news_data["message"])
        elif news_data["status"] == "rate_limit":
            # Return a more graceful response for rate limits
            return {
                "status": "rate_limit",
                "message": news_data["message"],
                "data": {
                    "formatted_text": "<div class='error-message'><h2>News API Rate Limit Reached</h2><p>We've reached our daily limit for news data. Please try again later.</p></div>"
                }
            }
        elif news_data["status"] != "success" and news_data["status"] != "partial_success":
            raise HTTPException(status_code=500, detail="Invalid response format from news service")
        
        if "data" not in news_data:
            raise HTTPException(status_code=500, detail="No news data available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news data: {str(e)}")
    
    # Get stock price data with better error handling
    try:
        price_data = get_stock_data(symbol, period)
        if not price_data or "data" not in price_data:
            # Return an error message instead of generating sample data
            return {
                "status": "error",
                "message": "Failed to retrieve stock price data",
                "data": {
                    "formatted_text": "<div class='error-message'><h2>Stock Data Error</h2><p>We couldn't retrieve the stock price data at this time. Please try again later.</p></div>"
                }
            }
        else:
            price_history = price_data["data"]
    except HTTPException as e:
        if e.status_code == 429:  # Rate limit error
            return {
                "status": "rate_limit",
                "message": "Yahoo Finance API rate limit reached",
                "data": {
                    "formatted_text": "<div class='error-message'><h2>Yahoo Finance API Rate Limit Reached</h2><p>We've reached the rate limit for stock data. Please try again later.</p></div>"
                }
            }
        raise e
    except Exception as e:
        # Log the error and return an error message
        import logging
        logging.error(f"Error fetching stock data: {str(e)}")
        
        return {
            "status": "error",
            "message": f"Failed to retrieve stock data: {str(e)}",
            "data": {
                "formatted_text": f"<div class='error-message'><h2>Stock Data Error</h2><p>We couldn't retrieve the stock price data: {str(e)}. Please try again later.</p></div>"
            }
        }
    
    # Generate summary using Together AI with better error handling
    try:
        summary_result = generate_news_summary(symbol, news_data["data"], price_history, date)
        
        if summary_result["status"] == "error":
            # Return a formatted error message instead of throwing an exception
            return {
                "status": "error",
                "message": summary_result["message"],
                "data": {
                    "formatted_text": f"<div class='error-message'><h2>AI Summary Error</h2><p>{summary_result['message']}</p><p>We're still showing you the news articles below.</p></div>"
                }
            }
        
        # Return the summary data
        return summary_result
    except Exception as e:
        # Return a formatted error message
        return {
            "status": "error",
            "message": str(e),
            "data": {
                "formatted_text": f"<div class='error-message'><h2>AI Summary Error</h2><p>An error occurred while generating the summary: {str(e)}</p><p>We're still showing you the news articles below.</p></div>"
            }
        }