import pandas as pd
import numpy as np

def compute_weighted_esg(df):
    """Calculate weighted ESG scores for each cryptocurrency"""
    df["ESG Score"] = (df["esg_e"] + df["esg_s"] + df["esg_g"]) / 3
    return df

def categorize_esg_score(score):
    """Categorize ESG scores into rating categories"""
    if score >= 80:
        return "A+ (Excellent)"
    elif score >= 70:
        return "A (Very Good)"
    elif score >= 60:
        return "B+ (Good)"
    elif score >= 50:
        return "B (Fair)"
    elif score >= 40:
        return "C+ (Below Average)"
    else:
        return "C (Poor)"

def merge_price_and_esg(price_df, esg_df):
    """Merge live price data with ESG scores"""
    # Ensure price data has the right columns
    price_df['last_price'] = pd.to_numeric(price_df['last_price'], errors='coerce')
    
    # Merge on market symbol
    merged = price_df.merge(esg_df, on="market", how="inner")
    
    # Calculate weighted ESG score
    merged = compute_weighted_esg(merged)
    
    # Add ESG rating category
    merged["ESG Rating"] = merged["ESG Score"].apply(categorize_esg_score)
    
    return merged

def calculate_portfolio_metrics(df, holdings_dict=None):
    """Calculate portfolio-level ESG and financial metrics"""
    if holdings_dict is None:
        # Sample holdings if none provided
        holdings_dict = {
            "BTCUSDT": 0.5,
            "ETHUSDT": 1.2,
            "ADAUSDT": 100,
            "MATICUSDT": 500,
            "SOLUSDT": 10
        }
    
    # Add holdings to dataframe
    df["Holding"] = df["market"].map(holdings_dict).fillna(0)
    
    # Calculate portfolio value
    df["Value (USD)"] = df["Holding"] * df["last_price"]
    
    # Calculate portfolio metrics
    total_value = df["Value (USD)"].sum()
    
    if total_value > 0:
        weighted_esg = (df["ESG Score"] * df["Value (USD)"]).sum() / total_value
        weighted_env = (df["esg_e"] * df["Value (USD)"]).sum() / total_value
        weighted_social = (df["esg_s"] * df["Value (USD)"]).sum() / total_value
        weighted_governance = (df["esg_g"] * df["Value (USD)"]).sum() / total_value
    else:
        weighted_esg = weighted_env = weighted_social = weighted_governance = 0
    
    metrics = {
        "total_value": total_value,
        "weighted_esg": weighted_esg,
        "weighted_environmental": weighted_env,
        "weighted_social": weighted_social,
        "weighted_governance": weighted_governance,
        "num_holdings": len(df[df["Holding"] > 0])
    }
    
    return df, metrics

def get_esg_insights(df):
    """Generate insights about ESG performance"""
    insights = []
    
    # Best and worst performers
    best_esg = df.loc[df["ESG Score"].idxmax()]
    worst_esg = df.loc[df["ESG Score"].idxmin()]
    
    insights.append(f"🏆 Highest ESG Score: {best_esg['name']} ({best_esg['ESG Score']:.1f})")
    insights.append(f"⚠️ Lowest ESG Score: {worst_esg['name']} ({worst_esg['ESG Score']:.1f})")
    
    # Category analysis
    high_esg_count = len(df[df["ESG Score"] >= 70])
    total_count = len(df)
    
    insights.append(f"📊 {high_esg_count}/{total_count} assets have ESG scores ≥ 70")
    
    # Environmental leaders
    env_leader = df.loc[df["esg_e"].idxmax()]
    insights.append(f"🌱 Environmental Leader: {env_leader['name']} ({env_leader['esg_e']}/100)")
    
    return insights
