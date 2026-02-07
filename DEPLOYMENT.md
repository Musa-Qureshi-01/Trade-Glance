# Streamlit Cloud Deployment Guide

## Environment Variables Setup

### Required Variables:
Go to your Streamlit Cloud dashboard → App Settings → Secrets

Add the following in TOML format:

```toml
# API Keys
FINNHUB_API_KEY = "d63h00pr01qnpqg12o20d63h00pr01qnpqg12o2g"
GOOGLE_API_KEY = "AIzaSyAXCUm-l7m8ESRHFN4kkMt0BdAsOfxhQ_U"
ALPHAVANTAGE_API_KEY = "N9BN6XP65071BE5A"
```

### Steps:
1. Go to https://share.streamlit.io/
2. Click on your app
3. Click "⋮" menu → "Settings"
4. Go to "Secrets" section
5. Paste the above TOML configuration
6. Click "Save"
7. Restart the app

The app will now have access to these environment variables in production.
