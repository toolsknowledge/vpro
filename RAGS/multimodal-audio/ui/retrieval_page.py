"""Search and Retrieval diagnostics: what happens between the question and the LLM."""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from backend.openai_client import OpenAIServiceError
from backend.rag_chain import build_messages
from backend.retrieval import format_citation, keyword_search
from backend.vector_store import VectorStoreError
from ui.chat_page import retrieval_controls
from ui.components import page_header, require_openai, show_chunk_card


def _explain() -> None:
    with st.expander("📖 Semantic search vs keyword search", expanded=False):
        st.markdown(
            """
* **Keyword search** looks for the *same words*. "course cost" will not match a chunk that only says "fee".
* **Semantic search** compares *meaning*. The question is turned into a vector with the same embedding model
  as the chunks, and ChromaDB returns the chunks whose vectors are closest.
* **Distance vs similarity:** this collection uses the **cosine** distance metric. ChromaDB returns
  `distance = 1 − cosine similarity`, so a *smaller* distance means *more similar*. The app converts it:
  `similarity = 1 − distance`. Raw distances are shown unchanged next to it.
"""
        )


def render(services) -> None:
    page_header("Search and Retrieval", "Inspect every step from your question to the context sent to the LLM.", "🔎")
    _explain()
    if not require_openai(services):
        return
    if services.store.count() == 0:
        st.info("No documents are indexed yet.")
        return

    question = st.text_input("Question", placeholder="What is the duration of the Python Full Stack course?")
    top_k, min_similarity = retrieval_controls("diag")
    if not st.button("Run retrieval", type="primary"):
        return
    if not question.strip():
        st.warning("Please type a question first.")
        return

    try:
        with st.spinner("Embedding the question and querying ChromaDB…"):
            result = services.retriever.retrieve(question, top_k=top_k, min_similarity=min_similarity)
    except (OpenAIServiceError, VectorStoreError, ValueError) as exc:
        st.error(str(exc))
        return

    st.subheader("1 · Query")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Query embedding dimension", result.query_dimension)
    c2.metric("Results requested (K)", result.top_k)
    c3.metric("Distance metric", result.metric)
    c4.metric("Passed threshold", f"{len(result.chunks)} / {len(result.chunks) + len(result.filtered_out)}")
    st.caption(f"Query text: “{result.question}” · embedding model `{result.embedding_model}`")

    st.subheader("2 · Diagnostics")
    if result.diagnostics:
        for note in result.diagnostics:
            st.warning(note)
    else:
        st.success("The top results look relevant: good similarity and the question's keywords appear in the chunks.")

    st.subheader("3 · Retrieved chunks")
    rows = [
        {
            "Rank": c.rank,
            "Chunk ID": c.chunk_id,
            "Source": format_citation(c.metadata),
            "Raw distance": round(c.distance, 4),
            "Cosine similarity": round(c.similarity, 4) if c.similarity is not None else None,
            "Keyword overlap": f"{c.keyword_overlap:.0%}",
            "Sent to LLM": c in result.chunks,
        }
        for c in sorted(result.chunks + result.filtered_out, key=lambda c: c.rank)
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    for chunk in result.chunks:
        show_chunk_card(chunk)
    for chunk in result.filtered_out:
        show_chunk_card(chunk, label="below threshold")

    st.subheader("4 · Keyword search, for comparison")
    keyword_hits = keyword_search(services.store, question, top_k)
    if keyword_hits:
        semantic_ids = {c.chunk_id for c in result.chunks}
        st.dataframe(
            pd.DataFrame(
                [
                    {"Keyword matches": hits, "Chunk ID": cid, "Source": format_citation(meta),
                     "Also found by semantic search": cid in semantic_ids, "Text": text[:100].replace("\n", " ")}
                    for hits, cid, text, meta in keyword_hits
                ]
            ),
            hide_index=True,
            width="stretch",
        )
    else:
        st.caption("No chunk contains any of the question's keywords. Semantic search can still find related meaning.")

    st.subheader("5 · Final context and prompt sent to the LLM")
    if not result.chunks:
        st.info("No chunks passed, so the app would answer “not found” without calling the chat model.")
        return
    messages = build_messages(result.question, result.chunks)
    for message in messages:
        st.markdown(f"**{message['role']}**")
        st.markdown(f'<div class="vp-chunk">{html.escape(message["content"])}</div>', unsafe_allow_html=True)
