import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.forecast import ForecastEngine
from core.market import fetch_price_data
from core.indicators import add_all_indicators
from ui.charts import render_candlestick_chart, render_forecast_chart
from core.logger import get_logger

logger = get_logger(__name__)

@st.cache_data(ttl=3600)
def load_market_data(t):
    try:
        df = fetch_price_data(t)
        if not df.empty:
            df = add_all_indicators(df)
        return df
    except Exception as e:
        logger.error(f"Error loading market data for {t}: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def generate_forecast(df, days, mode, scale, daily, weekly, yearly):
    try:
        engine = ForecastEngine(
            days=days,
            seasonality_mode=mode,
            changepoint_prior_scale=scale,
            daily_seasonality=daily,
            weekly_seasonality=weekly,
            yearly_seasonality=yearly
        )
        return engine.predict(df)
    except Exception as e:
        logger.error(f"Forecast generation error: {e}")
        return pd.DataFrame()

def render_analysis_page():
    # -------------------------------------------------
    # SIDEBAR CONTROLS
    # -------------------------------------------------
    st.sidebar.markdown("### Forecast Settings")
    forecast_days = st.sidebar.slider("Horizon (Days)", 7, 90, 30)
    
    with st.sidebar.expander("Advanced Tuning"):
        seasonality_mode = st.selectbox("Seasonality Mode", ["additive", "multiplicative"])
        prior_scale = st.slider("Trend Flexibility", 0.01, 0.5, 0.05, 0.01)
        daily_season = st.checkbox("Daily Seasonality", True)
        weekly_season = st.checkbox("Weekly Seasonality", True)
        yearly_season = st.checkbox("Yearly Seasonality", True)

    # -------------------------------------------------
    # MAIN CONTENT
    # -------------------------------------------------
    st.header(f"Market Analysis")
    
    # Asset Selection - Moved to Main Area
    st.markdown("##### Asset Selection")
    
    col_mode, col_input, col_btn = st.columns([1, 2, 1])
    
    with col_mode:
        selection_mode = st.radio("Mode", ["Quick Select", "Search"], horizontal=True, label_visibility="collapsed")
    
    with col_input:
        if selection_mode == "Quick Select":
            TOP_STOCKS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "META", "SPY", "BTC-USD", "ETH-USD"]
            ticker = st.selectbox("Select Asset", options=TOP_STOCKS, index=0, label_visibility="collapsed")
        else:
            ticker = st.text_input("Ticker Symbol", "AAPL", label_visibility="collapsed").upper()
            st.caption("Don't know the ticker? [Search on Yahoo Finance](https://finance.yahoo.com/lookup)")
            
    with col_btn:
        run_btn = st.button("Run Analysis", type="primary", use_container_width=True)
    
    if "analysis_ticker" not in st.session_state:
        st.session_state.analysis_ticker = None
    
    if run_btn:
        st.session_state.analysis_ticker = ticker
    
    if st.session_state.analysis_ticker == ticker:
        with st.spinner(f"Analyzing {ticker}..."):
            try:
                df = load_market_data(ticker)
                
                if df is None or df.empty:
                    st.error(f"❌ Could not fetch data for '{ticker}'.")
                    st.warning("Possible causes:\n1. Invalid Ticker Symbol.\n2. Internet Connection Issue.\n3. API Rate Limit (wait a moment).")
                    return

                # Calculate Metrics
                latest_price = df['y'].iloc[-1]
                prev_price = df['y'].iloc[-2]
                change = latest_price - prev_price
                pct_change = (change / prev_price) * 100
                
                # Metrics Row
                col1, col2, col3 = st.columns(3)
                col1.metric("Latest Closing Price", f"${latest_price:,.2f}", f"{change:+.2f} ({pct_change:+.2f}%)")
                col2.metric("Historical Samples", len(df))
                col3.metric("Forecast Range", f"{forecast_days} Days")
                
                st.markdown("---")
                
                # Tabs
                tab_overview, tab_forecast, tab_tech, tab_raw = st.tabs(["Overview", "AI Forecast", "Technical Indicators", "Raw Data"])
                
                with tab_overview:
                    st.subheader("Price Action")
                    fig_price = render_candlestick_chart(df, f"{ticker} Price History")
                    st.plotly_chart(fig_price, use_container_width=True)
                
                with tab_forecast:
                    st.subheader("Prophet Model Projection")
                    
                    forecast = generate_forecast(
                        df, forecast_days, seasonality_mode, prior_scale, 
                        daily_season, weekly_season, yearly_season
                    )
                    
                    if forecast.empty:
                        st.warning("⚠️ Not enough data to generate a reliable forecast.")
                    else:
                        last_pred = forecast['yhat'].iloc[-1]
                        expected_change = last_pred - latest_price
                        expected_pct = (expected_change / latest_price) * 100
                        direction = "Bullish" if expected_change > 0 else "Bearish"
                        
                        m1, m2 = st.columns(2)
                        m1.metric("Target Price (Forecast)", f"${last_pred:,.2f}")
                        m2.metric("Expected Return", f"{direction} {expected_pct:+.2f}%")
                        
                        fig_forecast = render_forecast_chart(df, forecast)
                        st.plotly_chart(fig_forecast, use_container_width=True)

                with tab_tech:
                    st.subheader("Technical Indicators")
                    
                    # RSI Chart
                    if 'RSI_14' in df.columns:
                        fig_rsi = go.Figure()
                        fig_rsi.add_trace(go.Scatter(x=df['ds'], y=df['RSI_14'], name='RSI', line=dict(color='purple')))
                        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                        fig_rsi.update_layout(title="Relative Strength Index (RSI)", template="plotly_dark", height=300)
                        st.plotly_chart(fig_rsi, use_container_width=True)
                    
                    # MACD Chart
                    if 'MACD_12_26_9' in df.columns:
                        fig_macd = go.Figure()
                        fig_macd.add_trace(go.Scatter(x=df['ds'], y=df['MACD_12_26_9'], name='MACD', line=dict(color='blue')))
                        fig_macd.add_trace(go.Scatter(x=df['ds'], y=df['MACDs_12_26_9'], name='Signal', line=dict(color='orange')))
                        fig_macd.add_bar(x=df['ds'], y=df['MACDh_12_26_9'], name='Hist')
                        fig_macd.update_layout(title="MACD", template="plotly_dark", height=300)
                        st.plotly_chart(fig_macd, use_container_width=True)
                    
                    # SMA Chart (New)
                    if 'SMA_20' in df.columns or 'SMA_50' in df.columns:
                        fig_sma = go.Figure()
                        fig_sma.add_trace(go.Scatter(x=df['ds'], y=df['y'], name='Price', line=dict(color='white', width=1)))
                        if 'SMA_20' in df.columns:
                            fig_sma.add_trace(go.Scatter(x=df['ds'], y=df['SMA_20'], name='SMA 20', line=dict(color='cyan')))
                        if 'SMA_50' in df.columns:
                            fig_sma.add_trace(go.Scatter(x=df['ds'], y=df['SMA_50'], name='SMA 50', line=dict(color='magenta')))
                        fig_sma.update_layout(title="Simple Moving Averages (SMA)", template="plotly_dark", height=300)
                        st.plotly_chart(fig_sma, use_container_width=True)

                with tab_raw:
                    st.dataframe(df.tail(100), use_container_width=True)
                    
            except Exception as e:
                logger.error(f"Analysis Page Error: {e}")
                st.error(f"An unexpected error occurred: {e}")
                
