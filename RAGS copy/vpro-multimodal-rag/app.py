"""VPro Skills EduTech — Smart Document RAG Assistant.   Run:  streamlit run app.py"""
import streamlit as st

from config.settings import APP_NAME

st.set_page_config(page_title="VPro Document RAG", page_icon="📚", layout="wide")

from ui import (chat_page, chunk_explorer, dashboard, database_explorer, embedding_explorer,  # noqa: E402
                indexing_page, retrieval_page, settings_page, upload_page)
from ui.common import get_services, inject_css  # noqa: E402

PAGES = {
    "🏠 Overview": dashboard.render,
    "📤 Upload Documents": upload_page.render,
    "🔄 Indexing Pipeline": indexing_page.render,
    "🧩 Chunk Explorer": chunk_explorer.render,
    "🧮 Embedding Explorer": embedding_explorer.render,
    "🗄️ ChromaDB Explorer": database_explorer.render,
    "💬 Ask Your Documents": chat_page.render,
    "🔎 Search and Retrieval": retrieval_page.render,
    "⚙️ System Settings": settings_page.render,
}


def main() -> None:
    inject_css()
    svc = get_services()
    with st.sidebar:
        st.markdown(f"### 📚 {APP_NAME}")
        page = st.radio("Navigation", list(PAGES), label_visibility="collapsed")
        st.divider()
        st.caption(f"Records in ChromaDB: **{svc.store.count()}**")
        st.caption(f"Embeddings: `{svc.settings.embedding_model}`  \nChat: `{svc.settings.chat_model}`")
    PAGES[page](svc)


main()
