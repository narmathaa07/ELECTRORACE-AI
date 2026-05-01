import streamlit as st

st.title("⚠ Energy Waste Analysis")

st.subheader("Top Energy Loss Sources")

st.write("🔴 AC Standby Loss → 42%")
st.write("🟠 Fridge Inefficiency → 28%")
st.write("🟡 Device Idle Power → 18%")

st.warning("Main issue: Air conditioner running without occupancy detected")
