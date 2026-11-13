from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from backend.chunker import find_overlap, strip_header
from ui.common import Services, fmt_location, hero


def _highlight(text: str, overlap: str, at_start: bool) -> str:
    esc = html.escape
    if not overlap:
        return esc(text)
    body_start = len(text) - len(strip_header(text))
    head, body = text[:body_start], text[body_start:]
    if at_start and body.startswith(overlap):
        return esc(head) + f'<mark class="ov">{esc(overlap)}</mark>' + esc(body[len(overlap):])
    if not at_start and body.endswith(overlap):
        return esc(head) + esc(body[:-len(overlap)]) + f'<mark class="ov">{esc(overlap)}</mark>'
    return esc(text)


def render(svc: Services) -> None:
    hero("Chunk Explorer", "Inspect the chunks stored in ChromaDB and see how overlap works.")
    records = svc.store.get_records()
    if not records:
        st.info("No chunks yet. Index a document first.")
        _example()
        return
    md = lambda r: r["metadata"]
    f1, f2, f3, f4 = st.columns(4)
    file = f1.selectbox("File", ["All"] + sorted({md(r)["source_file"] for r in records}))
    dtype = f2.selectbox("Document type", ["All"] + sorted({md(r)["document_type"] for r in records}))
    pages = sorted({md(r)["page_number"] for r in records if "page_number" in md(r)})
    sheets = sorted({md(r)["sheet_name"] for r in records if "sheet_name" in md(r)})
    page = f3.selectbox("PDF page", ["All"] + pages)
    sheet = f4.selectbox("Excel worksheet", ["All"] + sheets)
    q = st.text_input("Search inside chunk text")

    def keep(r):
        m = md(r)
        return ((file == "All" or m["source_file"] == file) and (dtype == "All" or m["document_type"] == dtype)
                and (page == "All" or m.get("page_number") == page) and (sheet == "All" or m.get("sheet_name") == sheet)
                and (not q or q.lower() in r["document"].lower()))
    shown = [r for r in records if keep(r)]
    st.write(f"**{len(shown)}** of {len(records)} chunks match.")
    if not shown:
        return
    key = "nav_chunk_pos"
    pos = min(st.session_state.get(key, 0), len(shown) - 1)
    a, b, c = st.columns([1, 1, 6])
    if a.button("◀ Prev", disabled=pos == 0):
        pos -= 1
    if b.button("Next ▶", disabled=pos >= len(shown) - 1):
        pos += 1
    st.session_state[key] = pos
    c.progress((pos + 1) / len(shown), text=f"Chunk {pos + 1} of {len(shown)}")

    r = shown[pos]
    m = md(r)
    same_doc = sorted((x for x in records if md(x)["document_id"] == m["document_id"]), key=lambda x: md(x)["chunk_index"])
    i = next(j for j, x in enumerate(same_doc) if x["id"] == r["id"])
    prev = same_doc[i - 1] if i > 0 else None
    overlap = find_overlap(prev["document"], r["document"]) if prev else ""

    st.markdown(f"**`{r['id']}`** · chunk index **{m['chunk_index']}** · **{m['token_count']}** tokens · {m['source_file']} · {fmt_location(m)}")
    st.markdown(f'<div class="vp-chunk">{_highlight(r["document"], overlap, True)}</div>', unsafe_allow_html=True)
    if overlap:
        st.caption(f"🟨 Highlighted: {len(overlap)} characters repeated from the end of the previous chunk (`{prev['id']}`). This is the overlap.")
    elif prev:
        st.caption("No textual overlap with the previous chunk (they come from different pages / sheets / sections, or rows are kept whole).")
    else:
        st.caption("First chunk of this document: nothing before it to overlap with.")
    with st.expander("Metadata"):
        st.json(m)
    if prev and overlap:
        with st.expander("Previous chunk (overlap highlighted at its end)"):
            st.markdown(f'<div class="vp-chunk">{_highlight(prev["document"], overlap, False)}</div>', unsafe_allow_html=True)

    with st.expander("Compare with the original extracted content"):
        trace = svc.registry.load_trace(m["document_id"])
        if not trace:
            st.write("No trace stored.")
        else:
            src = [s for s in trace["cleaned_sections"]
                   if s.get("page_number") == m.get("page_number") and s.get("sheet_name") == m.get("sheet_name")
                   and s.get("section_title") == m.get("section_title")]
            if m.get("row_start") is not None:
                src = [s for s in src if m["row_start"] <= (s.get("row_number") or 0) <= m["row_end"]]
            st.caption(f"{len(src)} extracted section(s) feed this chunk:")
            st.code("\n\n".join(s["text"] for s in src)[:6000] or "—", language=None, wrap_lines=True)
    _example()


def _example() -> None:
    with st.expander("📘 Illustrative example of overlap (not your data)"):
        st.markdown("**Original text:** \"RAG retrieves relevant documents and supplies them as context to a language model.\"")
        st.markdown("**Chunk 1:** \"RAG retrieves relevant documents and supplies them\"")
        st.markdown("**Chunk 2:** \"supplies them as context to a language model.\"")
        st.caption("The words *supplies them* appear in both chunks - that is the overlap. This is only an illustration; real chunk "
                   "boundaries depend on your chunk size and overlap settings, and are measured in tokens.")
