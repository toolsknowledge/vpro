
import streamlit as st
import requests

st.set_page_config(
    page_title="VPro Skills - Advanced RAG",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("🤖 VPro Skills - Advanced RAG")
st.caption("Ask questions about the indexed website using Claude and ChromaDB.")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed" not in st.session_state:
    st.session_state.indexed = False

# Sidebar
with st.sidebar:
    st.header("Website Indexing")

    website_url = st.text_input(
        "Website URL",
        value="https://www.vproskills.com/"
    )

    if st.button("Index Website", use_container_width=True):
        try:
            with st.spinner("Reading website and creating embeddings..."):
                response = requests.post(
                    f"{API_URL}/index",
                    json={"url": website_url},
                    timeout=300
                )
                response.raise_for_status()
                result = response.json()

            st.session_state.indexed = True
            st.session_state.messages = []

            st.success("Website indexed successfully!")
            st.json(result)

        except requests.RequestException as error:
            st.error(f"Indexing failed: {error}")

    st.divider()

    if st.button("Check Index Status", use_container_width=True):
        try:
            response = requests.get(
                f"{API_URL}/status",
                timeout=15
            )
            response.raise_for_status()
            st.json(response.json())
        except requests.RequestException as error:
            st.error(f"Could not check status: {error}")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Backend: FastAPI")
    st.caption("Vector database: ChromaDB")
    st.caption("LLM: Claude")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ask questions
question = st.chat_input(
    "Ask a question about VPro Skills..."
)

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching website content and generating answer..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question},
                    timeout=180
                )
                response.raise_for_status()
                result = response.json()

            # Support common response field names
            answer = (
                result.get("answer")
                or result.get("response")
                or result.get("result")
            )

            if answer is None:
                answer = str(result)

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            # Show additional response details if available
            with st.expander("View retrieval details"):
                st.json(result)

        except requests.RequestException as error:
            error_message = (
                f"Could not connect to the RAG backend: {error}\n\n"
                "Check that FastAPI is running and the endpoint is available."
            )
            st.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })
