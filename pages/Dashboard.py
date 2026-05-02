import streamlit as st
import sys
import os

# FIX PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.waste_engine import detect_waste

st.title("🏠 Energy Dashboard")

total_power = 2400
devices = disaggregate(total_power)

st.metric("Total Load", f"{total_power} W")
st.metric("Energy Score", "78 / 100")
st.metric("Estimated Bill", "RM 185")

st.subheader("Live Appliance Breakdown")

for device, power in devices.items():
    st.write(f"🔌 {device}: {round(power,2)} W")

st.subheader("AI Insight")

# Safe way to get AC power
ac_power = 0
# Try common AC name variations
for key in ['AC', 'ac', 'Air Conditioner', 'air_conditioner', 'aircon']:
    if key in devices:
        ac_power = devices[key]
        break

if ac_power > 0:
    st.warning(detect_waste(ac_power, False))
else:
    st.info("No AC device detected in current load")
