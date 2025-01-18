import streamlit as st
import pandas as pd
import plotly.express as px
from coingecko import MultiAgentSystem

# Initialize the MultiAgentSystem
system = MultiAgentSystem()

# Streamlit Dashboard
st.set_page_config(page_title="Crypto Analysis Dashboard", layout="wide")
st.title("Cryptocurrency Market Analysis Dashboard")

# Sidebar for user input
st.sidebar.header("Settings")
analysis_type = st.sidebar.radio("Choose Analysis Type", ["Global Market Overview", "Trending Coins", "Agent Insights", "Token Extraction"])

# Fetch Data
st.sidebar.markdown("**Fetch Data**")
if st.sidebar.button("Run Analysis"):
    with st.spinner("Fetching data and running analysis..."):
        system.run()
    st.sidebar.success("Analysis Completed!")

# Global Market Overview
if analysis_type == "Global Market Overview":
    st.subheader("Global Cryptocurrency Market Overview")
    global_data = system.api.get_global_data()
    
    if global_data:
        market_cap = global_data["data"]["total_market_cap"]["usd"]
        volume_24h = global_data["data"]["total_volume"]["usd"]
        market_cap_change = global_data["data"]["market_cap_change_percentage_24h_usd"]

        st.metric(label="Total Market Cap (USD)", value=f"${market_cap:,.2f}")
        st.metric(label="24h Volume (USD)", value=f"${volume_24h:,.2f}")
        st.metric(label="Market Cap Change (24h)", value=f"{market_cap_change:.2f}%")
    else:
        st.warning("Unable to fetch global market data.")

# Trending Coins
elif analysis_type == "Trending Coins":
    st.subheader("Trending Cryptocurrencies (Last 24h)")
    trending_data = system.api.get_trending()

    if trending_data:
        trending_coins = pd.DataFrame([
            {
                "Rank": idx + 1,
                "Name": coin["item"]["name"],
                "Symbol": coin["item"]["symbol"],
                "Market Cap Rank": coin["item"]["market_cap_rank"],
                "Price (BTC)": coin["item"]["price_btc"],
            }
            for idx, coin in enumerate(trending_data)
        ])
        st.dataframe(trending_coins)

        fig = px.bar(trending_coins, x="Name", y="Price (BTC)", title="Trending Coins (Price in BTC)", text="Price (BTC)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Unable to fetch trending coins.")

# Agent Insights
elif analysis_type == "Agent Insights":
    st.subheader("Agent-Based Analysis")
    st.write("Agent One (Technical Analysis):")
    agent_one_memory = system.agent_one.memory["conversations"]
    if agent_one_memory:
        st.json(agent_one_memory[-1]["response"])
    else:
        st.info("No recent data for Agent One.")

    st.write("Agent Two (Fundamental Analysis):")
    agent_two_memory = system.agent_two.memory["conversations"]
    if agent_two_memory:
        st.json(agent_two_memory[-1]["response"])
    else:
        st.info("No recent data for Agent Two.")

# Token Extraction
elif analysis_type == "Token Extraction":
    st.subheader("Extracted Tokens")
    token_history = system.token_extractor.token_history

    if not token_history.empty:
        st.dataframe(token_history)
        fig = px.histogram(token_history, x="token", title="Mentioned Tokens", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No tokens extracted yet. Run the analysis to see results.")

# Footer
st.sidebar.markdown("Made with ❤️ by Moon Dev")
