# pages/7_AI_Sustainability_Advisor.py

import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Sustainability Copilot",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 AI Sustainability Copilot (Advanced)")
st.markdown("""
An AI-powered decision engine that generates **Net-Zero strategies,
ESG improvements, and carbon reduction roadmaps**.
""")

# =====================================================
# INPUT SECTION
# =====================================================

st.subheader("📥 Company Sustainability Profile")

col1, col2, col3 = st.columns(3)

with col1:
    industry = st.selectbox(
        "Industry Type",
        ["Manufacturing", "IT Services", "Energy", "Transportation", "Healthcare"]
    )

with col2:
    carbon_emission = st.number_input("Annual Carbon Emission (tons)", value=120.0)

with col3:
    renewable_usage = st.number_input("Renewable Energy Usage (%)", value=40.0)

col4, col5, col6 = st.columns(3)

with col4:
    energy_efficiency = st.number_input("Energy Efficiency (%)", value=60.0)

with col5:
    waste_generation = st.number_input("Waste Generation (tons)", value=50.0)

with col6:
    downtime = st.number_input("Machine Downtime (hrs/month)", value=20.0)

# =====================================================
# AI COPILOT ENGINE
# =====================================================

def ai_copilot():

    insights = []
    roadmap = []
    risk_score = 0

    # ================= CARBON =================
    if carbon_emission > 150:
        insights.append(("HIGH", "Critical carbon emissions detected"))
        roadmap.append("Switch to renewable energy within 12–18 months")
        risk_score += 30

    elif carbon_emission > 100:
        insights.append(("MEDIUM", "Moderate carbon footprint"))
        roadmap.append("Optimize energy consumption and improve efficiency")
        risk_score += 15

    # ================= RENEWABLE =================
    if renewable_usage < 50:
        insights.append(("HIGH", "Low renewable energy adoption"))
        roadmap.append("Install solar/wind hybrid energy systems")
        risk_score += 25

    # ================= ENERGY =================
    if energy_efficiency < 70:
        insights.append(("MEDIUM", "Energy inefficiency detected"))
        roadmap.append("Deploy IoT-based energy monitoring system")
        risk_score += 15

    # ================= WASTE =================
    if waste_generation > 60:
        insights.append(("MEDIUM", "High industrial waste generation"))
        roadmap.append("Adopt circular economy & recycling systems")
        risk_score += 10

    # ================= DOWNTIME =================
    if downtime > 15:
        insights.append(("HIGH", "High machine downtime detected"))
        roadmap.append("Implement predictive maintenance AI models")
        risk_score += 20

    # ================= INDUSTRY ADAPTATION =================
    if industry == "Manufacturing":
        roadmap.append("Upgrade to low-emission smart manufacturing systems")

    elif industry == "IT Services":
        roadmap.append("Move data centers to green cloud infrastructure")

    elif industry == "Energy":
        roadmap.append("Increase renewable energy generation share")

    elif industry == "Transportation":
        roadmap.append("Transition to electric/hybrid fleet")

    elif industry == "Healthcare":
        roadmap.append("Optimize hospital energy and waste systems")

    return insights, roadmap, risk_score


# =====================================================
# GENERATE BUTTON
# =====================================================

if st.button("🤖 Generate AI Sustainability Plan"):

    insights, roadmap, risk_score = ai_copilot()

    st.subheader("📊 Risk Score")
    st.metric("Sustainability Risk Index", f"{risk_score} / 100")

    # ================= INSIGHTS =================
    st.subheader("⚠️ Key AI Insights")

    if insights:
        for level, msg in insights:
            if level == "HIGH":
                st.error(f"🔴 {msg}")
            elif level == "MEDIUM":
                st.warning(f"🟡 {msg}")
            else:
                st.info(f"🟢 {msg}")
    else:
        st.success("🎯 Company is highly sustainable!")

    # ================= ROADMAP =================
    st.subheader("🛣️ Net-Zero Roadmap (AI Generated)")

    for step in roadmap:
        st.success(f"✔ {step}")

    # ================= REPORT =================
    st.subheader("📄 AI Sustainability Report")

    report = f"""
AI SUSTAINABILITY REPORT
Generated: {datetime.now()}

Industry: {industry}
Carbon Emission: {carbon_emission}
Renewable Usage: {renewable_usage}%
Energy Efficiency: {energy_efficiency}%
Waste Generation: {waste_generation}
Downtime: {downtime}

Risk Score: {risk_score}/100

ROADMAP:
- {chr(10).join(roadmap)}
"""

    st.download_button(
        label="📥 Download AI Report",
        data=report,
        file_name="sustainability_ai_report.txt",
        mime="text/plain"
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.caption("🌍 AI ESG Predictive Maintenance | Sustainability Copilot v2.0")
