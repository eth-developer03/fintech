import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA

# Binance API Endpoints
BINANCE_BASE_URL = "https://api.binance.com"

# Fetch all crypto tickers
@st.cache_data
def fetch_tickers():
    url = f"{BINANCE_BASE_URL}/api/v3/ticker/price"
    response = requests.get(url)
    data = response.json()
    return {item['symbol']: item['price'] for item in data}

# Fetch historical data
def fetch_historical_data(symbol, interval="1d", limit=100):
    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time",
                                     "quote_asset_volume", "trades", "taker_buy_base", "taker_buy_quote", "ignore"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = pd.to_numeric(df["close"])
    return df[["timestamp", "open", "high", "low", "close", "volume"]]

# ARIMA Forecasting
def forecast_prices_arima(prices, future_days=7):
    model = ARIMA(prices, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=future_days)
    return forecast

# Moving Average Calculation
def calculate_moving_averages(prices, windows):
    averages = {}
    for window in windows:
        averages[f"{window}-Day MA"] = prices.rolling(window=window).mean()
    return averages

# Streamlit UI
st.set_page_config(page_title="Enhanced Crypto Analytics Dashboard", layout="wide")
st.title("🚀 Cryptocurrency Analytics Dashboard with Tickers")

# Fetch and display tickers
tickers = fetch_tickers()
ticker_list = sorted(list(tickers.keys()))
selected_ticker = st.sidebar.selectbox("Select Cryptocurrency Ticker", ticker_list)

# Fetch historical data
days = st.sidebar.slider("Select Historical Data Range (days)", 30, 365, 90)
interval_mapping = {"1d": "Daily", "1h": "Hourly", "15m": "15-Minute"}
selected_interval = st.sidebar.selectbox("Select Interval", list(interval_mapping.keys()), format_func=lambda x: interval_mapping[x])
historical_data = fetch_historical_data(selected_ticker, interval=selected_interval, limit=days)

# Display Live Price
st.subheader(f"🔴 Live Price for {selected_ticker}")
live_price = float(tickers[selected_ticker])
st.metric(label="Current Price (USD)", value=f"${live_price:,.2f}")

# Candlestick Chart
st.subheader(f"📊 Historical Price Trends for {selected_ticker}")
candlestick = go.Figure(data=[go.Candlestick(
    x=historical_data["timestamp"],
    open=pd.to_numeric(historical_data["open"]),
    high=pd.to_numeric(historical_data["high"]),
    low=pd.to_numeric(historical_data["low"]),
    close=historical_data["close"],
    name=selected_ticker
)])
candlestick.update_layout(title="Candlestick Chart", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(candlestick, use_container_width=True)

# Moving Averages
st.subheader(f"📈 Moving Averages for {selected_ticker}")
moving_averages = calculate_moving_averages(historical_data["close"], windows=[7, 30])
for label, series in moving_averages.items():
    candlestick.add_trace(go.Scatter(x=historical_data["timestamp"], y=series, mode="lines", name=label))
st.plotly_chart(candlestick, use_container_width=True)

# Performance Metrics
st.subheader(f"📊 Performance Metrics for {selected_ticker}")
returns = (historical_data["close"].pct_change().mean()) * 100
volatility = historical_data["close"].pct_change().std() * 100
metrics = {
    "Current Price (USD)": f"${live_price:,.2f}",
    "Average Daily Returns (%)": f"{returns:.2f}%",
    "Price Volatility (%)": f"{volatility:.2f}%",
    "Max Price (USD)": f"${historical_data['close'].max():,.2f}",
    "Min Price (USD)": f"${historical_data['close'].min():,.2f}",
    "Median Price (USD)": f"${historical_data['close'].median():,.2f}"
}
st.json(metrics)

# Predictive Analytics
st.subheader(f"🔮 7-Day Price Prediction for {selected_ticker}")
forecast = forecast_prices_arima(historical_data["close"])
future_dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 8)]
forecast_df = pd.DataFrame({"Date": future_dates, "Predicted Price (USD)": forecast})
st.table(forecast_df.style.format({"Predicted Price (USD)": "${:,.2f}"}))

# Footer
st.markdown("Made with ❤️ by [Your Name]")
