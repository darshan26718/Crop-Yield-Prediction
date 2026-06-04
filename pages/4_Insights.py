# ============================================================
# pages/4_Insights.py
# Crop Yield Insights Page
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Insights",
    page_icon="💡",
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
# HEADER
# ============================================================

st.title("💡 Agricultural Insights")

st.markdown("""
Smart insights generated from crop yield,
weather conditions and agricultural performance.
""")

st.divider()

# ============================================================
# FILTERS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    selected_crop = st.selectbox(
        "Crop",
        ["All"] + sorted(df["Crops"].unique().tolist())
    )

with col2:
    selected_season = st.selectbox(
        "Season",
        ["All"] + sorted(df["Season"].unique().tolist())
    )

with col3:
    selected_location = st.selectbox(
        "Location",
        ["All"] + sorted(df["Location"].unique().tolist())
    )

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
# KPI SECTION
# ============================================================

st.subheader("📊 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Average Yield",
        round(filtered_df["yeilds"].mean(), 2)
    )

with c2:
    st.metric(
        "Average Rainfall",
        round(filtered_df["Rainfall"].mean(), 2)
    )

with c3:
    st.metric(
        "Average Temperature",
        round(filtered_df["Temperature"].mean(), 2)
    )

with c4:
    st.metric(
        "Average Humidity",
        round(filtered_df["Humidity"].mean(), 2)
    )

# ============================================================
# BEST CROP
# ============================================================

st.divider()

st.subheader("🏆 Best Performing Crop")

best_crop = (
    filtered_df.groupby("Crops")["yeilds"]
    .mean()
    .idxmax()
)

best_crop_yield = (
    filtered_df.groupby("Crops")["yeilds"]
    .mean()
    .max()
)

st.success(
    f"Best Crop: {best_crop} "
    f"(Average Yield: {round(best_crop_yield,2)})"
)

# ============================================================
# BEST LOCATION
# ============================================================

best_location = (
    filtered_df.groupby("Location")["yeilds"]
    .mean()
    .idxmax()
)

best_location_yield = (
    filtered_df.groupby("Location")["yeilds"]
    .mean()
    .max()
)

st.success(
    f"Best Location: {best_location} "
    f"(Average Yield: {round(best_location_yield,2)})"
)

# ============================================================
# BEST SEASON
# ============================================================

best_season = (
    filtered_df.groupby("Season")["yeilds"]
    .mean()
    .idxmax()
)

best_season_yield = (
    filtered_df.groupby("Season")["yeilds"]
    .mean()
    .max()
)

st.success(
    f"Best Season: {best_season} "
    f"(Average Yield: {round(best_season_yield,2)})"
)

# ============================================================
# CROP PERFORMANCE
# ============================================================

st.divider()

st.subheader("🌾 Crop Performance")

crop_performance = (
    filtered_df.groupby("Crops")["yeilds"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    crop_performance,
    x="Crops",
    y="yeilds",
    color="yeilds",
    title="Average Yield by Crop"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# SEASON PERFORMANCE
# ============================================================

st.subheader("📅 Season Performance")

season_performance = (
    filtered_df.groupby("Season")["yeilds"]
    .mean()
    .reset_index()
)

fig = px.pie(
    season_performance,
    names="Season",
    values="yeilds",
    title="Season Contribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# LOCATION PERFORMANCE
# ============================================================

st.subheader("📍 Location Performance")

location_performance = (
    filtered_df.groupby("Location")["yeilds"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    location_performance,
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
# RECOMMENDATIONS
# ============================================================

st.divider()

st.subheader("🧠 Smart Recommendations")

avg_rainfall = filtered_df["Rainfall"].mean()
avg_temp = filtered_df["Temperature"].mean()
avg_humidity = filtered_df["Humidity"].mean()

recommendations = []

if avg_rainfall < 700:
    recommendations.append(
        "Increase irrigation in low rainfall regions."
    )

if avg_temp > 32:
    recommendations.append(
        "High temperature detected. Consider heat-resistant crops."
    )

if avg_humidity < 50:
    recommendations.append(
        "Maintain soil moisture using drip irrigation."
    )

if len(recommendations) == 0:
    recommendations.append(
        "Current agricultural conditions appear favorable."
    )

for rec in recommendations:
    st.info(rec)

# ============================================================
# DATA PREVIEW
# ============================================================

st.divider()

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ============================================================
# DOWNLOAD
# ============================================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Download Insights Data",
    csv,
    "insights_data.csv",
    "text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <center>
    <h4>💡 Agricultural Insights Platform</h4>
    <p>Powered by Streamlit, Plotly & Machine Learning</p>
    </center>
    """,
    unsafe_allow_html=True
)
