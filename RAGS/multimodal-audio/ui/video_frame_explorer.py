"""Video Frame Explorer: every extracted keyframe with its description, transcript and ChromaDB record."""

from __future__ import annotations

import streamlit as st

from backend.frame_analyzer import FrameAnalysis
from backend.frame_extractor import FrameRecord
from backend.media_utils import format_timestamp
from backend.transcript_chunker import MEDIA_VIDEO_FRAME
from ui.components import page_header
from ui.media_components import play_media, select_media

STATUS_TEXT = {"done": "✅ described", "skipped_duplicate": "⏭️ same screen as an earlier frame", "failed": "❌ failed"}


def _related_transcript(trace: dict | None, start: float, end: float) -> str:
    if not trace:
        return ""
    lines = [
        f"[{format_timestamp(s['start_seconds'])}] {s['text']}"
        for s in trace.get("clean_segments") or trace.get("raw_segments") or []
        if s["start_seconds"] <= end and s["end_seconds"] >= start
    ]
    return "\n".join(lines)


def render(services) -> None:
    page_header("Video Frame Explorer", "The sampled keyframes, what the vision model saw, and what was said then.", "🖼️")
    record = select_media(services, key="frame_media", kinds=("video",),
                          require=lambda r: services.media_registry.load_frames_manifest(r["document_id"]) is not None)
    if record is None:
        st.info("No video frames yet. Upload a video on **🎙️ Audio and Video Upload** with keyframe analysis turned on.")
        return
    document_id = record["document_id"]
    manifest = services.media_registry.load_frames_manifest(document_id) or {}
    frames = [FrameRecord.from_dict(f) for f in manifest.get("frames", [])]
    analyses = {a["frame_id"]: FrameAnalysis.from_dict(a) for a in manifest.get("analyses", [])}
    trace = services.media_registry.load_trace(document_id)
    frame_store = services.media_stores[MEDIA_VIDEO_FRAME]
    stored = {r.chunk_id: r for r in frame_store.get_records(where={"document_id": document_id}, include_embeddings=True)}
    options = manifest.get("options", {})

    c = st.columns(5)
    c[0].metric("Frames extracted", len(frames))
    c[1].metric("Described", sum(a.status == "done" for a in analyses.values()))
    c[2].metric("Duplicates skipped", sum(a.status == "skipped_duplicate" for a in analyses.values()))
    c[3].metric("Failed", sum(a.status == "failed" for a in analyses.values()))
    c[4].metric("In ChromaDB", len(stored))
    st.caption(
        f"Sampling: one frame every {options.get('frame_interval_seconds')}s"
        f"{' + scene changes' if options.get('scene_detection') else ''}, max {options.get('max_frames')} · "
        f"vision model `{manifest.get('vision_model')}`. Only these sampled frames were analysed, not every frame "
        "of the video. Vectors are *text* embeddings of the descriptions, not image embeddings."
    )

    play = st.session_state.get("frame_play")
    if play and play["document_id"] == document_id:
        with st.container(border=True):
            play_media(services, record, play["start"])

    show_dupes = st.toggle("Show near-duplicate frames too", value=False)
    interval = float(options.get("frame_interval_seconds") or 10)
    for frame in frames:
        analysis = analyses.get(frame.frame_id)
        if frame.duplicate_of and not show_dupes:
            continue
        with st.container(border=True):
            left, right = st.columns([2, 3])
            image = services.settings.data_directory / frame.frame_path
            with left:
                if image.exists():
                    st.image(str(image), width="stretch")
                st.caption(f"Frame {frame.frame_index} · {format_timestamp(frame.timestamp_seconds)} · {frame.extraction_method}")
                if st.button(f"▶ Play from {format_timestamp(frame.timestamp_seconds)}", key=f"fplay_{frame.frame_id}"):
                    st.session_state.frame_play = {"document_id": document_id, "start": frame.timestamp_seconds}
                    st.rerun()
            with right:
                status = analysis.status if analysis else "not analysed"
                st.markdown(f"**{format_timestamp(frame.timestamp_seconds)}** — {STATUS_TEXT.get(status, status)}")
                if frame.duplicate_of:
                    st.caption(f"Same screen as `{frame.duplicate_of}`; its description covers this moment.")
                if analysis and analysis.status == "done":
                    st.markdown(analysis.description.replace("\n", "  \n"))
                elif analysis and analysis.error:
                    st.error(analysis.error)
                related = _related_transcript(trace, frame.timestamp_seconds - interval / 2, frame.timestamp_seconds + interval / 2)
                if related:
                    with st.expander("What was said around this frame"):
                        st.text(related)
                record_in_db = stored.get(frame.frame_id)
                if record_in_db:
                    with st.expander(f"ChromaDB record · embedded ({len(record_in_db.embedding or [])} dims)"):
                        st.code(record_in_db.text, language=None)
                        st.json(record_in_db.metadata, expanded=False)
                elif analysis and analysis.status == "done":
                    st.caption("⚠️ Described but not in ChromaDB (embedding or storage failed — retry on the dashboard).")
