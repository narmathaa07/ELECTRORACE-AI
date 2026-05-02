import streamlit as st
import pandas as pd
import sys
import os
import importlib.util

st.title("🏠 Dashboard")

# Force direct import from file paths
def import_from_file(filepath, function_name):
    """Directly import a function from a file path"""
    try:
        spec = importlib.util.spec_from_file_location(
            os.path.basename(filepath).replace('.py', ''),
            filepath
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, function_name)
    except Exception as e:
        st.error(f"Error importing from {filepath}: {e}")
        return None

# Get the absolute paths
base_path = "/mount/src/electrorace-ai"
nilm_path = os.path.join(base_path, "core", "nilm_engine.py")
waste_path = os.path.join(base_path, "core", "waste_engine.py")

# Import functions
disaggregate_series = import_from_file(nilm_path, "disaggregate_series")
detect_waste = import_from_file(waste_path, "detect_waste")

# Check if imports were successful
if disaggregate_series is None:
    st.error("❌ Could not load nilm_engine.py")
    st.write(f"Looking for file at: {nilm_path}")
    st.write(f"File exists: {os.path.exists(nilm_path)}")
    st.stop()

if detect_waste is None:
    st.error("❌ Could not load waste_engine.py")
    st.write(f"Looking for file at: {waste_path}")
    st.write(f"File exists: {os.path.exists(waste_path)}")
    st.stop()

st.success("✅ Modules loaded successfully!")

# Check if data exists
if "energy_data" not in st.session_state:
    st.warning("⚠️ Please upload dataset from the Home page first")
    st.stop()

df = st.session_state["energy_data"]

# Validate dataframe
if df.empty or "power" not in df.columns:
    st.error("Invalid data format. Make sure your data has a 'power' column.")
    st.stop()

# Get latest power reading
latest_power = df["power"].iloc[-1]

# Disaggregate power usage
try:
    devices = disaggregate_series(latest_power)
except Exception as e:
    st.error(f"Error in disaggregation: {e}")
    devices = {"Unknown": latest_power}

# Display metrics
col1, col2 = st.columns(2)
col1.metric("⚡ Current Load", f"{round(latest_power, 2)} W")
col2.metric("📊 Data Points", len(df))

# Display device breakdown
st.subheader("📱 Device Power Breakdown")
if devices:
    for device, power in devices.items():
        st.write(f"**{device}:** {round(power, 2)} W")
        if latest_power > 0:
            st.progress(min(power / latest_power, 1.0))
else:
    st.info("No device data available")

# AI Insight Section
st.subheader("🤖 AI Insight")
try:
    occupied = st.checkbox("Room Occupied", value=True)
    waste_message = detect_waste(latest_power, occupied=occupied)
    
    if "⚠" in waste_message or "High" in waste_message:
        st.error(waste_message)
    elif "Normal" in waste_message:
        st.success(waste_message)
    else:
        st.warning(waste_message)
except Exception as e:
    st.error(f"Error generating insight: {e}")

# Add a chart for historical data
st.subheader("📈 Energy Consumption History")
if len(df) > 1:
    chart_data = df.tail(100)
    st.line_chart(chart_data["power"])
else:
    st.info("Not enough data points for chart")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()
