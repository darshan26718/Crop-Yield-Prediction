import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Crop Yield Prediction System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

.main-header{
    font-size:42px;
    font-weight:bold;
    text-align:center;
    color:#2E8B57;
}

.sub-header{
    font-size:20px;
    text-align:center;
    color:gray;
}

.feature-card{
    padding:20px;
    border-radius:10px;
    background-color:#f5f5f5;
    box-shadow:2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<p class="main-header">🌾 Crop Yield Prediction System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-header">AI Powered Agriculture Analytics Platform</p>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    ## Welcome 👋

    This platform helps farmers, researchers, and agricultural analysts
    predict crop yield and analyze agricultural data using
    Machine Learning and Interactive Visualizations.

    ### Key Benefits

    - Accurate Crop Yield Prediction
    - Rainfall Impact Analysis
    - Seasonal Trend Analysis
    - Crop Performance Insights
    - Interactive Analytics Dashboard
    - Data-Driven Decision Making
    """)

with col2:
    st.image(
        "https://images.unsplash.com/photo-1500937386664-56d1dfef3854",
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# FEATURES SECTION
# --------------------------------------------------
st.header("🚀 Platform Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 🌾 Yield Prediction

    Predict crop yield based on:
    - Rainfall
    - Temperature
    - Soil Type
    - Crop Type
    - Irrigation
    """)

with col2:
    st.success("""
    ### 📊 Analytics Dashboard

    Explore:
    - Crop Trends
    - Seasonal Analysis
    - Rainfall Analytics
    - Performance Metrics
    """)

with col3:
    st.warning("""
    ### 🧠 Smart Insights

    Discover:
    - Best Crops
    - Best Locations
    - Yield Drivers
    - Farming Recommendations
    """)

st.divider()

# --------------------------------------------------
# DASHBOARD OVERVIEW
# --------------------------------------------------
st.header("📌 Project Workflow")

st.markdown("""
### Step 1️⃣ Data Collection
Agricultural data is collected from different regions.

### Step 2️⃣ Data Processing
Cleaning and preprocessing are performed.

### Step 3️⃣ Machine Learning
The model learns patterns affecting crop yield.

### Step 4️⃣ Prediction
Users enter farming parameters to predict yield.

### Step 5️⃣ Insights
Interactive dashboards generate meaningful insights.
""")

st.divider()

# --------------------------------------------------
# SYSTEM MODULES
# --------------------------------------------------
st.header("🛠 Available Modules")

module1, module2, module3, module4 = st.columns(4)

with module1:
    st.metric(
        "Dashboard",
        "Analytics"
    )

with module2:
    st.metric(
        "Prediction",
        "ML Model"
    )

with module3:
    st.metric(
        "Insights",
        "Smart Reports"
    )

with module4:
    st.metric(
        "Data",
        "Visualization"
    )

st.divider()

# --------------------------------------------------
# TECHNOLOGY STACK
# --------------------------------------------------
st.header("💻 Technology Stack")

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    st.success("Python")

with tech2:
    st.success("Streamlit")

with tech3:
    st.success("Scikit-Learn")

with tech4:
    st.success("Plotly")

st.divider()

# --------------------------------------------------
# QUICK STATISTICS
# --------------------------------------------------
st.header("📈 System Highlights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("ML Algorithm", "Random Forest")

with col2:
    st.metric("Interactive Charts", "10+")

with col3:
    st.metric("Analytics Pages", "4")

with col4:
    st.metric("Prediction Accuracy", "High")

st.divider()

# --------------------------------------------------
# NAVIGATION GUIDE
# --------------------------------------------------
st.header("📚 Navigation Guide")

st.markdown("""
Use the sidebar to access:

### 📊 Dashboard
View crop yield analytics and trends.

### 🌾 Prediction
Predict crop yield using machine learning.

### 📈 Analytics
Explore rainfall, temperature, and seasonal impacts.

### 🧠 Insights
Generate intelligent recommendations and reports.
""")

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <center>
    <h4>🌱 Empowering Agriculture Through AI & Data Science</h4>
    </center>
    """,
    unsafe_allow_html=True
)
