import pandas as pd
import numpy as np
from sklearn.model_selection import ParameterGrid

def backtest_sma_strategy(df: pd.DataFrame) -> dict:
    """
    Optimizes a simple SMA crossover strategy.
    """
    if df.empty or 'Close' not in df:
        return {}
    
    param_grid = {
        'fast_sma': [10, 20, 30],
        'slow_sma': [50, 100, 200]
    }
    
    best_perf = -float('inf')
    best_params = {}
    best_equity = pd.Series()
    
    close = df['Close']
    
    for params in ParameterGrid(param_grid):
        fast = params['fast_sma']
        slow = params['slow_sma']
        
        if fast >= slow:
            continue
            
        sma_fast = close.rolling(window=fast).mean()
        sma_slow = close.rolling(window=slow).mean()
        
        signal = np.where(sma_fast > sma_slow, 1, 0)
        
        market_returns = close.pct_change()
        strategy_returns = market_returns * pd.Series(signal).shift(1).fillna(0)
        
        cum_ret = (1 + strategy_returns).cumprod().iloc[-1] - 1
        
        if cum_ret > best_perf:
            best_perf = cum_ret
            best_params = params
            best_equity = (1 + strategy_returns).cumprod() - 1
            
    return {
        'best_params': best_params,
        'return': best_perf,
        'equity_curve': best_equity
    }
