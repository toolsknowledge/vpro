"""Media Dashboard: counts, processing status and errors, plus retry and delete for each recording."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from backend.media_registry import STATUS_FAILED, STATUS_INDEXED, STATUS_PARTIAL, STATUS_PROCESSING
from backend.media_utils import MediaError, format_bytes, format_timestamp
from ui.components import format_time, metric_cards, page_header, require_openai
from ui.media_components import media_label, media_pipeline_diagram, media_privacy_note


def render(services) -> None:
    page_header("Media Dashboard", "Every indexed recording, its processing stages, and what can be retried.", "📊")
    records = services.media_registry.list_documents()
    counts = services.media_stores.counts()
    audio = [r for r in records if r.get("media_kind") == "audio"]
    video = [r for r in records if r.get("media_kind") == "video"]
    latest = max(records, key=lambda r: r.get("updated_at") or "", default=None)

    metric_cards(
        [
            ("Audio files", str(len(audio)), f"{sum(r.get('status') == STATUS_INDEXED for r in audio)} fully indexed"),
            ("Video files", str(len(video)), f"{sum(r.get('status') == STATUS_INDEXED for r in video)} fully indexed"),
            ("Transcript chunks", f"{counts['audio'] + counts['video_transcript']:,}",
             f"{counts['audio']} audio · {counts['video_transcript']} video"),
            ("Frame descriptions", f"{counts['video_frame']:,}", services.settings.video_frame_collection_name),
            ("Total embeddings", f"{sum(counts.values()) + services.store.count():,}",
             f"incl. {services.store.count():,} document chunks"),
            ("Last processing", latest.get("status", "—") if latest else "—",
             format_time(latest.get("updated_at")) if latest else "never"),
        ]
    )

    stuck = [r for r in records if r.get("status") == STATUS_PROCESSING]
    problems = [r for r in records if r.get("status") in (STATUS_FAILED, STATUS_PARTIAL) or r.get("last_error")]
    if stuck:
        st.warning(f"{len(stuck)} file(s) are marked 'processing' (interrupted run?). Retry them below.")

    st.subheader("Indexed media")
    if not records:
        st.info("No recordings yet. Go to **🎙️ Audio and Video Upload** (demo files: `sample_files/Python_Lecture.mp4`, "
                "`sample_files/RAG_Evaluation_Session.mp3`).")
        media_privacy_note()
        return
    table = pd.DataFrame(
        [
            {
                "File": r.get("filename"),
                "Kind": r.get("media_kind"),
                "Status": r.get("status"),
                "Duration": format_timestamp((r.get("info") or {}).get("duration_seconds")),
                "Size": format_bytes((r.get("info") or {}).get("size_bytes")),
                "Transcript chunks": r.get("transcript_chunk_count", 0),
                "Timing": r.get("timing_source") or "",
                "Frames (described/extracted)": f"{r.get('frames_described', 0)}/{r.get('frames_extracted', 0)}",
                "Records in ChromaDB": r.get("stored_records", 0),
                "Transcription model": r.get("transcription_model") or "",
                "Updated": format_time(r.get("updated_at")),
            }
            for r in records
        ]
    )
    st.dataframe(table, hide_index=True, width="stretch")

    if problems:
        st.subheader("Processing errors")
        for r in problems:
            st.error(f"**{r['filename']}** ({r['status']}): {r.get('last_error') or '; '.join(r.get('errors') or [])}")

    st.subheader("Inspect, retry or delete")
    by_id = {r["document_id"]: r for r in records}
    chosen = st.selectbox("Recording", list(by_id), format_func=lambda i: media_label(by_id[i]))
    record = by_id[chosen]
    media_pipeline_diagram(record.get("stages"), record.get("media_kind"))
    for warning in record.get("warnings") or []:
        st.caption(f"⚠️ {warning}")
    with st.expander("Registry record"):
        st.json({k: v for k, v in record.items() if k not in ("stages", "file_hash")}, expanded=False)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Retry / re-index**")
        st.caption("Uses the stored upload. Cached transcript pieces and frame descriptions are reused, so only "
                   "failed or changed stages call OpenAI again.")
        if st.button("🔁 Retry this file", disabled=not require_openai(services)):
            with st.status("Re-processing…", expanded=True) as box:
                try:
                    report = services.media_pipeline.retry(
                        chosen, progress=lambda stage, message, fraction: box.update(label=message)
                    )
                    st.write(f"{report.status}: {report.message}")
                    box.update(label=f"Finished: {report.status}", state="error" if report.status == "failed" else "complete")
                    st.session_state.last_media_reports = [report.to_dict()]
                except MediaError as exc:
                    box.update(label=str(exc), state="error")
    with c2:
        st.markdown("**Delete**")
        st.caption("Removes every ChromaDB record, the transcript, extracted frames and the original upload.")
        confirm = st.checkbox(f"Yes, delete '{record['filename']}'", key=f"confirm_delete_{chosen}")
        if st.button("🗑️ Delete", disabled=not confirm, type="secondary"):
            removed = services.media_pipeline.delete_media(chosen)
            st.success(f"Deleted '{record['filename']}' ({removed} ChromaDB records).")
            st.rerun()
    media_privacy_note()
