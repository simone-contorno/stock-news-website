from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)  # Alpha Vantage symbol
    yahoo_symbol = Column(String)  # Yahoo Finance symbol
    name = Column(String)
    category = Column(String, default='stock')  # 'major', 'minor'
    region = Column(String, default='US')
    last_updated = Column(DateTime, default=datetime.utcnow)

class StockPrice(Base):
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

class StockNews(Base):
    __tablename__ = "stock_news"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    title = Column(String)
    description = Column(Text)
    url = Column(String)
    source = Column(String)
    published_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)