# ============================================================
# pages/2_Prediction.py
# Crop Yield Prediction
# ============================================================

import streamlit as st
import pandas as pd

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
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    try:
        model = train_model()
        return model
    except Exception as e:
        st.error(f"Model Training Error: {e}")
        return None


model = load_model()

# ============================================================
# HEADER
# ============================================================

st.title("🌾 Crop Yield Prediction")

st.markdown("""
Predict crop yield using Machine Learning based on
environmental and agricultural parameters.
""")

st.divider()

# ============================================================
# CHECK MODEL
# ============================================================

if model is None:
    st.stop()

# ============================================================
# INPUT FORM
# ============================================================

st.subheader("📋 Enter Crop Information")

col1, col2 = st.columns(2)

with col1:

    year = st.number_input(
        "Year",
        min_value=2000,
        max_value=2100,
        value=2025
    )

    location = st.selectbox(
        "Location",
        sorted(df["Location"].dropna().unique())
    )

    area = st.number_input(
        "Area",
        min_value=0.0,
        value=100.0
    )

    rainfall = st.number_input(
        "Rainfall",
        min_value=0.0,
        value=float(df["Rainfall"].mean())
    )

    temperature = st.number_input(
        "Temperature",
        min_value=0.0,
        value=float(df["Temperature"].mean())
    )

with col2:

    soil_type = st.selectbox(
        "Soil Type",
        sorted(df["Soil type"].dropna().unique())
    )

    irrigation = st.selectbox(
        "Irrigation",
        sorted(df["Irrigation"].dropna().unique())
    )

    humidity = st.number_input(
        "Humidity",
        min_value=0.0,
        max_value=100.0,
        value=float(df["Humidity"].mean())
    )

    crop = st.selectbox(
        "Crop",
        sorted(df["Crops"].dropna().unique())
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        value=float(df["price"].mean())
    )

    season = st.selectbox(
        "Season",
        sorted(df["Season"].dropna().unique())
    )

# ============================================================
# PREDICT BUTTON
# ============================================================

if st.button(
    "🚀 Predict Yield",
    use_container_width=True
):

    try:

        input_df = pd.DataFrame([{

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

        prediction = model.predict(
            input_df
        )

        predicted_yield = round(
            float(prediction[0]),
            2
        )

        st.success(
            f"🌱 Predicted Yield: {predicted_yield}"
        )

        st.balloons()

        # ====================================================
        # METRICS
        # ====================================================

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Predicted Yield",
                predicted_yield
            )

        with c2:
            st.metric(
                "Rainfall",
                rainfall
            )

        with c3:
            st.metric(
                "Temperature",
                temperature
            )

        # ====================================================
        # YIELD CATEGORY
        # ====================================================

        st.subheader("📈 Yield Category")

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

        # ====================================================
        # VISUALIZATION
        # ====================================================

        chart_data = pd.DataFrame({

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

        st.subheader(
            "📊 Prediction Summary"
        )

        st.bar_chart(
            chart_data.set_index(
                "Metric"
            )
        )

    except Exception as e:

        st.error(
            f"Prediction Error: {e}"
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
# DOWNLOAD DATA
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
    <h4>🌱 Crop Yield Prediction System</h4>
    <p>Built with Streamlit, Scikit-Learn and Plotly</p>
    </center>
    """,
    unsafe_allow_html=True
)
