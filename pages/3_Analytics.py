# ============================================================
# pages/3_Analytics.py
# Crop Yield Analytics Page
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Crop Analytics",
    page_icon="📈",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/data_season.csv")

    numeric_columns = [
        "Year",
        "Area",
        "Rainfall",
        "Temperature",
        "Humidity",
        "price",
        "yeilds"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    df = df.dropna()

    return df


df = load_data()

# ============================================================
# TITLE
# ============================================================

st.title("📈 Advanced Crop Analytics")

st.markdown("""
Deep analytics and visualization of crop production,
environmental factors and agricultural performance.
""")

st.divider()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔍 Filters")

selected_crop = st.sidebar.selectbox(
    "Select Crop",
    ["All"] + sorted(df["Crops"].unique().tolist())
)

selected_season = st.sidebar.selectbox(
    "Select Season",
    ["All"] + sorted(df["Season"].unique().tolist())
)

selected_location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + sorted(df["Location"].unique().tolist())
)

# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()

if selected_crop != "All":
    filtered_df = filtered_df[
        filtered_df["Crops"] == selected_crop
    ]

if selected_season != "All":
    filtered_df = filtered_df[
        filtered_df["Season"] == selected_season
    ]

if selected_location != "All":
    filtered_df = filtered_df[
        filtered_df["Location"] == selected_location
    ]

# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Analytics Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Records",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Yield",
        round(filtered_df["yeilds"].mean(), 2)
    )

with col3:
    st.metric(
        "Average Rainfall",
        round(filtered_df["Rainfall"].mean(), 2)
    )

with col4:
    st.metric(
        "Average Temperature",
        round(filtered_df["Temperature"].mean(), 2)
    )

st.divider()

# ============================================================
# YIELD TREND
# ============================================================

st.subheader("📈 Yield Trend Over Years")

yield_year = (
    filtered_df.groupby("Year")["yeilds"]
    .mean()
    .reset_index()
)

fig = px.line(
    yield_year,
    x="Year",
    y="yeilds",
    markers=True,
    title="Average Yield Over Time"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# RAINFALL ANALYSIS
# ============================================================

st.subheader("🌧 Rainfall vs Yield")

fig = px.scatter(
    filtered_df,
    x="Rainfall",
    y="yeilds",
    color="Season",
    size="Area",
    hover_data=["Crops"],
    title="Rainfall Impact on Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# TEMPERATURE ANALYSIS
# ============================================================

st.subheader("🌡 Temperature vs Yield")

fig = px.scatter(
    filtered_df,
    x="Temperature",
    y="yeilds",
    color="Season",
    hover_data=["Location"],
    title="Temperature Impact on Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# HUMIDITY ANALYSIS
# ============================================================

st.subheader("💧 Humidity Distribution")

fig = px.histogram(
    filtered_df,
    x="Humidity",
    nbins=20,
    title="Humidity Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# SEASON ANALYSIS
# ============================================================

st.subheader("📅 Season Performance")

season_analysis = (
    filtered_df.groupby("Season")["yeilds"]
    .mean()
    .reset_index()
)

fig = px.bar(
    season_analysis,
    x="Season",
    y="yeilds",
    color="yeilds",
    title="Season-wise Average Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# LOCATION ANALYSIS
# ============================================================

st.subheader("📍 Location Analysis")

location_analysis = (
    filtered_df.groupby("Location")["yeilds"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    location_analysis,
    x="Location",
    y="yeilds",
    color="yeilds",
    title="Location-wise Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# CROP ANALYSIS
# ============================================================

st.subheader("🌾 Crop Analysis")

crop_analysis = (
    filtered_df.groupby("Crops")["yeilds"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    crop_analysis,
    x="Crops",
    y="yeilds",
    color="yeilds",
    title="Crop-wise Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.subheader("🔥 Correlation Heatmap")

numeric_cols = [
    "Area",
    "Rainfall",
    "Temperature",
    "Humidity",
    "price",
    "yeilds"
]

corr = filtered_df[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Feature Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# BOX PLOT
# ============================================================

st.subheader("📦 Yield Distribution by Season")

fig = px.box(
    filtered_df,
    x="Season",
    y="yeilds",
    color="Season",
    title="Yield Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# AREA VS YIELD
# ============================================================

st.subheader("🌱 Cultivated Area vs Yield")

fig = px.scatter(
    filtered_df,
    x="Area",
    y="yeilds",
    color="Crops",
    size="Rainfall",
    title="Area vs Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# DATA TABLE
# ============================================================

st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ============================================================
# DOWNLOAD DATA
# ============================================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Analytics Data",
    data=csv,
    file_name="analytics_data.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <center>
        <h4>📈 Advanced Agricultural Analytics</h4>
        <p>Built with Streamlit, Plotly & Machine Learning</p>
    </center>
    """,
    unsafe_allow_html=True
)
