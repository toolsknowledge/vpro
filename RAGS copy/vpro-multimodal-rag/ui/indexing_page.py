from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.common import Services, fmt_location, hero, pipeline_html


def _section_label(s: dict) -> str:
    return f"{fmt_location({**s, 'row_start': s.get('row_number'), 'row_end': s.get('row_number')})} · {len(s['text'])} chars"


def render(svc: Services) -> None:
    hero("Indexing Pipeline", "Upload → Extract → Clean → Chunk → Embed → Store in ChromaDB, with your real data.")
    docs = svc.registry.all()
    if not docs:
        st.markdown(pipeline_html(), unsafe_allow_html=True)
        st.info("No documents indexed yet. Upload one first; this page then shows every stage with real counts.")
        return
    names = {f"{d['filename']}  ({d['document_id'][:8]})": d for d in docs}
    doc = names[st.selectbox("Select a document", list(names))]
    trace = svc.registry.load_trace(doc["document_id"])
    in_db = len(svc.store.ids_for_document(doc["document_id"]))
    stg = (trace or {}).get("stages", {})

    counts = {"Upload": f"{doc['size_bytes'] / 1024:.1f} KB", "Extract": f"{stg.get('units', doc.get('units'))} {doc.get('unit_label', '')}",
              "Clean": f"{stg.get('cleaned_sections', doc.get('sections'))} sections", "Chunk": f"{doc['chunks']} chunks",
              "Embed": f"{doc['chunks']} × {doc.get('dimension')}d", "Store": f"{in_db} records"}
    st.markdown(pipeline_html(counts, failed="Store" if in_db != doc["chunks"] else None), unsafe_allow_html=True)
    if in_db != doc["chunks"]:
        st.error(f"Registry says {doc['chunks']} chunks but ChromaDB holds {in_db}. Re-index this document.")

    table = pd.DataFrame([
        ("Upload", "Validate extension, size & signature; SHA-256 hash identifies the version", "file bytes", "validated file + hash", "✅ done", 1),
        ("Extract", f"Read text ({', '.join({s['extraction_method'] for s in (trace or {}).get('raw_sections', [])}) or 'n/a'})", "file", "sections with metadata", "✅ done", stg.get("extracted_sections")),
        ("Clean", "Normalise whitespace / line breaks; drop empty text", "raw sections", "cleaned sections", "✅ done", stg.get("cleaned_sections")),
        ("Chunk", f"Token windows: {doc.get('chunk_size')} tokens, {doc.get('chunk_overlap')} overlap", "cleaned sections", "chunks with IDs", "✅ done", doc["chunks"]),
        ("Embed", f"OpenAI `{doc.get('embedding_model')}`", "chunk text", f"{doc.get('dimension')}-dim vectors", "✅ done", doc["chunks"]),
        ("Store", "Upsert text + vector + metadata in ChromaDB", "chunks + vectors", "persistent records", "✅ done" if in_db == doc["chunks"] else "⚠️ mismatch", in_db)],
        columns=["Stage", "Description", "Input", "Output", "Status", "Records"])
    st.dataframe(table, width="stretch", hide_index=True)

    if not trace:
        st.warning("No processing trace stored for this document (it may have been indexed by an older version).")
        return
    t1, t2, t3, t4, t5 = st.tabs(["1 · Extracted", "2 · Cleaned", "3 · Chunks", "4 · Embeddings", "5 · ChromaDB records"])
    raw, cleaned = trace["raw_sections"], trace["cleaned_sections"]
    with t1:
        st.caption(f"{len(raw)} section(s) extracted with `{raw[0]['extraction_method']}`. Each keeps its page / sheet / row / section metadata.")
        for s in raw[:50]:
            with st.expander(_section_label(s)):
                st.code(s["text"], language=None, wrap_lines=True)
        if len(raw) > 50:
            st.caption(f"Showing the first 50 of {len(raw)} sections.")
    with t2:
        st.caption("Cleaning changes only whitespace/line breaks. Differences are listed below.")
        raw_chars, cl_chars = sum(len(s["text"]) for s in raw), sum(len(s["text"]) for s in cleaned)
        st.write(f"Characters before: **{raw_chars}** · after: **{cl_chars}** · removed: **{raw_chars - cl_chars}** (whitespace only)")
        idx = st.number_input("Section number", 1, max(len(cleaned), 1), 1) - 1
        if cleaned:
            a, b = st.columns(2)
            a.markdown("**Extracted**"); a.code(raw[min(idx, len(raw) - 1)]["text"][:3000], language=None, wrap_lines=True)
            b.markdown("**Cleaned**"); b.code(cleaned[idx]["text"][:3000], language=None, wrap_lines=True)
    chunks = svc.store.get_records(where={"document_id": doc["document_id"]})
    chunks.sort(key=lambda r: r["metadata"].get("chunk_index", 0))
    with t3:
        st.write(f"**{len(chunks)}** chunks · tokenizer: `{trace['tokenizer']}` · target {trace['chunk_size']} tokens, overlap {trace['chunk_overlap']}.")
        st.dataframe(pd.DataFrame([{"Index": c["metadata"].get("chunk_index"), "Chunk ID": c["id"],
                                    "Location": fmt_location(c["metadata"]), "Tokens": c["metadata"].get("token_count"),
                                    "Preview": c["document"][:100].replace("\n", " ")} for c in chunks]),
                     width="stretch", hide_index=True)
        st.caption("Use **Chunk Explorer** to read chunks and see overlap highlighted.")
    with t4:
        if svc.store.compatibility_problem():
            st.error(svc.store.compatibility_problem())
        elif chunks:
            sample = svc.store.get_records(where={"chunk_id": chunks[0]["id"]}, include_embeddings=True)[0]
            st.write(f"Model **{trace['embedding_model']}** · **{len(sample['embedding'])}** dimensions · {len(chunks)} vectors")
            st.markdown("**Chunk text**"); st.code(sample["document"], language=None, wrap_lines=True)
            st.markdown("**First 10 vector values**"); st.code(str([round(x, 5) for x in sample["embedding"][:10]]))
            st.caption("See **Embedding Explorer** for the full vector and a 2-D map.")
    with t5:
        st.write(f"**{in_db}** record(s) in collection `{svc.store.collection_name}` for this document.")
        st.dataframe(pd.DataFrame([{"ID": c["id"], "Metadata": str(c["metadata"])} for c in chunks]), width="stretch", hide_index=True)
