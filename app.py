import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils.coindcx_api import fetch_live_prices
from utils.esg_logic import merge_price_and_esg, calculate_portfolio_metrics, get_esg_insights

# Page configuration
st.set_page_config(
    page_title="Crypto ESG Tracker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.esg-excellent { color: #28a745; font-weight: bold; }
.esg-good { color: #17a2b8; font-weight: bold; }
.esg-fair { color: #ffc107; font-weight: bold; }
.esg-poor { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Main title
st.title("🌱 Real-Time Crypto ESG Dashboard")
st.markdown("Track cryptocurrency prices with Environmental, Social & Governance scores")

# Sidebar for configuration
st.sidebar.header("⚙️ Dashboard Settings")

# Portfolio input
st.sidebar.subheader("📊 Portfolio Configuration")
use_custom_portfolio = st.sidebar.checkbox("Use Custom Portfolio", value=False)

if use_custom_portfolio:
    st.sidebar.markdown("Enter your holdings:")
    btc_holding = st.sidebar.number_input("Bitcoin (BTC) Holdings:", min_value=0.0, value=0.5, step=0.1)
    eth_holding = st.sidebar.number_input("Ethereum (ETH) Holdings:", min_value=0.0, value=1.2, step=0.1)
    ada_holding = st.sidebar.number_input("Cardano (ADA) Holdings:", min_value=0.0, value=100.0, step=10.0)
    matic_holding = st.sidebar.number_input("Polygon (MATIC) Holdings:", min_value=0.0, value=500.0, step=50.0)
    sol_holding = st.sidebar.number_input("Solana (SOL) Holdings:", min_value=0.0, value=10.0, step=1.0)
    
    custom_holdings = {
        "BTCUSDT": btc_holding,
        "ETHUSDT": eth_holding,
        "ADAUSDT": ada_holding,
        "MATICUSDT": matic_holding,
        "SOLUSDT": sol_holding
    }
else:
    custom_holdings = None

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)
if auto_refresh:
    st.rerun()

# Load data with error handling
@st.cache_data(ttl=30)  # Cache for 30 seconds
def load_data():
    try:
        # Load live prices
        price_df = fetch_live_prices()
        
        # Load ESG data
        esg_df = pd.read_csv("data/sample_esg_scores.csv")
        
        # Merge data
        merged_df = merge_price_and_esg(price_df, esg_df)
        
        return merged_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load the data
with st.spinner("Loading live cryptocurrency data..."):
    df = load_data()

if df is not None and not df.empty:
    # Calculate portfolio metrics
    df_with_portfolio, portfolio_metrics = calculate_portfolio_metrics(df, custom_holdings)
    
    # Filter to only show holdings with data
    holdings_df = df_with_portfolio[df_with_portfolio["Holding"] > 0].copy()
    
    # Main dashboard content
    st.header("📈 Portfolio Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💹 Portfolio Value",
            value=f"${portfolio_metrics['total_value']:,.2f}",
            delta=None
        )
    
    with col2:
        esg_score = portfolio_metrics['weighted_esg']
        st.metric(
            label="🌿 Weighted ESG Score",
            value=f"{esg_score:.1f}/100",
            delta=None
        )
    
    with col3:
        st.metric(
            label="🏢 Assets in Portfolio",
            value=f"{portfolio_metrics['num_holdings']}",
            delta=None
        )
    
    with col4:
        if portfolio_metrics['total_value'] > 0:
            largest_holding = holdings_df.loc[holdings_df["Value (USD)"].idxmax()]
            st.metric(
                label="🎯 Largest Position",
                value=f"{largest_holding['name']}",
                delta=f"${largest_holding['Value (USD)']:,.0f}"
            )
    
    # ESG Breakdown
    st.header("🌱 ESG Score Breakdown")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🌍 Environmental",
            value=f"{portfolio_metrics['weighted_environmental']:.1f}/100"
        )
    
    with col2:
        st.metric(
            label="👥 Social",
            value=f"{portfolio_metrics['weighted_social']:.1f}/100"
        )
    
    with col3:
        st.metric(
            label="🏛️ Governance",
            value=f"{portfolio_metrics['weighted_governance']:.1f}/100"
        )
    
    # Portfolio allocation and ESG charts
    st.header("📊 Portfolio Analysis")
    
    if not holdings_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💼 Portfolio Allocation")
            fig_pie = px.pie(
                holdings_df,
                values="Value (USD)",
                names="name",
                title="Portfolio Distribution by Value",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("🌱 ESG Scores by Asset")
            fig_bar = px.bar(
                holdings_df,
                x="name",
                y="ESG Score",
                title="ESG Scores of Portfolio Assets",
                color="ESG Score",
                color_continuous_scale="RdYlGn",
                range_color=[0, 100]
            )
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed portfolio table
    st.header("📋 Portfolio Details")
    
    if not holdings_df.empty:
        # Prepare display dataframe
        display_df = holdings_df[[
            "name", "market", "last_price", "Holding", "Value (USD)", 
            "ESG Score", "ESG Rating", "esg_e", "esg_s", "esg_g"
        ]].copy()
        
        display_df["last_price"] = display_df["last_price"].apply(lambda x: f"${x:,.4f}")
        display_df["Value (USD)"] = display_df["Value (USD)"].apply(lambda x: f"${x:,.2f}")
        display_df["ESG Score"] = display_df["ESG Score"].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(
            display_df,
            column_config={
                "name": "Cryptocurrency",
                "market": "Symbol",
                "last_price": "Price",
                "Holding": "Holdings",
                "Value (USD)": "Portfolio Value",
                "ESG Score": "ESG Score",
                "ESG Rating": "ESG Rating",
                "esg_e": "Environmental",
                "esg_s": "Social",
                "esg_g": "Governance"
            },
            use_container_width=True,
            hide_index=True
        )
    
    # ESG Analysis Section
    st.header("🔍 ESG Analysis")
    
    # ESG insights
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 ESG vs Price Performance")
        
        # Create scatter plot of ESG vs Price
        if not df_with_portfolio.empty:
            fig_scatter = px.scatter(
                df_with_portfolio,
                x="ESG Score",
                y="last_price",
                size="Value (USD)" if "Value (USD)" in df_with_portfolio.columns else None,
                color="esg_e",
                hover_name="name",
                title="ESG Score vs Price (Size = Portfolio Value)",
                labels={"last_price": "Price (USD)", "esg_e": "Environmental Score"},
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.subheader("💡 ESG Insights")
        insights = get_esg_insights(df_with_portfolio)
        for insight in insights:
            st.info(insight)
    
    # ESG Category Breakdown
    st.subheader("🌍 ESG Category Analysis")
    
    if not holdings_df.empty:
        # Create grouped bar chart for E, S, G scores
        fig_esg = go.Figure()
        
        fig_esg.add_trace(go.Bar(
            name='Environmental',
            x=holdings_df['name'],
            y=holdings_df['esg_e'],
            marker_color='lightgreen'
        ))
        
        fig_esg.add_trace(go.Bar(
            name='Social',
            x=holdings_df['name'],
            y=holdings_df['esg_s'],
            marker_color='lightblue'
        ))
        
        fig_esg.add_trace(go.Bar(
            name='Governance',
            x=holdings_df['name'],
            y=holdings_df['esg_g'],
            marker_color='lightcoral'
        ))
        
        fig_esg.update_layout(
            title='ESG Component Scores by Asset',
            xaxis_tickangle=-45,
            barmode='group',
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig_esg, use_container_width=True)
    
    # Market Overview
    st.header("🌍 Market Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 All Available Assets")
        market_df = df_with_portfolio[[
            "name", "market", "last_price", "ESG Score", "ESG Rating"
        ]].copy()
        
        market_df["last_price"] = market_df["last_price"].apply(lambda x: f"${x:,.4f}")
        market_df["ESG Score"] = market_df["ESG Score"].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(
            market_df,
            column_config={
                "name": "Cryptocurrency",
                "market": "Symbol", 
                "last_price": "Price",
                "ESG Score": "ESG Score",
                "ESG Rating": "ESG Rating"
            },
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.subheader("🏆 ESG Leaderboard")
        top_esg = df_with_portfolio.nlargest(5, "ESG Score")
        
        for idx, row in top_esg.iterrows():
            st.metric(
                label=f"{row['name']}",
                value=f"{row['ESG Score']:.1f}/100",
                delta=f"${row['last_price']:,.4f}"
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Note**: ESG scores are sample data for demonstration. "
        "Real ESG data should be sourced from certified ESG rating agencies."
    )
    
    # Auto-refresh
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()

else:
    st.error("Unable to load cryptocurrency data. Please check your internet connection and try again.")
    st.info("Make sure you have installed all required packages: `pip install -r requirements.txt`")
