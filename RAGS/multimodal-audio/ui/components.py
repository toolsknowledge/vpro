"""Reusable UI pieces: theme CSS, headers, metric cards, pipeline diagram, citations."""

from __future__ import annotations

import html
from datetime import datetime

import streamlit as st

from backend.indexing_pipeline import STAGES

CSS = """
<style>
.block-container {padding-top: 2rem; max-width: 1250px;}
.vp-header {background: linear-gradient(120deg, #4F46E5 0%, #7C3AED 100%); color: #fff;
  padding: 1.1rem 1.4rem; border-radius: 14px; margin-bottom: 1.2rem;}
.vp-header h1 {font-size: 1.55rem; margin: 0; color: #fff; padding: 0;}
.vp-header p {margin: .25rem 0 0; opacity: .9; font-size: .95rem;}
.vp-card {background: #fff; border: 1px solid #E5E7EB; border-radius: 12px; padding: .9rem 1rem;
  box-shadow: 0 1px 2px rgba(16,24,40,.04); height: 100%;}
.vp-card .label {color: #6B7280; font-size: .8rem; text-transform: uppercase; letter-spacing: .04em;}
.vp-card .value {font-size: 1.6rem; font-weight: 700; color: #111827; margin-top: .15rem;}
.vp-card .hint {color: #9CA3AF; font-size: .78rem;}
.vp-pipeline {display: flex; flex-wrap: wrap; gap: .4rem; align-items: stretch; margin: .4rem 0 1rem;}
.vp-stage {flex: 1 1 140px; background: #fff; border: 2px solid #E5E7EB; border-radius: 12px;
  padding: .6rem .7rem; min-width: 130px;}
.vp-stage .name {font-weight: 700; font-size: .95rem;}
.vp-stage .desc {font-size: .74rem; color: #6B7280; margin: .2rem 0;}
.vp-stage .count {font-size: 1.15rem; font-weight: 700; color: #4F46E5;}
.vp-stage .io {font-size: .72rem; color: #374151;}
.vp-arrow {align-self: center; color: #9CA3AF; font-size: 1.3rem;}
.vp-stage.done {border-color: #10B981; background: #F0FDF8;}
.vp-stage.failed {border-color: #EF4444; background: #FEF2F2;}
.vp-stage.skipped {border-color: #D1D5DB; background: #F9FAFB; opacity: .75;}
.vp-stage.pending {border-style: dashed;}
.vp-badge {display: inline-block; padding: .1rem .5rem; border-radius: 999px; font-size: .75rem; font-weight: 600;}
.vp-badge.ok {background: #D1FAE5; color: #065F46;}
.vp-badge.warn {background: #FEF3C7; color: #92400E;}
.vp-badge.err {background: #FEE2E2; color: #991B1B;}
.vp-badge.info {background: #E0E7FF; color: #3730A3;}
.vp-chunk {background: #fff; border: 1px solid #E5E7EB; border-radius: 10px; padding: .8rem 1rem;
  white-space: pre-wrap; font-size: .9rem; line-height: 1.5;}
.vp-chunk mark.prev {background: #FDE68A;}
.vp-chunk mark.next {background: #BFDBFE;}
</style>
"""

STATUS_ICONS = {"done": "✅", "failed": "❌", "skipped": "⏭️", "pending": "⏳", "running": "🔄"}


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str, icon: str = "") -> None:
    st.markdown(
        f'<div class="vp-header"><h1>{icon} {html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',
        unsafe_allow_html=True,
    )


def metric_cards(items: list[tuple[str, str, str]]) -> None:
    """items = [(label, value, hint), ...]"""
    columns = st.columns(len(items))
    for column, (label, value, hint) in zip(columns, items):
        column.markdown(
            f'<div class="vp-card"><div class="label">{html.escape(label)}</div>'
            f'<div class="value">{html.escape(str(value))}</div>'
            f'<div class="hint">{html.escape(hint)}</div></div>',
            unsafe_allow_html=True,
        )


def badge(text: str, kind: str = "info") -> str:
    return f'<span class="vp-badge {kind}">{html.escape(text)}</span>'


def status_badge(status: str) -> str:
    kind = {"indexed": "ok", "duplicate": "info", "failed": "err"}.get(status, "warn")
    return badge(status, kind)


def pipeline_diagram(stages: list[dict] | None = None) -> None:
    """Render Upload → Extract → Clean → Chunk → Embed → Store.

    `stages` are StageResult dicts from a real indexing run. Without them, the
    generic flow is shown with no counts.
    """
    by_key = {s["key"]: s for s in stages or []}
    parts = []
    for i, (key, name, description) in enumerate(STAGES):
        stage = by_key.get(key, {})
        status = stage.get("status", "pending")
        count = stage.get("count")
        count_html = f'<div class="count">{count:,}</div>' if isinstance(count, int) else ""
        io_html = ""
        if stage.get("input") or stage.get("output"):
            io_html = (
                f'<div class="io"><b>In:</b> {html.escape(stage.get("input", ""))}</div>'
                f'<div class="io"><b>Out:</b> {html.escape(stage.get("output", ""))}</div>'
            )
        if stage.get("message"):
            io_html += f'<div class="io"><i>{html.escape(stage["message"])}</i></div>'
        parts.append(
            f'<div class="vp-stage {status}"><div class="name">{STATUS_ICONS.get(status, "")} {i + 1}. {name}</div>'
            f'<div class="desc">{html.escape(description)}</div>{count_html}{io_html}</div>'
        )
        if i < len(STAGES) - 1:
            parts.append('<div class="vp-arrow">➜</div>')
    st.markdown(f'<div class="vp-pipeline">{"".join(parts)}</div>', unsafe_allow_html=True)


def format_time(iso_value: str | None) -> str:
    if not iso_value:
        return "never"
    try:
        return datetime.fromisoformat(iso_value).astimezone().strftime("%d %b %Y, %H:%M")
    except ValueError:
        return iso_value


def vector_preview(vector: list[float] | None, n: int = 10) -> str:
    if not vector:
        return "(no vector)"
    shown = ", ".join(f"{v:+.4f}" for v in vector[:n])
    return f"[{shown}{', …' if len(vector) > n else ''}]"


def show_chunk_card(chunk, label: str | None = None, expanded: bool = False) -> None:
    """Expandable view of a RetrievedChunk with its distance, similarity and metadata."""
    sim = f"similarity {chunk.similarity:.3f} · " if chunk.similarity is not None else ""
    title = f"{label + ' · ' if label else ''}#{chunk.rank} · {chunk.citation} · {sim}distance {chunk.distance:.4f}"
    with st.expander(title, expanded=expanded):
        st.markdown(f'<div class="vp-chunk">{html.escape(chunk.text)}</div>', unsafe_allow_html=True)
        st.caption(f"Chunk ID: `{chunk.chunk_id}` · keyword overlap with question: {chunk.keyword_overlap:.0%}")
        st.json(chunk.metadata, expanded=False)


def require_openai(services) -> bool:
    """Show setup help and return False if OpenAI is not configured."""
    if services.openai_ready:
        return True
    st.error(f"OpenAI is not available: {services.openai_error or 'not configured.'}")
    st.info(
        "Setup: copy `.env.example` to `.env`, set `OPENAI_API_KEY=sk-...`, then restart "
        "`streamlit run app.py`. API usage is billed separately from ChatGPT subscriptions."
    )
    return False


def privacy_note() -> None:
    st.caption(
        "🔒 Privacy: document text is sent to OpenAI to create embeddings, and the retrieved chunks plus "
        "your question are sent to OpenAI to generate answers. Do not upload confidential documents to this demo."
    )
