# AI Stock News Website 

A web application that displays daily performance of stock indices and individual stocks using interactive graphs, along with relevant news articles that may influence market movements. The system leverages artificial intelligence to combine news sentiment analysis with stock price data, enabling more accurate market evaluation and predictive insights. This innovative approach helps users identify correlations between financial news and market movements, providing a comprehensive tool for investment decision-making. This project has been entirely developed using AI Clause 3.7-Sonnet to explore the potentiality of AI today for web development.

## Features

- Interactive stock price charts with various timeframes
- Daily stock market news with sentiment analysis
- Correlation between news sentiment and stock price movements
- AI-powered market evaluation and prediction
- Responsive design for desktop and mobile devices

## AI-Driven Analytics

The application utilizes advanced artificial intelligence to provide valuable insights:

- **News Sentiment Analysis**: AI algorithms analyze financial news articles to determine positive, negative, or neutral sentiment
- **Stock-News Correlation**: The system identifies relationships between news sentiment and stock price movements
- **Predictive Analytics**: By combining historical stock data with news sentiment patterns, the AI generates potential market trend predictions
- **Automated Evaluation**: The AI continuously evaluates current market conditions based on real-time news and stock performance

This AI-driven approach helps investors make more informed decisions by understanding how news events might impact their investments.

## Technology Stack

### Backend
- Python 3.9+ with FastAPI
- SQLite for development database
- News API for real-time financial news
- Yahoo Finance API for stock data

### Frontend
- React 18+ with Vite
- Redux Toolkit for state management
- Material-UI (MUI) for components
- Highcharts for interactive stock charts

## Installation & Setup

### Prerequisites

- Python 3.9+
- Node.js 14+
- News API key (from newsapi.org)
- Together AI API key (optional, for enhanced sentiment analysis)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory:
   ```
   # Required
   NEWS_API_KEY=your_news_api_key_here
   
   # Optional - only needed for enhanced sentiment analysis
   TOGETHER_API_KEY=your_together_api_key_here
   
   # Optional - defaults will work for local development
   # DATABASE_URL=sqlite:///./stock_news.db
   # MONGODB_URL=mongodb://localhost:27017
   # MONGODB_DB=stocknews
   # REDIS_URL=redis://localhost:6379
   ```
   Replace the placeholder values with your actual API keys.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies to create the node_modules folder:
   ```bash
   npm install
   ```
   This will install all required dependencies specified in package.json.

## Running the Application

### Method 1: Using the Start Scripts

The project includes Python scripts to easily start both the frontend and backend servers.

1. Start the backend server:
   ```bash
   # From the project root directory
   python start_backend.py
   ```
   The backend API will be available at http://localhost:8000

2. Start the frontend development server:
   ```bash
   # From the project root directory
   python start_frontend.py
   ```
   The frontend application will be available at http://localhost:5173

### Method 2: Manual Startup

Alternatively, you can start the servers manually:

1. Start the backend server:
   ```bash
   # Navigate to the backend directory
   cd backend
   
   # Make sure your virtual environment is activated
   # On Windows: venv\Scripts\activate
   # On macOS/Linux: source venv/bin/activate
   
   # Start the server
   uvicorn app.main:app --reload
   ```
   The API will be available at http://localhost:8000

2. Start the frontend development server:
   ```bash
   # Navigate to the frontend directory
   cd frontend
   
   # Start the development server
   npm run dev
   ```
   The application will be available at http://localhost:5173

### Getting a News API Key

1. Sign up for a free account at [newsapi.org](https://newsapi.org)
2. After registration, get your API key from the dashboard
3. Add your API key to the `.env` file in the backend directory

### Getting a Together AI API Key (Optional)

1. Sign up for an account at [together.ai](https://together.ai)
2. After registration, get your API key from the dashboard
3. Add your API key to the `.env` file in the backend directory

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints for stocks and news
│   │   ├── core/         # Configuration and settings
│   │   ├── db/           # Database models and connection
│   │   └── services/     # Stock and news data services
│   ├── .env              # Environment variables
│   └── requirements.txt  # Python dependencies
└── frontend/
    ├── src/
    │   ├── components/   # Reusable React components
    │   ├── pages/        # Page components
    │   ├── store/        # Redux store configuration
    │   └── theme.js      # MUI theme configuration
    ├── package.json      # NPM dependencies
    └── vite.config.js    # Vite configuration
```

## Development Notes

- The backend uses SQLite for development through `stock_news.db` file which:
  - Stores stock information (symbols and names)
  - Caches stock price history data
  - Stores news articles related to stocks
  - Tables structure:
    - `stocks`: Basic stock information (id, symbol, name)
    - `stock_prices`: Historical price data (open, high, low, close, volume)
    - `stock_news`: News articles with metadata (title, description, url, source)
  - Located at `backend/stock_news.db` (auto-created on first run)
  - Serves as a local cache to reduce API calls
- Stock data is fetched from Yahoo Finance API through the `yfinance` library
- News data is fetched from News API with rate limiting (1000 requests per day for free tier)
- The frontend uses Vite for faster development and better performance
- Material-UI is used for consistent styling and responsive design
- Highcharts provides interactive stock price visualization

## License

MIT