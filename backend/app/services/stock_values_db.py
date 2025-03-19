import sqlite3
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

# Set up logging
logger = logging.getLogger(__name__)

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "stock_values.db")

def get_db_connection():
    """
    Create a connection to the SQLite database and return the connection object.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def initialize_db():
    """
    Initialize the database if it doesn't exist.
    """
    if not os.path.exists(DB_PATH):
        logger.info(f"Creating new stock values database at {DB_PATH}")
        # Database will be created when we connect to it
        conn = get_db_connection()
        conn.close()
        logger.info("Database initialized successfully")

def ensure_stock_table_exists(symbol: str) -> None:
    """
    Create a table for the given stock symbol if it doesn't exist.
    Each stock has its own table with date and closing price.
    """
    # Sanitize the symbol to create a valid table name
    table_name = f"stock_{symbol.replace('-', '_').replace('.', '_').replace('^', '_')}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        date TEXT PRIMARY KEY,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    
    return table_name

def get_date_range_for_period(period: str) -> Tuple[datetime, datetime]:
    """
    Convert a period string to a start and end date.
    """
    end_date = datetime.now()
    
    if period == "7d":
        start_date = end_date - timedelta(days=7)
    elif period == "1mo":
        start_date = end_date - timedelta(days=30)
    elif period == "1y":
        start_date = end_date - timedelta(days=365)
    elif period == "3y":
        start_date = end_date - timedelta(days=3*365)
    elif period == "5y":
        start_date = end_date - timedelta(days=5*365)
    elif period == "max":
        # For max, we'll use a very old date
        start_date = datetime(1900, 1, 1)
    else:
        # Default to 7 days
        start_date = end_date - timedelta(days=7)
    
    return start_date, end_date

def get_cached_stock_data(symbol: str, period: str) -> Dict:
    """
    Retrieve stock data from the database for the given symbol and period.
    Returns a dictionary with the data and a list of missing dates.
    """
    table_name = ensure_stock_table_exists(symbol)
    start_date, end_date = get_date_range_for_period(period)
    
    # Format dates for SQL query
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all dates in the range from the database
    cursor.execute(f"""
    SELECT date, open, high, low, close, volume 
    FROM {table_name} 
    WHERE date BETWEEN ? AND ? 
    ORDER BY date
    """, (start_date_str, end_date_str))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Process the data
    processed_data = []
    cached_dates = set()
    
    for row in rows:
        # Add all dates to cached_dates, whether they have data or not
        cached_dates.add(row['date'])
        
        # Skip entries where close is NULL (indicating data not available from API)
        if row['close'] is None:
            continue
            
        data_point = {
            "timestamp": f"{row['date']} 00:00:00",
            "open": float(row['open']) if row['open'] is not None else None,
            "high": float(row['high']) if row['high'] is not None else None,
            "low": float(row['low']) if row['low'] is not None else None,
            "close": float(row['close']) if row['close'] is not None else None,
            "volume": int(row['volume']) if row['volume'] is not None else 0
        }
        processed_data.append(data_point)
    
    # Generate all dates in the range to identify missing dates
    all_dates = set()
    current_date = start_date
    while current_date <= end_date:
        all_dates.add(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    # Find missing dates
    missing_dates = all_dates - cached_dates
    
    # Log cache hit/miss information
    if missing_dates:
        logger.info(f"Cache PARTIAL HIT for {symbol} with period {period}: {len(processed_data)} cached points, {len(missing_dates)} missing dates")
    else:
        logger.info(f"Cache COMPLETE HIT for {symbol} with period {period}: {len(processed_data)} cached points, no API call needed")
    
    return {
        "symbol": symbol,
        "data": processed_data,
        "missing_dates": sorted(list(missing_dates))
    }

def store_stock_data(symbol: str, data_points: List[Dict], not_available_dates: List[str] = None) -> None:
    """
    Store stock data in the database.
    For dates where data is not available, store NULL values for the closing price.
    Uses a transaction to ensure data integrity.
    """
    table_name = ensure_stock_table_exists(symbol)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Track successful inserts for logging
    inserted_count = 0
    unavailable_inserted = 0
    
    try:
        # Begin transaction
        conn.execute('BEGIN TRANSACTION')
        
        # Store data points
        for point in data_points:
            # Extract date from timestamp
            date_str = point["timestamp"].split()[0]
            
            try:
                cursor.execute(f"""
                INSERT OR REPLACE INTO {table_name} (date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    date_str,
                    point["open"],
                    point["high"],
                    point["low"],
                    point["close"],
                    point["volume"]
                ))
                inserted_count += 1
            except sqlite3.Error as e:
                logger.error(f"Database error when storing data for {symbol} on {date_str}: {str(e)}")
        
        # Store NULL values for dates where data is not available
        if not_available_dates:
            for date_str in not_available_dates:
                try:
                    cursor.execute(f"""
                    INSERT OR REPLACE INTO {table_name} (date, open, high, low, close, volume)
                    VALUES (?, NULL, NULL, NULL, NULL, NULL)
                    """, (date_str,))
                    unavailable_inserted += 1
                except sqlite3.Error as e:
                    logger.error(f"Database error when marking unavailable date for {symbol} on {date_str}: {str(e)}")
        
        # Commit transaction
        conn.commit()
        
        logger.info(f"Successfully stored {inserted_count}/{len(data_points)} data points and {unavailable_inserted}/{len(not_available_dates) if not_available_dates else 0} unavailable dates for {symbol}")
        if inserted_count > 0 or unavailable_inserted > 0:
            logger.info(f"Cache updated for {symbol} - future requests will use cached data")
            
    except sqlite3.Error as e:
        # Rollback transaction on error
        conn.rollback()
        logger.error(f"Transaction failed when storing data for {symbol}: {str(e)}")
    finally:
        # Always close the connection
        conn.close()

# Initialize the database when the module is imported
initialize_db()