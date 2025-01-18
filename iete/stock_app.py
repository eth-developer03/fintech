import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Define Alpha Vantage API key and URL
API_KEY = '5JJ7Q678U2SLO9NG'  # Replace with your API key
BASE_URL = "https://www.alphavantage.co/query"


# Function to get live stock data
def get_stock_data(symbol, interval="1min"):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series (1min)" in data:
        df = pd.DataFrame(data["Time Series (1min)"]).T
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        return df
    else:
        st.error("Error fetching data. Check symbol or API limits.")
        return None


# Function to get additional stock metrics
def get_stock_metrics(symbol):
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "MarketCapitalization" in data:
        return {
            "Market Cap": data.get("MarketCapitalization", "N/A"),
            "PE Ratio": data.get("PERatio", "N/A"),
            "Earnings Date": data.get("EarningsDate", "N/A")
        }
    else:
        st.error("Error fetching metrics data.")
        return None


# Function to calculate technical indicators
def calculate_indicators(df):
    # Moving Average (MA)
    df['MA20'] = df['4. close'].rolling(window=20).mean()

    # Relative Strength Index (RSI)
    delta = df['4. close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD (Moving Average Convergence Divergence)
    exp12 = df['4. close'].ewm(span=12, adjust=False).mean()
    exp26 = df['4. close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp12 - exp26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    df['BB_upper'] = df['MA20'] + (2 * df['4. close'].rolling(window=20).std())
    df['BB_lower'] = df['MA20'] - (2 * df['4. close'].rolling(window=20).std())

    # Stochastic Oscillator
    low14 = df['3. low'].rolling(window=14).min()
    high14 = df['2. high'].rolling(window=14).max()
    df['%K'] = (df['4. close'] - low14) / (high14 - low14) * 100
    df['%D'] = df['%K'].rolling(window=3).mean()

    return df


# Plot Candlestick Chart
def plot_candlestick(df, symbol):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['1. open'],
        high=df['2. high'],
        low=df['3. low'],
        close=df['4. close'],
        name=symbol
    )])
    fig.update_layout(title=f"{symbol} Candlestick Chart", xaxis_title="Time", yaxis_title="Price")
    st.plotly_chart(fig)


# Plot Moving Averages
def plot_ma(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df['4. close'], label='Closing Price', color='blue')
    plt.plot(df['MA20'], label='20-period Moving Average', color='red')
    plt.title(f"{symbol} Moving Averages")
    plt.legend()
    st.pyplot(plt)


# Plot RSI
def plot_rsi(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df['RSI'], label='RSI', color='purple')
    plt.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(y=30, color='green', linestyle='--', label='Oversold (30)')
    plt.title(f"{symbol} RSI")
    plt.legend()
    st.pyplot(plt)


# Plot MACD
def plot_macd(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df['MACD'], label='MACD', color='blue')
    plt.plot(df['MACD_signal'], label='MACD Signal', color='red')
    plt.title(f"{symbol} MACD")
    plt.legend()
    st.pyplot(plt)


# Plot Bollinger Bands
def plot_bollinger_bands(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df['4. close'], label='Closing Price', color='blue')
    plt.plot(df['BB_upper'], label='Upper Bollinger Band', color='red', linestyle='--')
    plt.plot(df['BB_lower'], label='Lower Bollinger Band', color='green', linestyle='--')
    plt.title(f"{symbol} Bollinger Bands")
    plt.legend()
    st.pyplot(plt)


# Plot Stochastic Oscillator
def plot_stochastic(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df['%K'], label='%K', color='blue')
    plt.plot(df['%D'], label='%D', color='red')
    plt.axhline(80, color='green', linestyle='--', label="Overbought (80)")
    plt.axhline(20, color='red', linestyle='--', label="Oversold (20)")
    plt.title(f"{symbol} Stochastic Oscillator")
    plt.legend()
    st.pyplot(plt)


# Streamlit app layout
def main():
    st.title("Live Stock Data Dashboard")
    st.sidebar.header("Stock Ticker and Settings")

    symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
    interval = st.sidebar.selectbox("Select Time Interval", ["1min", "5min", "15min", "30min", "60min"])
    time_range = st.sidebar.selectbox("Select Time Range", ["1 Day", "1 Week", "1 Month"])

    if symbol:
        # Fetch stock data
        df = get_stock_data(symbol, interval)
        if df is not None:
            # Show live stock data
            st.subheader(f"Live Data for {symbol}")
            st.write(df.tail())

            # Calculate technical indicators
            df = calculate_indicators(df)

            # Plot Candlestick Chart
            st.subheader(f"{symbol} Candlestick Chart")
            plot_candlestick(df, symbol)

            # Plot Moving Average
            st.subheader(f"{symbol} Moving Average")
            plot_ma(df, symbol)

            # Plot RSI
            st.subheader(f"{symbol} Relative Strength Index (RSI)")
            plot_rsi(df, symbol)

            # Plot MACD
            st.subheader(f"{symbol} Moving Average Convergence Divergence (MACD)")
            plot_macd(df, symbol)

            # Plot Bollinger Bands
            st.subheader(f"{symbol} Bollinger Bands")
            plot_bollinger_bands(df, symbol)

            # Plot Stochastic Oscillator
            st.subheader(f"{symbol} Stochastic Oscillator")
            plot_stochastic(df, symbol)

            # Fetch and display additional stock metrics
            metrics = get_stock_metrics(symbol)
            if metrics:
                st.subheader(f"Stock Metrics for {symbol}")
                st.write(f"Market Cap: {metrics['Market Cap']}")
                st.write(f"P/E Ratio: {metrics['PE Ratio']}")
                st.write(f"Earnings Date: {metrics['Earnings Date']}")


if __name__ == "__main__":
    main()
