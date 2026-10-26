"""VPro Skills EduTech — Smart Document RAG Assistant.

Start with:  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from backend.services import AppServices, build_services
from backend.vector_store import VectorStoreError
from config.settings import ConfigError, load_settings
from ui import (
    chat_page,
    chunk_explorer,
    dashboard,
    database_explorer,
    embedding_explorer,
    indexing_page,
    retrieval_page,
    settings_page,
    upload_page,
)
from ui.components import inject_css

APP_TITLE = "VPro Skills EduTech — Smart Document RAG Assistant"

PAGES = {
    "🏠 Overview": dashboard.render,
    "📤 Upload Documents": upload_page.render,
    "🛠️ Indexing Pipeline": indexing_page.render,
    "🧩 Chunk Explorer": chunk_explorer.render,
    "🔢 Embedding Explorer": embedding_explorer.render,
    "🗄️ ChromaDB Explorer": database_explorer.render,
    "💬 Ask Your Documents": chat_page.render,
    "🔎 Search and Retrieval": retrieval_page.render,
    "⚙️ System Settings": settings_page.render,
}


@st.cache_resource(show_spinner="Opening ChromaDB and connecting services…")
def get_services() -> AppServices:
    # Cached for the whole server process; "Reload services" in System Settings clears it.
    return build_services(load_settings())


def init_session_defaults(services: AppServices) -> None:
    s = services.settings
    defaults = {
        "chunk_size": s.chunk_size,
        "chunk_overlap": s.chunk_overlap,
        "top_k": s.top_k,
        "use_threshold": False,
        "min_similarity": 0.30,
        "chat_history": [],
        "last_index_reports": [],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def main() -> None:
    st.set_page_config(page_title="VPro Smart Document RAG", page_icon="📚", layout="wide")
    inject_css()

    try:
        services = get_services()
    except (ConfigError, VectorStoreError) as exc:
        st.title(APP_TITLE)
        st.error(f"The app could not start: {exc}")
        st.info("Fix the value in your `.env` file and restart with `streamlit run app.py`.")
        st.stop()

    init_session_defaults(services)

    with st.sidebar:
        st.markdown("### 📚 VPro Skills EduTech")
        st.caption("Smart Document RAG Assistant")
        page = st.radio("Navigate", list(PAGES), label_visibility="collapsed")
        st.divider()
        if services.openai_ready:
            st.success("OpenAI configured", icon="✅")
        else:
            st.warning("OpenAI API key missing", icon="⚠️")
        st.caption(f"Records in ChromaDB: **{services.store.count():,}**")
        st.caption(f"Embedding model: `{services.settings.embedding_model}`")
        st.caption(f"Chat model: `{services.settings.chat_model}`")
        st.caption(f"Chunk: {st.session_state.chunk_size} tok / overlap {st.session_state.chunk_overlap}")

    problems = [p for p in services.settings.validate() if "OPENAI_API_KEY" not in p]
    for problem in problems:
        st.warning(f"Configuration: {problem}")

    PAGES[page](services)


if __name__ == "__main__":
    main()
