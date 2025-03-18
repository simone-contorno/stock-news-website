import requests
from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException
from time import sleep
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_stock_data(symbol: str, period: str = "7d") -> Dict:
    if not settings.ALPHA_VANTAGE_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="ALPHA_VANTAGE_API_KEY environment variable is not configured"
        )
    
    # For Alpha Vantage API, remove the '^' prefix
    alpha_symbol = symbol.replace("^", "")
    logger.info(f"Using Alpha Vantage symbol: {alpha_symbol} (original: {symbol})")

    # Map API periods to Alpha Vantage functions and intervals
    period_mapping = {
        "7d": ("TIME_SERIES_DAILY", "Daily"),
        "1mo": ("TIME_SERIES_DAILY", "Daily"),
        "1y": ("TIME_SERIES_DAILY", "Daily"),
        "3y": ("TIME_SERIES_DAILY", "Daily"),
        "5y": ("TIME_SERIES_WEEKLY", "Weekly"),
        "max": ("TIME_SERIES_MONTHLY", "Monthly")
    }
    
    function, interval = period_mapping.get(period, ("TIME_SERIES_DAILY", "Daily"))
    
    params = {
        "function": function,
        "symbol": alpha_symbol,  # Use cleaned symbol for Alpha Vantage
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    
    if function == "TIME_SERIES_DAILY":
        params["outputsize"] = "full"
    
    max_retries = settings.ALPHA_VANTAGE_MAX_RETRIES
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = requests.get(
                settings.ALPHA_VANTAGE_BASE_URL,
                params=params,
                timeout=settings.ALPHA_VANTAGE_TIMEOUT
            )
            
            if response.status_code == 429:
                raise HTTPException(
                    status_code=429,
                    detail="Alpha Vantage API rate limit reached"
                )
            
            response.raise_for_status()
            data = response.json()
            
            # Check for error messages
            if "Error Message" in data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Invalid stock symbol: {alpha_symbol}"
                )
            
            # Get the time series data key based on the function
            time_series_key = f"Time Series ({interval})"
            if time_series_key not in data:
                raise HTTPException(
                    status_code=500,
                    detail="Invalid response format from Alpha Vantage"
                )
            
            time_series = data[time_series_key]
            
            # Convert data to our standard format
            processed_data = []
            for date, values in time_series.items():
                try:
                    price_data = {
                        "timestamp": date + " 00:00:00",
                        "open": float(values["1. open"]),
                        "high": float(values["2. high"]),
                        "low": float(values["3. low"]),
                        "close": float(values["4. close"]),
                        "volume": int(float(values["5. volume"]))
                    }
                    processed_data.append(price_data)
                except (ValueError, KeyError) as e:
                    continue
            
            # Sort by date and filter based on period
            processed_data.sort(key=lambda x: x["timestamp"])
            if period == "7d":
                processed_data = processed_data[-7:]
            elif period == "1mo":
                processed_data = processed_data[-30:]
            elif period == "1y":
                processed_data = processed_data[-365:]
            elif period == "3y":
                processed_data = processed_data[-1095:]
            elif period == "5y":
                processed_data = processed_data[-1825:]
            
            if not processed_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data available for {alpha_symbol}"
                )
            
            return {
                "symbol": symbol,  # Return original symbol for frontend use
                "data": processed_data
            }
            
        except HTTPException:
            raise
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to fetch data for {alpha_symbol} after {max_retries} attempts: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch stock data after {max_retries} attempts: {str(e)}"
                )
            sleep(retry_delay * (attempt + 1))