import streamlit as st
import time
from core.sentiment import SentimentEngine
from core.logger import get_logger

logger = get_logger(__name__)

def render_sentiment_page():
    # Header Section
    st.markdown("""
        <h2 style='text-align: left; margin-bottom: 20px;'>
            <span style='background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                Market Sentiment Hub
            </span> 📢
        </h2>
        <p style='margin-bottom: 30px; color: #a0aec0;'>
            Analyze market mood using AI-powered news processing (FinBERT).
        </p>
    """, unsafe_allow_html=True)
    
    # Input Section
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            ticker = st.text_input("Enter Ticker", "AAPL", placeholder="e.g. MSFT, BTC-USD").upper()
        with col2:
            st.write("") # Spacer
            st.write("")
            analyze_btn = st.button("Analyze News", type="primary", use_container_width=True)

    # Logic
    if analyze_btn or (ticker and st.session_state.get('last_sentiment_ticker') == ticker):
        st.session_state['last_sentiment_ticker'] = ticker
        
        engine = SentimentEngine()
        
        # Check API Key
        if not engine.client:
            st.error("⚠️ **Missing Finnhub API Key**")
            st.info("""
                To use this feature:
                1. get a free key from [finnhub.io](https://finnhub.io/).
                2. Open your `.env` file.
                3. Update `FINNHUB_API_KEY=your_key_here`.
                4. Restart the app.
            """)
            return

        with st.spinner(f"🔍 Scanning news headlines for {ticker}..."):
            try:
                score, label, detailed = engine.analyze(ticker)
                
                # Display Results
                st.divider()
                
                # 1. High Level Metrics
                col_score, col_gauge, col_count = st.columns([1, 2, 1])
                
                with col_score:
                    st.metric("Overall Sentiment", label, f"{score:.2f}")

                with col_gauge:
                    # Normalize -1 to 1 -> 0 to 100
                    normalized_score = int((score + 1) / 2 * 100)
                    normalized_score = max(0, min(100, normalized_score))
                    st.write("Confidence Gauge")
                    st.progress(normalized_score)
                    st.caption("Bearish (0%) ⟷ Bullish (100%)")

                with col_count:
                    st.metric("Articles Analyzed", len(detailed))
                
                # 2. Detailed Headlines
                st.subheader("📰 AI News Analysis")
                
                if not detailed:
                    st.warning(f"⚠️ No recent news found for {ticker} in the last 7 days.")
                    
                    # Check for cached/older articles in session
                    cached_key = f"cached_sentiment_{ticker}"
                    if cached_key in st.session_state:
                        st.info("📦 Showing last cached analysis (older data):")
                        cached = st.session_state[cached_key]
                        st.markdown(f"**Last headline analyzed:** {cached['headline']}")
                        st.caption(f"Sentiment: {cached['label']} ({cached['score']:.1%})")
                    else:
                        st.caption("No cached data available for this ticker.")
                else:
                    # Cache the first result for future fallback
                    first_headline, first_result = detailed[0]
                    st.session_state[f"cached_sentiment_{ticker}"] = {
                        'headline': first_headline,
                        'label': first_result['label'],
                        'score': first_result['score']
                    }
                    
                    # Display all headlines
                    for headline, result in detailed:
                        sentiment = result['label']
                        conf = result['score']
                        
                        # Card Styling
                        if sentiment == 'positive':
                            border_color = "#28a745" # Green
                            icon = "📈"
                            bg_color = "rgba(40, 167, 69, 0.1)"
                        elif sentiment == 'negative':
                            border_color = "#dc3545" # Red
                            icon = "📉"
                            bg_color = "rgba(220, 53, 69, 0.1)"
                        else:
                            border_color = "#6c757d" # Gray
                            icon = "😐"
                            bg_color = "rgba(108, 117, 125, 0.1)"
                        
                        with st.container():
                            st.markdown(f"""
                            <div style="
                                border-left: 4px solid {border_color};
                                background-color: {bg_color};
                                padding: 15px;
                                border-radius: 4px;
                                margin-bottom: 10px;
                            ">
                                <small style="color: {border_color}; font-weight: bold;">
                                    {icon} {sentiment.upper()} ({conf:.1%})
                                </small>
                                <div style="font-size: 1.1em; margin-top: 5px;">
                                    {headline}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
            except Exception as e:
                logger.error(f"Error in sentiment page: {e}")
                st.error(f"An error occurred while analyzing sentiment. Please check logs.")
