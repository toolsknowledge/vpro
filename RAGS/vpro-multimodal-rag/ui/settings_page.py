from __future__ import annotations

import streamlit as st

from backend.embeddings import get_client
from backend.errors import AppError, translate_openai_error
from backend.indexer import reindex_all
from ui.common import Services, cfg, get_embedder, hero, invalidate_state, setup_banner, show_error


def render(svc: Services) -> None:
    hero("System Settings", "Configuration (secrets are never shown), runtime tuning, health checks.")
    s = svc.settings
    setup_banner(svc)
    for p in s.problems():
        if "OPENAI_API_KEY" not in p:
            st.error(p)
    st.subheader("Configuration (from .env)")
    st.table({"Setting": ["OpenAI API key", "Chat model", "Embedding model", "ChromaDB directory", "Collection",
                          "Chunk size / overlap", "Top K", "Max upload size"],
              "Value": ["✅ configured" if s.has_api_key else "❌ missing", s.chat_model, s.embedding_model, str(s.chroma_dir),
                        s.collection_name, f"{s.chunk_size} / {s.chunk_overlap} tokens", str(s.top_k), f"{s.max_upload_mb} MB"]})
    st.caption("Edit `.env` and restart the app to change these permanently.")

    st.subheader("Session tuning")
    c = cfg()
    a, b, d = st.columns(3)
    c["chunk_size"] = int(a.number_input("Chunk size", 50, 8000, c["chunk_size"], 50))
    c["chunk_overlap"] = int(b.number_input("Chunk overlap", 0, 4000, c["chunk_overlap"], 10))
    c["top_k"] = int(d.number_input("Top K", 1, 30, c["top_k"]))
    if c["chunk_overlap"] >= c["chunk_size"]:
        st.error("Overlap must be smaller than chunk size.")
    st.caption("Applies to the next indexing run / question in this browser session. Existing chunks are not changed unless re-indexed.")

    st.subheader("Health check")
    if st.button("Test OpenAI access (checks both models; no tokens used)", disabled=not s.has_api_key):
        client = get_client(s)
        for label, model in (("Embedding", s.embedding_model), ("Chat", s.chat_model)):
            try:
                client.models.retrieve(model)
                st.success(f"{label} model `{model}` is available.")
            except Exception as exc:
                st.error(f"{label} model `{model}`: {translate_openai_error(exc, AppError, model)}")
    problem = svc.store.compatibility_problem()
    st.subheader("Re-indexing")
    if problem:
        st.error(problem)
    docs = svc.registry.all()
    st.write(f"{len(docs)} document(s) can be re-indexed from their stored copies with the current model "
             f"(`{s.embedding_model}`) and chunk settings. All embeddings are computed first; if anything fails, "
             "the existing index is left untouched.")
    if st.button("♻️ Re-index all documents", disabled=not docs or not s.has_api_key):
        bar = st.progress(0.0)
        try:
            res = reindex_all(settings=s, registry=svc.registry, store=svc.store, embedder=get_embedder(svc),
                              chunk_size=c["chunk_size"], chunk_overlap=c["chunk_overlap"],
                              progress=lambda stage, f: bar.progress(min(f, 1.0), text=stage))
            invalidate_state()
            st.success(f"Re-indexed {len(res)} document(s).")
        except Exception as exc:
            show_error(exc)

    st.subheader("Privacy, security & limits of this demo")
    st.markdown(
        "- Document text is sent to **OpenAI** for embeddings; retrieved passages + your question are sent for answers.\n"
        "- Uploaded text is treated as untrusted; the model is told never to follow instructions inside documents.\n"
        "- This is a **single-user local demo**: no login, no per-user data isolation, one shared collection, files stored on local disk. "
        "Before multi-user deployment you need authentication, per-user collections, encrypted storage, rate limiting, audit logs, "
        "and a managed vector database.\n"
        "- Scanned PDFs / images are **not** read (no OCR).")
