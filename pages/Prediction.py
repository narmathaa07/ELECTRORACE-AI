import streamlit as st
from core.prediction_engine import predict_bill

st.title("🔮 Prediction")

if "energy_data" not in st.session_state:
    st.warning("Upload dataset first")
    st.stop()

df = st.session_state["energy_data"]

bill = predict_bill(df)

st.metric("Estimated Monthly Bill", f"RM {bill}")

st.info("Prediction based on historical usage")
