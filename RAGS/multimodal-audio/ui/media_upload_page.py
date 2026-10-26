"""Audio and Video Upload: validate, preview and inspect media, choose options, run the pipeline."""

from __future__ import annotations

import math
import uuid

import pandas as pd
import streamlit as st

from backend.media_pipeline import MediaOptions
from backend.media_utils import (
    MediaError,
    check_media_extension,
    format_bytes,
    format_timestamp,
    probe_media,
    save_stream,
    validate_media_info,
)
from backend.transcription_service import capabilities_for
from backend.video_processor import describe_audio, describe_video
from config.settings import AUDIO_EXTENSIONS, MEDIA_EXTENSIONS, VIDEO_EXTENSIONS, ConfigError
from ui.components import page_header, require_openai
from ui.media_components import MEDIA_STATUS_KIND, ffmpeg_status, media_pipeline_diagram, media_privacy_note
from ui.components import badge


def _inspect(services, file) -> dict:
    """Probe an upload with FFprobe (cached per uploaded file). The temporary copy is always deleted."""
    cache = st.session_state.setdefault("media_probe_cache", {})
    if file.file_id in cache:
        return cache[file.file_id]
    settings = services.settings
    result: dict = {"error": None, "info": None, "warnings": []}
    try:
        extension = check_media_extension(file.name)
        if file.size > settings.max_media_upload_bytes:
            raise MediaError(
                f"{format_bytes(file.size)} is above the {settings.max_media_upload_size_mb} MB limit (MAX_MEDIA_UPLOAD_SIZE_MB)."
            )
        tmp = settings.media_uploads_directory / f".probe-{uuid.uuid4().hex}{extension}"
        try:
            save_stream(file, tmp, settings.max_media_upload_bytes)
            info = probe_media(tmp, services.ffmpeg)
            result["warnings"] = validate_media_info(info, extension, settings.max_media_duration_minutes * 60)
            result["info"] = info
        finally:
            tmp.unlink(missing_ok=True)
    except MediaError as exc:
        result["error"] = str(exc)
    cache[file.file_id] = result
    return result


def _options_form(services) -> MediaOptions | None:
    s = services.settings
    st.markdown("#### Processing options")
    c1, c2 = st.columns(2)
    chunk_size = c1.number_input("Transcript chunk size (tokens)", 50, 8000, int(st.session_state.chunk_size), 50)
    chunk_overlap = c2.number_input("Transcript chunk overlap (tokens)", 0, 3999, int(st.session_state.chunk_overlap), 10)

    st.markdown("**Video frames** (ignored for audio files)")
    c1, c2, c3 = st.columns(3)
    analyze = c1.toggle("Extract and describe keyframes", value=True,
                        help="Off = index only what was said in videos (no vision cost).")
    interval = c2.number_input("One frame every N seconds", 1, 600, int(s.video_frame_interval_seconds), disabled=not analyze)
    max_frames = c3.number_input("Max frames per video", 1, 5000, int(s.max_frames_per_video), disabled=not analyze)
    c1, c2, c3 = st.columns(3)
    scene = c1.toggle("Add scene-change frames", value=False, disabled=not analyze,
                      help="FFmpeg also grabs frames where the picture changes a lot (slower to scan).")
    threshold = c2.slider("Scene-change sensitivity", 0.1, 0.9, 0.3, 0.05, disabled=not (analyze and scene),
                          help="Lower = more frames.")
    detail = c3.selectbox("Image detail sent to vision model", ["auto", "low", "high"], disabled=not analyze,
                          help="'low' is cheapest but may not read small text or code.")
    skip_dupes = st.checkbox("Skip near-duplicate frames (same slide) to save vision calls", value=True, disabled=not analyze)

    st.markdown("**Re-processing**")
    c1, c2 = st.columns(2)
    reuse = c1.checkbox("Reuse cached transcripts and frame descriptions", value=True,
                        help="Unchanged media is not transcribed or analysed again.")
    replace = c2.checkbox("Replace older versions with the same file name", value=True)

    st.session_state.chunk_size, st.session_state.chunk_overlap = int(chunk_size), int(chunk_overlap)
    options = MediaOptions(
        chunk_size=int(chunk_size), chunk_overlap=int(chunk_overlap),
        frame_interval_seconds=int(interval), max_frames=int(max_frames), analyze_frames=analyze,
        scene_detection=scene, scene_threshold=float(threshold), skip_duplicate_frames=skip_dupes,
        image_detail=detail, reuse_cached_results=reuse, replace_previous_versions=replace,
    )
    try:
        options.validate()
    except ConfigError as exc:
        st.error(str(exc))
        return None
    return options


def render_media_reports(reports: list[dict]) -> None:
    if not reports:
        return
    st.subheader("Processing results")
    table = pd.DataFrame(
        [
            {
                "File": r["filename"],
                "Kind": r["media_kind"] or "",
                "Status": r["status"],
                "Duration": format_timestamp((r.get("info") or {}).get("duration_seconds")),
                "Transcript chunks": r["transcript_chunks"],
                "Frames extracted": r["frames_extracted"],
                "Frames described": r["frames_described"],
                "Embeddings": r["embeddings"],
                "Dimension": r["dimension"] or "",
                "Stored records": r["stored_records"],
                "Seconds": r["seconds"],
            }
            for r in reports
        ]
    )
    st.dataframe(table, hide_index=True, width="stretch")
    for r in reports:
        icon = {"indexed": "✅", "partial": "⚠️", "duplicate": "🔁", "failed": "❌"}.get(r["status"], "•")
        with st.expander(f"{icon} {r['filename']} — {r['status']}", expanded=r["status"] in ("failed", "partial")):
            st.markdown(badge(r["status"], MEDIA_STATUS_KIND.get(r["status"], "info")) + " " + r["message"],
                        unsafe_allow_html=True)
            media_pipeline_diagram([s for s in r["stages"]], r.get("media_kind"))
            for warning in r["warnings"]:
                st.warning(warning)
            for error in r["errors"]:
                st.error(error)


def render(services) -> None:
    page_header("Audio and Video Upload", "Add recorded classes, meetings and tutorials to the knowledge base.", "🎙️")
    openai_ok = require_openai(services)
    ffmpeg_ok = ffmpeg_status(services)
    s = services.settings
    caps = capabilities_for(s.transcription_model)

    st.markdown(
        f"**Audio:** {', '.join(sorted(AUDIO_EXTENSIONS))} · **Video:** {', '.join(sorted(VIDEO_EXTENSIONS))} · "
        f"max **{s.max_media_upload_size_mb} MB** and **{s.max_media_duration_minutes} min** per file. "
        "The real content is checked with FFprobe, not just the extension."
    )
    timing = (
        "segment timestamps from the model" if caps.segment_timestamps
        else f"no timestamps from the model → timed by {s.timestamp_fallback_seconds}s audio pieces"
    )
    st.caption(
        f"Transcription: `{s.transcription_model}` ({timing}{', speaker labels' if caps.speakers else ''}) · "
        f"Vision: `{s.vision_model}` · Embeddings: `{s.embedding_model}`"
    )

    files = st.file_uploader(
        "Drag and drop audio or video files here",
        type=sorted(ext.lstrip(".") for ext in MEDIA_EXTENSIONS),
        accept_multiple_files=True,
    )

    ready = []
    for file in files or []:
        with st.container(border=True):
            result = _inspect(services, file) if ffmpeg_ok else {"error": "FFmpeg is not installed.", "info": None, "warnings": []}
            info = result["info"]
            st.markdown(f"**{file.name}** · {format_bytes(file.size)}")
            if result["error"]:
                st.error(result["error"])
                continue
            cols = st.columns([3, 2])
            with cols[0]:
                if info.has_video:
                    st.video(file)
                else:
                    st.audio(file)
            with cols[1]:
                details = describe_video(info) if info.has_video else describe_audio(info)
                details = {"Detected as": info.media_kind, **details, "Status": "ready to process"}
                st.dataframe(pd.DataFrame(details.items(), columns=["Property", "Value"]), hide_index=True, width="stretch")
            for warning in result["warnings"]:
                st.warning(warning)
            ready.append((file, info))

    options = _options_form(services)
    force = st.checkbox("Re-index even if the same content was already indexed with the same settings")

    if ready and options:
        audio_minutes = sum(info.duration_seconds for _, info in ready if info.has_audio) / 60
        frames = sum(
            min(math.ceil(info.duration_seconds / options.frame_interval_seconds), options.max_frames)
            for _, info in ready if info.has_video and options.analyze_frames
        )
        st.info(
            f"Estimated work: **{audio_minutes:.1f} min** of audio to transcribe and up to **{frames}** keyframe(s) to "
            "describe (fewer if near-duplicates are skipped or cached results are reused)."
        )

    disabled = not (ready and options and openai_ok and ffmpeg_ok)
    if st.button("🚀 Start processing", type="primary", disabled=disabled):
        reports = []
        progress = st.progress(0.0, text="Starting…")
        with st.status("Processing media…", expanded=True) as box:
            for number, (file, _) in enumerate(ready):
                def on_progress(stage, message, fraction, number=number):
                    progress.progress(min(1.0, (number + (fraction or 0)) / len(ready)), text=message)
                    box.update(label=message)

                st.write(f"Processing **{file.name}**…")
                report = services.media_pipeline.process(file.name, file, options, force=force, progress=on_progress)
                reports.append(report.to_dict())
                st.write(f"→ {report.status}: {report.message}")
            progress.progress(1.0, text="Done")
            failed = sum(r["status"] == "failed" for r in reports)
            box.update(label=f"Finished: {len(reports) - failed} ok, {failed} failed",
                       state="error" if failed == len(reports) else "complete", expanded=False)
        st.session_state.last_media_reports = reports

    render_media_reports(st.session_state.get("last_media_reports", []))
    st.markdown("#### Pipeline")
    media_pipeline_diagram()
    media_privacy_note()
