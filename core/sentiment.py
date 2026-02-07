import os
import finnhub
import numpy as np
import streamlit as st
from transformers import pipeline
from datetime import datetime, timedelta
from core.logger import get_logger
import config

logger = get_logger(__name__)

# Lazy load the pipeline to avoid slow startup
@st.cache_resource(show_spinner="Loading AI Sentiment Model...")
def load_sentiment_pipeline():
    logger.info("Loading FinBERT model...")
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

class SentimentEngine:
    def __init__(self):
        # Initialize Finnhub Client using config
        api_key = config.FINNHUB_API_KEY
        if not api_key:
            logger.warning("Finnhub API Key missing")
            self.client = None
        else:
            try:
                self.client = finnhub.Client(api_key=api_key)
            except Exception as e:
                logger.error(f"Finnhub Init Error: {e}")
                self.client = None

    def fetch_news(self, ticker: str, days: int = 7, limit: int = 20):
        """
        Returns list of headlines from Finnhub.
        """
        if not self.client:
            return []

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        try:
            # _from and to are reserved keywords
            news = self.client.company_news(ticker, _from=start_date, to=end_date)
            
            # Filter for headlines
            headlines = [n["headline"] for n in news[:limit] if n.get("headline")]
            
            logger.info(f"Fetched {len(headlines)} headlines for {ticker}")
            return headlines
            
        except finnhub.FinnhubAPIException as e:
            if "429" in str(e):
                logger.warning(f"Finnhub Rate Limit Exceeded for {ticker}")
            else:
                logger.error(f"Finnhub API Error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []

    def analyze(self, ticker: str):
        """
        Orchestrates fetching and analyzing news.
        Returns:
            score: float (-1 to +1)
            label: str
            detailed: list of (headline, result)
        """
        headlines = self.fetch_news(ticker)
        
        if not headlines:
            logger.info(f"No headlines found for {ticker}, returning Neutral.")
            return 0, "Neutral 😐", []

        # Load pipeline (cached)
        try:
            pipe = load_sentiment_pipeline()
            results = pipe(headlines)
        except Exception as e:
            logger.error(f"Sentiment Analysis Failed: {e}")
            return 0, f"Error: {e}", []

        scores = []
        detailed = []

        for h, r in zip(headlines, results):
            s = 0
            if r["label"] == "positive":
                s = 1
            elif r["label"] == "negative":
                s = -1
            # Neutral is 0
            
            scores.append(s)
            
            # Store detail
            detailed.append((h, r))

        avg_score = float(np.mean(scores))
        logger.info(f"Sentiment Score for {ticker}: {avg_score}")

        if avg_score > 0.2:
            label = "Bullish 📈"
        elif avg_score < -0.2:
            label = "Bearish 📉"
        else:
            label = "Neutral 😐"

        return avg_score, label, detailed
