import streamlit as st
import os
import sys

# -------------------------------
# FIX IMPORT PATH (WORKS IN CLOUD)
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# -------------------------------
# SAFE IMPORTS (NO CRASH)
# -------------------------------
try:
   from core.waste_engine import detect_waste
from core.nilm_engine import disaggregate
except Exception as e:
    st.error(f"Import error: {e}")
    st.stop()

# -------------------------------
# UI START
# -------------------------------
st.title("🏠 Energy Dashboard")
st.caption("Real-time AI-powered energy monitoring")

# -------------------------------
# DATA SOURCE (SIMULATED / DATASET)
# -------------------------------
uploaded_file = st.file_uploader("Upload Energy Dataset (optional)", type=["csv"])

if uploaded_file:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    total_power = df["power"].mean() if "power" in df.columns else 2400
    st.success("Using uploaded dataset")
else:
    total_power = 2400  # fallback simulated value
    st.info("Using simulated real-time data")

# -------------------------------
# NILM AI DISAGGREGATION
# -------------------------------
devices = disaggregate(total_power)

# -------------------------------
# TOP METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("⚡ Total Load", f"{round(total_power,2)} W")
col2.metric("📊 Energy Score", "78 / 100")
col3.metric("💰 Estimated Bill", "RM 185")

# -------------------------------
# DEVICE BREAKDOWN
# -------------------------------
st.subheader("🔌 Live Appliance Breakdown")

for device, power in devices.items():
    st.write(f"{device}: {round(power,2)} W")

# -------------------------------
# FIND AC POWER SAFELY
# -------------------------------
ac_power = 0

for key in ['AC', 'ac', 'Air Conditioner', 'air_conditioner', 'aircon']:
    if key in devices:
        ac_power = devices[key]
        break

# -------------------------------
# AI INSIGHT
# -------------------------------
st.subheader("🧠 AI Insight")

if ac_power > 0:
    result = detect_waste(ac_power, False)
    st.warning(result)
else:
    st.info("No AC device detected in current load")

# -------------------------------
# VISUAL CHART (PROFESSIONAL TOUCH)
# -------------------------------
import pandas as pd

df_devices = pd.DataFrame({
    "Device": list(devices.keys()),
    "Power": list(devices.values())
})

st.subheader("📊 Energy Distribution")

st.bar_chart(df_devices.set_index("Device"))
