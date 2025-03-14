from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db.models import Stock, StockNews
from ..services.news_service import get_stock_news
from datetime import datetime

router = APIRouter()

@router.get("/stocks/{symbol}/news")
async def get_stock_news_endpoint(symbol: str, period: str = "7d", date: str = None, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Get news data from the service
    news_data = get_stock_news(symbol, period, date)
    
    # Handle different response statuses
    if news_data["status"] == "error":
        raise HTTPException(status_code=500, detail=news_data["message"])
    elif news_data["status"] == "rate_limit":
        raise HTTPException(status_code=429, detail=news_data["message"])
    elif news_data["status"] == "partial_success":
        # For partial success, we still process the available data but include the warning
        if "data" not in news_data:
            raise HTTPException(status_code=500, detail="Invalid response format from news service")
    elif news_data["status"] != "success" or "data" not in news_data:
        raise HTTPException(status_code=500, detail="Invalid response format from news service")
    
    # Clear existing news for this stock and period
    db.query(StockNews).filter(StockNews.stock_id == stock.id).delete()
    
    # Add new news data
    new_news = []
    for article in news_data["data"]:
        try:
            news_item = StockNews(
                stock_id=stock.id,
                title=article.get("title", ""),
                description=article.get("description", ""),
                url=article.get("url", ""),
                source=article.get("source", ""),
                published_at=datetime.strptime(article["published_at"], "%Y-%m-%dT%H:%M:%SZ"),
            )
            new_news.append(news_item)
        except (KeyError, ValueError) as e:
            continue  # Skip invalid articles
    
    if not new_news:
        raise HTTPException(status_code=404, detail="No valid news articles found")
    
    db.add_all(new_news)
    db.commit()
    
    # Replace the return statements at the end of get_stock_news_endpoint in news.py:

    # Return serialized data
    response_data = [{
        "title": news.title,
        "description": news.description,
        "url": news.url,
        "source": news.source,
        "published_at": news.published_at.strftime("%Y-%m-%d %H:%M:%S")
    } for news in new_news]
    
    # Include warning in response if present
    if "warning" in news_data and news_data["warning"]:
        return {"data": response_data, "warning": news_data["warning"]}
    
    return {"data": response_data}  # Always return with a data property