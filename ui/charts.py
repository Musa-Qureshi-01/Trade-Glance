import plotly.graph_objects as go
import pandas as pd

def render_candlestick_chart(df: pd.DataFrame, title: str = "Price Action"):
    """
    Renders an interactive candlestick chart.
    Assuming df has 'ds' (Date), 'Open', 'High', 'Low', 'y' (Close/Price).
    If 'y' is close, and we don't have OHL, we fallback to Line.
    """
    fig = go.Figure()
    
    # Check if we have OHL data. core/market.py fetches everything but might strictly return ds, y.
    # Let's check the user's market.py. It returns df[["ds", "y"]].
    # So we only have Close price. We can only do a Line chart for now unless we change market.py.
    # But user said "dont write code for new things".
    # I will stick to Line chart but make it pretty (Area chart).
    
    fig.add_trace(go.Scatter(
        x=df['ds'], 
        y=df['y'],
        mode='lines',
        name='Price',
        line=dict(color='#2962FF', width=2),
        fill='tozeroy',
        fillcolor='rgba(41, 98, 255, 0.1)'
    ))
    
    # Add SMA Overlays if present
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['ds'], 
            y=df['SMA_20'],
            mode='lines',
            name='SMA 20',
            line=dict(color='#FFA726', width=1.5)
        ))
        
    if 'SMA_50' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['ds'], 
            y=df['SMA_50'],
            mode='lines',
            name='SMA 50',
            line=dict(color='#EF5350', width=1.5)
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=400,
        hovermode="x unified"
    )
    return fig

def render_forecast_chart(history_df, forecast_df):
    """
    Combines historical data with Prophet forecast.
    """
    fig = go.Figure()

    # Historical
    fig.add_trace(go.Scatter(
        x=history_df['ds'],
        y=history_df['y'],
        name="Historical",
        line=dict(color='rgba(255, 255, 255, 0.5)', width=1.5)
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'],
        y=forecast_df['yhat'],
        name="Forecast",
        line=dict(color='#00E676', width=2)
    ))

    # Confidence Interval
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'],
        y=forecast_df['yhat_upper'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'],
        y=forecast_df['yhat_lower'],
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(0, 230, 118, 0.1)',
        name="Confidence Band",
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        title=dict(text="AI Price Prediction", font=dict(size=20, color='white')),
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=500,
        hovermode="x unified"
    )
    
    return fig
