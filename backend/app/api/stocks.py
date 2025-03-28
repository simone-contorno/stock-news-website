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
            {"symbol": "^NYA", "name": "NYSE Composite", "category": "major", "region": "US"},
            {"symbol": "^FTSE", "name": "FTSE 100", "category": "major", "region": "UK"},
            {"symbol": "^GDAXI", "name": "DAX", "category": "major", "region": "Germany"},
            {"symbol": "^FCHI", "name": "CAC 40", "category": "major", "region": "France"},
            {"symbol": "^N225", "name": "Nikkei 225", "category": "major", "region": "Japan"},
            {"symbol": "^HSI", "name": "Hang Seng", "category": "major", "region": "Hong Kong"},
            {"symbol": "000001.SS", "name": "Shanghai Composite", "category": "major", "region": "China"},
            {"symbol": "^BSESN", "name": "BSE SENSEX", "category": "major", "region": "India"},
            {"symbol": "^AXJO", "name": "ASX 200", "category": "major", "region": "Australia"},

            # US Market Indices
            {"symbol": "^RUT", "name": "Russell 2000", "category": "minor", "region": "US"},
            {"symbol": "^VIX", "name": "CBOE Volatility Index", "category": "minor", "region": "US"},
            {"symbol": "^DJT", "name": "Dow Jones Transportation", "category": "minor", "region": "US"},
            {"symbol": "^DJU", "name": "Dow Jones Utilities", "category": "minor", "region": "US"},
            {"symbol": "^NDX", "name": "NASDAQ-100", "category": "minor", "region": "US"},
            {"symbol": "^OEX", "name": "S&P 100", "category": "minor", "region": "US"},
            {"symbol": "^MID", "name": "S&P 400", "category": "minor", "region": "US"},

            # European Indices
            {"symbol": "^STOXX50E", "name": "EURO STOXX 50", "category": "minor", "region": "Europe"},
            {"symbol": "^AEX", "name": "AEX", "category": "minor", "region": "Netherlands"},
            {"symbol": "^IBEX", "name": "IBEX 35", "category": "minor", "region": "Spain"},
            {"symbol": "^SSMI", "name": "Swiss Market Index", "category": "minor", "region": "Switzerland"},
            {"symbol": "FTSEMIB.MI", "name": "FTSE MIB", "category": "minor", "region": "Italy"},
            {"symbol": "^OMXC25", "name": "OMX Copenhagen 25", "category": "minor", "region": "Denmark"},
            {"symbol": "^OSEAX", "name": "Oslo Stock Exchange", "category": "minor", "region": "Norway"},

            # Asian Indices
            {"symbol": "^KS11", "name": "KOSPI", "category": "minor", "region": "South Korea"},
            {"symbol": "^TWII", "name": "Taiwan Weighted", "category": "minor", "region": "Taiwan"},
            {"symbol": "^STI", "name": "Straits Times Index", "category": "minor", "region": "Singapore"},
            {"symbol": "^JKSE", "name": "Jakarta Composite", "category": "minor", "region": "Indonesia"},
            {"symbol": "^KLSE", "name": "FTSE Bursa Malaysia", "category": "minor", "region": "Malaysia"},
            {"symbol": "^SET.BK", "name": "SET Index", "category": "minor", "region": "Thailand"},

            # Other Regional Indices
            {"symbol": "^BVSP", "name": "Bovespa", "category": "minor", "region": "Brazil"},
            {"symbol": "^MXX", "name": "IPC Mexico", "category": "minor", "region": "Mexico"},
            {"symbol": "^MERV", "name": "MERVAL", "category": "minor", "region": "Argentina"},
            {"symbol": "^TA125.TA", "name": "Tel Aviv 125", "category": "minor", "region": "Israel"},
            {"symbol": "^CASE30", "name": "EGX 30", "category": "minor", "region": "Egypt"},

            # Tech Stocks
            {"symbol": "AAPL", "name": "Apple Inc.", "category": "stock", "region": "US"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "category": "stock", "region": "US"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "category": "stock", "region": "US"},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "category": "stock", "region": "US"},
            {"symbol": "NVDA", "name": "NVIDIA Corporation", "category": "stock", "region": "US"},
            {"symbol": "META", "name": "Meta Platforms Inc.", "category": "stock", "region": "US"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "category": "stock", "region": "US"},
            {"symbol": "AVGO", "name": "Broadcom Inc.", "category": "stock", "region": "US"},
            {"symbol": "ORCL", "name": "Oracle Corporation", "category": "stock", "region": "US"},
            {"symbol": "CRM", "name": "Salesforce Inc.", "category": "stock", "region": "US"},
            {"symbol": "AMD", "name": "Advanced Micro Devices", "category": "stock", "region": "US"},
            {"symbol": "INTC", "name": "Intel Corporation", "category": "stock", "region": "US"},

            # Financial Stocks
            {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "category": "stock", "region": "US"},
            {"symbol": "BAC", "name": "Bank of America Corp.", "category": "stock", "region": "US"},
            {"symbol": "WFC", "name": "Wells Fargo & Co.", "category": "stock", "region": "US"},
            {"symbol": "GS", "name": "Goldman Sachs Group", "category": "stock", "region": "US"},
            {"symbol": "MS", "name": "Morgan Stanley", "category": "stock", "region": "US"},
            {"symbol": "BLK", "name": "BlackRock Inc.", "category": "stock", "region": "US"},
            {"symbol": "V", "name": "Visa Inc.", "category": "stock", "region": "US"},
            {"symbol": "MA", "name": "Mastercard Inc.", "category": "stock", "region": "US"},

            # Healthcare & Pharma
            {"symbol": "JNJ", "name": "Johnson & Johnson", "category": "stock", "region": "US"},
            {"symbol": "UNH", "name": "UnitedHealth Group", "category": "stock", "region": "US"},
            {"symbol": "PFE", "name": "Pfizer Inc.", "category": "stock", "region": "US"},
            {"symbol": "MRK", "name": "Merck & Co.", "category": "stock", "region": "US"},
            {"symbol": "ABBV", "name": "AbbVie Inc.", "category": "stock", "region": "US"},

            # Consumer & Retail
            {"symbol": "WMT", "name": "Walmart Inc.", "category": "stock", "region": "US"},
            {"symbol": "PG", "name": "Procter & Gamble", "category": "stock", "region": "US"},
            {"symbol": "KO", "name": "Coca-Cola Company", "category": "stock", "region": "US"},
            {"symbol": "PEP", "name": "PepsiCo Inc.", "category": "stock", "region": "US"},
            {"symbol": "COST", "name": "Costco Wholesale", "category": "stock", "region": "US"},
            {"symbol": "MCD", "name": "McDonald's Corp.", "category": "stock", "region": "US"},
            {"symbol": "NKE", "name": "Nike Inc.", "category": "stock", "region": "US"},

            # Energy & Industrial
            {"symbol": "XOM", "name": "Exxon Mobil Corp.", "category": "stock", "region": "US"},
            {"symbol": "CVX", "name": "Chevron Corporation", "category": "stock", "region": "US"},
            {"symbol": "BA", "name": "Boeing Company", "category": "stock", "region": "US"},
            {"symbol": "CAT", "name": "Caterpillar Inc.", "category": "stock", "region": "US"},
            {"symbol": "HON", "name": "Honeywell International", "category": "stock", "region": "US"},
            {"symbol": "GE", "name": "General Electric", "category": "stock", "region": "US"}
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
    
    # Get stock data from cache or Yahoo Finance if needed
    try:
        # Pass the symbol to get_stock_data which will use cache when available
        stock_data = get_stock_data(symbol, period=period)
        
        # Check if we already have prices for this stock and period in the database
        existing_prices = db.query(StockPrice).filter(StockPrice.stock_id == stock.id).all()
        
        # Only clear and update if we have new data or no existing data
        if not existing_prices or len(existing_prices) != len(stock_data["data"]):
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
        if 'new_prices' in locals():
            # If we just updated the database, return the new prices
            return [{
                "timestamp": price.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "open": float(price.open) if price.open is not None else None,
                "high": float(price.high) if price.high is not None else None,
                "low": float(price.low) if price.low is not None else None,
                "close": float(price.close) if price.close is not None else None,
                "volume": int(price.volume) if price.volume is not None else None
            } for price in new_prices]
        else:
            # If we're using cached data without updating the database, query the prices
            prices = db.query(StockPrice).filter(StockPrice.stock_id == stock.id).all()
            return [{
                "timestamp": price.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "open": float(price.open) if price.open is not None else None,
                "high": float(price.high) if price.high is not None else None,
                "low": float(price.low) if price.low is not None else None,
                "close": float(price.close) if price.close is not None else None,
                "volume": int(price.volume) if price.volume is not None else None
            } for price in prices]
    except Exception as e:
        # If there's an error, check if we have existing prices in the database
        prices = db.query(StockPrice).filter(StockPrice.stock_id == stock.id).all()
        if prices:
            # Use existing prices if available
            return [{
                "timestamp": price.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "open": float(price.open) if price.open is not None else None,
                "high": float(price.high) if price.high is not None else None,
                "low": float(price.low) if price.low is not None else None,
                "close": float(price.close) if price.close is not None else None,
                "volume": int(price.volume) if price.volume is not None else None
            } for price in prices]
        
        # If no data can be retrieved, raise an error
        raise HTTPException(
            status_code=503, 
            detail=f"Unable to retrieve stock price data for {symbol}: {str(e)}"
        )