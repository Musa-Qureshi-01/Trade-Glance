<div align="center">

# TradeGlance

### AI-Powered Market Intelligence Platform

**Forecast** • **Indicators** • **Sentiment** • **AI Assistant**

<br>

<img src="assets/logo.png" width="120"/>

<br>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)]()
[![AI](https://img.shields.io/badge/AI-FinTech-000000?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)]()

</div>

---
> ## [Preview](https://trade-glance.streamlit.app/)
---

## ⚡ What is TradeGlance?

TradeGlance is a **clean, professional FinTech Platform** that gives traders:

✔️ Future price forecasts  
✔️ Technical signals  
✔️ News sentiment analysis  
✔️ AI-powered explanations  

All in **one minimal interface**.

> No clutter. No guesswork. Just actionable intelligence.

---

## 🎥 Demo

<p align="center">
  <img src="assets/demo.gif" width="95%" alt="TradeGlance Demo">
</p>

> 💡 *Add a short screen recording (10-15s) for instant impact*

---

## ✨ Core Features

### 🔮 Market Forecasting
- Prophet time-series model
- 7–90 day predictions
- Confidence intervals
- Interactive overlay charts

### 📊 Technical Indicators
| Indicator | Description |
|-----------|-------------|
| **SMA** | 20 & 50 day moving averages |
| **RSI** | Relative Strength Index (14-period) |
| **MACD** | Moving Average Convergence Divergence |

### 📰 Sentiment Intelligence
- Live news via **Finnhub API**
- **FinBERT** NLP analysis
- Bullish / Bearish scoring
- Headline-level breakdown

### 🤖 Agentic AI Assistant
- Explains market trends
- Answers trading questions
- Real-time web search
- Gemini 2.0 powered

---

## 🖥️ Interface Layout

```
┌─────────────────────────────────────────────────────┐
│  Sidebar                │  Main Dashboard           │
│  ┌───────────────────┐  │  ┌─────────────────────┐  │
│  │ 📊 Select Ticker  │  │  │ Price + Forecast    │  │
│  │ 📆 Forecast Days  │  │  │ Chart               │  │
│  │ 🔧 Indicators     │  │  ├─────────────────────┤  │
│  │ ▶️ Run Analysis   │  │  │ Technical Indicators│  │
│  └───────────────────┘  │  ├─────────────────────┤  │
│                         │  │ Sentiment Panel     │  │
│  💬 Chat History        │  └─────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

```
User Request
     ↓
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         ↓
┌─────────────────┐     ┌─────────────────┐
│   Data APIs     │     │   Core Engines  │
│  ├── yfinance   │ ──► │  ├── Forecast   │
│  ├── Finnhub    │     │  ├── Indicators │
│  └── Alpha V.   │     │  ├── Sentiment  │
└─────────────────┘     │  └── AI Agent   │
                        └────────┬────────┘
                                 ↓
                        ┌─────────────────┐
                        │ Insights Panel  │
                        └─────────────────┘
```

---

## 📁 Project Structure

```
tradeglance/
│
├── app.py                 # Main application entry
├── config.py              # Configuration & env vars
├── requirements.txt       # Dependencies
├── .env                   # API keys (not in git)
│
├── core/
│   ├── forecast.py        # Prophet forecasting
│   ├── indicators.py      # RSI, MACD, SMA
│   ├── sentiment.py       # FinBERT analysis
│   ├── assistant.py       # AI chatbot (LangGraph)
│   ├── market.py          # Data fetching
│   └── logger.py          # Logging setup
│
├── services/
│   └── yfinance_service.py
│
├── ui/
│   ├── landing.py         # Home page
│   ├── analysis.py        # Market analysis
│   ├── sentiment.py       # Sentiment hub
│   ├── chatbot.py         # AI assistant
│   └── charts.py          # Chart components
│
└── assets/
    ├── logo.png
    └── demo.gif
```

---

## 🚀 Quick Start

### 1️⃣ Clone & Install

```bash
git clone https://github.com/Musa-Qureshi-01/TradeGlance.git
cd TradeGlance
pip install -r requirements.txt
```

### 2️⃣ Configure API Keys

Create a `.env` file:
```env
FINNHUB_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
ALPHAVANTAGE_API_KEY=your_key_here
```

### 3️⃣ Run

```bash
streamlit run app.py
```

### 4️⃣ Open

```
http://localhost:8501
```

---

## 🎯 Why TradeGlance?

| Traditional Approach | TradeGlance |
|---------------------|-------------|
| Manual chart analysis | AI-powered insights |
| Static indicators | Predictive forecasting |
| News checked separately | Integrated sentiment |
| Guesswork trading | Data-driven decisions |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **UI** | Streamlit, Plotly |
| **Data** | yfinance, Finnhub, Alpha Vantage |
| **ML/AI** | Prophet, FinBERT, Gemini 2.0 |
| **Indicators** | pandas, numpy |
| **Agent** | LangGraph, LangChain |
| **Storage** | SQLite |

---

## 📈 Roadmap

- [ ] Strategy optimizer
- [ ] Portfolio tracking
- [ ] Backtesting engine
- [ ] FastAPI backend
- [ ] Next.js frontend (FSD)
- [ ] User authentication

---

## 👤 Author

**Musa Qureshi**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Musa-Qureshi-01)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/musaqureshi)

---

<div align="center">

### ⭐ Star the repo if you find it useful!

**Built with ❤️ for traders & builders**

</div>
