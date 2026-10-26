"""VPro Skills EduTech — Multimodal Document, Audio & Video RAG Assistant.

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
    media_chat_page,
    media_dashboard,
    media_diagnostics,
    media_upload_page,
    retrieval_page,
    settings_page,
    transcript_explorer,
    upload_page,
    video_frame_explorer,
)
from ui.components import inject_css

APP_TITLE = "VPro Skills EduTech — Audio & Video RAG Assistant"

# Grouped navigation: the original document RAG pages are unchanged; the media pages are new.
PAGE_GROUPS = {
    "Audio & Video RAG": {
        "📊 Media Dashboard": media_dashboard.render,
        "🎙️ Audio and Video Upload": media_upload_page.render,
        "📝 Transcript Explorer": transcript_explorer.render,
        "🖼️ Video Frame Explorer": video_frame_explorer.render,
        "🎬 Audio and Video Chat": media_chat_page.render,
        "🔬 Retrieval Diagnostics": media_diagnostics.render,
    },
    "Document RAG": {
        "🏠 Overview": dashboard.render,
        "📤 Upload Documents": upload_page.render,
        "🛠️ Indexing Pipeline": indexing_page.render,
        "🧩 Chunk Explorer": chunk_explorer.render,
        "🔢 Embedding Explorer": embedding_explorer.render,
        "🗄️ ChromaDB Explorer": database_explorer.render,
        "💬 Ask Your Documents": chat_page.render,
        "🔎 Search and Retrieval": retrieval_page.render,
    },
    "System": {
        "⚙️ System Settings": settings_page.render,
    },
}
PAGES = {name: render for group in PAGE_GROUPS.values() for name, render in group.items()}


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
        "media_top_k": s.media_top_k,
        "media_scope": "all",
        "media_chat_history": [],
        "last_media_reports": [],
        "media_player": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def main() -> None:
    st.set_page_config(page_title="VPro Audio & Video RAG", page_icon="🎬", layout="wide")
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
        st.markdown("### 🎬 VPro Skills EduTech")
        st.caption("Audio, Video & Document RAG Assistant")
        group = st.radio("Section", list(PAGE_GROUPS), horizontal=False, key="nav_group")
        page = st.radio("Navigate", list(PAGE_GROUPS[group]), label_visibility="collapsed", key=f"nav_{group}")
        st.divider()
        if services.openai_ready:
            st.success("OpenAI configured", icon="✅")
        else:
            st.warning("OpenAI API key missing", icon="⚠️")
        ffmpeg_ok, _ = services.ffmpeg.available()
        if not ffmpeg_ok:
            st.warning("FFmpeg not installed", icon="🎞️")
        media_counts = services.media_stores.counts()
        st.caption(f"Document chunks: **{services.store.count():,}**")
        st.caption(f"Transcript chunks: **{media_counts['audio'] + media_counts['video_transcript']:,}** · "
                   f"frame descriptions: **{media_counts['video_frame']:,}**")
        st.caption(f"Embedding model: `{services.settings.embedding_model}`")
        st.caption(f"Chat model: `{services.settings.chat_model}`")
        st.caption(f"Transcription: `{services.settings.transcription_model}` · vision: `{services.settings.vision_model}`")
        st.caption(f"Chunk: {st.session_state.chunk_size} tok / overlap {st.session_state.chunk_overlap}")

    problems = [p for p in services.settings.validate() if "OPENAI_API_KEY" not in p]
    for problem in problems:
        st.warning(f"Configuration: {problem}")

    PAGES[page](services)


if __name__ == "__main__":
    main()
