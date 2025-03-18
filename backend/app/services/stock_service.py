import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict
from time import sleep
from fastapi import HTTPException

def get_stock_data(symbol: str, period: str = "7d") -> Dict:
    # Map API periods to yfinance periods
    period_mapping = {
        "7d": "7d",
        "1mo": "1mo",
        "1y": "1y",
        "3y": "3y",
        "5y": "5y",
        "max": "max"
    }
    
    yf_period = period_mapping.get(period)
    if not yf_period:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid period: {period}. Valid periods are: {', '.join(period_mapping.keys())}"
        )
    
    max_retries = 5  # Increased from 3 to 5
    retry_delay = 2  # Increased from 1 to 2

    for attempt in range(max_retries):
        try:
            ticker = yf.Ticker(symbol)
            
            # Validate the symbol first
            if not ticker.info or 'regularMarketPrice' not in ticker.info:
                raise HTTPException(
                    status_code=404,
                    detail=f"Invalid stock symbol: {symbol}"
                )
            
            # Get historical data with error handling
            try:
                hist = ticker.history(period=yf_period)
            except Exception as hist_error:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error fetching historical data: {str(hist_error)}"
                )
            
            if hist.empty:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data available for {symbol} in the specified period"
                )
            
            # Ensure all required columns are present
            required_columns = ["Open", "High", "Low", "Close", "Volume"]
            missing_columns = [col for col in required_columns if col not in hist.columns]
            if missing_columns:
                raise HTTPException(
                    status_code=500,
                    detail=f"Missing required data columns: {', '.join(missing_columns)}"
                )
            
            # Process and validate each data point
            processed_data = []
            for index, row in hist.iterrows():
                try:
                    data_point = {
                        "timestamp": index.strftime("%Y-%m-%d %H:%M:%S"),
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": int(row["Volume"])
                    }
                    # Basic data validation
                    if any(value <= 0 for value in [data_point["open"], data_point["high"], data_point["low"], data_point["close"]]):
                        continue  # Skip invalid data points
                    processed_data.append(data_point)
                except (ValueError, TypeError) as e:
                    continue  # Skip malformed data points
            
            if not processed_data:
                raise HTTPException(
                    status_code=500,
                    detail=f"No valid data points found for {symbol}"
                )
            
            return {
                "symbol": symbol,  # Return original symbol for frontend use
                "data": processed_data
            }
            
        except HTTPException as http_error:
            # Re-raise HTTP exceptions immediately
            raise http_error
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to fetch data for {alpha_symbol} after {max_retries} attempts: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch stock data after {max_retries} attempts: {str(e)}"
                )
            sleep(retry_delay * (attempt + 1))