"""Chunk Explorer: browse, filter and compare the chunks created during indexing."""

from __future__ import annotations

import html

import streamlit as st

from backend.chunker import find_overlap
from backend.retrieval import format_citation
from ui.components import page_header


def _highlight(text: str, prefix: str, suffix: str) -> str:
    """HTML for a chunk: overlap with the previous chunk in yellow, with the next chunk in blue."""
    text = text.strip()
    start = len(prefix) if prefix and text.startswith(prefix) else 0
    end = len(text) - len(suffix) if suffix and text.endswith(suffix) and len(text) - len(suffix) >= start else len(text)
    body = f'<mark class="prev">{html.escape(text[:start])}</mark>' if start else ""
    body += html.escape(text[start:end])
    if end < len(text):
        body += f'<mark class="next">{html.escape(text[end:])}</mark>'
    return f'<div class="vp-chunk">{body}</div>'


def _illustration() -> None:
    with st.expander("💡 What is chunk overlap? (illustrative example)"):
        st.markdown(
            "**Original text:** “RAG retrieves relevant documents and supplies them as context to a language model.”\n\n"
            "**Chunk 1:** “RAG retrieves relevant documents and <mark>supplies them</mark>”\n\n"
            "**Chunk 2:** “<mark>supplies them</mark> as context to a language model.”\n\n"
            "The highlighted words appear in both chunks. That overlap keeps an idea that crosses a boundary "
            "readable in at least one chunk. *This is only an illustration: real boundaries depend on the "
            "configured chunk size, overlap and the token-aware chunking strategy.*",
            unsafe_allow_html=True,
        )


def render(services) -> None:
    page_header("Chunk Explorer", "Inspect every chunk, its metadata, token count and overlap.", "🧩")
    _illustration()

    traces = []
    for doc in services.registry.list_documents():
        trace = services.registry.load_trace(doc["document_id"])
        if trace:
            traces.append((doc, trace))
    if not traces:
        st.info("No chunks yet. Index a document on **📤 Upload Documents** first.")
        return

    all_chunks = [c for _, trace in traces for c in trace["chunks"]]

    # ---------------------------------------------------------------- filters
    col1, col2, col3 = st.columns(3)
    files = sorted({c["source_file"] for c in all_chunks})
    selected_files = col1.multiselect("File", files, default=files)
    types = sorted({c["document_type"] for c in all_chunks})
    selected_types = col2.multiselect("Document type", types, default=types)
    search = col3.text_input("Search chunk text", placeholder="e.g. duration")

    col4, col5 = st.columns(2)
    pages = sorted({c["page_number"] for c in all_chunks if c.get("page_number") is not None})
    selected_pages = col4.multiselect("PDF page", pages) if pages else []
    sheets = sorted({c["sheet_name"] for c in all_chunks if c.get("sheet_name")})
    selected_sheets = col5.multiselect("Excel worksheet", sheets) if sheets else []

    def keep(c: dict) -> bool:
        if c["source_file"] not in selected_files or c["document_type"] not in selected_types:
            return False
        if selected_pages and c.get("page_number") not in selected_pages:
            return False
        if selected_sheets and c.get("sheet_name") not in selected_sheets:
            return False
        return not search or search.lower() in c["text"].lower()

    filtered = [c for c in all_chunks if keep(c)]
    st.caption(f"{len(filtered)} of {len(all_chunks)} chunk(s) match.")
    if not filtered:
        return

    # ------------------------------------------------------------- navigation
    st.session_state.setdefault("chunk_pos", 0)
    st.session_state.chunk_pos = min(st.session_state.chunk_pos, len(filtered) - 1)
    nav1, nav2, nav3 = st.columns([1, 3, 1])
    if nav1.button("⬅️ Previous", disabled=st.session_state.chunk_pos == 0, width="stretch"):
        st.session_state.chunk_pos -= 1
        st.rerun()
    if nav3.button("Next ➡️", disabled=st.session_state.chunk_pos >= len(filtered) - 1, width="stretch"):
        st.session_state.chunk_pos += 1
        st.rerun()
    if len(filtered) > 1:
        position = nav2.slider("Chunk", 1, len(filtered), st.session_state.chunk_pos + 1, label_visibility="collapsed")
        st.session_state.chunk_pos = position - 1
    chunk = filtered[st.session_state.chunk_pos]

    # Neighbours come from the same document, not from the filtered list.
    doc_chunks = next(trace["chunks"] for _, trace in traces if trace["document_id"] == chunk["document_id"])
    i = chunk["chunk_index"]
    previous = doc_chunks[i - 1] if i > 0 else None
    following = doc_chunks[i + 1] if i + 1 < len(doc_chunks) else None
    overlap_prev = find_overlap(previous["text"], chunk["text"]) if previous else ""
    overlap_next = find_overlap(chunk["text"], following["text"]) if following else ""

    # ----------------------------------------------------------------- detail
    st.markdown(f"#### Chunk {i} of `{chunk['source_file']}`")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Chunk index", i)
    m2.metric("Tokens", chunk["token_count"])
    m3.metric("Characters", len(chunk["text"]))
    m4.metric("Chunks in document", len(doc_chunks))
    st.caption(f"Chunk ID `{chunk['chunk_id']}` · location: {format_citation(chunk)}")

    st.markdown(_highlight(chunk["text"], overlap_prev, overlap_next), unsafe_allow_html=True)
    legend = []
    if overlap_prev:
        legend.append(f'<mark class="prev">yellow</mark> = shared with chunk {i - 1} ({len(overlap_prev)} chars)')
    if overlap_next:
        legend.append(f'<mark class="next">blue</mark> = shared with chunk {i + 1} ({len(overlap_next)} chars)')
    if not legend:
        legend.append("No overlap with neighbours. Chunks from different pages, sections or worksheets never overlap.")
    st.markdown(f'<span style="font-size:.8rem">{" · ".join(legend)}</span>', unsafe_allow_html=True)

    with st.expander("Metadata"):
        st.json({k: v for k, v in chunk.items() if k != "text"})

    with st.expander("Compare with the original extracted content"):
        trace = next(t for _, t in traces if t["document_id"] == chunk["document_id"])
        sources = [
            s for s in trace["clean_sections"]
            if s.get("page_number") == chunk.get("page_number")
            and s.get("sheet_name") == chunk.get("sheet_name")
            and s.get("section_title") == chunk.get("section_title")
            and (chunk.get("row_start") is None or chunk["row_start"] <= (s.get("row_number") or 0) <= chunk["row_end"])
        ]
        original = "\n".join(s["text"] for s in sources) or "(original section not found)"
        col_a, col_b = st.columns(2)
        col_a.text_area("Original (cleaned) section text", original, height=260, disabled=True)
        col_b.text_area("This chunk", chunk["text"], height=260, disabled=True)
