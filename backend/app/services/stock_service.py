import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict
from time import sleep
import logging
from fastapi import HTTPException
from .stock_values_db import get_cached_stock_data, store_stock_data

# Set up logging
logger = logging.getLogger(__name__)

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
    
    # First, check if we have cached data in our SQLite database
    logger.info(f"Checking cached data for {symbol} with period {period}")
    cached_data = get_cached_stock_data(symbol, period)
    
    # If we have all the data we need, return it immediately
    if not cached_data["missing_dates"]:
        #logger.info(f"Using cached data for {symbol} with period {period} - No API call needed")
        #logger.info(f"Found {len(cached_data['data'])} data points in cache")
        return {
            "symbol": symbol,
            "data": cached_data["data"]
        }
    
    # If we have missing dates, fetch only those from Yahoo Finance
    logger.info(f"Found {len(cached_data['missing_dates'])} missing dates for {symbol}")
    
    max_retries = 1
    retry_delay = 1
    
    # If we have some missing dates, fetch them from Yahoo Finance
    if cached_data["missing_dates"]:
        for attempt in range(max_retries):
            try:
                ticker = yf.Ticker(symbol)
                
                # Validate the symbol first
                try:
                    if not ticker.info or 'regularMarketPrice' not in ticker.info:
                        logger.warning(f"Invalid or incomplete ticker info for {symbol}")
                        # For market indices, we'll try to proceed with historical data even if info is incomplete
                        if not symbol.startswith('^'):
                            raise HTTPException(
                                status_code=404,
                                detail=f"Invalid stock symbol: {symbol}"
                            )
                except Exception as info_error:
                    logger.warning(f"Error fetching ticker info for {symbol}: {str(info_error)}")
                    # Continue anyway and try to get historical data
                
                # Get historical data with error handling
                try:
                    logger.info(f"Retrieving historical data for {symbol} with period {yf_period}")
                    hist = ticker.history(period=yf_period)
                except Exception as hist_error:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error fetching historical data: {str(hist_error)}"
                    )
                
                if hist.empty:
                    # If no data is available, mark all missing dates as not available
                    store_stock_data(symbol, [], cached_data["missing_dates"])
                    return {
                        "symbol": symbol,
                        "data": cached_data["data"]
                    }
                
                # Ensure all required columns are present
                required_columns = ["Open", "High", "Low", "Close", "Volume"]
                missing_columns = [col for col in required_columns if col not in hist.columns]
                if missing_columns:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Missing required data columns: {', '.join(missing_columns)}"
                    )
                
                # Process and validate each data point
                new_data_points = []
                not_available_dates = []
                
                # Convert missing_dates to a set for faster lookups
                missing_dates_set = set(cached_data["missing_dates"])
                
                for index, row in hist.iterrows():
                    date_str = index.strftime("%Y-%m-%d")
                    
                    # Only process dates that are in our missing dates list
                    if date_str in missing_dates_set:
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
                                not_available_dates.append(date_str)
                                continue  # Skip invalid data points
                            
                            new_data_points.append(data_point)
                            missing_dates_set.remove(date_str)  # Remove from missing set
                        except (ValueError, TypeError) as e:
                            not_available_dates.append(date_str)
                            continue  # Skip malformed data points
                
                # Any dates still in missing_dates_set were not found in the API response
                not_available_dates.extend(list(missing_dates_set))
                
                # Store the new data points and mark not available dates in the database
                if new_data_points or not_available_dates:
                    store_stock_data(symbol, new_data_points, not_available_dates)
                
                # Combine cached data with new data
                all_data = cached_data["data"] + new_data_points
                
                # Sort by timestamp
                all_data.sort(key=lambda x: x["timestamp"])
                
                return {
                    "symbol": symbol,
                    "data": all_data
                }
                
            except HTTPException as http_error:
                # Re-raise HTTP exceptions immediately
                raise http_error
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to fetch data for {symbol} after {max_retries} attempts: {str(e)}")
                    # If we have some cached data, return that instead of failing
                    if cached_data["data"]:
                        logger.warning(f"Returning partial cached data for {symbol} due to API error")
                        return {
                            "symbol": symbol,
                            "data": cached_data["data"]
                        }
                    else:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Failed to fetch stock data after {max_retries} attempts: {str(e)}"
                        )
                sleep(retry_delay * (attempt + 1))
    
    # This should never be reached, but just in case
    return {
        "symbol": symbol,
        "data": cached_data["data"]
    }