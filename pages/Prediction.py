import streamlit as st
import pandas as pd

st.title("💰 Bill Prediction")

# Define the prediction function locally
def predict_bill(df, rate_per_kwh=0.12):
    """Predict electricity bill based on usage"""
    if df is None or df.empty:
        return 0
    
    # Calculate total energy in kWh (assuming power is in Watts)
    if "power" in df.columns:
        total_wh = df["power"].sum()
        total_kwh = total_wh / 1000
        predicted_bill = total_kwh * rate_per_kwh
        return round(predicted_bill, 2)
    else:
        return 0

if "energy_data" not in st.session_state:
    st.warning("⚠️ Please upload dataset from the Home page first")
    st.stop()

df = st.session_state["energy_data"]

# Input for electricity rate
rate = st.number_input("Electricity Rate (per kWh)", value=0.12, min_value=0.01, step=0.01, format="%.2f")

# Calculate predictions
if not df.empty and "power" in df.columns:
    total_energy_kwh = df["power"].sum() / 1000
    predicted_bill = predict_bill(df, rate)
    
    col1, col2 = st.columns(2)
    col1.metric("📊 Total Energy Used", f"{round(total_energy_kwh, 2)} kWh")
    col2.metric("💰 Predicted Bill", f"${predicted_bill}")
    
    # Show projection for next month
    st.subheader("📈 Next Month Projection")
    avg_daily = total_energy_kwh / len(df) if len(df) > 0 else 0
    next_month_kwh = avg_daily * 30
    next_month_bill = next_month_kwh * rate
    
    st.metric("Projected Next Month Bill", f"${round(next_month_bill, 2)}")
    
    # Show usage chart
    st.subheader("Energy Consumption Pattern")
    st.line_chart(df["power"].tail(168))  # Last week of hourly data
else:
    st.error("Invalid data format. Make sure your data has a 'power' column.")
