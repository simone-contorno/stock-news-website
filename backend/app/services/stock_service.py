import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict
from time import sleep
import logging
import random
from fastapi import HTTPException
from .stock_values_db import get_cached_stock_data, store_stock_data

# Set up logging
logger = logging.getLogger(__name__)

# Rate limiting settings
MAX_RETRIES = 1
BASE_DELAY = 2  # Base delay in seconds
JITTER = 0.5    # Random jitter to add to delay

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
    
    # If we have some missing dates, fetch them from Yahoo Finance
    if cached_data["missing_dates"]:
        for attempt in range(MAX_RETRIES):
            try:
                # Calculate exponential backoff with jitter for retries
                if attempt > 0:
                    # Exponential backoff: BASE_DELAY * 2^attempt + random jitter
                    delay = BASE_DELAY * (2 ** (attempt - 1)) + (random.random() * JITTER)
                    logger.info(f"Retry attempt {attempt+1}/{MAX_RETRIES} for {symbol} after {delay:.2f}s delay")
                    sleep(delay)
                
                # Make a single API call to Yahoo Finance for all missing dates
                logger.info(f"Making a single API call to Yahoo Finance for {symbol} with period {yf_period}")
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
                    # Check specifically for rate limit errors (429)
                    error_str = str(info_error)
                    if "429" in error_str and "Too Many Requests" in error_str:
                        logger.warning(f"Rate limit reached when fetching ticker info for {symbol}: {error_str}")
                        if attempt < MAX_RETRIES - 1:
                            continue  # Try again with backoff
                        elif cached_data["data"]:
                            # Return cached data if we have any
                            logger.warning(f"Returning cached data for {symbol} due to rate limiting")
                            return {
                                "symbol": symbol,
                                "data": cached_data["data"]
                            }
                    else:
                        logger.warning(f"Error fetching ticker info for {symbol}: {error_str}")
                    # Continue anyway and try to get historical data
                
                # Get all historical data in a single call with error handling
                try:
                    logger.info(f"Retrieving historical data for {symbol} with period {yf_period}")
                    hist = ticker.history(period=yf_period)
                except Exception as hist_error:
                    error_str = str(hist_error)
                    # Check for rate limit errors in historical data fetch
                    if "429" in error_str or "Too Many Requests" in error_str:
                        logger.warning(f"Rate limit reached when fetching historical data for {symbol}: {error_str}")
                        if attempt < MAX_RETRIES - 1:
                            continue  # Try again with backoff
                        elif cached_data["data"]:
                            # Return cached data if we have any
                            logger.warning(f"Returning cached data for {symbol} due to rate limiting")
                            return {
                                "symbol": symbol,
                                "data": cached_data["data"]
                            }
                    
                    # For other errors, raise HTTP exception
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error fetching historical data: {error_str}"
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
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Failed to fetch data for {symbol} after {MAX_RETRIES} attempts: {str(e)}")
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
                            detail=f"Failed to fetch stock data after {MAX_RETRIES} attempts: {str(e)}"
                        )
    
    # This should never be reached, but just in case
    return {
        "symbol": symbol,
        "data": cached_data["data"]
    }