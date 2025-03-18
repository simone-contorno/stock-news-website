from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from ..core.config import settings
from .models import Base
import os

# SQLite setup
db_path = "stocknews.db"
if os.path.exists(db_path):
    os.remove(db_path)  # Remove existing database to apply new schema

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
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