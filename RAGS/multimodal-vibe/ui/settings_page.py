"""System Settings: configuration (never secrets), connection test, and safe re-indexing."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from backend.openai_client import OpenAIServiceError, call_with_retries
from config.settings import ConfigError, validate_chunk_settings
from ui.components import page_header
from ui.upload_page import chunk_setting_controls


def render(services) -> None:
    page_header("System Settings", "Models, chunking, storage and maintenance.", "⚙️")
    settings = services.settings

    st.subheader("Configuration")
    st.caption("Read from environment variables / `.env`. The API key itself is never displayed.")
    st.dataframe(
        pd.DataFrame(settings.public_summary().items(), columns=["Setting", "Value"]),
        hide_index=True,
        width="stretch",
    )
    for problem in settings.validate():
        st.warning(problem)

    if not settings.has_api_key:
        st.markdown(
            """
**Set up your OpenAI API key**
1. Create a key at <https://platform.openai.com/api-keys> and make sure API billing is set up
   (a ChatGPT subscription does **not** include API credits).
2. In the project folder: `cp .env.example .env` (Windows: `copy .env.example .env`).
3. Edit `.env` and set `OPENAI_API_KEY=sk-...`.
4. Restart: stop Streamlit (Ctrl+C) and run `streamlit run app.py`, or click **Reload services** below.
"""
        )

    st.subheader("Test the OpenAI connection")
    if st.button("Run connection test", disabled=not services.openai_ready):
        client = services.rag.client
        for label, model in (("Embedding model", settings.embedding_model), ("Chat model", settings.chat_model)):
            try:
                call_with_retries(lambda m=model: client.models.retrieve(m), model=model, max_attempts=2)
                st.success(f"{label} `{model}` is available to your API key.")
            except OpenAIServiceError as exc:
                st.error(f"{label} `{model}`: {exc}")

    st.subheader("Session settings")
    st.caption("Used for new indexing runs and questions in this browser session. Defaults come from `.env`.")
    chunk_size, chunk_overlap = chunk_setting_controls("settings")
    try:
        validate_chunk_settings(chunk_size, chunk_overlap)
    except ConfigError as exc:
        st.error(str(exc))
    st.session_state.top_k = st.slider("Default top K", 1, 20, int(st.session_state.top_k))

    st.subheader("Maintenance")
    stored_model = services.store.stored_embedding_model
    if stored_model and stored_model != settings.embedding_model and services.store.count():
        st.error(
            f"The collection holds vectors from `{stored_model}`, but `.env` now says `{settings.embedding_model}`. "
            "Questions and new uploads are blocked until you rebuild the index (or switch the model back)."
        )
    st.markdown(
        "**Rebuild index with current model and chunk settings.** Re-embeds every stored document into a new "
        "collection and swaps it in only if *all* documents succeed; otherwise the current index is kept."
    )
    confirm = st.checkbox("I understand this re-sends all document text to OpenAI for embedding")
    if st.button("Rebuild index", disabled=not (confirm and services.openai_ready)):
        with st.status("Rebuilding…", expanded=True) as box:
            reports = services.pipeline.rebuild_all(
                chunk_size, chunk_overlap, progress=lambda stage, message: box.update(label=message)
            )
            for r in reports:
                st.write(f"{'✅' if r.status == 'indexed' else '❌'} {r.filename}: {r.message}")
            ok = reports and all(r.status == "indexed" for r in reports)
            box.update(label="Rebuild complete" if ok else "Rebuild failed; the previous index was kept",
                       state="complete" if ok else "error")

    if st.button("Reload services (after editing .env)"):
        st.cache_resource.clear()
        st.rerun()

    st.subheader("Running this beyond a local demo")
    st.markdown(
        """
This app is a **single-user local demo**. Before letting several people use it you would need:
user authentication and per-user document collections; a server-side ChromaDB (or managed vector DB) with
backups; malware scanning of uploads; secrets in a secret manager instead of `.env`; request quotas and cost
controls on OpenAI usage; logging that excludes document content; and a review of what data may be sent to
OpenAI under your organisation's privacy rules.
"""
    )
