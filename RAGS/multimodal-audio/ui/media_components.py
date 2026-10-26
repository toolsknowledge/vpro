"""UI pieces shared by the audio/video pages: stage diagram, media player, media citations."""

from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from backend.media_pipeline import MEDIA_STAGES
from backend.media_retrieval import SOURCE_LABELS, chunk_start
from backend.media_utils import format_timestamp
from backend.transcript_chunker import MEDIA_VIDEO_FRAME
from ui.components import STATUS_ICONS

STATUS_ICONS = {**STATUS_ICONS, "reused": "♻️", "partial": "⚠️"}
STATUS_CLASS = {"done": "done", "reused": "done", "partial": "failed", "failed": "failed", "skipped": "skipped"}

MEDIA_STATUS_KIND = {"indexed": "ok", "partial": "warn", "failed": "err", "processing": "info", "duplicate": "info"}


def media_pipeline_diagram(stages: list[dict] | None = None, kind: str | None = None) -> None:
    """Render the media stages. Audio files hide the two frame stages; silent videos the audio ones."""
    by_key = {s["key"]: s for s in stages or []}
    shown = [s for s in MEDIA_STAGES if not (kind == "audio" and s[0] in ("frames", "vision"))]
    parts = []
    for i, (key, name, description) in enumerate(shown):
        stage = by_key.get(key, {})
        status = stage.get("status", "pending")
        count = stage.get("count")
        count_html = f'<div class="count">{count:,}</div>' if isinstance(count, int) else ""
        message = f'<div class="io"><i>{html.escape(stage["message"])}</i></div>' if stage.get("message") else ""
        seconds = f'<div class="io">{stage["seconds"]:.1f}s</div>' if stage.get("seconds") else ""
        parts.append(
            f'<div class="vp-stage {STATUS_CLASS.get(status, "pending")}">'
            f'<div class="name">{STATUS_ICONS.get(status, "")} {i + 1}. {name}</div>'
            f'<div class="desc">{html.escape(description)}</div>{count_html}{message}{seconds}</div>'
        )
        if i < len(shown) - 1:
            parts.append('<div class="vp-arrow">➜</div>')
    st.markdown(f'<div class="vp-pipeline">{"".join(parts)}</div>', unsafe_allow_html=True)


def media_label(record: dict) -> str:
    icon = "🎬" if record.get("media_kind") == "video" else "🎧"
    duration = (record.get("info") or {}).get("duration_seconds")
    return f"{icon} {record.get('filename')} ({format_timestamp(duration)}) · {record.get('status')}"


def select_media(services, *, key: str, kinds: tuple[str, ...] = ("audio", "video"), require=None) -> dict | None:
    records = [
        r for r in services.media_registry.list_documents()
        if r.get("media_kind") in kinds and (require is None or require(r))
    ]
    if not records:
        return None
    by_id = {r["document_id"]: r for r in records}
    preselect = st.session_state.get(f"{key}_selected")
    ids = list(by_id)
    index = ids.index(preselect) if preselect in by_id else 0
    chosen = st.selectbox("Recording", ids, index=index, format_func=lambda i: media_label(by_id[i]), key=key)
    st.session_state[f"{key}_selected"] = chosen
    return by_id[chosen]


def play_media(services, record: dict, start_seconds: float = 0.0) -> None:
    """Show the original upload with the player positioned at `start_seconds`."""
    path = services.media_registry.upload_path(record)
    if path is None:
        st.warning("The original upload is missing, so it cannot be played.")
        return
    start = max(0, int(start_seconds))
    if record.get("media_kind") == "video":
        st.video(str(path), start_time=start)
    else:
        st.audio(str(path), start_time=start)
    st.caption(f"▶ {record.get('filename')} from {format_timestamp(start)} (press play)")


def request_playback(document_id: str, start_seconds: float) -> None:
    st.session_state.media_player = {"document_id": document_id, "start": float(start_seconds)}


def render_requested_player(services) -> None:
    request = st.session_state.get("media_player")
    if not request:
        return
    record = services.media_registry.get(request["document_id"])
    if not record:
        st.session_state.media_player = None
        return
    with st.container(border=True):
        cols = st.columns([6, 1])
        cols[0].markdown(f"**Now playing:** {html.escape(record['filename'])} at {format_timestamp(request['start'])}")
        if cols[1].button("Close", key="close_player"):
            st.session_state.media_player = None
            st.rerun()
        play_media(services, record, request["start"])


def frame_image_path(services, metadata: dict) -> Path | None:
    relative = metadata.get("frame_path")
    if not relative:
        return None
    data_dir = services.settings.data_directory.resolve()
    path = (data_dir / relative).resolve()
    return path if data_dir in path.parents and path.exists() else None


def show_media_chunk_card(services, chunk, label: str | None = None, key: str = "", expanded: bool = False) -> None:
    """A retrieved chunk of any type, with frame preview and a play button for media."""
    meta = chunk.metadata
    kind = SOURCE_LABELS.get(meta.get("media_type"), "Document")
    sim = f"similarity {chunk.similarity:.3f} · " if chunk.similarity is not None else ""
    title = f"{label + ' · ' if label else ''}#{chunk.rank} · {kind} · {chunk.citation} · {sim}distance {chunk.distance:.4f}"
    with st.expander(title, expanded=expanded):
        if meta.get("media_type") == MEDIA_VIDEO_FRAME:
            image = frame_image_path(services, meta)
            if image:
                st.image(str(image), caption=f"Frame at {format_timestamp(meta.get('timestamp_seconds'))}", width=480)
        st.markdown(f'<div class="vp-chunk">{html.escape(chunk.text)}</div>', unsafe_allow_html=True)
        doc_id = meta.get("document_id")
        if meta.get("media_type") in SOURCE_LABELS and meta.get("media_type") != "document" and doc_id:
            start = chunk_start(chunk)
            if st.button(f"▶ Play from {format_timestamp(start)}", key=f"play_{key}_{chunk.chunk_id}"):
                request_playback(doc_id, start)
                st.rerun()
        st.caption(
            f"Chunk ID: `{chunk.chunk_id}` · collection `{meta.get('collection', '?')}` · "
            f"keyword overlap {chunk.keyword_overlap:.0%}"
        )
        safe_meta = {k: v for k, v in meta.items() if k not in ("file_hash",)}
        st.json(safe_meta, expanded=False)


def ffmpeg_status(services) -> bool:
    ok, message = services.ffmpeg.available()
    if not ok:
        st.error(message)
    return ok


def media_privacy_note() -> None:
    st.caption(
        "🔒 Privacy: audio is sent to OpenAI for transcription, sampled video frames are sent to the vision model, "
        "and transcript/description text is sent for embeddings and answers. Do not upload confidential recordings."
    )
