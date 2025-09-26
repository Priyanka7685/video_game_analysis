import streamlit as st

# Page config
st.set_page_config(page_title="Video Games Dashboard", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        /* Background */
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h5, h6 {
            color: #ffcc70;
        }

        .block {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        ul {
            font-size: 16px;
            color: #ffffffcc;
        }

        .title-text {
            font-size: 58px;
            text-align: center;
            margin-bottom: 10px;
            color: orange;
            font-weight: 700;
        }

        .description {
            font-size: 18px;
            text-align: center;
            color: #ffffffaa;
        }

    </style>
""", unsafe_allow_html=True)

# Emoji & Title
st.markdown("<div class='title-text'>🎮 Video Games Trend & Insights Dashboard</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>Explore sales trends, top genres, publisher performance, ML predictions, and business insights</p>", unsafe_allow_html=True)

# Info block
st.markdown("""
<div class='block'>
    <h4>👋 Welcome</h4>
    <p>This dashboard presents an interactive track of video game sales across regions and platforms. 
    It also provides machine learning predictions for future game performance and actionable business insights.</p>
</div>
""", unsafe_allow_html=True)

# Navigation Instructions
st.markdown("""
<div class='block'>
    <h4>🔍 What You Can Explore</h4>
    <ul>
        <li><b>📘 Project Overview</b>: Objective, Dataset Information, and Conclusion</li>
        <li><b>📈 Exploratory Data Analysis</b>: Summary stats and data structure</li>
        <li><b>📊 Visualizations</b>: Interactive charts and graphs</li>
        <li><b>🤖 ML Predictions</b>: Forecasting future game performance and sales trends</li>
        
    
</div>
""", unsafe_allow_html=True)
