import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# ---------- Load Dataset ----------
df = pd.read_csv("vgsales.csv")
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

st.set_page_config(page_title="🎮 Game Sales Dashboard", layout="wide")
st.title("🎮 Future Sales & Profit Prediction")

# ---------- Sidebar Filters ----------
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range", 2000, 2020, (2000, 2020))
platforms = st.sidebar.multiselect("Platform", df['Platform'].unique(), default=df['Platform'].unique())
genres = st.sidebar.multiselect("Genre", df['Genre'].unique(), default=df['Genre'].unique())

# ---------- Filter Data ----------
filtered_df = df[
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1]) &
    (df['Platform'].isin(platforms)) &
    (df['Genre'].isin(genres))
].copy()

# If no data remains after filtering
if filtered_df.empty:
    st.error("⚠️ No data found for selected filters. Try changing the filters.")
    st.stop()

# ---------- Tabs ----------
tabs = st.tabs(["🏆 Leaderboard", "📊 Metrics & Trends", "🌎 Regional Sales", "🔮 Future Sales & Profit Prediction"])

# ---------- Leaderboard ----------
with tabs[0]:
    st.subheader("🏆 Top 10 Games")
    top_games = filtered_df.sort_values(by='Global_Sales', ascending=False).head(10)[
        ['Name', 'Platform', 'Genre', 'Publisher', 'Global_Sales']
    ]
    st.dataframe(top_games.style.format({"Global_Sales":"{:.2f}"}))

# ---------- Metrics & Trends ----------
with tabs[1]:
    total_sales = filtered_df['Global_Sales'].sum()
    col1, col2 = st.columns(2)
    col1.metric("Total Global Sales", f"{total_sales:.2f}M")
    col2.metric("Top Platform", filtered_df.groupby('Platform')['Global_Sales'].sum().idxmax())

    st.subheader("📈 Sales Trend (Top 5 Games)")
    top5 = filtered_df.sort_values(by='Global_Sales', ascending=False).head(5)
    fig = px.line(top5.melt(id_vars=['Name'], value_vars=['Global_Sales']), x='variable', y='value', color='Name', markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ---------- Regional Sales ----------
with tabs[2]:
    st.subheader("🌎 Regional Sales")
    regions = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
    regional_sales = filtered_df[regions].sum().reset_index()
    regional_sales.columns = ['Region', 'Sales']
    st.bar_chart(data=regional_sales, x='Region', y='Sales', use_container_width=True)

# ---------- Future Sales & Profit Prediction ----------
with tabs[3]:
    st.subheader("🔮 Predict Future Success & Profit of Released Games")

    # ---------- Prepare Data ----------
    df_ml = df.copy()
    features = ['Platform','Genre','Publisher','NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']

    # Encode categorical features
    le_dict = {}
    for col in ['Platform','Genre','Publisher']:
        le = LabelEncoder()
        df_ml[col] = le.fit_transform(df_ml[col].astype(str))
        le_dict[col] = le

    X = df_ml[features]
    y = df_ml['Global_Sales']  # Regression target

    # Train Regressor
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train, y_train)

    # ---------- User Input ----------
    st.write("Select Released Game to Predict Its Future Success & Profit:")
    selected_game_name = st.selectbox("Game", filtered_df['Name'].unique())
    game_row = filtered_df[filtered_df['Name'] == selected_game_name].iloc[0]

    # Prepare features for prediction
    game_features = pd.DataFrame({
        'Platform':[le_dict['Platform'].transform([game_row['Platform']])[0]],
        'Genre':[le_dict['Genre'].transform([game_row['Genre']])[0]],
        'Publisher':[le_dict['Publisher'].transform([game_row['Publisher']])[0]],
        'NA_Sales':[game_row['NA_Sales']],
        'EU_Sales':[game_row['EU_Sales']],
        'JP_Sales':[game_row['JP_Sales']],
        'Other_Sales':[game_row['Other_Sales']],
        'Global_Sales':[game_row['Global_Sales']]
    })

    # ---------- Prediction ----------
    predicted_global_sales = reg.predict(game_features)[0]

    # Probability of being a hit: relative to top 25% threshold
    threshold = df['Global_Sales'].quantile(0.75)
    prob = min(predicted_global_sales / threshold, 1)  # decimal between 0 and 1
    hit_status = "Hit ✅" if prob >= 1 else "Flop ❌"

    st.metric("Predicted Global Sales (M)", f"{predicted_global_sales:.2f}")
    st.metric("Probability of Future Success", f"{prob*100:.2f}%")
    st.metric("Predicted Future Status", hit_status)

    # ---------- Profit/Loss Estimation ----------
    st.subheader("💰 Estimate Revenue & Profit/Loss")
    price_per_unit = st.number_input("Game Price per Unit ($)", min_value=1, value=60)
    development_cost = st.number_input("Development Cost ($)", min_value=0, value=500000)

    revenue = predicted_global_sales * price_per_unit
    profit = revenue - development_cost

    st.metric("Estimated Revenue ($)", f"{revenue:,.0f}")
    st.metric("Estimated Profit/Loss ($)", f"{profit:,.0f}")
