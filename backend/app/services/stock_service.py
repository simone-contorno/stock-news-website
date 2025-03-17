import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Any
from time import sleep
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

def get_stock_data(symbol: str, period: str = "7d") -> Dict[str, Any]:
    """Get stock data from Yahoo Finance API with enhanced error handling and retry mechanism.
    
    Args:
        symbol: The stock symbol to fetch data for
        period: The time period to fetch data for (7d, 1mo, 1y, etc.)
        
    Returns:
        Dictionary containing the symbol and price data
        
    Raises:
        HTTPException: If the data cannot be fetched after retries or if there are validation errors
    """
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
        logger.error(f"Invalid period requested: {period}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid period: {period}. Valid periods are: {', '.join(period_mapping.keys())}"
        )
    
    # Enhanced retry mechanism with exponential backoff
    max_retries = 5
    base_delay = 2
    
    logger.info(f"Fetching stock data for {symbol} with period {period}")
    
    for attempt in range(max_retries):
        try:
            # Calculate exponential backoff delay
            retry_delay = base_delay * (2 ** attempt)
            
            # Log retry attempts
            if attempt > 0:
                logger.info(f"Retry attempt {attempt+1}/{max_retries} for {symbol} with delay {retry_delay}s")
            
            # Initialize ticker
            ticker = yf.Ticker(symbol)
            
            # Validate the symbol first
            if not ticker.info or 'regularMarketPrice' not in ticker.info:
                logger.error(f"Invalid stock symbol: {symbol}")
                raise HTTPException(
                    status_code=404,
                    detail=f"Invalid stock symbol: {symbol}"
                )
            
            # Get historical data with error handling
            try:
                hist = ticker.history(period=yf_period)
            except Exception as hist_error:
                logger.error(f"Error fetching historical data for {symbol}: {str(hist_error)}")
                # This is a retriable error, so we'll continue the retry loop
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error fetching historical data: {str(hist_error)}"
                    )
                sleep(retry_delay)
                continue
            
            if hist.empty:
                logger.error(f"No data available for {symbol} in period {period}")
                raise HTTPException(
                    status_code=404,
                    detail=f"No data available for {symbol} in the specified period"
                )
            
            # Ensure all required columns are present
            required_columns = ["Open", "High", "Low", "Close", "Volume"]
            missing_columns = [col for col in required_columns if col not in hist.columns]
            if missing_columns:
                logger.error(f"Missing required columns: {', '.join(missing_columns)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Missing required data columns: {', '.join(missing_columns)}"
                )
                
            # Format the data for the response
            formatted_data = []
            for index, row in hist.iterrows():
                formatted_data.append({
                    "timestamp": index.strftime("%Y-%m-%d %H:%M:%S"),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"])
                })
            
            # Return the formatted data
            return {
                "symbol": symbol,
                "period": period,
                "data": formatted_data
            }
        
        except HTTPException:
            # Re-raise HTTP exceptions without modification
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing stock data for {symbol}: {str(e)}")
            
            # If this is the last retry, raise an exception
            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to process stock data: {str(e)}"
                )
            
            # Otherwise, retry after delay
            sleep(retry_delay)
            continue
    
    # If we've exhausted all retries
    logger.error(f"All {max_retries} retry attempts failed for {symbol}")
    raise HTTPException(
        status_code=500,
        detail="Failed to retrieve stock data after multiple attempts"
    )