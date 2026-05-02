import streamlit as st
import pandas as pd

st.set_page_config(page_title="ElectroTrace AI", layout="wide")

st.title("⚡ ElectroTrace AI")
st.caption("Upload your energy dataset")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["energy_data"] = df
    st.success("Dataset loaded successfully!")
else:
    st.warning("Please upload a dataset to continue")
