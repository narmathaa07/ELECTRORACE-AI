import streamlit as st
import pandas as pd
from core.waste_engine import compute_loss

st.title("⚠ Waste Analysis")

if "energy_data" not in st.session_state:
    st.warning("Upload dataset first")
    st.stop()

df = st.session_state["energy_data"]

df = compute_loss(df)

st.metric("Total Loss", f"{round(df['loss'].sum(),2)} W")

st.line_chart(df["loss"])

st.subheader("Loss Over Time")
st.area_chart(df["loss"])
