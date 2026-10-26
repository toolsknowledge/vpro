"""Export transcripts as TXT or SRT subtitles.

SRT shows each line on screen during its start–end time, so it is only
produced when every segment's timing came from the transcription model.
For text-only models a segment spans a whole 30 s audio piece; turning that
into subtitles would display long paragraphs at the wrong moments, so SRT
export is refused and TXT (with honest, labelled piece times) is offered.
"""

from __future__ import annotations

from backend.media_utils import format_time_range, format_timestamp
from backend.transcription_service import TIMING_MODEL, TranscriptSegment


class ExportError(ValueError):
    pass


def srt_supported(segments: list[TranscriptSegment]) -> bool:
    return bool(segments) and all(s.timing_source == TIMING_MODEL for s in segments)


def to_srt(segments: list[TranscriptSegment]) -> str:
    if not srt_supported(segments):
        raise ExportError(
            "SRT needs per-segment timestamps from the transcription model. This transcript is timed by audio "
            "pieces only, so SRT export is disabled to avoid misleading subtitle timing. Use TXT instead."
        )
    blocks = []
    for number, seg in enumerate(sorted(segments, key=lambda s: s.start_seconds), start=1):
        end = max(seg.end_seconds, seg.start_seconds + 0.5)
        speaker = f"{seg.speaker}: " if seg.speaker else ""
        blocks.append(
            f"{number}\n{format_timestamp(seg.start_seconds, millis=True)} --> {format_timestamp(end, millis=True)}\n"
            f"{speaker}{seg.text}\n"
        )
    return "\n".join(blocks)


def to_txt(segments: list[TranscriptSegment], source_file: str, model: str) -> str:
    approximate = not srt_supported(segments)
    header = [
        f"Transcript of: {source_file}",
        f"Transcription model: {model}",
        "Timing: " + ("approximate — each time range is the audio piece the text came from"
                      if approximate else "segment timestamps returned by the model"),
        "",
    ]
    lines = []
    for seg in sorted(segments, key=lambda s: s.start_seconds):
        speaker = f" {seg.speaker}:" if seg.speaker else ""
        lines.append(f"[{format_time_range(seg.start_seconds, seg.end_seconds)}]{speaker} {seg.text}")
    return "\n".join(header + lines) + "\n"
