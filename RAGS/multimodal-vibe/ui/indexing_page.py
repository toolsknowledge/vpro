"""Indexing Pipeline: follow one real document through every stage."""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from backend.document_registry import STATUS_INDEXED
from backend.retrieval import format_citation
from ui.components import format_time, page_header, pipeline_diagram, vector_preview


def _location(section: dict) -> str:
    return format_citation({**section, "row_start": section.get("row_number"), "row_end": section.get("row_number")})


def render(services) -> None:
    page_header(
        "Indexing Pipeline",
        "Upload → Extract → Clean → Chunk → Embed → Store in ChromaDB, shown with real data from your files.",
        "🛠️",
    )

    documents = [d for d in services.registry.list_documents() if d.get("stages")]
    if not documents:
        st.info("No document has been processed yet. Upload one on **📤 Upload Documents**; its pipeline will appear here.")
        pipeline_diagram()
        return

    # Totals across all indexed documents: a real "sample flow" with actual counts.
    indexed = [d for d in documents if d.get("status") == STATUS_INDEXED]
    if indexed:
        st.subheader("All indexed documents together")
        totals = {
            "upload": len(indexed),
            "extract": sum(d.get("units", {}).get("pages", 0) + d.get("units", {}).get("worksheets", 0)
                           + d.get("units", {}).get("sections", 0) for d in indexed),
            "clean": sum(d.get("section_count", 0) for d in indexed),
            "chunk": sum(d.get("chunk_count", 0) for d in indexed),
            "embed": sum(d.get("embedding_count", 0) for d in indexed),
            "store": services.store.count(),
        }
        outputs = {
            "upload": f"{len(indexed)} file(s)",
            "extract": "pages + worksheets + sections",
            "clean": "cleaned sections / rows",
            "chunk": "chunks",
            "embed": f"vectors ({services.settings.embedding_model})",
            "store": f"records in '{services.store.collection_name}'",
        }
        pipeline_diagram([{"key": k, "status": "done", "count": v, "output": outputs[k]} for k, v in totals.items()])

    st.subheader("Follow one document")
    labels = {f"{d['filename']} ({d.get('status')})": d for d in documents}
    choice = st.selectbox("Document", list(labels))
    doc = labels[choice]

    st.caption(
        f"Document ID `{doc['document_id']}` · SHA-256 `{(doc.get('file_hash') or '')[:16]}…` · "
        f"indexed {format_time(doc.get('indexed_at'))} · chunk size {doc.get('chunk_size', '–')} / overlap "
        f"{doc.get('chunk_overlap', '–')} · {doc.get('processing_seconds', '–')} s"
    )
    if doc.get("last_error"):
        st.error(f"Last error: {doc['last_error']}")
    pipeline_diagram(doc["stages"])
    for warning in doc.get("warnings", []):
        st.warning(warning)

    trace = services.registry.load_trace(doc["document_id"])
    if not trace:
        st.info("No pipeline trace is stored for this document (it failed before chunking, or was indexed elsewhere).")
        return

    tab_extract, tab_clean, tab_chunks, tab_embed, tab_store = st.tabs(
        ["1–2 · Extracted text", "3 · Cleaned text", "4 · Chunks", "5 · Embeddings", "6 · ChromaDB records"]
    )

    raw, clean = trace["raw_sections"], trace["clean_sections"]
    with tab_extract:
        st.markdown(f"**{len(raw)} extracted section(s)**. Each has its own source metadata.")
        idx = st.number_input("Section", 1, len(raw), 1, key="trace_raw_idx") - 1
        section = raw[idx]
        st.caption(f"{_location(section)} · method: {section['extraction_method']}")
        st.text_area("Raw extracted text", section["text"], height=220, disabled=True, key=f"raw_{doc['document_id']}_{idx}")

    with tab_clean:
        st.markdown(
            f"Cleaning normalised **{sum(len(s['text']) for s in raw):,}** characters into "
            f"**{sum(len(s['text']) for s in clean):,}** characters across {len(clean)} section(s)."
        )
        idx = st.number_input("Section", 1, len(clean), 1, key="trace_clean_idx") - 1
        cleaned = clean[idx]
        original = next((s for s in raw if s["group_key"] == cleaned["group_key"] and s.get("row_number") == cleaned.get("row_number")), None)
        col1, col2 = st.columns(2)
        col1.text_area("Before cleaning", original["text"] if original else "(not found)", height=220, disabled=True, key=f"before_{idx}")
        col2.text_area("After cleaning", cleaned["text"], height=220, disabled=True, key=f"after_{idx}")

    chunks = trace["chunks"]
    with tab_chunks:
        st.markdown(f"**{len(chunks)} chunk(s)**. Open **🧩 Chunk Explorer** for overlap highlighting and filters.")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "#": c["chunk_index"],
                        "Chunk ID": c["chunk_id"],
                        "Location": format_citation(c),
                        "Tokens": c["token_count"],
                        "Preview": c["text"][:120].replace("\n", " ") + ("…" if len(c["text"]) > 120 else ""),
                    }
                    for c in chunks
                ]
            ),
            hide_index=True,
            width="stretch",
        )

    records = services.store.get_records(where={"document_id": doc["document_id"]}, include_embeddings=True)
    records.sort(key=lambda r: r.metadata.get("chunk_index", 0))
    with tab_embed:
        if not records:
            st.warning("No vectors for this document are in ChromaDB right now.")
        else:
            st.markdown(
                f"**{len(records)}** vector(s) from `{records[0].metadata.get('embedding_model', '?')}`, "
                f"each with **{len(records[0].embedding or [])}** numbers. First 10 values per chunk:"
            )
            for r in records[:10]:
                st.markdown(f"`{r.chunk_id}` → `{vector_preview(r.embedding)}`")
            if len(records) > 10:
                st.caption(f"…and {len(records) - 10} more. See **🔢 Embedding Explorer**.")

    with tab_store:
        st.markdown(
            f"ChromaDB holds **{len(records)}** record(s) for this document in collection "
            f"`{services.store.collection_name}` (expected {doc.get('chunk_count', '?')})."
        )
        for r in records[:5]:
            with st.expander(f"Record {r.chunk_id}"):
                st.markdown(f'<div class="vp-chunk">{html.escape(r.text)}</div>', unsafe_allow_html=True)
                st.json(r.metadata, expanded=False)
                st.caption(f"Vector: {vector_preview(r.embedding, 5)}")
        if len(records) > 5:
            st.caption("Showing 5 records. Open **🗄️ ChromaDB Explorer** to browse all.")
