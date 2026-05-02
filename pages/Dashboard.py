import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try multiple import methods
disaggregate_series = None
detect_waste = None

# Method 1: Standard import
try:
    from core.nilm_engine import disaggregate_series
    from core.waste_engine import detect_waste
    st.success("✅ Modules loaded successfully")
except ModuleNotFoundError:
    try:
        # Method 2: Relative import
        from ..core.nilm_engine import disaggregate_series
        from ..core.waste_engine import detect_waste
        st.success("✅ Modules loaded successfully (relative import)")
    except (ImportError, ValueError):
        try:
            # Method 3: Direct file import
            import importlib.util
            import pathlib
            
            # Import waste_engine
            waste_path = pathlib.Path(__file__).parent.parent / "core" / "waste_engine.py"
            if waste_path.exists():
                spec = importlib.util.spec_from_file_location("waste_engine", waste_path)
                waste_engine = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(waste_engine)
                detect_waste = waste_engine.detect_waste
            else:
                st.error(f"❌ waste_engine.py not found at {waste_path}")
            
            # Import nilm_engine
            nilm_path = pathlib.Path(__file__).parent.parent / "core" / "nilm_engine.py"
            if nilm_path.exists():
                spec = importlib.util.spec_from_file_location("nilm_engine", nilm_path)
                nilm_engine = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(nilm_engine)
                disaggregate_series = nilm_engine.disaggregate_series
            else:
                st.error(f"❌ nilm_engine.py not found at {nilm_path}")
                
            if disaggregate_series and detect_waste:
                st.success("✅ Modules loaded successfully (direct import)")
        except Exception as e:
            st.error(f"❌ Failed to import modules: {e}")
            st.stop()

# Check if imports were successful
if disaggregate_series is None or detect_waste is None:
    st.error("Could not import required modules. Please check the file structure.")
    st.info("Required files: core/nilm_engine.py and core/waste_engine.py")
    st.stop()

st.title("🏠 Dashboard")

# Check if data exists in session state
if "energy_data" not in st.session_state:
    st.warning("⚠️ Please upload dataset from the Home page first")
    st.info("Go to the Home page to upload your energy data")
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
        st.progress(min(power / max(latest_power, 1), 1.0))
else:
    st.info("No device data available")

# AI Insight Section
st.subheader("🤖 AI Insight")
try:
    # Check if room is occupied (you can add logic to track this)
    # For now, assuming occupied=True for demo
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
    chart_data = df.tail(100)  # Show last 100 points
    st.line_chart(chart_data["power"])
else:
    st.info("Not enough data points for chart")

# Add refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()
