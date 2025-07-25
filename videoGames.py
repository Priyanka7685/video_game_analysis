import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# Setting streamlit page config
st.set_page_config(page_title="Video Games Sales Dashboard", layout="wide")


# Loading the data
def load_data():
    df = pd.read_csv("vgsales.csv")

    # Data Preprocessing
    df.fillna({"Year":df["Year"].mean()}, inplace=True)
    df.fillna({"Publisher":df["Publisher"].mode()[0]}, inplace=True)
    df['Year'] = df['Year'].astype('int64') 
    return df

df = load_data()

search_game = st.sidebar.text_input("Search by Game Name")
if search_game:
    df = df[df['Name'].str.contains(search_game, case=False, na=False)]


# Displaying title
st.title("VIDEO GAMES ANALYSIS DASHBOARD")
st.subheader("Raw data preview")
st.dataframe(df.head(10))


# Displaying total games, top publishers and total global sales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Games: ", len(df))

with col2:
    st.metric("Top Publisher: ", df.groupby('Publisher')['Global_Sales'].sum().idxmax())

with col3:
    st.metric("Total Global Sales", f"{df['Global_Sales'].sum():.2f} M")    

# Sidebar filters
if not search_game:
    st.sidebar.header("Filter options")
    genre_filter = st.sidebar.multiselect("Select genre", df['Genre'].unique())
    platform_filter = st.sidebar.multiselect("Select platform", df["Platform"].unique())

    if genre_filter:
        df = df[df['Genre'].isin(genre_filter)]

    if platform_filter:
        df = df[df['Platform'].isin(platform_filter)]



# Graphs

# 1. Global Sales Distribution  
st.subheader("📈 Global Sales Distribution")
fig = px.histogram(df, x='Global_Sales', nbins=40, 
                   color_discrete_sequence=["#7F00FF"], 
                   title="Global Sales (Millions)")
st.plotly_chart(fig, use_container_width=True)


# 2. Top 10 Games by global sales
st.subheader("Top 10 games by Global sales")
top10 = df.sort_values(by='Global_Sales', ascending=False).head(10)

fig = px.bar(top10, x='Name', y='Global_Sales', color='Platform',
             title="Top 10 Best-Selling Games", labels={'Global_Sales': 'Global Sales (Millions)'})
st.plotly_chart(fig, use_container_width=True)


# 3. Region-wise genre sales
st.subheader("Region-wise genre sales")
genre_region = df.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
genre_region = genre_region.melt(id_vars='Genre', var_name='Region', value_name='Sales')

fig = px.bar(genre_region, x='Genre', y='Sales', color='Region', barmode='group',
             title="Genre Sales Comparison Across Regions")
st.plotly_chart(fig, use_container_width=True)

# 4. Games releases over the years

st.subheader("Games releases over the years")
games_per_year = df['Year'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(x=games_per_year.index, y=games_per_year.values, marker='o', color='crimson', ax = ax)
ax.set_title("Number of Games Released Per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Games Released")
st.pyplot(fig)


# 5. Top 10 publishers by global sales

st.subheader("Top 10 publishers by global sales")
top_publishers = df.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(10).reset_index()

fig = px.bar(top_publishers, x='Global_Sales', y='Publisher', orientation='h', color='Publisher',
             title="Top 10 Publishers by Global Sales", labels={'Global_Sales': 'Global Sales (Millions)'})
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig, use_container_width=True)


# 6. Global Sales by genre

st.subheader("Global Sales by Genre")
genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).reset_index()

fig = px.pie(genre_sales, values='Global_Sales', names='Genre',
             title="🎮 Global Sales Distribution by Genre",
             hole=0.4)  # Donut style
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)


# 7. Correlation Heatmap of Sales by region

st.subheader("Correlation Heatmap of Sales by Region")
numeric_df = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']]

plt.figure(figsize=(10, 3))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap of Sales by Region')
st.pyplot(plt)


# 8. Sales comparison over the years

st.subheader("Sales comparison over the years")
fig = px.scatter(
    df, 
    x='NA_Sales', 
    y='EU_Sales', 
    animation_frame='Year', 
    size='Global_Sales', 
    color='Genre',
    hover_name='Name', 
    title='Sales Comparison Over Years',
    size_max=60,
    range_x=[0, df['NA_Sales'].max() + 1],
    range_y=[0, df['EU_Sales'].max() + 1]
)

st.plotly_chart(fig, use_container_width=True, key="animated_sales_plot")

