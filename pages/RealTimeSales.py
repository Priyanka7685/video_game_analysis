import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# ---------- Load Dataset ----------
df = pd.read_csv("vgsales.csv")
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

st.set_page_config(page_title="🎮 Game Sales Dashboard", layout="wide")
st.title("🎮 Real-Time Video Game Sales Dashboard", anchor=None)

# ---------- Sidebar Filters ----------
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (2000, 2022))
platforms = st.sidebar.multiselect("Platform", df['Platform'].unique(), default=df['Platform'].unique())
genres = st.sidebar.multiselect("Genre", df['Genre'].unique(), default=df['Genre'].unique())
publishers = st.sidebar.multiselect("Publisher", df['Publisher'].unique(), default=df['Publisher'].unique())
regions = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]

# ---------- Real-Time Simulation Settings ----------
st.sidebar.header("Simulation Settings")
update_interval = st.sidebar.slider("Update Interval (seconds)", 1, 5, 2)

# ---------- Filter Data ----------
filtered_df = df[
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1]) &
    (df['Platform'].isin(platforms)) &
    (df['Genre'].isin(genres)) &
    (df['Publisher'].isin(publishers))
].copy()

prev_sales = filtered_df.set_index('Name')['Global_Sales'].to_dict()

# ---------- Tabs for UI ----------
tabs = st.tabs(["🏆 Leaderboard", "📊 Metrics & Trends", "🌎 Regional Sales"])

# for i in range(num_updates):
    # Simulate new sales increment
filtered_df['Global_Sales'] += np.random.uniform(0, 1, size=len(filtered_df))
filtered_df['Sales_Velocity'] = filtered_df['Global_Sales'] - filtered_df['Name'].map(prev_sales)
filtered_df['Growth_%'] = filtered_df['Sales_Velocity'] / filtered_df['Name'].map(lambda x: prev_sales.get(x,0)+0.01) * 100
prev_sales = filtered_df.set_index('Name')['Global_Sales'].to_dict()
    
    # ---------- Leaderboard ----------
with tabs[0]:
    st.subheader("🏆 Top 10 Games")
    top_games = filtered_df.sort_values(by='Global_Sales', ascending=False).head(10)[
        ['Name', 'Platform', 'Genre', 'Publisher', 'Global_Sales', 'Sales_Velocity', 'Growth_%']
    ]
        # Color growth
    def highlight_growth(val):
        color = "green" if val > 0 else "red"
        return f"color: {color}; font-weight:bold"
    st.dataframe(top_games.style.format({"Global_Sales":"{:.2f}", "Sales_Velocity":"{:.2f}", "Growth_%":"{:.1f}%"}).applymap(highlight_growth, subset=['Growth_%']))
    
    # ---------- Metrics & Trend Charts ----------
    with tabs[1]:
        total_sales = filtered_df['Global_Sales'].sum()
        avg_growth = filtered_df['Growth_%'].mean()
        # Metrics in columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Global Sales", f"{total_sales:.2f}M")
        col2.metric("Avg Growth %", f"{avg_growth:.2f}%")
        col3.metric("Top Platform", filtered_df.groupby('Platform')['Global_Sales'].sum().idxmax())
        
        st.subheader("📈 Sales Trend (Top 5 Games)")
        top5 = filtered_df.sort_values(by='Global_Sales', ascending=False).head(5)
        fig = px.line(top5.melt(id_vars=['Name'], value_vars=['Global_Sales']), x='variable', y='value', color='Name', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # ---------- Regional Sales ----------
    with tabs[2]:
        st.subheader("🌎 Regional Sales")
        regional_sales = filtered_df[regions].sum().reset_index()
        regional_sales.columns = ['Region', 'Sales']
        st.bar_chart(data=regional_sales, x='Region', y='Sales', use_container_width=True)
    
    time.sleep(update_interval)

# ---------- Download CSV ----------
st.sidebar.header("Export Data")
st.sidebar.download_button(
    label="Download Current Top Games CSV",
    data=top_games.to_csv(index=False),
    file_name='top_games.csv',
    mime='text/csv'
)
