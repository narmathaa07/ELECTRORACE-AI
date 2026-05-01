import streamlit as st
from core.prediction import predict_bill

st.title("🔮 Energy Prediction System")

total_kwh = 3.2

bill = predict_bill(total_kwh)

st.metric("Predicted Monthly Bill", f"RM {bill}")

st.info("Energy usage trend: increasing 8% weekly")
