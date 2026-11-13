from __future__ import annotations

import pandas as pd
import streamlit as st

from backend.errors import AppError
from backend.indexer import clear_everything, delete_document
from ui.common import Services, cards, fmt_location, hero, invalidate_state, show_error


def render(svc: Services) -> None:
    hero("ChromaDB Explorer", "The real contents of the persistent vector database.")
    if st.button("🔄 Refresh"):
        st.rerun()
    store = svc.store
    cards([("Collection", store.collection_name), ("Records", store.count()),
           ("Embedding dimension", store.stored_dimension() or "—"), ("Distance metric", store.distance_metric)])
    st.caption(f"Persisted at `{store.persist_dir}` · created for model `{store.stored_model or '?'}`")
    problem = store.compatibility_problem()
    if problem:
        st.error(problem)
    docs = svc.registry.all()
    file = st.selectbox("Filter by source document", ["All"] + [d["filename"] for d in docs])
    where = None if file == "All" else {"source_file": file}
    recs = store.get_records(where=where, limit=2000, include_embeddings=True)
    if not recs:
        st.info("No records.")
    else:
        st.dataframe(pd.DataFrame([{
            "Chunk ID": r["id"], "Source": r["metadata"].get("source_file"), "Location": fmt_location(r["metadata"]),
            "Tokens": r["metadata"].get("token_count"), "Dim": len(r["embedding"]),
            "Vector preview": str([round(x, 4) for x in r["embedding"][:5]]) + " …",
            "Text": r["document"][:200].replace("\n", " "), "Metadata": str(r["metadata"])} for r in recs]),
            width="stretch", hide_index=True)
        pick = st.selectbox("Read a full stored document text", [r["id"] for r in recs])
        st.code(next(r["document"] for r in recs if r["id"] == pick), language=None, wrap_lines=True)

    st.subheader("Delete data")
    if docs:
        with st.container(border=True):
            target = st.selectbox("Document to remove", [f"{d['filename']} ({d['document_id'][:8]})" for d in docs], key="del_doc")
            doc = docs[[f"{d['filename']} ({d['document_id'][:8]})" for d in docs].index(target)]
            sure = st.checkbox(f"I understand this permanently deletes all chunks and vectors of '{doc['filename']}'")
            if st.button("🗑️ Delete this document", disabled=not sure):
                try:
                    n = delete_document(doc["document_id"], registry=svc.registry, store=store)
                    invalidate_state()
                    st.toast(f"Deleted {n} record(s) and the registry entry for {doc['filename']}.", icon="🗑️")
                    st.rerun()
                except AppError as exc:
                    show_error(exc)
    with st.container(border=True):
        st.markdown("**Clear the entire collection**")
        phrase = st.text_input("Type DELETE ALL to confirm")
        if st.button("⚠️ Clear everything", disabled=phrase != "DELETE ALL"):
            try:
                clear_everything(registry=svc.registry, store=store)
                invalidate_state()
                st.session_state.pop("last_run", None)
                st.toast("Collection cleared and registry reset.", icon="🧹")
                st.rerun()
            except AppError as exc:
                show_error(exc)
