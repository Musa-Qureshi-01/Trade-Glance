"""
Forecast Engine
Handles all time-series prediction logic.
Framework independent.
"""

import pandas as pd
from prophet import Prophet
from core.logger import get_logger

logger = get_logger(__name__)

class ForecastEngine:
    def __init__(
        self,
        days: int = 30,
        daily_seasonality: bool = True,
        weekly_seasonality: bool = True,
        yearly_seasonality: bool = True,
        seasonality_mode: str = "additive",
        changepoint_prior_scale: float = 0.05,
    ):
        self.days = days
        self.daily_seasonality = daily_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.yearly_seasonality = yearly_seasonality
        self.seasonality_mode = seasonality_mode
        self.changepoint_prior_scale = changepoint_prior_scale

    def _prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or 'y' not in df.columns:
            return pd.DataFrame()
            
        df = df.copy()
        # Ensure ds is available or index is datetime
        if 'ds' not in df.columns and isinstance(df.index, pd.DatetimeIndex):
             df['ds'] = df.index
        
        if 'ds' in df.columns:
            df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)
        
        return df[["ds", "y"]]

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Running Prophet forecast...")

        df = self._prepare(df)
        
        # Prophet requires at least 2 data points, but practically needs more
        MIN_DATA_POINTS = 30
        if len(df) < MIN_DATA_POINTS:
            logger.warning(f"Not enough data points for forecast. Need {MIN_DATA_POINTS}, got {len(df)}")
            return pd.DataFrame()

        try:
            model = Prophet(
                daily_seasonality=self.daily_seasonality,
                weekly_seasonality=self.weekly_seasonality,
                yearly_seasonality=self.yearly_seasonality,
                seasonality_mode=self.seasonality_mode,
                changepoint_prior_scale=self.changepoint_prior_scale,
            )

            model.fit(df)

            future = model.make_future_dataframe(periods=self.days)

            forecast = model.predict(future)
            
            logger.info("Forecast generated successfully.")
            return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
            
        except Exception as e:
            logger.error(f"Prophet Forecast Failed: {e}")
            return pd.DataFrame()
