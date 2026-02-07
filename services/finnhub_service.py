import finnhub
from datetime import datetime, timedelta
from core.logger import get_logger

logger = get_logger(__name__)

def fetch_company_news(ticker: str, api_key: str, days: int = 7) -> list:
    """
    Fetches company news from Finnhub for the last N days.
    Returns empty list on failure.
    """
    if not api_key:
        logger.warning("Finnhub API key is missing.")
        return []
    
    if not ticker:
        return []
    
    try:
        finnhub_client = finnhub.Client(api_key=api_key)
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # _from and to are reserved keywords, but finnhub client uses them as args
        news = finnhub_client.company_news(ticker, _from=start_date, to=end_date)
        
        if not news:
            logger.info(f"No news found for {ticker}")
            return []
            
        logger.info(f"Fetched {len(news)} news items for {ticker}")
        
        # Return top 10 most recent
        return news[:10]
        
    except finnhub.FinnhubAPIException as e:
        # Handle specific API errors like 429 Rate Limit
        if "429" in str(e):
             logger.warning(f"Finnhub Rate Limit Exceeded for {ticker}")
        else:
             logger.error(f"Finnhub API Error for {ticker}: {e}")
        return []
        
    except Exception as e:
        logger.error(f"Unexpected error fetching news for {ticker}: {e}")
        return []
