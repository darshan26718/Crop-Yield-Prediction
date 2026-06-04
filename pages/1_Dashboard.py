import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Crop Yield Dashboard",
    page_icon="🌾",
    layout="wide"
)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/data_season.csv")

df = load_data()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🔍 Filters")

location_filter = st.sidebar.multiselect(
    "Select Location",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)

season_filter = st.sidebar.multiselect(
    "Select Season",
    options=df["Season"].unique(),
    default=df["Season"].unique()
)

crop_filter = st.sidebar.multiselect(
    "Select Crop",
    options=df["Crops"].unique(),
    default=df["Crops"].unique()
)

filtered_df = df[
    (df["Location"].isin(location_filter)) &
    (df["Season"].isin(season_filter)) &
    (df["Crops"].isin(crop_filter))
]

# -------------------------------
# HEADER
# -------------------------------
st.title("🌾 Crop Yield Analytics Dashboard")

st.markdown("""
Analyze agricultural data with interactive visualizations,
yield trends, crop performance, rainfall impact, and seasonal insights.
""")

# -------------------------------
# KPI SECTION
# -------------------------------
total_records = len(filtered_df)
avg_yield = filtered_df["yeilds"].mean()
avg_rainfall = filtered_df["Rainfall"].mean()
avg_temp = filtered_df["Temperature"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Records",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "🌾 Avg Yield",
        f"{avg_yield:.2f}"
    )

with col3:
    st.metric(
        "🌧 Avg Rainfall",
        f"{avg_rainfall:.2f}"
    )

with col4:
    st.metric(
        "🌡 Avg Temp",
        f"{avg_temp:.2f}°C"
    )

st.divider()

# -------------------------------
# CHART ROW 1
# -------------------------------
col1, col2 = st.columns(2)

with col1:

    crop_yield = (
        filtered_df
        .groupby("Crops")["yeilds"]
        .mean()
        .reset_index()
        .sort_values(by="yeilds", ascending=False)
    )

    fig = px.bar(
        crop_yield,
        x="Crops",
        y="yeilds",
        title="Average Yield by Crop",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    season_yield = (
        filtered_df
        .groupby("Season")["yeilds"]
        .mean()
        .reset_index()
    )

    fig = px.pie(
        season_yield,
        values="yeilds",
        names="Season",
        title="Yield Distribution by Season"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------
# CHART ROW 2
# -------------------------------
col1, col2 = st.columns(2)

with col1:

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

with col2:

    fig = px.box(
        filtered_df,
        x="Season",
        y="yeilds",
        color="Season",
        title="Yield Distribution Across Seasons"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------
# LOCATION ANALYSIS
# -------------------------------
st.subheader("📍 Location-wise Performance")

location_yield = (
    filtered_df
    .groupby("Location")["yeilds"]
    .mean()
    .reset_index()
    .sort_values(by="yeilds", ascending=False)
)

fig = px.bar(
    location_yield,
    x="Location",
    y="yeilds",
    color="yeilds",
    title="Average Yield by Location"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------
# CORRELATION HEATMAP
# -------------------------------
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

# -------------------------------
# TREEMAP
# -------------------------------
st.subheader("🌳 Crop Yield Treemap")

fig = px.treemap(
    filtered_df,
    path=["Season", "Crops"],
    values="yeilds",
    title="Season → Crop Yield Contribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------
# TOP PERFORMERS
# -------------------------------
st.subheader("🏆 Top Performers")

col1, col2 = st.columns(2)

with col1:

    top_crop = (
        filtered_df
        .groupby("Crops")["yeilds"]
        .mean()
        .idxmax()
    )

    st.success(
        f"Best Performing Crop: {top_crop}"
    )

with col2:

    top_location = (
        filtered_df
        .groupby("Location")["yeilds"]
        .mean()
        .idxmax()
    )

    st.success(
        f"Best Performing Location: {top_location}"
    )

# -------------------------------
# DATA TABLE
# -------------------------------
st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown(
    "Developed with ❤️ using Streamlit, Plotly and Machine Learning"
)
