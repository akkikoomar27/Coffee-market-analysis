
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# DB connection
engine = create_engine("postgresql://neondb_owner:npg_SvpBngb9G8Tt@ep-shiny-thunder-atq1t5e6.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require")

# Load data
df = pd.read_sql("SELECT * FROM coffee_data", engine)

st.title("☕ Coffee Market Analysis Dashboard")

# --- Top Countries ---
top_countries = df.groupby('country')['consumption'].sum().reset_index()
top_countries = top_countries.sort_values(by='consumption', ascending=False).head(10)

fig1 = px.bar(top_countries, x='country', y='consumption', title="Top Coffee Consuming Countries")
st.plotly_chart(fig1)

# --- Trend ---
trend = df.groupby('year')['consumption'].sum().reset_index()

fig2 = px.line(trend, x='year', y='consumption', title="Global Coffee Consumption Trend")
st.plotly_chart(fig2)

# --- Per Capita ---
per_capita = df.groupby('country')['coffee_per_capita'].mean().reset_index()
per_capita = per_capita.sort_values(by='coffee_per_capita', ascending=False).head(10)

fig3 = px.bar(per_capita, x='country', y='coffee_per_capita', title="Top Per Capita Consumers")
st.plotly_chart(fig3)

# --- Recommendation ---
st.subheader("📊 Recommended Markets")

recommend = pd.read_sql("""
    SELECT country, total_consumption, per_capita, avg_population
    FROM market_analysis
    ORDER BY total_consumption DESC, per_capita DESC
    LIMIT 3;
""", engine)

st.dataframe(recommend)
