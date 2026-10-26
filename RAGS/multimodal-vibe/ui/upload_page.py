"""Upload Documents: drag-and-drop files, validate them, and run the indexing pipeline."""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from backend.document_loader import DocumentLoadError, validate_upload
from config.settings import ConfigError, SUPPORTED_EXTENSIONS, validate_chunk_settings
from ui.components import page_header, pipeline_diagram, privacy_note, require_openai, status_badge


def chunk_setting_controls(key_prefix: str = "upload") -> tuple[int, int]:
    col1, col2 = st.columns(2)
    size = col1.number_input(
        "Chunk size (tokens)", min_value=50, max_value=8000, step=50,
        value=int(st.session_state.chunk_size), key=f"{key_prefix}_chunk_size",
        help="Maximum tokens per chunk. ~800 tokens ≈ 600 words.",
    )
    overlap = col2.number_input(
        "Chunk overlap (tokens)", min_value=0, max_value=3999, step=10,
        value=int(st.session_state.chunk_overlap), key=f"{key_prefix}_chunk_overlap",
        help="Tokens repeated between neighbouring chunks so ideas are not cut in half.",
    )
    st.session_state.chunk_size, st.session_state.chunk_overlap = int(size), int(overlap)
    return int(size), int(overlap)


def render_report_details(reports: list[dict]) -> None:
    """Indexing summary table plus per-file stage details."""
    if not reports:
        return
    indexed = [r for r in reports if r["status"] == "indexed"]
    st.subheader("Indexing summary")
    cols = st.columns(6)
    cols[0].metric("Files", len(reports))
    cols[1].metric("Indexed", len(indexed))
    cols[2].metric("Duplicates", sum(r["status"] == "duplicate" for r in reports))
    cols[3].metric("Failed", sum(r["status"] == "failed" for r in reports))
    cols[4].metric("Chunks embedded", sum(r["embeddings"] for r in indexed))
    cols[5].metric("Time (s)", f"{sum(r['seconds'] for r in reports):.1f}")

    dims = sorted({r["dimension"] for r in indexed if r["dimension"]})
    if dims:
        st.caption(f"Vector dimension(s): {', '.join(map(str, dims))} · records stored this run: "
                   f"{sum(r['stored_records'] for r in indexed):,}")

    table = pd.DataFrame(
        [
            {
                "File": r["filename"],
                "Status": r["status"],
                "Units": ", ".join(f"{v} {k}" for k, v in r["units"].items()),
                "Sections": r["sections"],
                "Chunks": r["chunks"],
                "Embeddings": r["embeddings"],
                "Dimension": r["dimension"] or "",
                "Stored records": r["stored_records"],
                "Seconds": round(r["seconds"], 2),
                "Message": r["message"],
            }
            for r in reports
        ]
    )
    st.dataframe(table, hide_index=True, width="stretch")

    for r in reports:
        icon = {"indexed": "✅", "duplicate": "🔁", "failed": "❌"}.get(r["status"], "•")
        with st.expander(f"{icon} {r['filename']} — {r['status']}"):
            st.markdown(status_badge(r["status"]) + " " + html.escape(r["message"]), unsafe_allow_html=True)
            pipeline_diagram(r["stages"])
            for warning in r["warnings"]:
                st.warning(warning)


def render(services) -> None:
    page_header("Upload Documents", "Add PDF, Excel, Word or TXT files to the knowledge base.", "📤")
    openai_ok = require_openai(services)

    st.markdown(
        "**Supported formats:** `.pdf` (text layer, page by page) · `.xlsx` / `.xls` (every worksheet, row by row) · "
        "`.docx` (paragraphs, headings and tables) · `.txt` (UTF-8, split at headings). "
        f"Maximum size per file: **{services.settings.max_upload_size_mb} MB**. "
        "Scanned PDFs and images are not supported (no OCR)."
    )

    files = st.file_uploader(
        "Drag and drop files here",
        type=[ext.lstrip(".") for ext in SUPPORTED_EXTENSIONS],
        accept_multiple_files=True,
    )

    with st.expander("Chunking settings", expanded=False):
        chunk_size, chunk_overlap = chunk_setting_controls()
        try:
            validate_chunk_settings(chunk_size, chunk_overlap)
            settings_ok = True
        except ConfigError as exc:
            st.error(str(exc))
            settings_ok = False

    force = st.checkbox("Re-index duplicates (process files again even if the same content is already indexed)")

    valid_files = []
    for file in files or []:
        try:
            validate_upload(file.name, file.size, services.settings.max_upload_bytes)
            valid_files.append(file)
        except DocumentLoadError as exc:
            st.error(str(exc))

    if valid_files:
        st.write(f"Ready to index **{len(valid_files)}** file(s): " + ", ".join(f"`{f.name}`" for f in valid_files))

    if st.button("🚀 Index documents", type="primary", disabled=not (valid_files and settings_ok and openai_ok)):
        reports = []
        progress = st.progress(0.0, text="Starting…")
        with st.status("Running the indexing pipeline…", expanded=True) as status_box:
            for number, file in enumerate(valid_files):
                def on_progress(stage: str, message: str, number=number):
                    progress.progress(number / len(valid_files), text=message)
                    status_box.update(label=message)

                st.write(f"Processing **{file.name}**…")
                report = services.pipeline.index_file(
                    file.name, file.getvalue(), chunk_size, chunk_overlap, force=force, progress=on_progress
                )
                reports.append(report.to_dict())
                st.write(f"→ {report.status}: {report.message}")
            progress.progress(1.0, text="Done")
            failed = sum(r["status"] == "failed" for r in reports)
            status_box.update(
                label=f"Finished: {len(reports) - failed} ok, {failed} failed",
                state="error" if failed == len(reports) else "complete",
                expanded=False,
            )
        st.session_state.last_index_reports = reports

    render_report_details(st.session_state.last_index_reports)
    privacy_note()
