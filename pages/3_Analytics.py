import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Deep Analytics",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/data_season.csv")

df = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📈 Deep Analytics Dashboard")

st.markdown("""
Explore advanced analytics and visual insights from the agricultural dataset.
Analyze crop performance, seasonal trends, rainfall impact, temperature effects,
and feature relationships.
""")

st.divider()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔍 Analytics Filters")

selected_location = st.sidebar.multiselect(
    "Location",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)

selected_season = st.sidebar.multiselect(
    "Season",
    options=df["Season"].unique(),
    default=df["Season"].unique()
)

selected_crop = st.sidebar.multiselect(
    "Crop",
    options=df["Crops"].unique(),
    default=df["Crops"].unique()
)

filtered_df = df[
    (df["Location"].isin(selected_location)) &
    (df["Season"].isin(selected_season)) &
    (df["Crops"].isin(selected_crop))
]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

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

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌧 Rainfall Analysis",
    "🌡 Temperature Analysis",
    "🌾 Crop Analysis",
    "📅 Seasonal Analysis",
    "🔥 Correlation Analysis"
])

# --------------------------------------------------
# TAB 1
# --------------------------------------------------

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
    )

    fig = px.bar(
        rainfall_crop,
        x="Crops",
        y="Rainfall",
        title="Average Rainfall by Crop"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# TAB 2
# --------------------------------------------------

with tab2:

    st.subheader("Temperature Impact Analysis")

    fig = px.scatter(
        filtered_df,
        x="Temperature",
        y="yeilds",
        color="Crops",
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

# --------------------------------------------------
# TAB 3
# --------------------------------------------------

with tab3:

    st.subheader("Crop Performance Analysis")

    crop_yield = (
        filtered_df.groupby("Crops")["yeilds"]
        .mean()
        .reset_index()
        .sort_values(by="yeilds", ascending=False)
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

# --------------------------------------------------
# TAB 4
# --------------------------------------------------

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

# --------------------------------------------------
# TAB 5
# --------------------------------------------------

with tab5:

    st.subheader("Correlation Heatmap")

    numeric_columns = [
        "Area",
        "Rainfall",
        "Temperature",
        "Humidity",
        "price",
        "yeilds"
    ]

    correlation = (
        filtered_df[numeric_columns]
        .corr()
    )

    fig = px.imshow(
        correlation,
        text_auto=True,
        aspect="auto",
        title="Feature Correlation Matrix"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        correlation,
        use_container_width=True
    )

# --------------------------------------------------
# LOCATION ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("📍 Location Performance Analysis")

location_yield = (
    filtered_df.groupby("Location")["yeilds"]
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

# --------------------------------------------------
# TOP INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader("🏆 Analytics Insights")

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

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------

st.divider()

st.subheader("📄 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <center>
    <h4>📊 Advanced Agricultural Analytics Platform</h4>
    <p>Built with Streamlit, Plotly & Machine Learning</p>
    </center>
    """,
    unsafe_allow_html=True
)
