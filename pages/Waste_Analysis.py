import streamlit as st
import pandas as pd

st.title("🗑️ Waste Analysis")

# Define waste analysis functions locally
def compute_loss(df):
    """Calculate energy loss"""
    if df is None or df.empty:
        return df
    
    df = df.copy()
    if "power_used" in df.columns:
        df["loss"] = df["power"] - df["power_used"]
    else:
        df["loss"] = df["power"] * 0.1
    return df

def detect_waste(power, occupied=False):
    """Detect energy waste based on power consumption"""
    if power > 1000 and not occupied:
        return "High", "⚠ High power usage in empty condition - Consider turning off devices"
    elif power > 500 and not occupied:
        return "Medium", "⚡ Moderate power usage while unoccupied - Some devices may be left on"
    elif power > 1000 and occupied:
        return "Medium", "💡 High power usage - Check for energy efficiency opportunities"
    else:
        return "Low", "✅ Normal energy usage"

if "energy_data" not in st.session_state:
    st.warning("⚠️ Please upload dataset from the Home page first")
    st.stop()

df = st.session_state["energy_data"]

if df.empty or "power" not in df.columns:
    st.error("Invalid data format. Make sure your data has a 'power' column.")
    st.stop()

# Calculate losses
df_with_loss = compute_loss(df)

# Get latest readings
latest_power = df["power"].iloc[-1]

# Occupancy status
occupied = st.checkbox("Room/Area Occupied", value=True)

# Detect waste
waste_level, waste_message = detect_waste(latest_power, occupied)

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Current Power", f"{round(latest_power, 2)} W")
col2.metric("Waste Level", waste_level)
col3.metric("Total Loss", f"{round(df_with_loss['loss'].sum(), 2)} Wh")

# Waste message
if waste_level == "High":
    st.error(waste_message)
elif waste_level == "Medium":
    st.warning(waste_message)
else:
    st.success(waste_message)

# Waste over time
st.subheader("Energy Loss Over Time")
if len(df_with_loss) > 1:
    st.line_chart(df_with_loss[["power", "loss"]].tail(100))

# Waste reduction suggestions
st.subheader("💡 Waste Reduction Suggestions")

if latest_power > 1000:
    st.write("• Consider turning off high-power devices when not in use")
    st.write("• Schedule heavy operations during occupied hours")
    st.write("• Upgrade to energy-efficient appliances")
elif latest_power > 500:
    st.write("• Review always-on devices in the area")
    st.write("• Consider using smart power strips")
    st.write("• Check for vampire power drain")
else:
    st.write("• Great job! Your energy usage is efficient")
    st.write("• Continue monitoring for unusual spikes")

# Calculate potential savings
if waste_level != "Low":
    potential_savings = latest_power * 0.3 / 1000 * 0.12 * 24 * 30  # Rough estimate
    st.info(f"💵 Potential monthly savings: ${round(potential_savings, 2)} by reducing waste")
