import streamlit as st

# Page config
st.set_page_config(page_title=" Video Games Dashboard", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        /* Background */
        .stApp {
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h4, h5, h6 {
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
        }

        .description {
            font-size: 18px;
            text-align: center;
            color: #ffffffaa;
        }

    </style>
""", unsafe_allow_html=True)

# Emoji & Title
st.markdown("<div class='title-text'>Video Games Analysis Dashboard</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>Explore sales trends, top genres, and publisher performance</p>", unsafe_allow_html=True)

# Info block
st.markdown("""
<div class='block'>
    <h4>👋 Welcome</h4>
    <p>This dashboard presents an interactive analysis of video game sales across regions and platforms.</p>
</div>
""", unsafe_allow_html=True)

# Navigation Instructions
st.markdown("""
<div class='block'>
    <h4>🔍 What You Can Explore</h4>
    <ul>
        <li><b>📘 Project Overview</b>: Objective, Dataset Information and Conclusion </li>
        <li><b>📈 Exploratory Data Analysis</b>: Summary stats and data structure</li>
        <li><b>📊 Visualizations</b>: Interactive charts and graphs</li>
    </ul>
</div>
""", unsafe_allow_html=True)
