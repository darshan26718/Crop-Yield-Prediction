# ============================================================
# pages/4_Insights.py
# Smart Agricultural Insights Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.insights import (
    get_best_crop,
    get_best_location,
    get_best_season,
    get_top_crops,
    get_top_locations,
    get_season_performance,
    generate_recommendations,
    generate_full_report
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart Insights",
    page_icon="🧠",
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
# HEADER
# ============================================================

st.title("🧠 AI Powered Agricultural Insights")

st.markdown("""
Generate smart recommendations and discover hidden patterns
from agricultural data using analytics and machine learning.
""")

st.divider()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔍 Filters")

selected_location = st.sidebar.multiselect(
    "Location",
    options=sorted(df["Location"].unique()),
    default=sorted(df["Location"].unique())
)

selected_crop = st.sidebar.multiselect(
    "Crop",
    options=sorted(df["Crops"].unique()),
    default=sorted(df["Crops"].unique())
)

selected_season = st.sidebar.multiselect(
    "Season",
    options=sorted(df["Season"].unique()),
    default=sorted(df["Season"].unique())
)

filtered_df = df[
    (df["Location"].isin(selected_location))
    &
    (df["Crops"].isin(selected_crop))
    &
    (df["Season"].isin(selected_season))
]

# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Records",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Locations",
        filtered_df["Location"].nunique()
    )

with col3:
    st.metric(
        "Crops",
        filtered_df["Crops"].nunique()
    )

with col4:
    st.metric(
        "Average Yield",
        round(filtered_df["yeilds"].mean(), 2)
    )

st.divider()

# ============================================================
# BEST PERFORMERS
# ============================================================

best_crop, crop_yield = get_best_crop(filtered_df)

best_location, location_yield = get_best_location(filtered_df)

best_season, season_yield = get_best_season(filtered_df)

st.subheader("🏆 Top Performers")

c1, c2, c3 = st.columns(3)

with c1:
    st.success(
        f"""
        🌾 Best Crop
        
        {best_crop}
        
        Yield: {crop_yield:.2f}
        """
    )

with c2:
    st.success(
        f"""
        📍 Best Location
        
        {best_location}
        
        Yield: {location_yield:.2f}
        """
    )

with c3:
    st.success(
        f"""
        📅 Best Season
        
        {best_season}
        
        Yield: {season_yield:.2f}
        """
    )

st.divider()

# ============================================================
# TOP CROPS
# ============================================================

st.subheader("🌾 Top Crops by Yield")

top_crops = get_top_crops(filtered_df)

fig = px.bar(
    top_crops,
    x="Crops",
    y="yeilds",
    color="yeilds",
    title="Top Crops"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# TOP LOCATIONS
# ============================================================

st.subheader("📍 Top Locations by Yield")

top_locations = get_top_locations(filtered_df)

fig = px.bar(
    top_locations,
    x="Location",
    y="yeilds",
    color="yeilds",
    title="Top Locations"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# SEASON ANALYSIS
# ============================================================

st.subheader("📅 Seasonal Performance")

season_data = get_season_performance(filtered_df)

fig = px.pie(
    season_data,
    values="yeilds",
    names="Season",
    title="Season-wise Yield Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# RAINFALL ANALYSIS
# ============================================================

st.subheader("🌧 Rainfall Impact")

fig = px.scatter(
    filtered_df,
    x="Rainfall",
    y="yeilds",
    color="Season",
    size="Area",
    hover_data=["Crops"],
    title="Rainfall vs Yield"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# TEMPERATURE ANALYSIS
# ============================================================

st.subheader("🌡 Temperature Impact")

fig = px.scatter(
    filtered_df,
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
# RECOMMENDATIONS
# ============================================================

st.subheader("🤖 Smart Recommendations")

recommendations = generate_recommendations(
    filtered_df
)

for recommendation in recommendations:
    st.info(recommendation)

st.divider()

# ============================================================
# FULL INSIGHT REPORT
# ============================================================

st.subheader("📋 AI Generated Report")

report = generate_full_report(
    filtered_df
)

with st.expander(
    "View Detailed Report"
):

    st.json(report)

# ============================================================
# DATA PREVIEW
# ============================================================

st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ============================================================
# DOWNLOAD REPORT
# ============================================================

st.subheader("📥 Export Dataset")

csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="crop_insights_report.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <center>
    <h4>🌱 Crop Yield Prediction & Smart Analytics Platform</h4>
    <p>Built using Python, Machine Learning, Streamlit & Plotly</p>
    </center>
    """,
    unsafe_allow_html=True
)
