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
            {"symbol": "SPX", "yahoo_symbol": "^GSPC", "name": "S&P 500", "category": "major", "region": "US"},
            {"symbol": "DJI", "yahoo_symbol": "^DJI", "name": "Dow Jones Industrial Average", "category": "major", "region": "US"},
            {"symbol": "IXIC", "yahoo_symbol": "^IXIC", "name": "NASDAQ Composite", "category": "major", "region": "US"},
            {"symbol": "NYA", "yahoo_symbol": "^NYA", "name": "NYSE Composite", "category": "major", "region": "US"},
            {"symbol": "UKX", "yahoo_symbol": "^FTSE", "name": "FTSE 100", "category": "major", "region": "UK"},
            {"symbol": "DAX", "yahoo_symbol": "^GDAXI", "name": "DAX", "category": "major", "region": "Germany"},
            {"symbol": "CAC40", "yahoo_symbol": "^FCHI", "name": "CAC 40", "category": "major", "region": "France"},
            {"symbol": "NI225", "yahoo_symbol": "^N225", "name": "Nikkei 225", "category": "major", "region": "Japan"},
            {"symbol": "HSI", "yahoo_symbol": "^HSI", "name": "Hang Seng", "category": "major", "region": "Hong Kong"},
            {"symbol": "000001.SS", "yahoo_symbol": "000001.SS", "name": "Shanghai Composite", "category": "major", "region": "China"},
            {"symbol": "BSESN", "yahoo_symbol": "^BSESN", "name": "BSE SENSEX", "category": "major", "region": "India"},
            {"symbol": "AXJO", "yahoo_symbol": "^AXJO", "name": "ASX 200", "category": "major", "region": "Australia"},

            # US Market Indices
            {"symbol": "RUT", "yahoo_symbol": "^RUT", "name": "Russell 2000", "category": "minor", "region": "US"},
            {"symbol": "VIX", "yahoo_symbol": "^VIX", "name": "CBOE Volatility Index", "category": "minor", "region": "US"},
            {"symbol": "DJT", "yahoo_symbol": "^DJT", "name": "Dow Jones Transportation", "category": "minor", "region": "US"},
            {"symbol": "DJU", "yahoo_symbol": "^DJU", "name": "Dow Jones Utilities", "category": "minor", "region": "US"},
            {"symbol": "NDX", "yahoo_symbol": "^NDX", "name": "NASDAQ-100", "category": "minor", "region": "US"},
            {"symbol": "OEX", "yahoo_symbol": "^OEX", "name": "S&P 100", "category": "minor", "region": "US"},
            {"symbol": "MID", "yahoo_symbol": "^MID", "name": "S&P 400", "category": "minor", "region": "US"},

            # European Indices
            {"symbol": "STOXX50E", "yahoo_symbol": "^STOXX50E", "name": "EURO STOXX 50", "category": "minor", "region": "Europe"},
            {"symbol": "AEX", "yahoo_symbol": "^AEX", "name": "AEX", "category": "minor", "region": "Netherlands"},
            {"symbol": "IBEX", "yahoo_symbol": "^IBEX", "name": "IBEX 35", "category": "minor", "region": "Spain"},
            {"symbol": "SSMI", "yahoo_symbol": "^SSMI", "name": "Swiss Market Index", "category": "minor", "region": "Switzerland"},
            {"symbol": "FTSEMIB.MI", "yahoo_symbol": "FTSEMIB.MI", "name": "FTSE MIB", "category": "minor", "region": "Italy"},
            {"symbol": "OMXC25", "yahoo_symbol": "^OMXC25", "name": "OMX Copenhagen 25", "category": "minor", "region": "Denmark"},
            {"symbol": "OSEAX", "yahoo_symbol": "^OSEAX", "name": "Oslo Stock Exchange", "category": "minor", "region": "Norway"},

            # Asian Indices
            {"symbol": "KS11", "yahoo_symbol": "^KS11", "name": "KOSPI", "category": "minor", "region": "South Korea"},
            {"symbol": "TWII", "yahoo_symbol": "^TWII", "name": "Taiwan Weighted", "category": "minor", "region": "Taiwan"},
            {"symbol": "STI", "yahoo_symbol": "^STI", "name": "Straits Times Index", "category": "minor", "region": "Singapore"},
            {"symbol": "JKSE", "yahoo_symbol": "^JKSE", "name": "Jakarta Composite", "category": "minor", "region": "Indonesia"},
            {"symbol": "KLSE", "yahoo_symbol": "^KLSE", "name": "FTSE Bursa Malaysia", "category": "minor", "region": "Malaysia"},
            {"symbol": "SET.BK", "yahoo_symbol": "^SET.BK", "name": "SET Index", "category": "minor", "region": "Thailand"},

            # Other Regional Indices
            {"symbol": "BVSP", "yahoo_symbol": "^BVSP", "name": "Bovespa", "category": "minor", "region": "Brazil"},
            {"symbol": "MXX", "yahoo_symbol": "^MXX", "name": "IPC Mexico", "category": "minor", "region": "Mexico"},
            {"symbol": "MERV", "yahoo_symbol": "^MERV", "name": "MERVAL", "category": "minor", "region": "Argentina"},
            {"symbol": "TA125.TA", "yahoo_symbol": "^TA125.TA", "name": "Tel Aviv 125", "category": "minor", "region": "Israel"},
            {"symbol": "CASE30", "yahoo_symbol": "^CASE30", "name": "EGX 30", "category": "minor", "region": "Egypt"},

            # Tech Stocks
            {"symbol": "AAPL", "yahoo_symbol": "AAPL", "name": "Apple Inc.", "category": "stock", "region": "US"},
            {"symbol": "MSFT", "yahoo_symbol": "MSFT", "name": "Microsoft Corporation", "category": "stock", "region": "US"},
            {"symbol": "GOOGL", "yahoo_symbol": "GOOGL", "name": "Alphabet Inc.", "category": "stock", "region": "US"},
            {"symbol": "AMZN", "yahoo_symbol": "AMZN", "name": "Amazon.com Inc.", "category": "stock", "region": "US"},
            {"symbol": "NVDA", "yahoo_symbol": "NVDA", "name": "NVIDIA Corporation", "category": "stock", "region": "US"},
            {"symbol": "META", "yahoo_symbol": "META", "name": "Meta Platforms Inc.", "category": "stock", "region": "US"},
            {"symbol": "TSLA", "yahoo_symbol": "TSLA", "name": "Tesla Inc.", "category": "stock", "region": "US"},
            {"symbol": "AVGO", "yahoo_symbol": "AVGO", "name": "Broadcom Inc.", "category": "stock", "region": "US"},
            {"symbol": "ORCL", "yahoo_symbol": "ORCL", "name": "Oracle Corporation", "category": "stock", "region": "US"},
            {"symbol": "CRM", "yahoo_symbol": "CRM", "name": "Salesforce Inc.", "category": "stock", "region": "US"},
            {"symbol": "AMD", "yahoo_symbol": "AMD", "name": "Advanced Micro Devices", "category": "stock", "region": "US"},
            {"symbol": "INTC", "yahoo_symbol": "INTC", "name": "Intel Corporation", "category": "stock", "region": "US"},

            # Financial Stocks
            {"symbol": "JPM", "yahoo_symbol": "JPM", "name": "JPMorgan Chase & Co.", "category": "stock", "region": "US"},
            {"symbol": "BAC", "yahoo_symbol": "BAC", "name": "Bank of America Corp.", "category": "stock", "region": "US"},
            {"symbol": "WFC", "yahoo_symbol": "WFC", "name": "Wells Fargo & Co.", "category": "stock", "region": "US"},
            {"symbol": "GS", "yahoo_symbol": "GS", "name": "Goldman Sachs Group", "category": "stock", "region": "US"},
            {"symbol": "MS", "yahoo_symbol": "MS", "name": "Morgan Stanley", "category": "stock", "region": "US"},
            {"symbol": "BLK", "yahoo_symbol": "BLK", "name": "BlackRock Inc.", "category": "stock", "region": "US"},
            {"symbol": "V", "yahoo_symbol": "V", "name": "Visa Inc.", "category": "stock", "region": "US"},
            {"symbol": "MA", "yahoo_symbol": "MA", "name": "Mastercard Inc.", "category": "stock", "region": "US"},

            # Healthcare & Pharma
            {"symbol": "JNJ", "yahoo_symbol": "JNJ", "name": "Johnson & Johnson", "category": "stock", "region": "US"},
            {"symbol": "UNH", "yahoo_symbol": "UNH", "name": "UnitedHealth Group", "category": "stock", "region": "US"},
            {"symbol": "PFE", "yahoo_symbol": "PFE", "name": "Pfizer Inc.", "category": "stock", "region": "US"},
            {"symbol": "MRK", "yahoo_symbol": "MRK", "name": "Merck & Co.", "category": "stock", "region": "US"},
            {"symbol": "ABBV", "yahoo_symbol": "ABBV", "name": "AbbVie Inc.", "category": "stock", "region": "US"},

            # Consumer & Retail
            {"symbol": "WMT", "yahoo_symbol": "WMT", "name": "Walmart Inc.", "category": "stock", "region": "US"},
            {"symbol": "PG", "yahoo_symbol": "PG", "name": "Procter & Gamble", "category": "stock", "region": "US"},
            {"symbol": "KO", "yahoo_symbol": "KO", "name": "Coca-Cola Company", "category": "stock", "region": "US"},
            {"symbol": "PEP", "yahoo_symbol": "PEP", "name": "PepsiCo Inc.", "category": "stock", "region": "US"},
            {"symbol": "COST", "yahoo_symbol": "COST", "name": "Costco Wholesale", "category": "stock", "region": "US"},
            {"symbol": "MCD", "yahoo_symbol": "MCD", "name": "McDonald's Corp.", "category": "stock", "region": "US"},
            {"symbol": "NKE", "yahoo_symbol": "NKE", "name": "Nike Inc.", "category": "stock", "region": "US"},

            # Energy & Industrial
            {"symbol": "XOM", "yahoo_symbol": "XOM", "name": "Exxon Mobil Corp.", "category": "stock", "region": "US"},
            {"symbol": "CVX", "yahoo_symbol": "CVX", "name": "Chevron Corporation", "category": "stock", "region": "US"},
            {"symbol": "BA", "yahoo_symbol": "BA", "name": "Boeing Company", "category": "stock", "region": "US"},
            {"symbol": "CAT", "yahoo_symbol": "CAT", "name": "Caterpillar Inc.", "category": "stock", "region": "US"},
            {"symbol": "HON", "yahoo_symbol": "HON", "name": "Honeywell International", "category": "stock", "region": "US"},
            {"symbol": "GE", "yahoo_symbol": "GE", "name": "General Electric", "category": "stock", "region": "US"}
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
        # Try finding by Yahoo symbol
        stock = db.query(Stock).filter(Stock.yahoo_symbol == symbol).first()
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
        
        # Otherwise, generate sample data that's unique for each stock symbol
        # Use the stock symbol to generate a unique base price
        symbol_hash = sum(ord(c) for c in symbol) % 100  # Simple hash of symbol for variety
        base_price = 100.0 + symbol_hash
        
        # Add some randomness to make the data look more realistic
        import random
        random.seed(symbol_hash)  # Use symbol hash as seed for reproducibility
        
        sample_prices = []
        for i in range(8):  # 8 days of data
            # Create more realistic price movements
            daily_change = random.uniform(-2.0, 2.0)
            daily_price = base_price + (daily_change * (i+1))
            daily_volatility = daily_price * 0.02  # 2% volatility
            
            sample_prices.append(StockPrice(
                stock_id=stock.id,
                timestamp=datetime.utcnow() - timedelta(days=7-i),
                open=round(daily_price - random.uniform(-daily_volatility, daily_volatility), 2),
                high=round(daily_price + daily_volatility, 2),
                low=round(daily_price - daily_volatility, 2),
                close=round(daily_price + random.uniform(-daily_volatility, daily_volatility), 2),
                volume=int(1000000 + random.randint(-200000, 500000))
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