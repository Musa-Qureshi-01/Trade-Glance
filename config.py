import os
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

def get_secret(key: str, default: str = "") -> str:
    """
    Get secret from Streamlit Cloud secrets or environment variable.
    Priority: st.secrets > os.environ > default
    """
    try:
        import streamlit as st
        # Try Streamlit Cloud secrets first
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except (ImportError, FileNotFoundError, KeyError):
        pass
    
    # Fall back to environment variable
    return os.getenv(key, default)


# App Settings
APP_TITLE = "TradeGlance"
APP_ICON = "📈"

# Defaults
DEFAULT_TICKER = "AAPL"
DEFAULT_PERIOD = "1y"
DEFAULT_FORECAST_DAYS = 14

# API Keys (from Streamlit secrets or .env)
FINNHUB_API_KEY = get_secret("FINNHUB_API_KEY", "")
GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY", "")
ALPHAVANTAGE_API_KEY = get_secret("ALPHAVANTAGE_API_KEY", "")

