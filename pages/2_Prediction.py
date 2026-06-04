import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Crop Yield Prediction",
    page_icon="🌾",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("model/crop_yield_model.pkl")

model = load_model()

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

st.title("🌾 Crop Yield Prediction")

st.markdown("""
Predict crop yield using Machine Learning based on
environmental and agricultural factors.
""")

st.divider()

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

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
        "Area",
        min_value=1.0,
        value=100.0
    )

    rainfall = st.number_input(
        "Rainfall",
        min_value=0.0,
        value=800.0
    )

    temperature = st.number_input(
        "Temperature",
        min_value=0.0,
        value=28.0
    )

with col2:

    soil_type = st.selectbox(
        "Soil Type",
        sorted(df["Soil type"].unique())
    )

    irrigation = st.selectbox(
        "Irrigation",
        sorted(df["Irrigation"].unique())
    )

    humidity = st.number_input(
        "Humidity",
        min_value=0.0,
        max_value=100.0,
        value=65.0
    )

    crop = st.selectbox(
        "Crop",
        sorted(df["Crops"].unique())
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        value=2000.0
    )

    season = st.selectbox(
        "Season",
        sorted(df["Season"].unique())
    )

st.divider()

# --------------------------------------------------
# PREDICTION BUTTON
# --------------------------------------------------

if st.button("🚀 Predict Yield", use_container_width=True):

    input_data = pd.DataFrame({
        "Year": [year],
        "Location": [location],
        "Area": [area],
        "Rainfall": [rainfall],
        "Temperature": [temperature],
        "Soil type": [soil_type],
        "Irrigation": [irrigation],
        "Humidity": [humidity],
        "Crops": [crop],
        "price": [price],
        "Season": [season]
    })

    prediction = model.predict(input_data)[0]

    st.success(
        f"🌾 Predicted Crop Yield: {prediction:.2f}"
    )

    st.balloons()

    st.divider()

    # ----------------------------------------------
    # INTERPRETATION
    # ----------------------------------------------

    st.subheader("📊 Prediction Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Predicted Yield",
            f"{prediction:.2f}"
        )

    with col2:
        st.metric(
            "Rainfall",
            f"{rainfall}"
        )

    with col3:
        st.metric(
            "Temperature",
            f"{temperature} °C"
        )

    # ----------------------------------------------
    # YIELD CATEGORY
    # ----------------------------------------------

    if prediction < 30:
        st.error("🔴 Low Yield Expected")

    elif prediction < 60:
        st.warning("🟡 Moderate Yield Expected")

    else:
        st.success("🟢 High Yield Expected")

    # ----------------------------------------------
    # INPUT SUMMARY
    # ----------------------------------------------

    st.subheader("📋 Input Summary")

    st.dataframe(
        input_data,
        use_container_width=True
    )

# --------------------------------------------------
# INFORMATION SECTION
# --------------------------------------------------

st.divider()

st.subheader("ℹ️ About Prediction")

st.info("""
The prediction is generated using a trained Machine Learning model.

Factors considered:

• Location

• Area

• Rainfall

• Temperature

• Soil Type

• Irrigation Method

• Humidity

• Crop Type

• Market Price

• Season
""")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <center>
    <h4>🌱 Smart Agriculture using AI & Machine Learning</h4>
    </center>
    """,
    unsafe_allow_html=True
)
