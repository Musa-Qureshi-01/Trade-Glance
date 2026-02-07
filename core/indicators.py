import pandas as pd
import numpy as np

def calculate_rsi(data, window=14):
    """Calculate Relative Strength Index (RSI)"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, slow=26, fast=12, signal=9):
    """Calculate MACD, Signal line, and Histogram"""
    exp1 = data.ewm(span=fast, adjust=False).mean()
    exp2 = data.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches the dataframe with SMA, RSI, and MACD using manual calculations.
    Replaces pandas_ta dependency.
    """
    if df.empty:
        return df
    
    # We work on a copy to avoid side effects
    result_df = df.copy()
    
    # Ensure 'y' column exists (Close price)
    if 'y' not in result_df.columns:
        return result_df

    # Simple Moving Averages
    # pandas_ta names: SMA_20, SMA_50
    result_df['SMA_20'] = result_df['y'].rolling(window=20).mean()
    result_df['SMA_50'] = result_df['y'].rolling(window=50).mean()
    
    # RSI
    # pandas_ta name: RSI_14
    result_df['RSI_14'] = calculate_rsi(result_df['y'], window=14)
    
    # MACD
    # pandas_ta names: MACD_12_26_9, MACDs_12_26_9, MACDh_12_26_9
    macd, signal, hist = calculate_macd(result_df['y'])
    result_df['MACD_12_26_9'] = macd
    result_df['MACDs_12_26_9'] = signal
    result_df['MACDh_12_26_9'] = hist
    
    return result_df
