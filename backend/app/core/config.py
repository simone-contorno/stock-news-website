import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Stock News API"
    VERSION: str = "1.0.0"
    
    # Use SQLite for development
    DATABASE_URL: str = "sqlite:///./stocknews.db"
    
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "stocknews")
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # News API Configuration
    NEWS_API_KEY: str = os.getenv('NEWS_API_KEY')
    NEWS_API_BASE_URL: str = "https://newsapi.org/v2/everything"
    NEWS_API_MAX_RETRIES: int = 1
    NEWS_API_TIMEOUT: int = 10
    
    # Together AI Configuration
    TOGETHER_API_KEY: str = os.getenv('TOGETHER_API_KEY')
    TOGETHER_API_BASE_URL: str = "https://api.together.xyz/v1/completions"
    TOGETHER_API_MODEL: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    TOGETHER_API_TIMEOUT: int = 30

settings = Settings()