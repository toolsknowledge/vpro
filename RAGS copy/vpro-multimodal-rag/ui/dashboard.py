from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.common import Services, cards, hero, pipeline_html, setup_banner, store_ready


def render(svc: Services) -> None:
    hero("Overview", "Upload documents, watch them become chunks and vectors, then ask questions with cited answers.")
    setup_banner(svc)
    store_ready(svc)
    docs = svc.registry.all()
    records = svc.store.count()
    cards([("Documents indexed", len(docs)), ("Chunks", sum(d.get("chunks", 0) for d in docs)),
           ("Embeddings", records), ("ChromaDB records", records),
           ("Last indexed", (svc.registry.last_indexed_at() or "never").replace("T", " ")[:19])])
    if records != sum(d.get("chunks", 0) for d in docs):
        st.warning("The registry and ChromaDB disagree on the number of chunks. Open **ChromaDB Explorer** to inspect, "
                   "or re-index the affected document.")
    st.subheader("How it works")
    st.markdown(pipeline_html(), unsafe_allow_html=True)
    st.caption("Then, for each question: **embed the question → search ChromaDB (top K) → build a grounded prompt → "
               "LLM answers with citations**.")
    st.subheader("Indexed documents")
    if not docs:
        st.info("Nothing is indexed yet. Go to **Upload Documents** (the four sample files are in `sample_files/`).")
        return
    df = pd.DataFrame([{"File": d["filename"], "Type": d["document_type"],
                        "Content": f"{d.get('units', '?')} {d.get('unit_label', '')}", "Chunks": d["chunks"],
                        "Dim": d.get("dimension"), "Embedding model": d.get("embedding_model"),
                        "Indexed at": d["indexed_at"].replace("T", " ")[:19]} for d in docs])
    st.dataframe(df, width="stretch", hide_index=True)
