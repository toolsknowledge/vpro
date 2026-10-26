"""Ask Your Documents: chat with grounded answers and expandable citations."""

from __future__ import annotations

import streamlit as st

from backend.openai_client import OpenAIServiceError
from backend.vector_store import VectorStoreError
from ui.components import page_header, privacy_note, require_openai, show_chunk_card

EXAMPLES = [
    "What is the difference between chunking and embeddings?",
    "What is the duration of the Python Full Stack course?",
    "Which courses are listed in the Excel file?",
    "What does the training policy say about project assessment?",
    "Summarize the PDF's explanation of the indexing pipeline.",
    "Compare the courses based on duration and fee.",
]


def retrieval_controls(prefix: str) -> tuple[int, float | None]:
    col1, col2, col3 = st.columns([1, 1, 1])
    top_k = col1.slider("Top K chunks", 1, 20, int(st.session_state.top_k), key=f"{prefix}_top_k")
    use_threshold = col2.toggle("Similarity threshold", value=st.session_state.use_threshold, key=f"{prefix}_use_thr",
                                help="Drop chunks whose cosine similarity is below this value.")
    threshold = col3.slider("Minimum cosine similarity", 0.0, 1.0, float(st.session_state.min_similarity), 0.05,
                            key=f"{prefix}_thr", disabled=not use_threshold)
    st.session_state.top_k, st.session_state.use_threshold, st.session_state.min_similarity = top_k, use_threshold, threshold
    return top_k, (threshold if use_threshold else None)


def _render_answer(entry: dict) -> None:
    st.markdown(entry["answer"])
    if entry.get("error"):
        return
    citations = entry.get("citations", [])
    if citations:
        st.markdown("**Sources:**")
        for citation in citations:
            show_chunk_card(citation.chunk, label=f"[{citation.label}]")
    elif entry.get("grounded") is False:
        st.caption("No citations: the retrieved chunks did not contain the answer.")
    retrieval = entry.get("retrieval")
    if retrieval:
        for note in retrieval.diagnostics:
            st.caption(f"⚠️ {note}")
        with st.expander(f"All {len(retrieval.chunks)} retrieved chunk(s) and metadata"):
            for chunk in retrieval.chunks:
                show_chunk_card(chunk)
            if retrieval.filtered_out:
                st.caption(f"{len(retrieval.filtered_out)} chunk(s) were below the similarity threshold and not sent to the model.")


def render(services) -> None:
    page_header("Ask Your Documents", "Questions are answered only from your indexed documents, with citations.", "💬")
    if not require_openai(services):
        return
    if services.store.count() == 0:
        st.info("No documents are indexed yet. Upload some on **📤 Upload Documents** first.")
        return

    with st.expander("Retrieval settings"):
        top_k, min_similarity = retrieval_controls("chat")
        if st.button("Clear chat history"):
            st.session_state.chat_history = []
            st.rerun()

    with st.expander("Example questions"):
        for example in EXAMPLES:
            if st.button(example, key=f"ex_{example}"):
                st.session_state.pending_question = example
                st.rerun()

    for entry in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(entry["question"])
        with st.chat_message("assistant"):
            _render_answer(entry)

    question = st.chat_input("Ask a question about your documents…") or st.session_state.pop("pending_question", None)
    if question is None:
        privacy_note()
        return
    if not question.strip():
        st.warning("Please type a question.")
        return

    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching your documents and writing an answer…"):
            try:
                result = services.rag.ask(question, top_k=top_k, min_similarity=min_similarity)
                entry = {
                    "question": question,
                    "answer": result.answer,
                    "citations": result.citations,
                    "retrieval": result.retrieval,
                    "grounded": result.grounded,
                }
            except (OpenAIServiceError, VectorStoreError, ValueError) as exc:
                entry = {"question": question, "answer": f"⚠️ {exc}", "error": True}
        _render_answer(entry)
    st.session_state.chat_history.append(entry)
