"""Video helpers: describe a video and pull out its audio track.

A video file is a *container* holding separate streams: usually one video
stream (the pictures) and one audio stream (the sound). For Video RAG we treat
them separately:

* the audio stream is extracted with FFmpeg and sent through the same
  transcription pipeline as an audio upload (what the instructor *said*);
* the video stream is sampled into keyframes (see frame_extractor.py) and
  described by a vision model (what was *shown*).
"""

from __future__ import annotations

from pathlib import Path

from backend.audio_processor import prepare_audio
from backend.media_utils import FFmpegTools, MediaError, MediaInfo, format_timestamp


def describe_video(info: MediaInfo) -> dict[str, str]:
    """Human-friendly summary for the upload page."""
    return {
        "Duration": format_timestamp(info.duration_seconds),
        "Resolution": info.resolution or "unknown",
        "Frame rate": f"{info.fps:g} fps" if info.fps else "unknown",
        "Video codec": info.video_codec or "none",
        "Audio": f"yes ({info.audio_codec}, {info.sample_rate or '?'} Hz)" if info.has_audio else "no audio track",
        "Container": info.format_long_name or info.format_name,
    }


def describe_audio(info: MediaInfo) -> dict[str, str]:
    channels = {1: "mono", 2: "stereo"}.get(info.channels or 0, f"{info.channels} channels" if info.channels else "?")
    return {
        "Duration": format_timestamp(info.duration_seconds),
        "Audio codec": info.audio_codec or "unknown",
        "Sample rate": f"{info.sample_rate} Hz" if info.sample_rate else "unknown",
        "Channels": channels,
        "Bit rate": f"{info.bit_rate // 1000} kbps" if info.bit_rate else "unknown",
        "Container": info.format_long_name or info.format_name,
    }


def extract_audio_track(video_path: Path, target: Path, info: MediaInfo, tools: FFmpegTools) -> Path | None:
    """Extract the audio track as speech-ready MP3. Returns None when the video has no audio."""
    if not info.has_audio:
        return None
    try:
        return prepare_audio(video_path, target, tools)
    except MediaError as exc:
        raise MediaError(f"Could not extract the audio track from the video: {exc}") from exc
