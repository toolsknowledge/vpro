import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

FASTAPI_URL = "http://localhost:8000"


# ============================================================
# STREAMLIT PAGE
# ============================================================

st.set_page_config(
    page_title="Advanced RAG",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 Advanced RAG Application")

st.write(
    "Upload a PDF and ask questions from the document."
)


# ============================================================
# SIDEBAR - PDF UPLOAD
# ============================================================

st.sidebar.header("Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    if st.sidebar.button("Upload PDF"):

        with st.spinner("Uploading PDF..."):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }

                response = requests.post(
                    f"{FASTAPI_URL}/upload",
                    files=files
                )

                if response.status_code == 200:

                    result = response.json()

                    st.sidebar.success(
                        "PDF uploaded successfully!"
                    )

                    st.sidebar.write(
                        f"Chunks created: {result['chunks']}"
                    )

                else:

                    st.sidebar.error(
                        response.text
                    )

            except requests.exceptions.ConnectionError:

                st.sidebar.error(
                    "FastAPI is not running."
                )


# ============================================================
# QUESTION
# ============================================================

st.subheader("Ask a Question")

question = st.text_input(
    "Enter your question",
    placeholder="Example: What technologies does VPro Skills teach?"
)


# ============================================================
# ASK BUTTON
# ============================================================

if st.button("Ask"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Running Advanced RAG..."
        ):

            try:

                response = requests.post(
                    f"{FASTAPI_URL}/ask",
                    json={
                        "question": question
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    # ----------------------------------------
                    # ANSWER
                    # ----------------------------------------

                    st.subheader("Answer")

                    st.write(
                        result["answer"]
                    )

                    # ----------------------------------------
                    # SOURCES
                    # ----------------------------------------

                    st.subheader("Sources")

                    for source in result["sources"]:

                        st.write(
                            f"📄 {source['source']} "
                            f"- Chunk {source['chunk']}"
                        )

                else:

                    st.error(
                        response.text
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI is not running. "
                    "Start main.py first."
                )