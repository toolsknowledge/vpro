"""Shared UI helpers: cached services, runtime settings, styling, error display."""
from __future__ import annotations

import html
from dataclasses import dataclass

import streamlit as st

from backend.document_registry import DocumentRegistry
from backend.embeddings import OpenAIEmbedder, get_client
from backend.errors import AppError, VectorStoreError
from backend.vector_store import VectorStore
from config.settings import Settings

STAGES = [
    ("Upload", "📤", "Validate type, size and content; hash the file"),
    ("Extract", "🔍", "Read text from the file with metadata"),
    ("Clean", "🧹", "Normalise whitespace and line breaks"),
    ("Chunk", "✂️", "Split into overlapping token-sized pieces"),
    ("Embed", "🧮", "Turn each chunk into a vector (OpenAI)"),
    ("Store", "🗄️", "Save text + vector + metadata in ChromaDB"),
]

CSS = """
<style>
.block-container {padding-top: 1.6rem;}
.vp-hero {background: linear-gradient(120deg,#4f46e5,#7c3aed); color:#fff; padding: 1.1rem 1.4rem; border-radius: 14px; margin-bottom: 1rem;}
.vp-hero h2 {margin:0; color:#fff; font-size:1.5rem;} .vp-hero p {margin:.25rem 0 0; opacity:.9;}
.vp-card {background: var(--secondary-background-color); border-radius: 12px; padding: .9rem 1rem; border:1px solid rgba(120,120,160,.2);}
.vp-card .l {font-size:.78rem; opacity:.7; text-transform:uppercase; letter-spacing:.04em;} .vp-card .v {font-size:1.7rem; font-weight:700;}
.vp-flow {display:flex; flex-wrap:wrap; gap:.4rem; align-items:stretch; margin:.5rem 0 1rem;}
.vp-stage {flex:1 1 120px; background: var(--secondary-background-color); border:1px solid rgba(120,120,160,.25); border-radius:12px; padding:.6rem .7rem; text-align:center;}
.vp-stage.done {border-color:#16a34a; box-shadow: inset 0 0 0 1px #16a34a33;} .vp-stage.fail {border-color:#dc2626;}
.vp-stage .n {font-weight:700;} .vp-stage .c {font-size:.78rem; opacity:.75;} .vp-stage .k {font-size:.95rem; color:#4f46e5; font-weight:600;}
.vp-arrow {align-self:center; opacity:.5; font-size:1.2rem;}
mark.ov {background:#fde68a; color:#111; padding:0 2px; border-radius:3px;}
.vp-chunk {white-space:pre-wrap; background: var(--secondary-background-color); border-radius:10px; padding:.8rem 1rem; border:1px solid rgba(120,120,160,.2);}
</style>
"""


@dataclass
class Services:
    settings: Settings
    registry: DocumentRegistry
    store: VectorStore


@st.cache_resource(show_spinner=False)
def _build_services() -> Services:
    settings = Settings.from_env()
    settings.ensure_dirs()
    registry = DocumentRegistry(settings.registry_path, settings.processed_dir, settings.uploads_dir)
    store = VectorStore(settings.chroma_dir, settings.collection_name, settings.embedding_model)
    return Services(settings, registry, store)


def get_services() -> Services:
    try:
        return _build_services()
    except (AppError, Exception) as exc:
        st.error(f"Could not start the app: {exc}")
        st.stop()


def get_embedder(svc: Services) -> OpenAIEmbedder:
    return OpenAIEmbedder(get_client(svc.settings), svc.settings.embedding_model)


def cfg() -> dict:
    """Runtime (per-session) tuning values, initialised from .env."""
    if "cfg" not in st.session_state:
        s = get_services().settings
        st.session_state.cfg = {"chunk_size": s.chunk_size, "chunk_overlap": s.chunk_overlap,
                                "top_k": s.top_k, "threshold": None}
    return st.session_state.cfg


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="vp-hero"><h2>{html.escape(title)}</h2><p>{html.escape(subtitle)}</p></div>',
                unsafe_allow_html=True)


def card(label: str, value) -> str:
    return f'<div class="vp-card"><div class="l">{html.escape(label)}</div><div class="v">{html.escape(str(value))}</div></div>'


def cards(items: list[tuple[str, object]]) -> None:
    for col, (label, value) in zip(st.columns(len(items)), items):
        col.markdown(card(label, value), unsafe_allow_html=True)


def pipeline_html(counts: dict[str, str] | None = None, failed: str | None = None) -> str:
    counts = counts or {}
    parts = []
    for i, (name, icon, desc) in enumerate(STAGES):
        cls = "fail" if failed == name else ("done" if name in counts else "")
        k = f'<div class="k">{html.escape(counts[name])}</div>' if name in counts else ""
        parts.append(f'<div class="vp-stage {cls}"><div>{icon}</div><div class="n">{name}</div>{k}'
                     f'<div class="c">{html.escape(desc)}</div></div>')
        if i < len(STAGES) - 1:
            parts.append('<div class="vp-arrow">➜</div>')
    return f'<div class="vp-flow">{"".join(parts)}</div>'


def show_error(exc: Exception) -> None:
    if isinstance(exc, AppError):
        st.error(str(exc))
    else:
        st.error(f"Something unexpected happened: {type(exc).__name__}: {exc}")
        with st.expander("Technical details"):
            st.exception(exc)


def setup_banner(svc: Services) -> bool:
    """Show setup guidance when the API key is missing. Returns True if OpenAI can be used."""
    if svc.settings.has_api_key:
        return True
    st.warning("**OpenAI API key not configured.** Browsing existing data works, but indexing and asking questions need it.\n\n"
               "1. Copy `.env.example` to `.env`  2. Put your key in `OPENAI_API_KEY=`  3. Restart `streamlit run app.py`.\n\n"
               "API billing is separate from a ChatGPT plan - add credits at platform.openai.com → Billing.")
    return False


def store_ready(svc: Services) -> bool:
    problem = svc.store.compatibility_problem()
    if problem:
        st.error(problem)
        return False
    return True


def invalidate_state() -> None:
    """Clear session caches that may refer to deleted/changed documents."""
    for k in list(st.session_state.keys()):
        if k.startswith(("nav_", "last_retrieval", "full_vec")):
            del st.session_state[k]


def fmt_location(md: dict) -> str:
    bits = []
    if md.get("page_number") is not None:
        bits.append(f"page {md['page_number']}")
    if md.get("sheet_name"):
        bits.append(f"sheet {md['sheet_name']}")
    if md.get("row_start") is not None:
        bits.append(f"row {md['row_start']}" if md.get("row_start") == md.get("row_end") else f"rows {md['row_start']}–{md.get('row_end')}")
    if md.get("section_title"):
        bits.append(f"section {md['section_title']}")
    return ", ".join(bits) or "—"
