import streamlit as st
import pandas as pd
import sys
import os

# Add path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions (with error handling)
try:
    from core.nilm_engine import disaggregate_series
    from core.waste_engine import detect_waste, compute_loss
except ModuleNotFoundError:
    # Define fallback functions if imports fail
    def disaggregate_series(total_power):
        if isinstance(total_power, (int, float)):
            power_val = total_power
        else:
            power_val = float(total_power.iloc[-1]) if hasattr(total_power, 'iloc') else 500
        
        devices = {"HVAC": 0, "Lighting": 0, "Electronics": 0, "Other": 0}
        if power_val > 2000:
            devices["HVAC"] = round(power_val * 0.5, 2)
            devices["Lighting"] = round(power_val * 0.1, 2)
            devices["Electronics"] = round(power_val * 0.25, 2)
            devices["Other"] = round(power_val * 0.15, 2)
        elif power_val > 500:
            devices["HVAC"] = round(power_val * 0.4, 2)
            devices["Lighting"] = round(power_val * 0.15, 2)
            devices["Electronics"] = round(power_val * 0.3, 2)
            devices["Other"] = round(power_val * 0.15, 2)
        else:
            devices["Lighting"] = round(power_val * 0.3, 2)
            devices["Electronics"] = round(power_val * 0.5, 2)
            devices["Other"] = round(power_val * 0.2, 2)
        return {k: v for k, v in devices.items() if v > 0}
    
    def detect_waste(power, occupied=False):
        if power > 1000 and not occupied:
            return "⚠ High power usage in empty condition"
        elif power > 500 and not occupied:
            return "⚡ Moderate power usage while unoccupied"
        elif power > 1500:
            return "💡 Very high energy consumption detected"
        else:
            return "✅ Normal energy usage"
    
    def compute_loss(df):
        if df is None or df.empty:
            return df
        df = df.copy()
        if "power_used" in df.columns:
            df["loss"] = df["power"] - df["power_used"]
        else:
            df["loss"] = df["power"] * 0.1
        return df

st.set_page_config(page_title="NILM & AI Analysis", page_icon="🤖", layout="wide")

st.title("🤖 NILM & AI Energy Analysis")
st.markdown("---")

# Check if data exists
if "energy_data" not in st.session_state:
    st.warning("⚠️ Please upload dataset from the Home page first")
    st.info("Go to the **Home** page to upload your energy data")
    st.stop()

df = st.session_state["energy_data"]

# Validate dataframe
if df.empty:
    st.error("❌ The dataset is empty. Please upload valid data.")
    st.stop()

if "power" not in df.columns:
    st.error("❌ The dataset must contain a 'power' column.")
    st.write(f"Available columns: {list(df.columns)}")
    st.stop()

# Ensure timestamp is datetime
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

# Get the latest power value
latest_power = df["power"].iloc[-1]

# Display current metrics
col1, col2, col3 = st.columns(3)
col1.metric("⚡ Current Power", f"{latest_power:.2f} W")
col2.metric("📊 Total Data Points", len(df))
col3.metric("📈 Average Power", f"{df['power'].mean():.2f} W")

st.markdown("---")

# Device Disaggregation
st.subheader("📱 Device Power Disaggregation")

# Pass SINGLE NUMBER to disaggregate_series
try:
    devices = disaggregate_series(latest_power)
    
    if devices:
        col1, col2 = st.columns(2)
        for i, (device, power) in enumerate(devices.items()):
            if i % 2 == 0:
                col1.write(f"**{device}:** {power:.2f} W")
            else:
                col2.write(f"**{device}:** {power:.2f} W")
        
        # Progress bars
        st.subheader("Energy Distribution")
        for device, power in devices.items():
            percentage = (power / latest_power) * 100 if latest_power > 0 else 0
            st.write(f"{device}: {percentage:.1f}%")
            st.progress(min(percentage / 100, 1.0))
    else:
        st.info("No devices detected")
        
except Exception as e:
    st.error(f"Error in device disaggregation: {e}")
    st.write("Using simple device estimation...")
    devices = {"Appliances": round(latest_power, 2)}
    st.write(f"**Total Load:** {latest_power:.2f} W")

st.markdown("---")

# AI Waste Detection
st.subheader("🗑️ AI Waste Detection")

# Get occupancy status
occupied = st.checkbox("🏠 Room/Area Occupied", value=True)

# Detect waste
try:
    waste_result = detect_waste(latest_power, occupied)
    
    if "⚠" in waste_result or "High" in waste_result:
        st.error(waste_result)
    elif "⚡" in waste_result or "Moderate" in waste_result:
        st.warning(waste_result)
    else:
        st.success(waste_result)
except Exception as e:
    st.error(f"Error in waste detection: {e}")

st.markdown("---")

# Energy Loss Analysis
st.subheader("📉 Energy Loss Analysis")

try:
    df_with_loss = compute_loss(df.copy())
    
    if "loss" in df_with_loss.columns:
        total_loss = df_with_loss["loss"].sum()
        avg_loss = df_with_loss["loss"].mean()
        loss_percentage = (total_loss / df_with_loss["power"].sum()) * 100 if df_with_loss["power"].sum() > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Energy Loss", f"{total_loss:.2f} Wh")
        col2.metric("Average Loss", f"{avg_loss:.2f} Wh")
        col3.metric("Loss Percentage", f"{loss_percentage:.1f}%")
        
        # Loss over time chart (only if there's valid data)
        chart_df = df_with_loss[["power", "loss"]].tail(50)
        if not chart_df.empty and len(chart_df) > 1:
            st.line_chart(chart_df)
        else:
            st.info("Not enough data points for loss chart")
    else:
        st.info("Loss column not available. Using default loss calculation.")
        
except Exception as e:
    st.error(f"Error in loss analysis: {e}")

st.markdown("---")

# Time-based Analysis
st.subheader("📈 Consumption Patterns")

# Create hour column for analysis
if 'timestamp' in df.columns:
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    
    # Hourly average consumption
    hourly_avg = df.groupby('hour')['power'].mean()
    
    if not hourly_avg.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            peak_hour = hourly_avg.idxmax()
            peak_value = hourly_avg.max()
            st.metric("⏰ Peak Hour", f"{int(peak_hour)}:00", f"{peak_value:.0f} W avg")
        
        with col2:
            off_peak_hour = hourly_avg.idxmin()
            off_peak_value = hourly_avg.min()
            st.metric("🌙 Off-Peak Hour", f"{int(off_peak_hour)}:00", f"{off_peak_value:.0f} W avg")
        
        # Hourly consumption chart
        st.subheader("Hourly Consumption Pattern")
        st.bar_chart(hourly_avg)
    else:
        st.info("Not enough data for hourly analysis")
    
    # Daily pattern (if enough days)
    if df['day'].nunique() > 1:
        daily_avg = df.groupby('day')['power'].mean()
        if not daily_avg.empty:
            st.subheader("Daily Average Consumption")
            st.bar_chart(daily_avg)
else:
    st.info("Timestamp column not available for time-based analysis")

st.markdown("---")

# Energy Saving Suggestions
st.subheader("💡 Energy Saving Suggestions")

suggestions = []

# Generate suggestions based on data
if latest_power > 2000:
    suggestions.append("🔴 **CRITICAL:** Very high energy usage detected - check for overloaded circuits")
elif latest_power > 1500:
    suggestions.append("🟠 **HIGH:** Energy consumption is high - consider reducing HVAC usage")
elif latest_power > 1000:
    suggestions.append("🟡 **MODERATE:** Energy usage is moderate - look for optimization opportunities")

if not occupied and latest_power > 500:
    suggestions.append("⚠️ **WASTE DETECTED:** High power usage while unoccupied - turn off devices")

if "loss" in df_with_loss.columns and loss_percentage > 15:
    suggestions.append("📉 **ENERGY LOSS:** Significant loss detected - check for inefficient appliances")

if devices.get("HVAC", 0) > 1000:
    suggestions.append("❄️ **HVAC OPTIMIZATION:** Air conditioner using high power - increase temperature by 2°C")

if devices.get("Lighting", 0) > 300:
    suggestions.append("💡 **LIGHTING:** High lighting load - consider switching to LED bulbs")

if suggestions:
    for suggestion in suggestions:
        st.write(suggestion)
else:
    st.success("✅ Great job! Your energy usage looks efficient. Keep monitoring!")

st.markdown("---")

# Raw data preview (optional)
with st.expander("📊 View Raw Data Preview"):
    st.dataframe(df.tail(20))
    st.caption(f"Showing last 20 of {len(df)} records")

# Refresh button
if st.button("🔄 Refresh Analysis", use_container_width=True):
    st.rerun()
 
