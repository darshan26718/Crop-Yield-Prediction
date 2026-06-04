# ============================================================
# pages/1_Dashboard.py
# Crop Yield Prediction Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="🌾",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/data_season.csv")

df = load_data()

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.metric-card {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

h1,h2,h3 {
    color: #2E8B57;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.title("🌾 Crop Yield Prediction Dashboard")

st.markdown("""
### Smart Agriculture Analytics Platform

Analyze crop production, rainfall patterns, seasonal performance,
and predict agricultural yield using Machine Learning.
""")

st.divider()

# ============================================================
# KPI SECTION
# ============================================================

total_records = len(df)
total_crops = df["Crops"].nunique()
total_locations = df["Location"].nunique()
avg_yield = round(df["yeilds"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Records",
        total_records
    )

with col2:
    st.metric(
        "🌾 Total Crops",
        total_crops
    )

with col3:
    st.metric(
        "📍 Locations",
        total_locations
    )

with col4:
    st.metric(
        "📈 Avg Yield",
        avg_yield
    )

st.divider()

# ============================================================
# DATASET OVERVIEW
# ============================================================

st.subheader("📄 Dataset Overview")

c1, c2 = st.columns(2)

with c1:

    st.info(f"Rows : {df.shape[0]}")
    st.info(f"Columns : {df.shape[1]}")

with c2:

    st.info(
        f"Average Rainfall : {round(df['Rainfall'].mean(),2)}"
    )

    st.info(
        f"Average Temperature : {round(df['Temperature'].mean(),2)}"
    )

# ============================================================
# CHARTS ROW 1
# ============================================================

st.subheader("📊 Crop Analytics")

col1, col2 = st.columns(2)

with col1:

    crop_counts = (
        df["Crops"]
        .value_counts()
        .reset_index()
    )

    crop_counts.columns = [
        "Crop",
        "Count"
    ]

    fig = px.bar(
        crop_counts,
        x="Crop",
        y="Count",
        title="Crop Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    season_count = (
        df["Season"]
        .value_counts()
        .reset_index()
    )

    season_count.columns = [
        "Season",
        "Count"
    ]

    fig = px.pie(
        season_count,
        names="Season",
        values="Count",
        title="Season Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# CHARTS ROW 2
# ============================================================

st.subheader("🌦 Environmental Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        df,
        x="Rainfall",
        y="yeilds",
        color="Season",
        hover_data=["Crops"],
        title="Rainfall vs Yield"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.scatter(
        df,
        x="Temperature",
        y="yeilds",
        color="Season",
        hover_data=["Location"],
        title="Temperature vs Yield"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# TOP CROPS
# ============================================================

st.subheader("🏆 Top Crops by Average Yield")

top_crops = (
    df.groupby("Crops")["yeilds"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_crops,
    x="Crops",
    y="yeilds",
    color="yeilds",
    title="Top 10 Crops"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# LOCATION PERFORMANCE
# ============================================================

st.subheader("📍 Location Performance")

location_yield = (
    df.groupby("Location")["yeilds"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    location_yield,
    x="Location",
    y="yeilds",
    color="yeilds",
    title="Top Locations by Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.subheader("🔥 Correlation Analysis")

numerical_cols = [
    "Area",
    "Rainfall",
    "Temperature",
    "Humidity",
    "price",
    "yeilds"
]

corr = df[numerical_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Feature Correlation Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# INSIGHTS SECTION
# ============================================================

st.subheader("💡 Key Insights")

best_crop = (
    df.groupby("Crops")["yeilds"]
    .mean()
    .idxmax()
)

best_location = (
    df.groupby("Location")["yeilds"]
    .mean()
    .idxmax()
)

best_season = (
    df.groupby("Season")["yeilds"]
    .mean()
    .idxmax()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        f"🌾 Best Crop: {best_crop}"
    )

with col2:
    st.success(
        f"📍 Best Location: {best_location}"
    )

with col3:
    st.success(
        f"📅 Best Season: {best_season}"
    )

# ============================================================
# DATA PREVIEW
# ============================================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# ============================================================
# DOWNLOAD DATASET
# ============================================================

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="crop_yield_dataset.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <center>
        <h4>🌱 Crop Yield Prediction & Analytics Platform</h4>
        <p>Built with Streamlit, Plotly, Pandas & Machine Learning</p>
    </center>
    """,
    unsafe_allow_html=True
)
