"""Retrieval Diagnostics (multimodal): every step between the question and the LLM, across all collections."""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from backend.media_retrieval import SCOPES, SOURCE_LABELS
from backend.media_utils import format_timestamp
from backend.openai_client import OpenAIServiceError
from backend.rag_chain import build_messages
from backend.unified_rag import SYSTEM_PROMPT
from backend.vector_store import VectorStoreError
from ui.components import page_header, require_openai
from ui.media_chat_page import media_retrieval_controls
from ui.media_components import render_requested_player, show_media_chunk_card


def render(services) -> None:
    page_header("Retrieval Diagnostics", "Query embedding, per-collection hits, timestamps, distances and the final prompt.", "🔬")
    if not require_openai(services):
        return
    render_requested_player(services)
    question = st.text_input("Question", placeholder="What code is visible on the screen at 00:00:25?")
    controls = media_retrieval_controls(services, "mdiag")
    if st.button("Run retrieval", type="primary"):
        try:
            with st.spinner("Embedding the question and querying ChromaDB…"):
                st.session_state.media_diag_result = services.unified_retriever.retrieve(question, **controls)
        except (OpenAIServiceError, VectorStoreError, ValueError) as exc:
            st.error(str(exc))
            return
    # Kept in the session so that pressing a ▶ Play button (which reruns the page) does not lose the results.
    result = st.session_state.get("media_diag_result")
    if result is None:
        return

    st.subheader("1 · Query")
    c = st.columns(4)
    c[0].metric("Query embedding dimension", result.query_dimension or "—")
    c[1].metric("Embedding model", result.embedding_model)
    c[2].metric("Top K", result.top_k)
    c[3].metric("Scope", SCOPES[result.scope][0])
    st.caption(
        "Time window parsed from the question: "
        + (f"**{result.time_window.label}** (used as a ChromaDB metadata filter)" if result.time_window else "none")
    )
    collections = {
        SOURCE_LABELS[m]: f"{n:,} records in `{services.unified_retriever.stores[m].collection_name}`"
        for m, n in (result.searched or {}).items()
    }
    st.dataframe(pd.DataFrame(collections.items(), columns=["Searched", "Collection"]), hide_index=True, width="stretch")

    st.subheader("2 · Diagnostics")
    for note in result.diagnostics or ["The top results look relevant."]:
        (st.warning if result.diagnostics else st.success)(note)

    st.subheader("3 · Retrieved chunks")
    rows = []
    for chunk in sorted(result.chunks + result.filtered_out, key=lambda c: c.rank):
        meta = chunk.metadata
        rows.append(
            {
                "Rank": chunk.rank,
                "Type": SOURCE_LABELS.get(meta.get("media_type"), "Document"),
                "Source": meta.get("source_file"),
                "Transcript time": (f"{format_timestamp(meta['start_time_seconds'])}–{format_timestamp(meta['end_time_seconds'])}"
                                    if "start_time_seconds" in meta else ""),
                "Frame time": format_timestamp(meta["timestamp_seconds"]) if "timestamp_seconds" in meta else "",
                "Timing source": meta.get("timing_source", ""),
                "Raw distance": round(chunk.distance, 4),
                "Cosine similarity": round(chunk.similarity, 4) if chunk.similarity is not None else None,
                "Sent to LLM": chunk in result.chunks,
                "Chunk ID": chunk.chunk_id,
            }
        )
    if rows:
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    for chunk in result.chunks:
        show_media_chunk_card(services, chunk, key="diag")
    for chunk in result.filtered_out:
        show_media_chunk_card(services, chunk, label="below threshold", key="diagf")

    st.subheader("4 · Final context and prompt sent to the LLM")
    if not result.chunks:
        st.info("Nothing passed, so the app answers “not enough information” without calling the chat model.")
        return
    for message in build_messages(result.question, result.chunks, SYSTEM_PROMPT):
        st.markdown(f"**{message['role']}**")
        st.markdown(f'<div class="vp-chunk">{html.escape(message["content"])}</div>', unsafe_allow_html=True)
