import streamlit as st
from core.copilot import chat_response

st.title("🧠 Energy AI Copilot")

query = st.text_input("Ask your energy assistant:")

if query:
    response = chat_response(query)
    st.success(response)
