import yfinance as yf
import pandas as pd
from core.logger import get_logger

logger = get_logger(__name__)

def fetch_historical_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetches historical OHLCV data from Yahoo Finance.
    Returns an empty DataFrame on failure.
    """
    if not ticker:
        logger.warning("Empty ticker provided to fetch_historical_data")
        return pd.DataFrame()

    try:
        stock = yf.Ticker(ticker)
        
        # Add basic validation that ticker exists by checking info property lightly?
        # yfinance can be slow with .info, so we skip that and just try history.
        
        df = stock.history(period=period)
        
        if df.empty:
            logger.warning(f"No data returned for ticker: {ticker} (period={period})")
            return pd.DataFrame()
        
        # Remove timezone to simplify downstream processing
        df.index = df.index.tz_localize(None)
        
        logger.info(f"Successfully fetched {len(df)} rows for {ticker}")
        return df
        
    except Exception as e:
        logger.error(f"Error fetching historical data for {ticker}: {e}")
        return pd.DataFrame()

def fetch_current_price(ticker: str) -> float:
    """
    Fetches the latest available close price.
    Returns 0.0 on failure.
    """
    if not ticker:
        return 0.0

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1d") # 5d is safer for weekends/holidays? 1d usually works if market open or data exists. 
        # Actually 1d might be empty if called on Sunday morning before pre-market? 
        # safe choice: try fetching slightly more and take last.
        
        if df.empty:
            # try 5d just in case of long weekend
            df = stock.history(period="5d")
            
        if not df.empty:
            price = df['Close'].iloc[-1]
            return float(price)
            
        logger.warning(f"No price data found for {ticker}")
        return 0.0
    except Exception as e:
        logger.error(f"Error fetching current price for {ticker}: {e}")
        return 0.0
