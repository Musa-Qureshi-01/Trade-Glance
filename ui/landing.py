import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        print(f"Lottie loading failed: {e}")
        return None

def render_landing_page():
    # Load Bootstrap Icons CSS
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)
    
    # Hero Section - Text on left, Animation on right
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("""
            <div style="text-align: left; padding-top: 2rem;">
                <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem; background: -webkit-linear-gradient(45deg, #2962ff, #29b6f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    TradeGlance ⚡
                </h1>
                <p style="font-size: 1.4rem; color: #a0aec0; margin-bottom: 1.5rem;">
                    AI-Powered Market Intelligence Platform
                </p>
                <p style="font-size: 1.1rem; color: #718096; margin-bottom: 2rem;">
                    <strong>Forecast</strong> • <strong>Indicators</strong> • <strong>Sentiment</strong> • <strong>AI Assistant</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # CTA Buttons - Using links styled as buttons (more reliable)
        st.markdown("""
            <style>
                .cta-button {
                    display: inline-block;
                    padding: 0.75rem 1.5rem;
                    margin: 0.25rem;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                    text-align: center;
                    transition: all 0.3s ease;
                }
                .cta-primary {
                    background: linear-gradient(90deg, #2962ff, #29b6f6);
                    color: white !important;
                }
                .cta-secondary {
                    background: rgba(255,255,255,0.1);
                    border: 1px solid rgba(255,255,255,0.2);
                    color: #a0aec0 !important;
                }
                .cta-button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(41,98,255,0.3);
                }
            </style>
            <div style="margin-top: 1rem;">
                <p style="color: #718096; margin-bottom: 1rem;">Use the sidebar to navigate to:</p>
                <span class="cta-button cta-primary">🔮 Market Analysis</span>
                <span class="cta-button cta-secondary">📰 Sentiment Hub</span>
                <span class="cta-button cta-secondary">🤖 AI Agent</span>
            </div>
        """, unsafe_allow_html=True)
            
    with c2:
        # Animation
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=300, key="trading_anim")

    st.markdown("---")

    # Features Section (Improved)
    st.markdown("""
        <h2 style="text-align: center; margin-bottom: 2rem;">
            <i class="bi bi-stars" style="color: #ffc107;"></i> Core Features
        </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, rgba(41,98,255,0.1), rgba(41,182,246,0.1)); border: 1px solid rgba(41,98,255,0.2);">
                <h3><i class="bi bi-graph-up-arrow" style="color: #2962ff;"></i></h3>
                <h4>Forecasting</h4>
                <p style="color: #a0aec0; font-size: 0.9rem;">Prophet ML predictions with 7-90 day horizons</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, rgba(76,175,80,0.1), rgba(129,199,132,0.1)); border: 1px solid rgba(76,175,80,0.2);">
                <h3><i class="bi bi-bar-chart-line" style="color: #4caf50;"></i></h3>
                <h4>Indicators</h4>
                <p style="color: #a0aec0; font-size: 0.9rem;">RSI, MACD, SMA overlays on live charts</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, rgba(255,152,0,0.1), rgba(255,183,77,0.1)); border: 1px solid rgba(255,152,0,0.2);">
                <h3><i class="bi bi-newspaper" style="color: #ff9800;"></i></h3>
                <h4>Sentiment</h4>
                <p style="color: #a0aec0; font-size: 0.9rem;">FinBERT NLP analysis of market news</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, rgba(156,39,176,0.1), rgba(186,104,200,0.1)); border: 1px solid rgba(156,39,176,0.2);">
                <h3><i class="bi bi-robot" style="color: #9c27b0;"></i></h3>
                <h4>AI Agent</h4>
                <p style="color: #a0aec0; font-size: 0.9rem;">Gemini-powered trading assistant</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Why TradeGlance Section
    st.markdown("""
        <h2 style="text-align: center; margin-bottom: 1.5rem;">
            <i class="bi bi-bullseye" style="color: #e91e63;"></i> Why TradeGlance?
        </h2>
    """, unsafe_allow_html=True)
    
    col_why1, col_why2 = st.columns(2)
    with col_why1:
        st.markdown("""
            | Traditional Approach | TradeGlance |
            |---------------------|-------------|
            | Manual chart analysis | AI-powered insights |
            | Static indicators | Predictive forecasting |
            | News checked separately | Integrated sentiment |
            | Guesswork trading | Data-driven decisions |
        """)
    with col_why2:
        st.markdown("""
            **No clutter. No guesswork.**  
            Just actionable intelligence.
            
            <i class="bi bi-check-circle-fill" style="color: #4caf50;"></i> Future price forecasts  
            <i class="bi bi-check-circle-fill" style="color: #4caf50;"></i> Technical signals  
            <i class="bi bi-check-circle-fill" style="color: #4caf50;"></i> News sentiment analysis  
            <i class="bi bi-check-circle-fill" style="color: #4caf50;"></i> AI-powered explanations  
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Contact Section with Web3Forms
    st.markdown("""
        <h2 style="text-align: center; margin-bottom: 1.5rem;">
            <i class="bi bi-send" style="color: #2196f3;"></i> Get in Touch
        </h2>
        <p style="text-align: center; color: #a0aec0; margin-bottom: 2rem;">
            Have questions, feedback, or want to collaborate? Drop me a message!
        </p>
    """, unsafe_allow_html=True)
    
    # Contact Form
    with st.form("contact_form", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            name = st.text_input("Your Name", placeholder="e.g. Musa Qureshi")
        with col_form2:
            email = st.text_input("Your Email", placeholder="e.g. musaqureshi@example.com")
        
        message = st.text_area("Message", placeholder="Tell me what's on your mind...", height=120)
        
        submitted = st.form_submit_button("📤 Send Message", type="primary", use_container_width=True)
        
        if submitted:
            if name and email and message:
                # Web3Forms API
                try:
                    response = requests.post(
                        "https://api.web3forms.com/submit",
                        data={
                            "access_key": "b712a805-9a6a-40a9-b782-0c9b2c5893d5",
                            "name": name,
                            "email": email,
                            "message": message,
                            "subject": f"TradeGlance Contact: {name}",
                        },
                        timeout=10
                    )
                    
                    # Check response
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            st.success("✅ Message sent successfully! I'll get back to you soon.")
                        else:
                            error_msg = result.get("message", "Unknown error")
                            st.error(f"❌ Failed to send: {error_msg}")
                    else:
                        st.error(f"❌ Server error ({response.status_code}). Please try again later.")
                        
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. Please check your internet connection.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Network error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all fields.")
    
    # Social Links (Using Bootstrap Icons via CDN)
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    col_social1, col_social2, col_social3 = st.columns(3)
    with col_social1:
        st.markdown("""
            <a href="https://github.com/Musa-Qureshi-01" target="_blank" style="text-decoration: none;">
                <div style="text-align: center; padding: 1rem; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
                    <h4><i class="bi bi-github" style="font-size: 1.5rem;"></i> GitHub</h4>
                    <p style="color: #a0aec0; font-size: 0.85rem;">View Source Code</p>
                </div>
            </a>
        """, unsafe_allow_html=True)
    with col_social2:
        st.markdown("""
            <a href="https://linkedin.com/in/musaqureshi" target="_blank" style="text-decoration: none;">
                <div style="text-align: center; padding: 1rem; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
                    <h4><i class="bi bi-linkedin" style="font-size: 1.5rem; color: #0077b5;"></i> LinkedIn</h4>
                    <p style="color: #a0aec0; font-size: 0.85rem;">Connect with Me</p>
                </div>
            </a>
        """, unsafe_allow_html=True)
    with col_social3:
        st.markdown("""
            <a href="mailto:musaqureshi0000@gmail.com" style="text-decoration: none;">
                <div style="text-align: center; padding: 1rem; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
                    <h4><i class="bi bi-envelope-fill" style="font-size: 1.5rem; color: #ea4335;"></i> Email</h4>
                    <p style="color: #a0aec0; font-size: 0.85rem;">musaqureshi0000@gmail.com</p>
                </div>
            </a>
        """, unsafe_allow_html=True)
        
    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; border-top: 1px solid #2d3748; color: #718096;">
            <p style="margin-bottom: 0.5rem;">
                <strong>TradeGlance</strong> — AI-Powered Market Intelligence
            </p>
            <p style="font-size: 0.85rem;">
                © 2026 TradeGlance. All rights reserved.<br>
                Built with <i class="bi bi-heart-fill" style="color: #e25555;"></i> using Streamlit, Prophet & Gemini
            </p>
        </div>
    """, unsafe_allow_html=True)
