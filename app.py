import random

import streamlit as st
from src.config import MonitoringConfig
from src.stability_engine import calculate_adsi, detect_degradation, detect_anomaly

METRIC_ORDER = ("kpi_error", "retrieval_score", "latency_dev", "embedding_shift")
DEFAULT_METRICS = {
    "kpi_error": 0.1,
    "retrieval_score": 0.9,
    "latency_dev": 0.1,
    "embedding_shift": 0.05,
}

st.set_page_config(page_title="AI-OS Dashboard", layout="wide")

# Session state: bounded ADSI history plus the last recorded telemetry snapshot.
# Recording is keyed on the snapshot so a plain rerun never appends a duplicate.
if "history" not in st.session_state:
    st.session_state.history = []
if "last_snapshot" not in st.session_state:
    st.session_state.last_snapshot = None
for key, value in DEFAULT_METRICS.items():
    st.session_state.setdefault(key, value)

st.title("AI-OS: Deployment Stability Monitoring System")
st.markdown("""
AI-OS evaluates enterprise AI system stability using the **Deployment Stability Index (ADSI)**.

The system integrates:
- Alignment health
- Infrastructure reliability
- Drift resilience

to provide real-time stability assessment and anomaly detection.
""")

st.latex(r"ADSI = \frac{AHI + IHI + DHI}{3}")

st.markdown("""
### Stability Tiers

- 🟢 Stable (≥ 0.85)
- 🟡 Warning (0.75 – 0.85)
- 🟠 Degrading (0.65 – 0.75)
- 🔴 Critical (< 0.65)
""")

# Rendered before the sliders so a click can update their state on the same run.
if st.button("Simulate Degradation"):
    for key in ("kpi_error", "latency_dev", "embedding_shift"):
        st.session_state[key] = random.uniform(0.3, 1.0)
    st.session_state["retrieval_score"] = random.uniform(0.0, 0.7)

# Sidebar
st.sidebar.header("Input Telemetry")

kpi_error = st.sidebar.slider("KPI Error", 0.0, 1.0, key="kpi_error")
retrieval_score = st.sidebar.slider("Retrieval Score", 0.0, 1.0, key="retrieval_score")
latency_dev = st.sidebar.slider("Latency Deviation", 0.0, 1.0, key="latency_dev")
embedding_shift = st.sidebar.slider("Embedding Shift", 0.0, 1.0, key="embedding_shift")

metrics = {
    "kpi_error": kpi_error,
    "retrieval_score": retrieval_score,
    "latency_dev": latency_dev,
    "embedding_shift": embedding_shift,
}

# Compute
adsi = calculate_adsi(metrics)
tier = detect_degradation(adsi)

# Record only when the telemetry actually changes, and keep the window bounded.
snapshot = tuple(metrics[name] for name in METRIC_ORDER)
if snapshot != st.session_state.last_snapshot:
    st.session_state.history.append(adsi)
    st.session_state.history = st.session_state.history[-MonitoringConfig.HISTORY_LIMIT:]
    st.session_state.last_snapshot = snapshot

# Anomaly detection
anomaly = detect_anomaly(st.session_state.history)

# Display
col1, col2, col3 = st.columns(3)

col1.metric("ADSI", round(adsi, 3))
col2.metric("Stability Tier", tier.upper())
col3.metric("Anomaly", "YES" if anomaly else "NO")

st.subheader("ADSI Trend")
st.line_chart(st.session_state.history)

# Interpretation
if tier == "stable":
    st.success("System stable")
elif tier == "warning":
    st.warning("Early instability detected")
elif tier == "degrading":
    st.error("System degrading")
else:
    st.error("Critical failure risk")
