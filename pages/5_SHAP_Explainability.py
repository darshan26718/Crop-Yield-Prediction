# pages/5_SHAP_Explainability.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SHAP Explainability",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 SHAP Explainability Dashboard")
st.markdown("""
Understand how the AI model makes predictive maintenance decisions using SHAP (SHapley Additive exPlanations).
""")

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():
    return joblib.load("models/maintenance_xgb_model.pkl")

model = load_model()

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/maintenance_failure_dataset.csv")
    return df

df = load_data()

TARGET_COLUMN = "Failure"

X = df.drop(columns=[TARGET_COLUMN])

# Handle categorical columns if present
X = pd.get_dummies(X, drop_first=True)

# =====================================================
# SHAP EXPLAINER
# =====================================================

with st.spinner("Generating SHAP explanations..."):

    explainer = shap.TreeExplainer(model)

    sample_size = min(500, len(X))
    X_sample = X.sample(sample_size, random_state=42)

    shap_values = explainer.shap_values(X_sample)

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

st.subheader("📊 Global Feature Importance")

fig1, ax1 = plt.subplots(figsize=(10, 6))

shap.summary_plot(
    shap_values,
    X_sample,
    plot_type="bar",
    show=False
)

st.pyplot(fig1)

# =====================================================
# SHAP SUMMARY PLOT
# =====================================================

st.subheader("📈 SHAP Summary Plot")

fig2, ax2 = plt.subplots(figsize=(10, 6))

shap.summary_plot(
    shap_values,
    X_sample,
    show=False
)

st.pyplot(fig2)

# =====================================================
# FEATURE CONTRIBUTION
# =====================================================

st.subheader("🎯 Explain Individual Prediction")

selected_index = st.selectbox(
    "Select Machine Record",
    X_sample.index
)

selected_row = X.loc[[selected_index]]

st.write("Selected Machine Data")

st.dataframe(selected_row)

individual_shap = explainer.shap_values(selected_row)

prediction = model.predict(selected_row)[0]

probability = model.predict_proba(selected_row)[0][1]

st.metric(
    "Failure Probability",
    f"{probability:.2%}"
)

if prediction == 1:
    st.error("⚠️ Predicted Failure")
else:
    st.success("✅ Machine Healthy")

# =====================================================
# WATERFALL PLOT
# =====================================================

st.subheader("🌊 SHAP Waterfall Explanation")

try:

    explanation = shap.Explanation(
        values=individual_shap[0],
        base_values=explainer.expected_value,
        data=selected_row.iloc[0],
        feature_names=selected_row.columns
    )

    fig3 = plt.figure(figsize=(12, 6))

    shap.plots.waterfall(
        explanation,
        max_display=10,
        show=False
    )

    st.pyplot(fig3)

except Exception as e:

    st.warning(
        "Waterfall visualization could not be generated."
    )

# =====================================================
# TOP FEATURES TABLE
# =====================================================

st.subheader("🏆 Most Influential Features")

importance_df = pd.DataFrame({
    "Feature": X_sample.columns,
    "Mean |SHAP Value|": np.abs(shap_values).mean(axis=0)
})

importance_df = importance_df.sort_values(
    by="Mean |SHAP Value|",
    ascending=False
)

st.dataframe(
    importance_df,
    use_container_width=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("💡 AI Insights")

top_feature = importance_df.iloc[0]["Feature"]

st.info(
    f"""
    The most important feature influencing maintenance failure predictions
    is **{top_feature}**.

    Higher SHAP values increase failure risk,
    while lower SHAP values decrease failure risk.

    Use this information to proactively schedule maintenance
    before equipment breakdown occurs.
    """
)

# =====================================================
# DOWNLOAD REPORT
# =====================================================

csv = importance_df.to_csv(index=False)

st.download_button(
    label="📥 Download SHAP Importance Report",
    data=csv,
    file_name="shap_feature_importance.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.caption(
    "AI ESG Predictive Maintenance Platform | Explainable AI using SHAP"
)
