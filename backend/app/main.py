from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import stocks, news, news_summary

app = FastAPI()

# Ensure the app is properly initialized

# Configure CORS with origins from settings
from .core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stocks.router, prefix="/api")
app.include_router(news.router, prefix="/api")
app.include_router(news_summary.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Stock News API"}

@app.get("/api")
async def api_root():
    return {
        "message": "Stock News API",
        "version": settings.VERSION,
        "endpoints": [
            "/api/stocks",
            "/api/stocks/{symbol}/news",
            "/api/stocks/{symbol}/news-summary"
        ]
    }