from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db.models import Stock, StockPrice
from ..services.stock_service import get_stock_data
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stocks/")
async def get_stocks(db: Session = Depends(get_db)):
    stocks = db.query(Stock).all()
    if not stocks:
        indices = [
            # Major Global Indices
            {"symbol": "^GSPC", "name": "S&P 500", "category": "major", "region": "US"},
            {"symbol": "^DJI", "name": "Dow Jones Industrial Average", "category": "major", "region": "US"},
            {"symbol": "^IXIC", "name": "NASDAQ Composite", "category": "major", "region": "US"},
            {"symbol": "^FTSE", "name": "FTSE 100", "category": "major", "region": "UK"},
            {"symbol": "^GDAXI", "name": "DAX", "category": "major", "region": "Germany"},
            {"symbol": "^FCHI", "name": "CAC 40", "category": "major", "region": "France"},
            {"symbol": "^N225", "name": "Nikkei 225", "category": "major", "region": "Japan"},
            {"symbol": "^HSI", "name": "Hang Seng", "category": "major", "region": "Hong Kong"},
            {"symbol": "000001.SS", "name": "Shanghai Composite", "category": "major", "region": "China"},
            {"symbol": "^BSESN", "name": "BSE SENSEX", "category": "major", "region": "India"},

            # Minor/Regional Indices
            {"symbol": "^RUT", "name": "Russell 2000", "category": "minor", "region": "US"},
            {"symbol": "^VIX", "name": "CBOE Volatility Index", "category": "minor", "region": "US"},
            {"symbol": "^STOXX50E", "name": "EURO STOXX 50", "category": "minor", "region": "Europe"},
            {"symbol": "^AEX", "name": "AEX", "category": "minor", "region": "Netherlands"},
            {"symbol": "^IBEX", "name": "IBEX 35", "category": "minor", "region": "Spain"},
            {"symbol": "^SSMI", "name": "Swiss Market Index", "category": "minor", "region": "Switzerland"},
            {"symbol": "^AXJO", "name": "ASX 200", "category": "minor", "region": "Australia"},
            {"symbol": "^KS11", "name": "KOSPI", "category": "minor", "region": "South Korea"},
            {"symbol": "^TWII", "name": "Taiwan Weighted", "category": "minor", "region": "Taiwan"},
            {"symbol": "^BVSP", "name": "Bovespa", "category": "minor", "region": "Brazil"},

            # Major Tech Stocks
            {"symbol": "AAPL", "name": "Apple Inc.", "category": "stock", "region": "US"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "category": "stock", "region": "US"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "category": "stock", "region": "US"},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "category": "stock", "region": "US"},
            {"symbol": "NVDA", "name": "NVIDIA Corporation", "category": "stock", "region": "US"},
            {"symbol": "META", "name": "Meta Platforms Inc.", "category": "stock", "region": "US"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "category": "stock", "region": "US"},

            # Major Financial Stocks
            {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "category": "stock", "region": "US"},
            {"symbol": "BAC", "name": "Bank of America Corp.", "category": "stock", "region": "US"},
            {"symbol": "V", "name": "Visa Inc.", "category": "stock", "region": "US"},

            # Other Major Stocks
            {"symbol": "JNJ", "name": "Johnson & Johnson", "category": "stock", "region": "US"},
            {"symbol": "WMT", "name": "Walmart Inc.", "category": "stock", "region": "US"},
            {"symbol": "PG", "name": "Procter & Gamble Co.", "category": "stock", "region": "US"},
            {"symbol": "XOM", "name": "Exxon Mobil Corp.", "category": "stock", "region": "US"},
            {"symbol": "KO", "name": "Coca-Cola Company", "category": "stock", "region": "US"}
        ]
        
        sample_stocks = [Stock(**data) for data in indices]
        db.add_all(sample_stocks)
        db.commit()
        stocks = sample_stocks

    return stocks

@router.get("/stocks/{symbol}/prices")
async def get_stock_prices(symbol: str, period: str = "7d", db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Validate period parameter
    valid_periods = ["7d", "1mo", "1y", "3y", "5y", "max"]
    if period not in valid_periods:
        raise HTTPException(status_code=400, detail=f"Invalid period. Must be one of: {', '.join(valid_periods)}")
    
    # Get real stock data from Yahoo Finance
    try:
        stock_data = get_stock_data(symbol, period=period)
        
        # Clear existing prices for this stock
        db.query(StockPrice).filter(StockPrice.stock_id == stock.id).delete()
        
        # Add new price data
        new_prices = []
        for price_data in stock_data["data"]:
            new_price = StockPrice(
                stock_id=stock.id,
                timestamp=datetime.strptime(price_data["timestamp"], "%Y-%m-%d %H:%M:%S"),
                open=price_data["open"],
                high=price_data["high"],
                low=price_data["low"],
                close=price_data["close"],
                volume=price_data["volume"]
            )
            new_prices.append(new_price)
        
        db.add_all(new_prices)
        db.commit()
        
        # Return serialized data
        return [{
            "timestamp": price.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "open": float(price.open),
            "high": float(price.high),
            "low": float(price.low),
            "close": float(price.close),
            "volume": int(price.volume)
        } for price in new_prices]
    except Exception as e:
        # If there's an error, check if we have existing prices in the database
        prices = db.query(StockPrice).filter(StockPrice.stock_id == stock.id).all()
        if prices:
            # Use existing prices if available
            return [{
                "timestamp": price.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "open": float(price.open),
                "high": float(price.high),
                "low": float(price.low),
                "close": float(price.close),
                "volume": int(price.volume)
            } for price in prices]
        
        # Otherwise, generate sample data
        base_price = 150.0
        sample_prices = []
        for i in range(8):  # Changed from 7 to 8 to include today
            sample_prices.append(StockPrice(
                stock_id=stock.id,
                timestamp=datetime.utcnow() - timedelta(days=7-i),  # Changed to start from 7 days ago
                open=base_price - i,
                high=base_price - i + 2,
                low=base_price - i - 2,
                close=base_price - i + 1,
                volume=1000000 + i * 10000
            ))
        db.add_all(sample_prices)
        db.commit()
        
        # Return the sample prices
        return [{
            "timestamp": price.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "open": float(price.open),
            "high": float(price.high),
            "low": float(price.low),
            "close": float(price.close),
            "volume": int(price.volume)
        } for price in sample_prices]