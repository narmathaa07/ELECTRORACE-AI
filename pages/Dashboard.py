import streamlit as st
from core.nilm_engine import disaggregate
from core.waste_engine import detect_waste

st.title("🏠 Energy Dashboard")

total_power = 2400  # simulated NILM input

devices = disaggregate(total_power)

st.metric("Total Load", f"{total_power} W")
st.metric("Energy Score", "78 / 100")
st.metric("Estimated Bill", "RM 185")

st.subheader("Live Appliance Breakdown")

for device, power in devices.items():
    st.write(f"🔌 {device}: {round(power,2)} W")

st.subheader("AI Insight")

st.warning(detect_waste(devices["AC"], False))
