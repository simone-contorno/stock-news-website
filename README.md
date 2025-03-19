# Stock News Website with Interactive Graphs

A web application that displays daily performance of stock indices and individual stocks using interactive graphs, along with relevant news articles that may influence market movements.

## Features

- Interactive stock price charts with various timeframes
- Daily stock market news with sentiment analysis
- Correlation between news sentiment and stock price movements
- Responsive design for desktop and mobile devices

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
   ```bash
   # backend/.env
   NEWS_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual API key from newsapi.org

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```
   This will create the node_modules folder with all required dependencies

### Running the Application

1. Start the backend server (from the backend directory):
   ```bash
   # Make sure your virtual environment is activated
   uvicorn app.main:app --reload
   ```
   The API will be available at http://localhost:8000

2. Start the frontend development server (from the frontend directory):
   ```bash
   npm run dev
   ```
   The application will be available at http://localhost:5173

### Getting a News API Key

1. Sign up for a free account at [newsapi.org](https://newsapi.org)
2. After registration, get your API key from the dashboard
3. Create a `.env` file in the backend directory if it doesn't exist
4. Add your API key to the `.env` file:
   ```
   NEWS_API_KEY=your_api_key_here
   ```

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