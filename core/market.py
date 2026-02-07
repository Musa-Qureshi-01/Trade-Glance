import yfinance as yf
import pandas as pd


def fetch_price_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Download historical prices and return Prophet-safe dataframe
    Output:
        ds (datetime)
        y (float)
    """

    df = yf.download(ticker, period=period, progress=False)

    # -------- FIX 1: flatten multi-index columns --------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    df.rename(
        columns={
            "Date": "ds",
            "Close": "y"
        },
        inplace=True
    )

    # -------- FIX 2: ensure numeric --------
    df["y"] = pd.to_numeric(df["y"], errors="coerce")

    # -------- FIX 3: drop NaNs --------
    df = df.dropna(subset=["y"])

    return df[["ds", "y"]]
