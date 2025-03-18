from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from ..core.config import settings
from .models import Base
import os

# SQLite setup
db_path = "stocknews.db"

# Only reset the database in development mode
if not settings.IS_PRODUCTION and os.path.exists(db_path):
    os.remove(db_path)  # Remove existing database to apply new schema

# Configure SQLAlchemy engine with appropriate options
# For SQLite, we need check_same_thread=False
# For other databases (PostgreSQL, etc.), we don't need this option
connect_args = {}
if settings.DATABASE_URL.startswith('sqlite'):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
Base.metadata.create_all(bind=engine)  # Create new tables with updated schema
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# MongoDB setup
mongo_client = MongoClient(settings.MONGODB_URL)
mongo_db = mongo_client[settings.MONGODB_DB]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_mongo_db():
    return mongo_db