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
    
    # Get news data
    news_data = get_stock_news(symbol, period, date)
    
    # Handle different response statuses for news
    if news_data["status"] == "error":
        raise HTTPException(status_code=500, detail=news_data["message"])
    elif news_data["status"] == "rate_limit":
        raise HTTPException(status_code=429, detail=news_data["message"])
    elif news_data["status"] != "success" or "data" not in news_data:
        raise HTTPException(status_code=500, detail="Invalid response format from news service")
    
    # Get stock price data
    try:
        price_data = get_stock_data(symbol, period)
        if not price_data or "data" not in price_data:
            raise HTTPException(status_code=500, detail="Failed to fetch stock price data")
        
        price_history = price_data["data"]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")
    
    # Generate summary using Together AI
    summary_result = generate_news_summary(symbol, news_data["data"], price_history)
    
    if summary_result["status"] == "error":
        raise HTTPException(status_code=500, detail=summary_result["message"])
    
    # Return the summary data
    return summary_result