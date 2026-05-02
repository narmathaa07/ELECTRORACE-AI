import streamlit as st
import pandas as pd
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now try imports
from core.nilm_engine import disaggregate_series
from core.waste_engine import detect_waste

st.title("🏠 Dashboard")

if "energy_data" not in st.session_state:
    st.warning("Upload dataset from Home page")
    st.stop()

df = st.session_state["energy_data"]

latest_power = df["power"].iloc[-1]

devices = disaggregate_series(latest_power)

col1, col2 = st.columns(2)
col1.metric("⚡ Current Load", f"{round(latest_power,2)} W")
col2.metric("📊 Data Points", len(df))

st.subheader("Devices")
for d, p in devices.items():
    st.write(f"{d}: {round(p,2)} W")

st.subheader("AI Insight")
# Note: detect_waste expects 2 parameters but you're only passing 1
# You need to provide the 'occupied' parameter
waste_message = detect_waste(latest_power, occupied=False)
st.warning(waste_message)
