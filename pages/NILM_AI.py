import streamlit as st
import pandas as pd
from core.nilm_engine import disaggregate_series

st.title("🧠 NILM AI")

if "energy_data" not in st.session_state:
    st.warning("Upload dataset first")
    st.stop()

df = st.session_state["energy_data"]

st.line_chart(df["power"])

devices = disaggregate_series(df["power"])

st.subheader("Appliance Trends")

for name, series in devices.items():
    st.line_chart(series, height=150)
