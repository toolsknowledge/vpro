"""Overview dashboard: headline numbers, the pipeline, and the list of indexed documents."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from backend.document_registry import STATUS_INDEXED
from ui.components import format_time, metric_cards, page_header, pipeline_diagram, privacy_note


def render(services) -> None:
    page_header(
        "Smart Document RAG Assistant",
        "Upload PDF, Excel, Word and TXT files, watch them become chunks and vectors, then ask questions.",
        "📚",
    )
    if not services.openai_ready:
        st.warning(
            "OpenAI is not configured yet, so new documents cannot be indexed and questions cannot be answered. "
            "See **System Settings** for setup steps. Explorer pages still show existing data."
        )

    services.sync_registry()
    documents = services.registry.list_documents()
    indexed = [d for d in documents if d.get("status") == STATUS_INDEXED]
    total_records = services.store.count()

    metric_cards(
        [
            ("Documents indexed", f"{len(indexed)}", f"{len(documents) - len(indexed)} failed / missing"),
            ("Chunks", f"{sum(d.get('chunk_count', 0) for d in indexed):,}", "from the registry"),
            ("Embeddings", f"{sum(d.get('embedding_count', 0) for d in indexed):,}", services.settings.embedding_model),
            ("ChromaDB records", f"{total_records:,}", services.settings.chroma_collection_name),
            ("Last indexing", format_time(services.registry.last_indexed_at), "successful run"),
        ]
    )

    st.subheader("How the app works")
    st.markdown("**Indexing pipeline** (runs when you upload a document):")
    pipeline_diagram()
    st.markdown(
        "**Question answering:** your question → query embedding → nearest chunks in ChromaDB → "
        "prompt with those chunks → OpenAI chat model → answer with citations."
    )

    st.subheader("Indexed documents")
    if not documents:
        st.info("No documents yet. Go to **📤 Upload Documents** to add some (sample files are in `sample_files/`).")
    else:
        table = pd.DataFrame(
            [
                {
                    "File": d.get("filename"),
                    "Type": (d.get("document_type") or "").upper(),
                    "Status": d.get("status"),
                    "Chunks": d.get("chunk_count", 0),
                    "Units": ", ".join(f"{v} {k}" for k, v in (d.get("units") or {}).items()),
                    "Embedding model": d.get("embedding_model", ""),
                    "Indexed": format_time(d.get("indexed_at")),
                    "Document ID": d.get("document_id"),
                }
                for d in documents
            ]
        )
        st.dataframe(table, hide_index=True, width="stretch")

    privacy_note()
