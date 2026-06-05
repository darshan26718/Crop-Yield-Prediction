# pages/6_ESG_Scoring.py

import streamlit as st
import pandas as pd
import joblib
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ESG Scoring Engine",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI ESG Scoring Engine")
st.markdown("""
Predict and analyze ESG (Environmental, Social, Governance) score using AI.
The score ranges from **0 (poor sustainability)** to **100 (excellent sustainability)**.
""")

# =====================================================
# LOAD MODEL & SCALER
# =====================================================

@st.cache_resource
def load_model():
    model = joblib.load("models/esg_scoring_model.pkl")
    scaler = joblib.load("models/esg_scaler.pkl")
    return model, scaler

model, scaler = load_model()

# =====================================================
# INPUT SECTION
# =====================================================

st.subheader("📥 Enter Company ESG Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    carbon_emission = st.number_input("Carbon Emission", min_value=0.0, value=100.0)

with col2:
    renewable_energy = st.number_input("Renewable Energy Usage (%)", min_value=0.0, max_value=100.0, value=40.0)

with col3:
    waste_recycled = st.number_input("Waste Recycled (%)", min_value=0.0, max_value=100.0, value=50.0)

col4, col5, col6 = st.columns(3)

with col4:
    employee_satisfaction = st.number_input("Employee Satisfaction (%)", min_value=0.0, max_value=100.0, value=75.0)

with col5:
    gender_diversity = st.number_input("Gender Diversity (%)", min_value=0.0, max_value=100.0, value=45.0)

with col6:
    board_independence = st.number_input("Board Independence (%)", min_value=0.0, max_value=100.0, value=60.0)

# =====================================================
# PREDICTION BUTTON
# =====================================================

if st.button("🔍 Predict ESG Score"):

    # Create input dataframe
    input_data = pd.DataFrame([{
        "Carbon_Emission": carbon_emission,
        "Renewable_Energy_Usage": renewable_energy,
        "Waste_Recycled": waste_recycled,
        "Employee_Satisfaction": employee_satisfaction,
        "Gender_Diversity": gender_diversity,
        "Board_Independence": board_independence
    }])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Predict ESG score
    prediction = model.predict(input_scaled)[0]

    # Clamp score (0–100 safety)
    prediction = np.clip(prediction, 0, 100)

    # =====================================================
    # OUTPUT
    # =====================================================

    st.subheader("📊 ESG Score Result")

    st.metric(label="Predicted ESG Score", value=f"{prediction:.2f} / 100")

    # ESG Rating System
    if prediction >= 80:
        st.success("🌟 Excellent ESG Performance")
    elif prediction >= 60:
        st.info("🟢 Good ESG Performance")
    elif prediction >= 40:
        st.warning("🟡 Moderate ESG Performance")
    else:
        st.error("🔴 Poor ESG Performance")

    # =====================================================
    # INSIGHTS
    # =====================================================

    st.subheader("💡 AI Insights")

    insights = []

    if carbon_emission > 120:
        insights.append("⚠️ High carbon emission detected. Consider renewable transition.")

    if renewable_energy < 40:
        insights.append("🌱 Increase renewable energy usage for better ESG score.")

    if waste_recycled < 50:
        insights.append("♻️ Improve waste recycling practices.")

    if employee_satisfaction < 70:
        insights.append("👥 Improve employee satisfaction and workplace conditions.")

    if gender_diversity < 40:
        insights.append("⚖️ Increase gender diversity in workforce.")

    if board_independence < 50:
        insights.append("🏛️ Improve board independence for better governance.")

    if insights:
        for i in insights:
            st.warning(i)
    else:
        st.success("🎯 Strong sustainability profile across all ESG factors!")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.caption("AI ESG Predictive Maintenance Platform | ESG Scoring Module")
