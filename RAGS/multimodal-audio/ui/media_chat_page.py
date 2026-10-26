"""Audio and Video Chat: questions over documents, transcripts and frames, with timestamped citations."""

from __future__ import annotations

import streamlit as st

from backend.media_retrieval import SCOPES
from backend.openai_client import OpenAIServiceError
from backend.vector_store import VectorStoreError
from ui.components import page_header, require_openai
from ui.media_components import media_privacy_note, render_requested_player, show_media_chunk_card

EXAMPLES = [
    "What topics did the instructor explain in the Python lecture?",
    "At what time did the instructor explain list comprehensions?",
    "Summarize the lecture between 0 and 1 minutes.",
    "What did the instructor say about embeddings?",
    "Which timestamp shows the slide explaining ChromaDB?",
    "What code is visible on the screen at 00:00:25?",
    "Compare the instructor's explanation of chunk overlap with the displayed slide.",
    "Which recorded session discusses RAG evaluation?",
    "Summarize all uploaded classes about vector databases.",
    "What is shown in the video when the instructor discusses chunk overlap?",
]


def media_retrieval_controls(services, prefix: str) -> dict:
    c1, c2, c3 = st.columns([2, 1, 1])
    scope_keys = list(SCOPES)
    scope = c1.selectbox("Search in", scope_keys, index=scope_keys.index(st.session_state.media_scope),
                         format_func=lambda k: SCOPES[k][0], key=f"{prefix}_scope")
    top_k = c2.slider("Top K", 1, 20, int(st.session_state.media_top_k), key=f"{prefix}_topk")
    use_thr = c3.toggle("Similarity threshold", value=False, key=f"{prefix}_usethr")
    c1, c2, c3 = st.columns([2, 1, 1])
    threshold = c1.slider("Minimum cosine similarity", 0.0, 1.0, 0.25, 0.05, disabled=not use_thr, key=f"{prefix}_thr")
    time_filter = c2.toggle("Use times in question", value=True, key=f"{prefix}_time",
                            help="'at 00:12:30' or 'between 10 and 20 minutes' filter the media by timestamp.")
    rerank = c3.toggle("Keyword rerank", value=False, key=f"{prefix}_rerank",
                       help="Small boost for chunks that contain the question's keywords.")
    names = sorted({r["filename"] for r in services.media_registry.list_documents()}
                   | {d["filename"] for d in services.registry.list_documents()})
    files = st.multiselect("Only these files (optional)", names, key=f"{prefix}_files")
    st.session_state.media_scope, st.session_state.media_top_k = scope, top_k
    return {
        "scope": scope, "top_k": top_k, "min_similarity": threshold if use_thr else None,
        "use_time_filter": time_filter, "rerank": rerank, "source_files": files or None,
    }


def _render_answer(services, entry: dict, index: int) -> None:
    st.markdown(entry["answer"])
    if entry.get("error"):
        return
    retrieval = entry.get("retrieval")
    if retrieval and retrieval.time_window:
        st.caption(f"🕒 Time filter applied: {retrieval.time_window.label}")
    if entry.get("citations"):
        st.markdown("**Sources:**")
        for citation in entry["citations"]:
            st.markdown(f"- **[{citation.label}]** {citation.chunk.citation}")
        for citation in entry["citations"]:
            show_media_chunk_card(services, citation.chunk, label=f"[{citation.label}]", key=f"c{index}")
    elif entry.get("grounded") is False:
        st.caption("No citations: the indexed content did not contain the answer.")
    if retrieval:
        for note in retrieval.diagnostics:
            st.caption(f"⚠️ {note}")
        with st.expander(f"All {len(retrieval.chunks)} retrieved chunk(s)"):
            for chunk in retrieval.chunks:
                show_media_chunk_card(services, chunk, key=f"r{index}")


def render(services) -> None:
    page_header("Audio and Video Chat", "Ask about your recorded classes; answers cite files and timestamps.", "🎬")
    if not require_openai(services):
        return
    if services.media_stores.total() + services.store.count() == 0:
        st.info("Nothing is indexed yet. Upload recordings on **🎙️ Audio and Video Upload**.")
        return

    render_requested_player(services)
    with st.expander("Search settings", expanded=False):
        controls = media_retrieval_controls(services, "mchat")
        if st.button("Clear chat history"):
            st.session_state.media_chat_history = []
            st.rerun()
    with st.expander("Example questions"):
        for example in EXAMPLES:
            if st.button(example, key=f"mex_{example}"):
                st.session_state.pending_media_question = example
                st.rerun()

    for i, entry in enumerate(st.session_state.media_chat_history):
        with st.chat_message("user"):
            st.markdown(entry["question"])
        with st.chat_message("assistant"):
            _render_answer(services, entry, i)

    question = st.chat_input("Ask about your recordings and documents…") or st.session_state.pop("pending_media_question", None)
    if question is None:
        media_privacy_note()
        return
    if not question.strip():
        st.warning("Please type a question.")
        return
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching transcripts, frames and documents…"):
            try:
                result = services.unified_rag.ask(question, **controls)
                entry = {"question": question, "answer": result.answer, "citations": result.citations,
                         "retrieval": result.retrieval, "grounded": result.grounded}
            except (OpenAIServiceError, VectorStoreError, ValueError) as exc:
                entry = {"question": question, "answer": f"⚠️ {exc}", "error": True}
        _render_answer(services, entry, len(st.session_state.media_chat_history))
    st.session_state.media_chat_history.append(entry)
