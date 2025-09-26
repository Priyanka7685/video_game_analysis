import streamlit as st

# Configure the page
st.set_page_config(page_title="About the Project", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
        }
        .card {
            background-color: rgba(255, 255, 255, 0.05);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
        }
        .title-text {
            font-size: 38px;
            font-weight: 700;
        }
        .section-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        ul {
            padding-left: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title-text'>📁 About the Project</h1>", unsafe_allow_html=True)

# Objective
st.markdown("""
<div class='card'>
    <div class='section-title'>🎯 Objective</div>
    <p>
        The objective of this project is to analyze the <strong>Video Game Trend Tracker</strong> dataset to uncover trends, patterns, and insights across different regions, platforms, and genres.
        Additionally, the project leverages <strong>Machine Learning</strong> to predict future sales and identify potential high-performing games. 
        These insights help developers, publishers, and investors make informed business decisions.
    </p>
</div>
""", unsafe_allow_html=True)

# Dataset Information
st.markdown("""
<div class='card'>
    <div class='section-title'>📂 Dataset Information</div>
    <p>The dataset contains information on video game sales across regions and platforms, with the following columns:</p>
    <ul>
        <li><strong>Name</strong>: Name of the game</li>
        <li><strong>Platform</strong>: Platform on which the game was released</li>
        <li><strong>Year</strong>: Release year of the game</li>
        <li><strong>Genre</strong>: Genre of the game</li>
        <li><strong>Publisher</strong>: Publisher of the game</li>
        <li><strong>NA_Sales</strong>: Sales in North America</li>
        <li><strong>EU_Sales</strong>: Sales in Europe</li>
        <li><strong>JP_Sales</strong>: Sales in Japan</li>
        <li><strong>Other_Sales</strong>: Sales in other regions</li>
        <li><strong>Global_Sales</strong>: Total global sales</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Insights
st.markdown("""
<div class='card'>
    <div class='section-title'>📈 Insights & Business Value</div>
    <p>This project provides value in several ways:</p>
    <ul>
        <li>Understanding market dynamics of video games across regions and platforms</li>
        <li>Identifying the most popular genres, platforms, and publishers</li>
        <li>Analyzing the impact of release year, genre, and publisher on sales</li>
        <li>Providing <strong>ML-based predictions</strong> for future game performance</li>
        <li>Deriving actionable <strong>business insights</strong> like potential profit, risk, and market opportunities</li>
        <li>Helping game developers and publishers optimize strategies and marketing decisions</li>
    </ul>
</div>
""", unsafe_allow_html=True)
