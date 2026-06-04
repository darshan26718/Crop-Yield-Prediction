# ============================================================
# pages/2_Prediction.py
# Crop Yield Prediction Page
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np

from model.train_model import train_model

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Crop Yield Prediction",
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
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return train_model()

model = load_model()

# ============================================================
# HEADER
# ============================================================

st.title("🌾 Crop Yield Prediction")

st.markdown("""
Predict crop yield using Machine Learning based on
environmental and agricultural factors.
""")

st.divider()

# ============================================================
# INPUT FORM
# ============================================================

st.subheader("📋 Enter Crop Details")

col1, col2 = st.columns(2)

with col1:

    year = st.number_input(
        "Year",
        min_value=2000,
        max_value=2050,
        value=2025
    )

    location = st.selectbox(
        "Location",
        sorted(df["Location"].unique())
    )

    area = st.number_input(
        "Area (Acres)",
        min_value=0.0,
        value=100.0
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        value=float(df["Rainfall"].mean())
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        value=float(df["Temperature"].mean())
    )

with col2:

    soil_type = st.selectbox(
        "Soil Type",
        sorted(df["Soil type"].unique())
    )

    irrigation = st.selectbox(
        "Irrigation Type",
        sorted(df["Irrigation"].unique())
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(df["Humidity"].mean())
    )

    crop = st.selectbox(
        "Crop",
        sorted(df["Crops"].unique())
    )

    price = st.number_input(
        "Market Price",
        min_value=0.0,
        value=float(df["price"].mean())
    )

    season = st.selectbox(
        "Season",
        sorted(df["Season"].unique())
    )

st.divider()

# ============================================================
# PREDICTION BUTTON
# ============================================================

if st.button("🚀 Predict Yield", use_container_width=True):

    input_data = pd.DataFrame([{
        "Year": year,
        "Location": location,
        "Area": area,
        "Rainfall": rainfall,
        "Temperature": temperature,
        "Soil type": soil_type,
        "Irrigation": irrigation,
        "Humidity": humidity,
        "Crops": crop,
        "price": price,
        "Season": season
    }])

    prediction = model.predict(input_data)

    predicted_yield = round(float(prediction[0]), 2)

    st.success(
        f"🌱 Predicted Crop Yield: {predicted_yield}"
    )

    st.balloons()

    # ========================================================
    # RESULT METRICS
    # ========================================================

    st.subheader("📊 Prediction Summary")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Predicted Yield",
            predicted_yield
        )

    with m2:
        st.metric(
            "Rainfall",
            rainfall
        )

    with m3:
        st.metric(
            "Temperature",
            temperature
        )

    # ========================================================
    # YIELD CATEGORY
    # ========================================================

    st.subheader("📈 Yield Assessment")

    if predicted_yield >= 80:
        st.success(
            "Excellent Yield Expected 🌟"
        )

    elif predicted_yield >= 60:
        st.info(
            "Good Yield Expected 👍"
        )

    elif predicted_yield >= 40:
        st.warning(
            "Moderate Yield Expected ⚠️"
        )

    else:
        st.error(
            "Low Yield Expected ❌"
        )

    # ========================================================
    # VISUALIZATION
    # ========================================================

    chart_df = pd.DataFrame({
        "Metric": [
            "Rainfall",
            "Temperature",
            "Humidity",
            "Price",
            "Predicted Yield"
        ],
        "Value": [
            rainfall,
            temperature,
            humidity,
            price,
            predicted_yield
        ]
    })

    st.subheader("📉 Prediction Visualization")

    st.bar_chart(
        chart_df.set_index("Metric")
    )

# ============================================================
# DATASET REFERENCE
# ============================================================

st.divider()

st.subheader("📄 Dataset Sample")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <center>
        <h4>🌱 Crop Yield Prediction System</h4>
        <p>Machine Learning • Streamlit • Agriculture Analytics</p>
    </center>
    """,
    unsafe_allow_html=True
)
