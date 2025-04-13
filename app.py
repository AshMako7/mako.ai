import streamlit as st
import random
import matplotlib.pyplot as plt
import requests
import datetime
import pandas as pd
import plotly.express as px

# Set up the page
st.set_page_config(page_title="Crypto Robo-Advisor", layout="centered")
st.title("🤖 Crypto Robo-Advisor")


coin_info = {
    "BTC": {
        "name": "Bitcoin",
        "desc": "The original cryptocurrency, a decentralized store of value.",
        "logo": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png"
    },
    "ETH": {
        "name": "Ethereum",
        "desc": "Smart contract platform powering DeFi, NFTs, and more.",
        "logo": "https://assets.coingecko.com/coins/images/279/large/ethereum.png"
    },
    "BNB": {
        "name": "BNB",
        "desc": "Native coin of Binance ecosystem and BSC chain.",
        "logo": "https://assets.coingecko.com/coins/images/825/large/binance-coin-logo.png"
    },
    "USDC": {
        "name": "USD Coin",
        "desc": "Stablecoin backed 1:1 with USD.",
        "logo": "https://assets.coingecko.com/coins/images/6319/large/USD_Coin_icon.png"
    },
    "SOL": {
        "name": "Solana",
        "desc": "High-speed Layer 1 blockchain for DeFi & NFTs.",
        "logo": "https://assets.coingecko.com/coins/images/4128/large/Solana.png"
    },
    "MATIC": {
        "name": "Polygon",
        "desc": "Ethereum Layer 2 scaling solution.",
        "logo": "https://assets.coingecko.com/coins/images/4713/large/polygon.png"
    },
    "LINK": {
        "name": "Chainlink",
        "desc": "Decentralized oracle network.",
        "logo": "https://assets.coingecko.com/coins/images/877/large/chainlink-new-logo.png"
    },
    "DOT": {
        "name": "Polkadot",
        "desc": "Blockchain interoperability platform.",
        "logo": "https://assets.coingecko.com/coins/images/12171/large/polkadot.png"
    },
    "ATOM": {
        "name": "Cosmos",
        "desc": "Enabling communication across multiple blockchains.",
        "logo": "https://assets.coingecko.com/coins/images/1481/large/cosmos.png"
    },
    "AVAX": {
        "name": "Avalanche",
        "desc": "High-throughput smart contract platform.",
        "logo": "https://assets.coingecko.com/coins/images/12559/large/avax.png"
    },
    "APT": {
        "name": "Aptos",
        "desc": "Scalable Layer 1 blockchain with Move language.",
        "logo": "https://assets.coingecko.com/coins/images/26455/large/aptos_round.png"
    },
    "ARB": {
        "name": "Arbitrum",
        "desc": "Layer 2 scaling solution for Ethereum.",
        "logo": "https://assets.coingecko.com/coins/images/16547/large/photo_2023-03-29_21.47.00.jpeg"
    },
    "SUI": {
        "name": "Sui",
        "desc": "Fast Layer 1 blockchain built for low latency.",
        "logo": "https://assets.coingecko.com/coins/images/26801/large/sui_asset.jpeg"
    },
    "NEAR": {
        "name": "NEAR Protocol",
        "desc": "User-friendly Layer 1 platform.",
        "logo": "https://assets.coingecko.com/coins/images/10365/large/near.jpg"
    },
    "RUNE": {
        "name": "THORChain",
        "desc": "Cross-chain liquidity protocol.",
        "logo": "https://assets.coingecko.com/coins/images/6595/large/Rune200x200.png"
    }
}



# Define coin pools by risk level
coin_pools = {
    "Low": [("BTC", 0.4), ("ETH", 0.3), ("BNB", 0.2), ("USDC", 0.1)],
    "Medium": [("BTC", 0.25), ("ETH", 0.2), ("SOL", 0.15), ("MATIC", 0.1), ("LINK", 0.1), ("ATOM", 0.1), ("DOT", 0.1)],
    "High": [("SOL", 0.2), ("AVAX", 0.15), ("APT", 0.15), ("MATIC", 0.15), ("ARB", 0.1), ("SUI", 0.1), ("NEAR", 0.1), ("RUNE", 0.05)]
}

# Initialize session state variables
if "risk_level" not in st.session_state:
    st.session_state.risk_level = "Low"
if "investment" not in st.session_state:
    st.session_state.investment = 100
if "suggested_portfolio" not in st.session_state:
    st.session_state.suggested_portfolio = []

# Input form
with st.form("portfolio_form"):
    risk_level = st.selectbox("Select your risk profile:", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(st.session_state.risk_level))
    investment = st.number_input("Enter your investment budget ($)", min_value=100, step=50, value=st.session_state.investment)
    submitted = st.form_submit_button("Get Portfolio Suggestion")

    if submitted:
        st.session_state.risk_level = risk_level
        st.session_state.investment = investment
        pool = coin_pools[risk_level]

        available_coins = [c[0] for c in pool]
        coin_weights_dict = {c[0]: c[1] for c in pool}

        max_unique = min(4, len(available_coins))
        num_coins = random.choice([3, max_unique])
        selected_coins = random.sample(available_coins, k=num_coins)

        # Get weights and normalize
        selected_weights = [coin_weights_dict[coin] for coin in selected_coins]
        total_weight = sum(selected_weights)
        normalized_weights = [w / total_weight for w in selected_weights]

        # Allocate based on normalized weights
        allocations = [investment * w for w in normalized_weights]
        st.session_state.suggested_portfolio = list(zip(selected_coins, allocations))


currency = st.selectbox("Select Currency for Value Conversion", ("USD", "PKR"))

# Conversion rate (change this as needed)
usd_to_pkr = 290  # Example conversion rate


# Show suggested portfolio
if st.session_state.suggested_portfolio:
    # Sorting portfolio by amount (largest to smallest)
    sorted_portfolio = sorted(st.session_state.suggested_portfolio, key=lambda x: x[1], reverse=True)

    st.subheader(f"💼 Suggested Portfolio ({currency})")
    for coin, amount in sorted_portfolio:
        info = coin_info.get(coin, {})
        amount_display = amount if currency == "USD" else amount * usd_to_pkr
        symbol = "PKR " if currency == "PKR" else "$"
        
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image(info.get("logo", ""), width=40)
        with col2:
            st.markdown(f"**{info.get('name', coin)} ({coin})** — {symbol}{amount_display:,.2f}")
            st.caption(info.get("desc", ""))


# ============ INVESTMENT INSIGHTS ============

st.subheader("🧠 Investment Insights")

for coin, amount in sorted_portfolio:
    info = coin_info.get(coin, {})
    weight = amount / st.session_state.investment
    reasoning = ""

    # Insight logic
    if weight >= 0.3:
        reasoning += "This coin has a **high weight**, reflecting strong confidence in its long-term stability or market dominance. "
    elif weight >= 0.15:
        reasoning += "This coin has a **moderate allocation**, indicating it's considered a core part of this risk profile. "
    else:
        reasoning += "This coin is a **smaller allocation**, possibly due to its niche use case or volatility. "

    if coin in ["BTC", "ETH", "USDC"]:
        reasoning += "It's a well-established coin with high market cap, suitable for preserving value."
    elif coin in ["SOL", "MATIC", "LINK", "DOT", "ATOM"]:
        reasoning += "This coin supports DeFi, scalability, or cross-chain features — aligned with growth sectors."
    else:
        reasoning += "It's a newer or emerging project — potentially high growth, but comes with higher risk."

    st.markdown(f"**{info.get('name', coin)} ({coin})**")
    st.caption(reasoning)

# Pie chart
labels = [coin for coin, _ in st.session_state.suggested_portfolio]
sizes = [amount for _, amount in st.session_state.suggested_portfolio]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures pie is a circle.
st.pyplot(fig)

def plot_portfolio_performance(portfolio_performance):
    fig = px.line(portfolio_performance, x="Date", y="Portfolio Value", title="Portfolio Performance Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Portfolio Value (USD)")
    fig.show()

# ============ RISK PROFILE SUMMARY ============
risk_summaries = {
    "Low": """
**Risk Level**: Low 🟢  
**Volatility**: Minimal — stablecoins and blue-chip assets dominate.  
**Diversification**: Moderate — fewer assets but generally stable.  
**Suitability**: Best for conservative investors looking to preserve capital and earn modest returns.
""",
    "Medium": """
**Risk Level**: Medium 🟡  
**Volatility**: Moderate — mix of strong performers and growth coins.  
**Diversification**: High — balanced across multiple sectors and use cases.  
**Suitability**: Ideal for investors seeking growth with manageable risk.
""",
    "High": """
**Risk Level**: High 🔴  
**Volatility**: High — includes emerging assets with high return potential.  
**Diversification**: Broad — but includes more speculative picks.  
**Suitability**: For aggressive investors aiming for high returns with tolerance for volatility.
"""
}

st.subheader("📊 Portfolio Risk Summary")
st.markdown(risk_summaries[st.session_state.risk_level])


# Reset button
if st.button("🔁 Reset"):
    st.session_state.risk_level = "Low"
    st.session_state.investment = 100
    st.session_state.suggested_portfolio = []
    st.rerun()
