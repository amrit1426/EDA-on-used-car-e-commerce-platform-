import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page config
st.set_page_config(
    page_title="Used Car EDA Dashboard",
    page_icon="🚗",
    layout="wide",
)

# Custom header
st.title("🚗 Used Car Marketplace — EDA Dashboard")
st.markdown("Interactive exploration of the CarLoop used-car dataset.")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("20251115_CarLoop_Dataset.csv")
    
    # Feature engineering from notebook
    df[['Max Power bhp', 'Max Power rpm']] = df['Max Power'].str.split('@', expand=True)
    df[['Max Torque Nm', 'Max Torque rpm']] = df['Max Torque'].str.split('@', expand=True)
    df = df.drop(['Max Power', 'Max Torque'], axis=1)
    
    str_cols = ['Engine', 'Max Power bhp', 'Max Power rpm', 'Max Torque Nm', 'Max Torque rpm']
    df[str_cols] = df[str_cols].replace({" cc": '', " bhp": '', " rpm": '', " Nm": ''}, regex=True)
    df[str_cols] = df[str_cols].apply(pd.to_numeric, errors='coerce')
    
    df['Age of Car'] = pd.Timestamp('now').year - df['Year']
    df['Volume'] = df['Length'] * df['Width'] * df['Height']
    
    # Missing value treatment
    for col in df.columns:
        if df[col].dtypes == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())
    
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
    makes = st.multiselect(
        "Make",
        options=df["Make"].dropna().unique(),
        default=[],
    )

# Apply filters
filtered = df[
    df["Fuel Type"].isin(fuel_types)
    & df["Transmission"].isin(transmissions)
    & df["Seller Type"].isin(seller_types)
]
if makes:
    filtered = filtered[filtered["Make"].isin(makes)]

# Chart styling helper
def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc",
        xaxis_gridcolor="#1e293b",
        yaxis_gridcolor="#1e293b",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

# Tabs
tab_overview, tab_analysis, tab_details = st.tabs(["Overview", "Analysis", "Details"])

with tab_overview:
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Listings", len(filtered))
    col2.metric(
        "Avg Price (₹)",
        f"{filtered['Price'].mean():,.0f}" if len(filtered) else "N/A",
    )
    col3.metric(
        "Avg Year",
        f"{filtered['Year'].mean():.0f}" if len(filtered) else "N/A",
    )
    col4.metric(
        "Avg Km",
        f"{filtered['Kilometer'].mean():,.0f}" if len(filtered) else "N/A",
    )

    st.subheader("Price Distribution by Brand")
    if len(filtered):
        brand_avg = filtered.groupby("Make")["Price"].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(
            brand_avg,
            x="Make",
            y="Price",
            title="Average Price by Brand",
            color="Price",
            color_continuous_scale=px.colors.sequential.Blues,
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Average Price by Fuel Type")
    if len(filtered):
        fuel_avg = filtered.groupby("Fuel Type")["Price"].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(
            fuel_avg,
            x="Fuel Type",
            y="Price",
            title="Average Price by Fuel Type",
            color="Price",
            color_continuous_scale=px.colors.sequential.Oranges,
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Most Economical Brands")
    if len(filtered):
        eco = filtered.groupby("Make")["Price"].mean().sort_values().head(5).reset_index()
        fig = px.bar(
            eco,
            x="Price",
            y="Make",
            orientation="h",
            title="Top 5 Most Economical Brands",
            color="Price",
            color_continuous_scale=px.colors.sequential.Greens,
        )
        st.plotly_chart(style_chart(fig), width="stretch")

with tab_analysis:
    st.subheader("Price vs Mileage")
    if len(filtered):
        fig = px.scatter(
            filtered,
            x="Kilometer",
            y="Price",
            color="Fuel Type",
            size="Age of Car",
            title="Price vs Mileage (bubble size = car age)",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Price Trend by Manufacturing Year")
    if len(filtered):
        year_avg = filtered.groupby("Year")["Price"].mean().reset_index()
        fig = px.line(
            year_avg,
            x="Year",
            y="Price",
            title="Average Price Trend Over Years",
            markers=True,
        )
        fig.update_traces(line_color="#38bdf8")
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Economical Brands Price Trend")
    if len(filtered):
        eco_makes = filtered.groupby("Make")["Price"].mean().sort_values().head(5).index
        trend = filtered[filtered["Make"].isin(eco_makes) & (filtered["Year"] > 2005)]
        if len(trend):
            trend_data = trend.groupby(["Make", "Year"])["Price"].mean().reset_index()
            fig = px.line(
                trend_data,
                x="Year",
                y="Price",
                color="Make",
                title="Average Price Trend for Economical Brands",
                markers=True,
            )
            st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Volume vs Price by Transmission")
    if len(filtered):
        fig = px.scatter(
            filtered,
            x="Volume",
            y="Price",
            color="Transmission",
            title="Volume vs Price by Transmission",
            color_discrete_sequence=["#38bdf8", "#22d3ee"],
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Correlation Heatmap")
    if len(filtered):
        num_cols = filtered.select_dtypes(["int", "float"]).columns
        corr = filtered[num_cols].corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale="RdBu_r",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, width="stretch")

with tab_details:
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
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Data Preview")
    st.dataframe(filtered.head(100), width="stretch")

# Footer
st.divider()
st.caption("Built with Streamlit | Data source: 20251115_CarLoop_Dataset.csv")
