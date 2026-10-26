"""Audio preprocessing with FFmpeg: normalise → find pauses → split into timed pieces.

Why split? The OpenAI transcription endpoint accepts files up to 25 MB, and
long inputs are slower and fail more painfully. We therefore:

1. Convert the audio track to mono, 16 kHz, 64 kbps MP3. Speech models do not
   need more, and 5 minutes of it is only ~2.4 MB. The original upload is kept.
2. Detect silences with FFmpeg's `silencedetect` filter.
3. Plan cut points near every `target_seconds`, moved to the middle of a nearby
   pause when one exists, so words are not cut in half.
4. Cut the pieces and remember each piece's start and end time in the original
   recording. Those offsets turn per-piece timestamps back into global ones.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

from backend.media_utils import FFmpegTools, MediaError
from config.settings import TRANSCRIPTION_UPLOAD_LIMIT_BYTES

SPEECH_SAMPLE_RATE = 16000
SPEECH_BITRATE = "64k"

_SILENCE_START = re.compile(r"silence_start:\s*(-?[\d.]+)")
_SILENCE_END = re.compile(r"silence_end:\s*([\d.]+)")


@dataclass
class AudioPiece:
    index: int
    start_seconds: float
    end_seconds: float
    path: str  # relative to the data directory once stored
    size_bytes: int = 0
    cut_at_silence: bool = False

    @property
    def duration(self) -> float:
        return self.end_seconds - self.start_seconds

    def to_dict(self) -> dict:
        return asdict(self)


def prepare_audio(source: Path, target: Path, tools: FFmpegTools) -> Path:
    """Extract/convert the first audio stream to speech-friendly MP3. Works for audio *and* video input."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".part.mp3")
    try:
        tools.run(
            [
                tools.ffmpeg, "-hide_banner", "-nostdin", "-y", "-i", str(source),
                "-map", "0:a:0", "-vn", "-ac", "1", "-ar", str(SPEECH_SAMPLE_RATE), "-b:a", SPEECH_BITRATE,
                str(tmp),
            ],
            what="FFmpeg audio extraction",
        )
        if not tmp.exists() or tmp.stat().st_size == 0:
            raise MediaError("FFmpeg produced an empty audio file; the audio track may be silent or unreadable.")
        tmp.replace(target)
    finally:
        tmp.unlink(missing_ok=True)
    return target


def detect_silences(
    path: Path, tools: FFmpegTools, noise_db: int = -35, min_silence: float = 0.4
) -> list[tuple[float, float]]:
    """Return (start, end) of every pause FFmpeg finds. An empty list is fine (continuous speech)."""
    result = tools.run(
        [
            tools.ffmpeg, "-hide_banner", "-nostdin", "-i", str(path),
            "-af", f"silencedetect=noise={noise_db}dB:d={min_silence}", "-f", "null", "-",
        ],
        what="FFmpeg silence detection",
    )
    return parse_silences(result.stderr)


def parse_silences(stderr: str) -> list[tuple[float, float]]:
    silences, start = [], None
    for line in stderr.splitlines():
        if (m := _SILENCE_START.search(line)) is not None:
            start = max(0.0, float(m.group(1)))
        elif (m := _SILENCE_END.search(line)) is not None and start is not None:
            silences.append((start, float(m.group(1))))
            start = None
    return silences


def plan_segments(
    duration: float,
    target_seconds: float,
    silences: list[tuple[float, float]] | None = None,
    search_window: float | None = None,
    min_piece: float = 1.0,
) -> list[tuple[float, float, bool]]:
    """Plan (start, end, cut_at_silence) pieces covering [0, duration] without gaps.

    Each cut is placed at the middle of the pause closest to the ideal cut
    point, searching `search_window` seconds *before* it (so no piece grows
    longer than `target_seconds`). With no pause nearby, it cuts exactly at
    the ideal point. Pure function: easy to test.
    """
    if duration <= 0:
        return []
    if target_seconds <= 0:
        raise ValueError("target_seconds must be positive.")
    silences = sorted(silences or [])
    window = search_window if search_window is not None else min(15.0, target_seconds * 0.25)

    pieces: list[tuple[float, float, bool]] = []
    start = 0.0
    while duration - start > target_seconds:
        ideal = start + target_seconds
        candidates = [
            (s + e) / 2 for s, e in silences
            if ideal - window <= (s + e) / 2 <= ideal and (s + e) / 2 - start >= min_piece
        ]
        if candidates:
            cut, at_silence = max(candidates), True  # the latest pause before the ideal point
        else:
            cut, at_silence = ideal, False
        pieces.append((round(start, 3), round(cut, 3), at_silence))
        start = cut
    if duration - start < min_piece and pieces:
        # A tiny tail is merged into the previous piece instead of becoming its own request.
        prev_start, _, prev_silence = pieces.pop()
        pieces.append((prev_start, round(duration, 3), prev_silence))
    else:
        pieces.append((round(start, 3), round(duration, 3), False))
    return pieces


def split_audio(source: Path, plan: list[tuple[float, float, bool]], out_dir: Path, tools: FFmpegTools) -> list[AudioPiece]:
    """Cut `source` into the planned pieces (re-encoded, so cut times are exact)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pieces = []
    for index, (start, end, at_silence) in enumerate(plan):
        target = out_dir / f"piece_{index:04d}.mp3"
        tools.run(
            [
                tools.ffmpeg, "-hide_banner", "-nostdin", "-y", "-ss", f"{start:.3f}", "-t", f"{end - start:.3f}",
                "-i", str(source), "-vn", "-ac", "1", "-ar", str(SPEECH_SAMPLE_RATE), "-b:a", SPEECH_BITRATE,
                str(target),
            ],
            what="FFmpeg audio split",
        )
        size = target.stat().st_size if target.exists() else 0
        if size == 0:
            raise MediaError(f"Audio piece {index} ({start:.0f}s–{end:.0f}s) came out empty.")
        if size > TRANSCRIPTION_UPLOAD_LIMIT_BYTES:
            raise MediaError(
                f"Audio piece {index} is {size / 1_048_576:.1f} MB, above the transcription upload limit. "
                "Lower AUDIO_CHUNK_SECONDS."
            )
        pieces.append(AudioPiece(index, start, end, str(target), size, at_silence))
    return pieces
