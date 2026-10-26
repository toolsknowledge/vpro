"""ChromaDB Explorer: the actual contents of the persistent collection, plus safe deletion."""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from backend.vector_store import VectorStoreError
from ui.components import page_header, vector_preview

PAGE_SIZE = 25


def render(services) -> None:
    page_header("ChromaDB Explorer", "What is really stored in the vector database.", "🗄️")
    store = services.store

    top1, top2 = st.columns([4, 1])
    if top2.button("🔄 Refresh", width="stretch"):
        services.sync_registry()
        st.rerun()

    total = store.count()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Collection", store.collection_name)
    c2.metric("Records", f"{total:,}")
    c3.metric("Distance metric", store.distance_metric)
    c4.metric("Embedding dimension", store.stored_dimension or "–")
    top1.caption(f"Persist directory: `{store.persist_directory}` · stored embedding model: `{store.stored_embedding_model or '–'}`")

    if total == 0:
        st.info("The collection is empty. Index documents on **📤 Upload Documents**.")
        _danger_zone(services, total)
        return

    # ------------------------------------------------------------- browse
    all_meta = store.get_records()
    sources = sorted({(r.metadata.get("source_file", "?"), r.metadata.get("document_id", "?")) for r in all_meta})
    labels = ["All documents"] + [f"{name}  ({doc_id})" for name, doc_id in sources]
    choice = st.selectbox("Filter by source document", labels)
    where = None
    if choice != "All documents":
        where = {"document_id": sources[labels.index(choice) - 1][1]}

    matching = len(store.get_records(where=where)) if where else total
    pages = max(1, -(-matching // PAGE_SIZE))
    page = st.number_input(f"Page (1–{pages})", 1, pages, 1) if pages > 1 else 1
    records = store.get_records(where=where, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE, include_embeddings=True)

    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Chunk ID": r.chunk_id,
                    "Source": r.metadata.get("source_file"),
                    "Index": r.metadata.get("chunk_index"),
                    "Page": r.metadata.get("page_number"),
                    "Sheet": r.metadata.get("sheet_name"),
                    "Section": r.metadata.get("section_title"),
                    "Tokens": r.metadata.get("token_count"),
                    "Dim": len(r.embedding or []),
                    "Vector preview": vector_preview(r.embedding, 4),
                    "Text": r.text[:100].replace("\n", " "),
                }
                for r in records
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption(f"Showing {len(records)} of {matching} record(s).")

    if records:
        ids = [r.chunk_id for r in records]
        selected = st.selectbox("Inspect a record", ids)
        record = records[ids.index(selected)]
        with st.container(border=True):
            st.markdown(f'<div class="vp-chunk">{html.escape(record.text)}</div>', unsafe_allow_html=True)
            st.json(record.metadata, expanded=False)
            st.code(vector_preview(record.embedding, 10), language=None)

    _danger_zone(services, total)


def _danger_zone(services, total: int) -> None:
    st.divider()
    st.subheader("🗑️ Delete data")
    documents = services.registry.list_documents()
    with st.container(border=True):
        st.markdown("**Remove one document** (its chunks, vectors, registry entry, trace and stored upload).")
        if documents:
            options = {f"{d['filename']} ({d['document_id']}, {d.get('chunk_count', 0)} chunks)": d for d in documents}
            target = st.selectbox("Document to remove", list(options))
            confirm = st.checkbox("Yes, delete this document's indexed records", key="confirm_delete_one")
            if st.button("Delete document", disabled=not confirm):
                doc = options[target]
                try:
                    removed = services.pipeline.delete_document(doc["document_id"])
                    st.session_state.last_index_reports = []
                    st.success(f"Deleted '{doc['filename']}' ({removed} record(s) removed from ChromaDB).")
                except VectorStoreError as exc:
                    st.error(f"Deletion failed; nothing was removed from the registry. {exc}")
        else:
            st.caption("No documents in the registry.")

    with st.container(border=True):
        st.markdown(f"**Clear the entire collection** ({total:,} records) and forget all documents.")
        typed = st.text_input("Type DELETE ALL to confirm", key="confirm_clear_all")
        if st.button("Clear everything", type="primary", disabled=typed.strip() != "DELETE ALL"):
            try:
                services.store.reset_collection()
                services.registry.clear()
                st.session_state.last_index_reports = []
                st.session_state.chat_history = []
                st.success("The collection was cleared.")
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(f"Clearing failed: {exc}")
