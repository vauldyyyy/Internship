"""
Nifty 100 Financial Intelligence System - Web Dashboard
Streamlit-based interactive dashboard with real data

Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ============== PAGE CONFIG ==============
st.set_page_config(
    page_title="Nifty 100 Financial Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CSS STYLING ==============
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    h1 {
        color: #1f2937;
        margin-bottom: 30px;
    }
    h2 {
        color: #374151;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ============== DATABASE CONNECTION ==============
@st.cache_resource
def get_db_connection():
    """Create cached database connection"""
    conn = sqlite3.connect("bluestock_dw.db")
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_data
def load_data():
    """Load data from database"""
    conn = get_db_connection()
    
    companies = pd.read_sql("SELECT * FROM dim_company", conn)
    profit_loss = pd.read_sql("SELECT * FROM fact_profit_loss", conn)
    balance_sheet = pd.read_sql("SELECT * FROM fact_balance_sheet", conn)
    cash_flow = pd.read_sql("SELECT * FROM fact_cash_flow", conn)
    ml_scores = pd.read_sql("SELECT * FROM fact_ml_scores", conn)
    pros_cons = pd.read_sql("SELECT * FROM fact_pros_cons", conn)
    years = pd.read_sql("SELECT * FROM dim_year ORDER BY year_id", conn)
    
    return {
        'companies': companies,
        'profit_loss': profit_loss,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow,
        'ml_scores': ml_scores,
        'pros_cons': pros_cons,
        'years': years
    }

# ============== UTILITY FUNCTIONS ==============
def get_health_color(score):
    """Get color based on health score"""
    if score >= 85:
        return "#10B981"  # Green
    elif score >= 70:
        return "#34D399"  # Light Green
    elif score >= 50:
        return "#FBBF24"  # Yellow
    else:
        return "#EF4444"  # Red

def get_health_label(score):
    """Get label based on health score"""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Weak"

# ============== MAIN APP ==============
def main():
    data = load_data()
    
    # Sidebar Navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio(
        "Select Dashboard:",
        [
            "📈 Executive Overview",
            "🏢 Company Deep Dive",
            "🏭 Sector Analysis",
            "🤖 ML Intelligence",
            "📊 Data Explorer"
        ]
    )
    
    if page == "📈 Executive Overview":
        executive_overview(data)
    elif page == "🏢 Company Deep Dive":
        company_deep_dive(data)
    elif page == "🏭 Sector Analysis":
        sector_analysis(data)
    elif page == "🤖 ML Intelligence":
        ml_intelligence(data)
    else:
        data_explorer(data)

# ============== PAGE: EXECUTIVE OVERVIEW ==============
def executive_overview(data):
    st.title("📈 Executive Overview Dashboard")
    st.markdown("*High-level market snapshot for decision makers*")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # KPI Cards
    total_companies = data['companies'].shape[0]
    avg_roe = data['profit_loss']['roe_pct_3y'].mean()
    total_revenue = data['profit_loss']['sales'].sum()
    avg_health = data['ml_scores']['overall_score'].mean()
    
    with col1:
        st.metric("Total Companies", f"{total_companies}", delta=None)
    
    with col2:
        st.metric("Average ROE", f"{avg_roe:.1f}%", delta=None)
    
    with col3:
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}Cr", delta=None)
    
    with col4:
        st.metric("Avg Health Score", f"{avg_health:.1f}/100", delta=None)
    
    st.divider()
    
    # Revenue by Sector
    st.subheader("💰 Revenue by Sector")
    col1, col2 = st.columns(2)
    
    with col1:
        sector_revenue = (
            data['profit_loss']
            .merge(data['companies'], on='symbol')
            .groupby('sector')['sales']
            .sum()
            .sort_values(ascending=False)
        )
        
        fig1 = px.bar(
            x=sector_revenue.index,
            y=sector_revenue.values,
            labels={'x': 'Sector', 'y': 'Revenue (₹ Cr)'},
            title='Revenue by Sector',
            color=sector_revenue.values,
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    # Health Score Distribution
    with col2:
        health_dist = data['ml_scores']['health_label'].value_counts()
        colors_map = {
            'Excellent': '#10B981',
            'Good': '#34D399',
            'Average': '#FBBF24',
            'Weak': '#EF4444'
        }
        colors = [colors_map.get(label, '#gray') for label in health_dist.index]
        
        fig2 = px.pie(
            values=health_dist.values,
            names=health_dist.index,
            title='Company Health Distribution',
            color=health_dist.index,
            color_discrete_map=colors_map
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # Revenue Trend
    st.subheader("📅 5-Year Revenue Trend")
    
    # Prepare trend data
    trend_data = data['profit_loss'].groupby('year_id')['sales'].sum().reset_index()
    trend_data = trend_data.merge(data['years'], left_on='year_id', right_on='year_id')
    
    fig3 = px.line(
        trend_data,
        x='year_value',
        y='sales',
        markers=True,
        title='Total Market Revenue Trend',
        labels={'year_value': 'Year', 'sales': 'Revenue (₹ Cr)'}
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Top Companies Table
    st.subheader("🏆 Top 10 Companies by ROE")
    
    top_companies = (
        data['profit_loss']
        .merge(data['companies'][['symbol', 'company_name', 'sector']], on='symbol')
        .groupby('symbol')
        .agg({
            'company_name': 'first',
            'sector': 'first',
            'roe_pct_3y': 'mean',
            'opm_pct': 'mean',
            'sales': 'mean'
        })
        .sort_values('roe_pct_3y', ascending=False)
        .head(10)
        .reset_index()
    )
    
    st.dataframe(
        top_companies[['company_name', 'sector', 'roe_pct_3y', 'opm_pct', 'sales']].rename(columns={
            'company_name': 'Company',
            'sector': 'Sector',
            'roe_pct_3y': 'ROE %',
            'opm_pct': 'OPM %',
            'sales': 'Avg Revenue'
        }),
        use_container_width=True,
        hide_index=True
    )

# ============== PAGE: COMPANY DEEP DIVE ==============
def company_deep_dive(data):
    st.title("🏢 Company Deep Dive")
    st.markdown("*Detailed analysis for individual company research*")
    
    # Company Selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_company = st.selectbox(
            "Select Company:",
            data['companies'].sort_values('company_name')['company_name'].values
        )
    
    # Get symbol using proper indexing
    symbol_mask = data['companies']['company_name'] == selected_company
    symbol = data['companies'][symbol_mask]['symbol'].values[0]
    company_info = data['companies'][data['companies']['symbol'] == symbol].iloc[0]
    
    # Get company data
    company_pl = data['profit_loss'][data['profit_loss']['symbol'] == symbol].sort_values('year_id')
    company_bs = data['balance_sheet'][data['balance_sheet']['symbol'] == symbol]
    company_cf = data['cash_flow'][data['cash_flow']['symbol'] == symbol]
    
    health_mask = data['ml_scores']['symbol'] == symbol
    company_health = data['ml_scores'][health_mask].iloc[0] if health_mask.any() else None
    
    pros_cons_mask = data['pros_cons']['symbol'] == symbol
    company_pros_cons = data['pros_cons'][pros_cons_mask].iloc[0] if pros_cons_mask.any() else None
    
    with col2:
        if company_health is not None:
            health_score = company_health['overall_score']
            health_color = get_health_color(health_score)
            st.markdown(f"""
            <div style="background-color: {health_color}; padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3>Health Score</h3>
                <h1>{health_score:.0f}/100</h1>
                <p>{get_health_label(health_score)}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No health score data available for this company")
    
    st.divider()
    
    # Financial Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    latest_year = company_pl.iloc[-1] if len(company_pl) > 0 else None
    
    if latest_year is not None:
        with col1:
            st.metric("Latest Revenue", f"₹{latest_year['sales']:,.0f}Cr")
        with col2:
            st.metric("Latest Net Profit", f"₹{latest_year['net_profit']:,.0f}Cr")
        with col3:
            st.metric("ROE", f"{latest_year['roe_pct_3y']:.1f}%")
        with col4:
            st.metric("OPM", f"{latest_year['opm_pct']:.1f}%")
    
    st.divider()
    
    # 5-Year Profitability Trend
    if len(company_pl) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.line(
                company_pl.merge(data['years'], on='year_id'),
                x='year_value',
                y=['roe_pct_3y', 'opm_pct'],
                markers=True,
                title=f'{selected_company} - Profitability Metrics',
                labels={'year_value': 'Year', 'value': 'Percentage'}
            )
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                company_pl.merge(data['years'], on='year_id'),
                x='year_value',
                y='sales',
                title=f'{selected_company} - Revenue Trend',
                labels={'year_value': 'Year', 'sales': 'Revenue (₹ Cr)'}
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # Pros and Cons
    if company_pros_cons is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Strengths")
            st.write(company_pros_cons['pros_text'])
        with col2:
            st.subheader("⚠️ Risks")
            st.write(company_pros_cons['cons_text'])
    else:
        st.info("No pros/cons analysis available for this company")
    
    # Financial Data Table
    st.subheader("📊 5-Year Financial Summary")
    
    if len(company_pl) > 0:
        summary_df = company_pl.merge(data['years'], on='year_id')[
            ['year_value', 'sales', 'net_profit', 'opm_pct', 'roe_pct_3y']
        ].rename(columns={
            'year_value': 'Year',
            'sales': 'Revenue (₹Cr)',
            'net_profit': 'Net Profit (₹Cr)',
            'opm_pct': 'OPM %',
            'roe_pct_3y': 'ROE %'
        })
        
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ============== PAGE: SECTOR ANALYSIS ==============
def sector_analysis(data):
    st.title("🏭 Sector Analysis")
    st.markdown("*Cross-company sector comparison and benchmarking*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_sectors = st.multiselect(
            "Select Sectors:",
            data['companies']['sector'].unique(),
            default=data['companies']['sector'].unique()[:3]
        )
    
    # Filter data
    sector_companies = data['companies'][data['companies']['sector'].isin(selected_sectors)]['symbol'].values
    sector_pl = data['profit_loss'][data['profit_loss']['symbol'].isin(sector_companies)]
    
    st.divider()
    
    # Sector Comparison
    col1, col2 = st.columns(2)
    
    with col1:
        sector_metrics = (
            sector_pl
            .merge(data['companies'], on='symbol')
            .groupby('sector')
            .agg({
                'sales': 'mean',
                'roe_pct_3y': 'mean',
                'opm_pct': 'mean',
                'symbol': 'nunique'
            })
            .rename(columns={'symbol': 'Company Count'})
            .reset_index()
        )
        
        fig1 = px.bar(
            sector_metrics,
            x='sector',
            y='roe_pct_3y',
            title='Average ROE by Sector',
            labels={'sector': 'Sector', 'roe_pct_3y': 'ROE %'},
            color='roe_pct_3y',
            color_continuous_scale='RdYlGn'
        )
        fig1.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(
            sector_metrics,
            x='sector',
            y='opm_pct',
            title='Average OPM by Sector',
            labels={'sector': 'Sector', 'opm_pct': 'OPM %'},
            color='opm_pct',
            color_continuous_scale='Blues'
        )
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # Sector Comparison Table
    st.subheader("📊 Sector Comparison Matrix")
    
    comparison_df = (
        sector_pl
        .merge(data['companies'], on='symbol')
        .groupby('sector')
        .agg({
            'sales': ['sum', 'mean'],
            'net_profit': ['sum', 'mean'],
            'roe_pct_3y': 'mean',
            'opm_pct': 'mean',
            'symbol': 'nunique'
        })
        .round(2)
        .reset_index()
    )
    
    comparison_df.columns = ['Sector', 'Total Revenue', 'Avg Revenue', 'Total Profit', 'Avg Profit', 'Avg ROE %', 'Avg OPM %', 'Companies']
    
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# ============== PAGE: ML INTELLIGENCE ==============
def ml_intelligence(data):
    st.title("🤖 ML Intelligence & Health Scores")
    st.markdown("*AI-based health assessment and investment signals*")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        excellent = len(data['ml_scores'][data['ml_scores']['overall_score'] >= 85])
        st.metric("Excellent Health (85+)", excellent)
    
    with col2:
        good = len(data['ml_scores'][(data['ml_scores']['overall_score'] >= 70) & (data['ml_scores']['overall_score'] < 85)])
        st.metric("Good Health (70-84)", good)
    
    with col3:
        weak = len(data['ml_scores'][data['ml_scores']['overall_score'] < 50])
        st.metric("Weak Health (<50)", weak)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    # Health Score Distribution
    with col1:
        health_dist = data['ml_scores']['health_label'].value_counts()
        colors_map = {'Excellent': '#10B981', 'Good': '#34D399', 'Average': '#FBBF24', 'Weak': '#EF4444'}
        
        fig1 = px.pie(
            values=health_dist.values,
            names=health_dist.index,
            title='Health Score Distribution',
            color=health_dist.index,
            color_discrete_map=colors_map
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    # Health Scores Gauge
    with col2:
        top_scores = data['ml_scores'].nlargest(5, 'overall_score').merge(
            data['companies'][['symbol', 'company_name']], on='symbol'
        )
        
        fig2 = px.bar(
            top_scores,
            y='company_name',
            x='overall_score',
            orientation='h',
            title='Top 5 Companies by Health Score',
            labels={'company_name': 'Company', 'overall_score': 'Health Score'},
            color='overall_score',
            color_continuous_scale='RdYlGn',
            range_color=[0, 100]
        )
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # Company Health Scores Table
    st.subheader("📋 All Companies Health Scores")
    
    scores_table = (
        data['ml_scores']
        .merge(data['companies'][['symbol', 'company_name', 'sector']], on='symbol')
        .sort_values('overall_score', ascending=False)
        .rename(columns={
            'company_name': 'Company',
            'sector': 'Sector',
            'overall_score': 'Health Score',
            'health_label': 'Rating'
        })
        [['Company', 'Sector', 'Health Score', 'Rating']]
    )
    
    st.dataframe(scores_table, use_container_width=True, hide_index=True)

# ============== PAGE: DATA EXPLORER ==============
def data_explorer(data):
    st.title("📊 Data Explorer")
    st.markdown("*Browse raw data tables*")
    
    table_choice = st.selectbox(
        "Select Table:",
        [
            "Companies",
            "Profit & Loss",
            "Balance Sheet",
            "Cash Flow",
            "ML Scores",
            "Pros & Cons"
        ]
    )
    
    if table_choice == "Companies":
        st.dataframe(data['companies'], use_container_width=True)
    elif table_choice == "Profit & Loss":
        st.dataframe(data['profit_loss'], use_container_width=True)
    elif table_choice == "Balance Sheet":
        st.dataframe(data['balance_sheet'], use_container_width=True)
    elif table_choice == "Cash Flow":
        st.dataframe(data['cash_flow'], use_container_width=True)
    elif table_choice == "ML Scores":
        st.dataframe(data['ml_scores'], use_container_width=True)
    else:
        st.dataframe(data['pros_cons'], use_container_width=True)

if __name__ == "__main__":
    main()
