from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import stocks, news

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stocks.router, prefix="/api")
app.include_router(news.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Stock News API"}