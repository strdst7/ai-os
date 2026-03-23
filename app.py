import streamlit as st
import numpy as np
from src.stability_engine import calculate_adsi, detect_degradation, detect_anomaly

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="AI-OS Dashboard", layout="wide")

st.title("AI-OS Monitoring Dashboard")

# Sidebar Inputs
st.sidebar.header("Input Telemetry")

kpi_error = st.sidebar.slider("KPI Error", 0.0, 1.0, 0.1)
retrieval_score = st.sidebar.slider("Retrieval Score", 0.0, 1.0, 0.9)
latency_dev = st.sidebar.slider("Latency Deviation", 0.0, 1.0, 0.1)
embedding_shift = st.sidebar.slider("Embedding Shift", 0.0, 1.0, 0.05)

metrics = {
    "kpi_error": kpi_error,
    "retrieval_score": retrieval_score,
    "latency_dev": latency_dev,
    "embedding_shift": embedding_shift
}

# Compute ADSI
adsi = calculate_adsi(metrics)
tier = detect_degradation(adsi)

# Store history
st.session_state.history.append(adsi)

# Detect anomaly
anomaly = detect_anomaly(st.session_state.history)

# Display Metrics
col1, col2, col3 = st.columns(3)

col1.metric("ADSI", round(adsi, 3))
col2.metric("Stability Tier", tier.upper())
col3.metric("Anomaly", "YES" if anomaly else "NO")

# Chart
st.subheader("ADSI Trend")
st.line_chart(st.session_state.history)

# Explanation
st.markdown("### System Interpretation")

if tier == "stable":
    st.success("System operating within stable parameters.")
elif tier == "warning":
    st.warning("Early signs of instability detected.")
elif tier == "degrading":
    st.error("System degradation detected. Intervention recommended.")
else:
    st.error("Critical failure risk. Immediate action required.")
