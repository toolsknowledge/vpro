import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

st.title("📚 RAG Application")

question = st.text_input("Ask your Question")

if st.button("Submit"):

    response = requests.post(
        API_URL,
        json={
            "question": question
        }
    )

    data = response.json()

    st.success(data["answer"])