import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Used Car EDA Dashboard", layout="wide")

st.title("🚗 Used Car Marketplace — EDA Dashboard")
st.markdown("Interactive exploration of the CarLoop used-car dataset.")

with st.sidebar:
    st.header("Filters")
    df = pd.read_csv("20251115_CarLoop_Dataset.csv")
    fuel_types = st.multiselect("Fuel Type", options=df["Fuel Type"].dropna().unique(), default=df["Fuel Type"].dropna().unique())
    transmissions = st.multiselect("Transmission", options=df["Transmission"].dropna().unique(), default=df["Transmission"].dropna().unique())
    seller_types = st.multiselect("Seller Type", options=df["Seller Type"].dropna().unique(), default=df["Seller Type"].dropna().unique())

filtered = df[
    df["Fuel Type"].isin(fuel_types) &
    df["Transmission"].isin(transmissions) &
    df["Seller Type"].isin(seller_types)
]

col1, col2, col3 = st.columns(3)
col1.metric("Total Listings", len(filtered))
col2.metric("Avg Price (₹)", f"{filtered['Price'].mean():,.0f}" if len(filtered) else "N/A")
col3.metric("Avg Year", f"{filtered['Year'].mean():.0f}" if len(filtered) else "N/A")

st.subheader("Price Distribution by Brand")
if len(filtered):
    fig = px.box(filtered, x="Make", y="Price", points="outliers")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Price vs Mileage")
if len(filtered):
    fig = px.scatter(filtered, x="Kilometer", y="Price", color="Fuel Type", trendline="ols")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Listings by City")
if len(filtered):
    city_counts = filtered["Location"].value_counts().reset_index()
    city_counts.columns = ["Location", "Count"]
    fig = px.bar(city_counts, x="Location", y="Count")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(filtered.head(100))
