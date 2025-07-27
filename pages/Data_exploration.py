import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# Setting streamlit page config
st.set_page_config(page_title="Video Games Sales Dashboard", layout="wide")

# To download dataset
st.sidebar.header("Click to Download Dataset")
st.sidebar.download_button(
    label="Download Dataset",
    data="vgsales.csv",
    file_name="vgsales.csv",
    mime="csv",
)

# Loading the data

df = pd.read_csv("vgsales.csv")

# Data Preprocessing
df.fillna({"Year":df["Year"].mean()}, inplace=True)
df.fillna({"Publisher":df["Publisher"].mode()[0]}, inplace=True)
df['Year'] = df['Year'].astype('int64') 

# Displaying total games, top publishers and total global sales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Games: ", len(df))

with col2:
    st.metric("Top Publisher: ", df.groupby('Publisher')['Global_Sales'].sum().idxmax())

with col3:
    st.metric("Total Global Sales", f"{df['Global_Sales'].sum():.2f} M")


# Show dataset
st.subheader("Dataset Preview")
st.dataframe(df.head(10))

st.subheader("Summary Stats")
st.dataframe(df.describe())

st.subheader("Dataset Missing Values")
st.dataframe(df.isnull().sum()) 




