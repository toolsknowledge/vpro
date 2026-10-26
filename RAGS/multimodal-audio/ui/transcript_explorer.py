"""Transcript Explorer: read, search and download transcripts; inspect segments and chunk boundaries."""

from __future__ import annotations

import html
from pathlib import Path

import pandas as pd
import streamlit as st

from backend.media_utils import format_time_range, format_timestamp, parse_timestamp
from backend.transcript_export import ExportError, srt_supported, to_srt, to_txt
from backend.transcription_service import TranscriptSegment, capabilities_for
from ui.components import page_header
from ui.media_components import play_media, select_media


def _segments(trace: dict, key: str) -> list[TranscriptSegment]:
    return [TranscriptSegment.from_dict(s) for s in trace.get(key) or []]


def render(services) -> None:
    page_header("Transcript Explorer", "What was said, when — with the exact segments and chunk boundaries.", "📝")
    record = select_media(services, key="transcript_media",
                          require=lambda r: services.media_registry.load_trace(r["document_id"]) is not None)
    if record is None:
        st.info("No transcripts yet. Upload an audio file or a video with sound on **🎙️ Audio and Video Upload**.")
        return
    trace = services.media_registry.load_trace(record["document_id"]) or {}
    raw = _segments(trace, "raw_segments")
    clean = _segments(trace, "clean_segments") or raw
    caps = capabilities_for(trace.get("transcription_model", ""))

    c = st.columns(5)
    c[0].metric("Segments", len(clean))
    c[1].metric("Chunks", len(trace.get("chunks") or []))
    c[2].metric("Audio pieces", len(trace.get("pieces") or []))
    c[3].metric("Timing source", trace.get("timing_source") or "—")
    c[4].metric("Language", record.get("language") or "not reported")
    st.caption(
        f"Model `{trace.get('transcription_model')}` · response format `{trace.get('response_format')}` · "
        f"speaker labels: {'yes' if caps.speakers else 'not provided by this model'}"
    )
    if trace.get("timing_source") == "audio_split":
        st.info(
            f"This model returned text without timestamps. Each segment is timed by the "
            f"{trace.get('split_seconds')}s audio piece it was cut from, so times are approximate to that window."
        )
    for failure in trace.get("failures") or []:
        st.error(f"Piece {format_time_range(failure['start_seconds'], failure['end_seconds'])} failed: {failure['error']}")

    # ---------------------------------------------------------------- player
    st.subheader("Play")
    jump_text = st.text_input("Jump to timestamp (HH:MM:SS, MM:SS or seconds)",
                              value=st.session_state.get("transcript_jump", "0"), key="transcript_jump_input")
    jump = parse_timestamp(jump_text)
    if jump is None:
        st.warning("Could not read that timestamp; starting from 00:00:00.")
    play_media(services, record, jump or 0)

    # -------------------------------------------------------------- segments
    st.subheader("Segments")
    query = st.text_input("Search the transcript", placeholder="e.g. list comprehension").strip().lower()
    view = st.radio("View", ["Cleaned", "Raw vs cleaned"], horizontal=True)
    raw_by_id = {s.segment_id: s for s in raw}
    rows = [
        {
            "Start": format_timestamp(s.start_seconds),
            "End": format_timestamp(s.end_seconds),
            "Speaker": s.speaker or "",
            "Segment ID": s.segment_id,
            "Text": s.text,
            **({"Raw text": raw_by_id.get(s.segment_id).text if raw_by_id.get(s.segment_id) else ""}
               if view == "Raw vs cleaned" else {}),
            "_start": s.start_seconds,
        }
        for s in clean
        if not query or query in s.text.lower()
    ]
    st.caption(f"{len(rows)} of {len(clean)} segment(s){' match' if query else ''}. Select a row to play from it.")
    if rows:
        frame = pd.DataFrame(rows)
        event = st.dataframe(
            frame.drop(columns=["_start"]), hide_index=True, width="stretch",
            on_select="rerun", selection_mode="single-row", key=f"seg_table_{record['document_id']}",
        )
        selected = event.selection.rows if event and event.selection else []
        if selected:
            start = rows[selected[0]]["_start"]
            st.session_state.transcript_jump = format_timestamp(start)
            st.markdown(f"**Playing from {format_timestamp(start)}**")
            play_media(services, record, start)

    # ---------------------------------------------------------------- chunks
    st.subheader("Chunk boundaries")
    for chunk in trace.get("chunks") or []:
        title = (f"Chunk {chunk['chunk_index']} · {format_time_range(chunk['start_time_seconds'], chunk['end_time_seconds'])}"
                 f" · {chunk['token_count']} tokens · {len(chunk['transcript_segment_ids'])} segment(s)")
        with st.expander(title):
            st.markdown(f'<div class="vp-chunk">{html.escape(chunk.get("timed_text") or chunk["text"])}</div>',
                        unsafe_allow_html=True)
            st.caption(f"Chunk ID `{chunk['chunk_id']}` · segments: {', '.join(chunk['transcript_segment_ids'])}")

    # -------------------------------------------------------------- download
    st.subheader("Download")
    stem = Path(record["filename"]).stem
    c1, c2 = st.columns(2)
    c1.download_button("⬇️ Transcript (.txt)", to_txt(clean, record["filename"], trace.get("transcription_model", "")),
                       file_name=f"{stem}_transcript.txt", mime="text/plain")
    if srt_supported(clean):
        c2.download_button("⬇️ Subtitles (.srt)", to_srt(clean), file_name=f"{stem}.srt", mime="application/x-subrip")
    else:
        try:
            to_srt(clean)
        except ExportError as exc:
            c2.caption(f"SRT disabled: {exc}")
