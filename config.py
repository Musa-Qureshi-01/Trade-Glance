import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# App Settings
APP_TITLE = "TradeGlance"
APP_ICON = "📈"

# Defaults
DEFAULT_TICKER = "AAPL"
DEFAULT_PERIOD = "1y"
DEFAULT_FORECAST_DAYS = 14

# API Keys (Loaded from .env)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "")
