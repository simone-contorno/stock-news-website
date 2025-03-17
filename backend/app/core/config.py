import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Stock News API"
    VERSION: str = "1.0.0"
    
    # Detect if running on Render (production environment)
    IS_PRODUCTION: bool = os.getenv("RENDER", "") != ""
    
    # Database configurations
    # Use SQLite for local development, but allow override via env var for production
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./stocknews.db")
    
    # MongoDB configuration with environment-specific defaults
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "stocknews")
    
    # Redis configuration with environment-specific defaults
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # CORS settings for frontend
    # In production, allow requests from Vercel frontend
    # In development, allow requests from local frontend
    CORS_ORIGINS: list = [
        "http://localhost:5173",  # Local Vite development server
        "https://stock-news-website.vercel.app"  # Production Vercel frontend
    ]

    # News API Configuration
    NEWS_API_KEY: str = os.getenv('NEWS_API_KEY')
    NEWS_API_BASE_URL: str = "https://newsapi.org/v2/everything"
    NEWS_API_MAX_RETRIES: int = 1
    NEWS_API_TIMEOUT: int = 10
    
    # Together AI Configuration
    TOGETHER_API_KEY: str = os.getenv('TOGETHER_API_KEY')
    TOGETHER_API_BASE_URL: str = "https://api.together.xyz/v1/chat/completions"
    TOGETHER_API_MODEL: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
    TOGETHER_API_TIMEOUT: int = 120

settings = Settings()