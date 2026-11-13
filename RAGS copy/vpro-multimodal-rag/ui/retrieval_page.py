from __future__ import annotations

import pandas as pd
import streamlit as st

from backend.errors import AppError
from backend.rag_chain import build_messages
from backend.retrieval import Retriever, diagnose, format_context
from ui.common import Services, cfg, get_embedder, hero, setup_banner, show_error, store_ready


def render(svc: Services) -> None:
    hero("Search and Retrieval", "See exactly what the database returns for a question - before any LLM is involved.")
    with st.expander("Semantic search vs keyword search", expanded=True):
        st.markdown(
            "- **Keyword search** looks for the same *words*. \"How long is the Python course?\" would miss a row that says "
            "\"Duration: 16 weeks\" because the words differ.\n"
            "- **Semantic search** compares *meaning*. The question and every chunk are turned into vectors; ChromaDB returns the chunks "
            "whose vectors point in the most similar direction (smallest cosine distance).\n"
            "- Semantic search can still return irrelevant chunks, which is why the scores and text are shown here.")
    can_use_api = setup_banner(svc)
    ready = store_ready(svc)
    c = cfg()
    q = st.text_input("Question", placeholder="What is the duration of the Python Full Stack course?")
    a, b, d = st.columns(3)
    k = int(a.number_input("Top K", 1, 30, c["top_k"]))
    use_t = b.checkbox("Use similarity threshold")
    thr = d.slider("Minimum similarity", 0.0, 1.0, 0.2, 0.05, disabled=not use_t)
    only = st.multiselect("Limit to files", [x["filename"] for x in svc.registry.all()])
    if st.button("🔎 Run retrieval", type="primary", disabled=not (can_use_api and ready)):
        if not q.strip():
            st.warning("Please type a question.")
            return
        try:
            with st.spinner("Embedding the question and searching ChromaDB…"):
                st.session_state["last_retrieval"] = Retriever(svc.store, get_embedder(svc)).retrieve(
                    q, k, thr if use_t else None, only or None)
        except AppError as exc:
            show_error(exc)
            return
    res = st.session_state.get("last_retrieval")
    if not res:
        return
    st.subheader("1 · Query")
    cols = st.columns(4)
    cols[0].metric("Query embedding dimension", res.embedding_dim)
    cols[1].metric("Results requested", res.k_requested)
    cols[2].metric("Distance metric", res.metric)
    cols[3].metric("Results returned", len(res.hits))
    st.write(f"Query text: **{res.query}**")
    for level, msg in diagnose(res):
        {"ok": st.success, "warning": st.warning, "error": st.error}[level](msg)
    if not res.hits:
        return
    st.subheader("2 · Retrieved chunks")
    st.caption("Chroma returns a *distance* (cosine distance = 1 − cosine similarity; smaller is closer). Similarity below is computed from it.")
    st.dataframe(pd.DataFrame([{"Rank": h.rank, "Chunk ID": h.chunk_id, "Source": h.metadata.get("source_file"),
                                "Citation": h.citation, "Raw distance": round(h.distance, 4),
                                "Similarity": None if h.similarity is None else round(h.similarity, 4),
                                "Tokens": h.metadata.get("token_count")} for h in res.hits]),
                 width="stretch", hide_index=True)
    for h in res.hits:
        with st.expander(f"[{h.rank}] {h.citation}  ·  distance {h.distance:.4f}"):
            st.code(h.text, language=None, wrap_lines=True)
            st.json(h.metadata)
    st.subheader("3 · Final context sent to the LLM")
    st.caption("Only these passages and your question are sent to OpenAI (no other document content).")
    st.code(format_context(res.hits), language=None, wrap_lines=True)
    with st.expander("Full prompt messages (system rules + context + question)"):
        for m in build_messages(res.query, res.hits):
            st.markdown(f"**{m['role']}**")
            st.code(m["content"], language=None, wrap_lines=True)
