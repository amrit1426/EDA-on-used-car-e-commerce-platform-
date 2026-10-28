import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Used Car EDA Dashboard",
    page_icon="🚗",
    layout="wide",
)

# Custom header
st.title("🚗 Used Car Marketplace — EDA Dashboard")
st.markdown("Interactive exploration of the CarLoop used-car dataset.")

# Load data once
@st.cache_data
def load_data():
    df = pd.read_csv("20251115_CarLoop_Dataset.csv")
    return df

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    fuel_types = st.multiselect(
        "Fuel Type",
        options=df["Fuel Type"].dropna().unique(),
        default=df["Fuel Type"].dropna().unique(),
    )
    transmissions = st.multiselect(
        "Transmission",
        options=df["Transmission"].dropna().unique(),
        default=df["Transmission"].dropna().unique(),
    )
    seller_types = st.multiselect(
        "Seller Type",
        options=df["Seller Type"].dropna().unique(),
        default=df["Seller Type"].dropna().unique(),
    )

# Apply filters
filtered = df[
    df["Fuel Type"].isin(fuel_types)
    & df["Transmission"].isin(transmissions)
    & df["Seller Type"].isin(seller_types)
]

# Tabs
tab_overview, tab_analysis, tab_details = st.tabs(["Overview", "Analysis", "Details"])

with tab_overview:
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Listings", len(filtered))
    col2.metric(
        "Avg Price (₹)",
        f"{filtered['Price'].mean():,.0f}" if len(filtered) else "N/A",
    )
    col3.metric(
        "Avg Year",
        f"{filtered['Year'].mean():.0f}" if len(filtered) else "N/A",
    )

    st.subheader("Price Distribution by Brand")
    if len(filtered):
        fig = px.box(
            filtered,
            x="Make",
            y="Price",
            points="outliers",
            title="Price Distribution by Brand",
            color_discrete_sequence=["#38bdf8"],
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc",
            xaxis_gridcolor="#1e293b",
            yaxis_gridcolor="#1e293b",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, width="stretch")

with tab_analysis:
    st.subheader("Price vs Mileage")
    if len(filtered):
        fig = px.scatter(
            filtered,
            x="Kilometer",
            y="Price",
            color="Fuel Type",
            title="Price vs Mileage",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc",
            xaxis_gridcolor="#1e293b",
            yaxis_gridcolor="#1e293b",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, width="stretch")

    st.subheader("Listings by City")
    if len(filtered):
        city_counts = filtered["Location"].value_counts().reset_index()
        city_counts.columns = ["Location", "Count"]
        fig = px.bar(
            city_counts,
            x="Location",
            y="Count",
            title="Listings by City",
            color_discrete_sequence=["#38bdf8"],
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc",
            xaxis_gridcolor="#1e293b",
            yaxis_gridcolor="#1e293b",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, width="stretch")

with tab_details:
    st.subheader("Data Preview")
    st.dataframe(filtered.head(100), width="stretch")

# Footer
st.divider()
st.caption("Built with Streamlit | Data source: 20251115_CarLoop_Dataset.csv")
