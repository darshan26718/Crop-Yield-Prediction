# ============================================================
# pages/3_Analytics.py
# Deep Analytics Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Deep Analytics",
    page_icon="📈",
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

st.title("📈 Deep Analytics Dashboard")

st.markdown("""
Analyze agricultural data through interactive charts,
correlation studies, crop performance metrics,
seasonal trends, and environmental impact analysis.
""")

st.divider()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔍 Analytics Filters")

locations = st.sidebar.multiselect(
    "Location",
    options=sorted(df["Location"].unique()),
    default=sorted(df["Location"].unique())
)

crops = st.sidebar.multiselect(
    "Crop",
    options=sorted(df["Crops"].unique()),
    default=sorted(df["Crops"].unique())
)

seasons = st.sidebar.multiselect(
    "Season",
    options=sorted(df["Season"].unique()),
    default=sorted(df["Season"].unique())
)

filtered_df = df[
    (df["Location"].isin(locations))
    &
    (df["Crops"].isin(crops))
    &
    (df["Season"].isin(seasons))
]

# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Analytics Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
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
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌧 Rainfall",
    "🌡 Temperature",
    "🌾 Crops",
    "📅 Seasons",
    "🔥 Correlation"
])

# ============================================================
# RAINFALL ANALYSIS
# ============================================================

with tab1:

    st.subheader("Rainfall Impact on Yield")

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

    rainfall_crop = (
        filtered_df.groupby("Crops")["Rainfall"]
        .mean()
        .reset_index()
        .sort_values(
            by="Rainfall",
            ascending=False
        )
    )

    fig = px.bar(
        rainfall_crop,
        x="Crops",
        y="Rainfall",
        color="Rainfall",
        title="Average Rainfall by Crop"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# TEMPERATURE ANALYSIS
# ============================================================

with tab2:

    st.subheader("Temperature Impact")

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

    fig = px.box(
        filtered_df,
        x="Season",
        y="Temperature",
        color="Season",
        title="Temperature Distribution by Season"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# CROP ANALYSIS
# ============================================================

with tab3:

    st.subheader("Crop Performance")

    crop_yield = (
        filtered_df.groupby("Crops")["yeilds"]
        .mean()
        .reset_index()
        .sort_values(
            by="yeilds",
            ascending=False
        )
    )

    fig = px.bar(
        crop_yield,
        x="Crops",
        y="yeilds",
        color="yeilds",
        title="Average Yield by Crop"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.treemap(
        filtered_df,
        path=["Season", "Crops"],
        values="yeilds",
        title="Crop Yield Treemap"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# SEASON ANALYSIS
# ============================================================

with tab4:

    st.subheader("Seasonal Yield Analysis")

    season_yield = (
        filtered_df.groupby("Season")["yeilds"]
        .mean()
        .reset_index()
    )

    fig = px.pie(
        season_yield,
        values="yeilds",
        names="Season",
        title="Yield Contribution by Season"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.box(
        filtered_df,
        x="Season",
        y="yeilds",
        color="Season",
        title="Yield Distribution by Season"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# CORRELATION ANALYSIS
# ============================================================

with tab5:

    st.subheader("Correlation Matrix")

    numerical_columns = [
        "Area",
        "Rainfall",
        "Temperature",
        "Humidity",
        "price",
        "yeilds"
    ]

    corr = (
        filtered_df[numerical_columns]
        .corr()
    )

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

    st.dataframe(
        corr,
        use_container_width=True
    )

# ============================================================
# LOCATION ANALYSIS
# ============================================================

st.divider()

st.subheader("📍 Location Performance")

location_yield = (
    filtered_df.groupby("Location")["yeilds"]
    .mean()
    .reset_index()
    .sort_values(
        by="yeilds",
        ascending=False
    )
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

# ============================================================
# TOP INSIGHTS
# ============================================================

st.divider()

st.subheader("🏆 Key Analytics Insights")

best_crop = (
    filtered_df.groupby("Crops")["yeilds"]
    .mean()
    .idxmax()
)

best_location = (
    filtered_df.groupby("Location")["yeilds"]
    .mean()
    .idxmax()
)

best_season = (
    filtered_df.groupby("Season")["yeilds"]
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
# RAW DATA
# ============================================================

st.divider()

st.subheader("📄 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ============================================================
# DOWNLOAD DATA
# ============================================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="analytics_dataset.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <center>
        <h4>🌱 Crop Yield Prediction Analytics Platform</h4>
        <p>Built with Streamlit, Plotly & Machine Learning</p>
    </center>
    """,
    unsafe_allow_html=True
)
