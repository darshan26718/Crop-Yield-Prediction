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

    return df


df = load_data()

# ============================================================
# HEADER
# ============================================================

st.title("🌾 Crop Yield Prediction Dashboard")

st.markdown("""
### Smart Agriculture Analytics Platform

Analyze crop production, rainfall patterns,
seasonal performance and agricultural yield.
""")

st.divider()

# ============================================================
# KPI SECTION
# ============================================================

total_records = len(df)

total_crops = (
    df["Crops"].nunique()
    if "Crops" in df.columns
    else 0
)

total_locations = (
    df["Location"].nunique()
    if "Location" in df.columns
    else 0
)

avg_yield = round(
    df["yeilds"].mean(),
    2
)

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

# ============================================================
# DATASET OVERVIEW
# ============================================================

st.divider()

st.subheader("📄 Dataset Overview")

c1, c2 = st.columns(2)

with c1:

    st.info(
        f"Rows : {df.shape[0]}"
    )

    st.info(
        f"Columns : {df.shape[1]}"
    )

with c2:

    avg_rainfall = round(
        df["Rainfall"].mean(),
        2
    )

    avg_temperature = round(
        df["Temperature"].mean(),
        2
    )

    st.info(
        f"Average Rainfall : {avg_rainfall}"
    )

    st.info(
        f"Average Temperature : {avg_temperature}"
    )

# ============================================================
# CROP DISTRIBUTION
# ============================================================

st.divider()

st.subheader("🌾 Crop Distribution")

crop_count = (
    df["Crops"]
    .value_counts()
    .reset_index()
)

crop_count.columns = [
    "Crop",
    "Count"
]

fig = px.bar(
    crop_count,
    x="Crop",
    y="Count",
    title="Crop Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# SEASON DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📅 Season Distribution")

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
# RAINFALL VS YIELD
# ============================================================

st.divider()

st.subheader("🌧 Rainfall vs Yield")

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

# ============================================================
# TEMPERATURE VS YIELD
# ============================================================

st.divider()

st.subheader("🌡 Temperature vs Yield")

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

st.divider()

st.subheader("🏆 Top Crops By Yield")

top_crops = (
    df.groupby("Crops")["yeilds"]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_crops,
    x="Crops",
    y="yeilds",
    color="yeilds",
    title="Top Crops By Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# TOP LOCATIONS
# ============================================================

st.divider()

st.subheader("📍 Top Locations")

top_locations = (
    df.groupby("Location")["yeilds"]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_locations,
    x="Location",
    y="yeilds",
    color="yeilds",
    title="Top Locations By Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.divider()

st.subheader("🔥 Correlation Heatmap")

numeric_cols = [
    "Area",
    "Rainfall",
    "Temperature",
    "Humidity",
    "price",
    "yeilds"
]

corr = df[numeric_cols].corr()

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
# KEY INSIGHTS
# ============================================================

st.divider()

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

c1, c2, c3 = st.columns(3)

with c1:
    st.success(
        f"🌾 Best Crop: {best_crop}"
    )

with c2:
    st.success(
        f"📍 Best Location: {best_location}"
    )

with c3:
    st.success(
        f"📅 Best Season: {best_season}"
    )

# ============================================================
# DATA PREVIEW
# ============================================================

st.divider()

st.subheader("📄 Dataset Preview")

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
    <p>Built using Python, Streamlit, Plotly and Machine Learning</p>
    </center>
    """,
    unsafe_allow_html=True
)
