
import sys
from pathlib import Path

import streamlit as st

# Locate the project root: crag/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import load_chunks, build_index, answer_question


st.set_page_config(
    page_title="VPro Skills | CRAG Demo",
    page_icon="📚",
    layout="wide",
)

st.title("CRAG — Corrective Retrieval-Augmented Generation")
st.caption("VPro Skills | OpenAI + FAISS")

st.write(
    "Ask a question about the information stored in sample.txt."
)


@st.cache_data
def get_chunks():
    return load_chunks()


@st.cache_resource
def get_index():
    chunks = get_chunks()
    return build_index(chunks)


try:
    chunks = get_chunks()
    index = get_index()
except Exception as error:
    st.error(f"Failed to initialize CRAG: {error}")
    st.stop()


question = st.text_input(
    "Enter your question",
    placeholder="What is the duration of the Python course?",
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Retrieving and evaluating documents..."):
                result = answer_question(
                    question.strip(),
                    chunks,
                    index,
                )

            st.subheader("Final Answer")
            st.write(result["answer"])

            st.subheader("Retrieval Status")

            if result["corrected"]:
                st.info("Corrective retrieval was attempted.")
                st.write(
                    "Rewritten query:",
                    result["search_query"],
                )
            else:
                st.write("No corrective retrieval was needed.")

            if result["relevant"]:
                st.success(
                    "Retrieved information was evaluated as sufficient."
                )
            else:
                st.warning(
                    "Retrieved information was still insufficient."
                )

            st.subheader("Retrieved Chunks")

            if result["results"]:
                for number, item in enumerate(
                    result["results"], start=1
                ):
                    with st.expander(
                        f"Chunk {number} | Cosine similarity: "
                        f"{item['score']:.3f}"
                    ):
                        st.write(item["text"])
            else:
                st.info("No chunks were retrieved.")

        except Exception as error:
            st.error(f"CRAG execution failed: {error}")
