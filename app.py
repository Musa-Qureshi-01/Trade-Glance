import streamlit as st
from streamlit_option_menu import option_menu
from ui.landing import render_landing_page
from ui.analysis import render_analysis_page
from ui.sentiment import render_sentiment_page
from ui.chatbot import render_chatbot_page
from core.logger import setup_logging

# Initialize Logging
setup_logging()

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TradeGlance",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS for consistent spacing and responsiveness
st.markdown("""
    <style>
        /* Consistent main content padding */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Consistent sidebar spacing */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }
        
        /* Responsive text sizing */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. NAVIGATION (Sidebar or Top)
# -----------------------------------------------------------------------------

# Use the sidebar for navigation to keep the main area clean
with st.sidebar:
    # SaaS-style header - no top spacing, bigger elements
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("assets/logo.png", width=75)
    with col2:
        st.markdown("""
            <div style="padding-top: 10px;">
                <div style="font-size: 1.6rem; font-weight: 700; margin-bottom: 3px;">TradeGlance</div>
                <div style="font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 0.5px;">Market Intelligence</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Market Analysis", "Sentiment Hub", "AI Agent"],
        icons=["house-fill", "graph-up-arrow", "newspaper", "robot"],
        default_index=0,
        styles={
            "container": {"padding": "0"},
            "icon": {"color": "#718096", "font-size": "16px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0",
                "padding": "10px 12px",
                "border-radius": "8px",
            },
            "nav-link-selected": {
                "background-color": "#2962ff",
                "color": "white",
                "font-weight": "600",
            },
        }
    )
    
    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. MAIN APP ROUTER
# -----------------------------------------------------------------------------

if selected_page == "Home":
    render_landing_page()

elif selected_page == "Market Analysis":
    render_analysis_page()

elif selected_page == "Sentiment Hub":
    render_sentiment_page()

elif selected_page == "AI Agent":
    render_chatbot_page()

# About Section at the bottom of the sidebar
with st.sidebar:
    st.markdown("### About")
    st.info("""
        **TradeGlance**  
        Enterprise-grade market intelligence.  
        © 2026 TradeGlance Inc.
    """)

# # Simple Footer at the very bottom of the page (Only on Landing Page)
# if selected_page == "Home":
#     st.divider()
#     st.markdown(
#         """
#         <div style="text-align: center; color: gray; font-size: 0.8em;">
#             © 2026 TradeGlance Inc. | <a href="#">Privacy</a> | <a href="#">Terms</a>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
