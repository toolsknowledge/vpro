"""Shared media helpers: running FFmpeg/FFprobe safely, inspecting files, hashing uploads.

Every FFmpeg call goes through `run_command`, which:
* passes arguments as a list (never through a shell), so file names cannot inject commands;
* has a timeout, so a broken file cannot hang the app;
* turns failures into `MediaError` with a short, readable message.

`probe_media()` asks FFprobe what is *really* inside a file (streams, codecs,
duration). The file extension is only used to pick the uploader; the content
decides whether a file is audio, video, or unusable.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, BinaryIO

from config.settings import AUDIO_EXTENSIONS, MEDIA_EXTENSIONS, VIDEO_EXTENSIONS

READ_BLOCK = 1024 * 1024  # copy uploads 1 MB at a time instead of holding several copies in memory


class MediaError(Exception):
    """A friendly, user-facing problem with a media file or with FFmpeg."""


@dataclass
class FFmpegTools:
    ffmpeg: str = "ffmpeg"
    ffprobe: str = "ffprobe"
    timeout: int = 600

    def available(self) -> tuple[bool, str]:
        """(ok, message). Explains how to install FFmpeg when it is missing."""
        missing = [name for name in (self.ffmpeg, self.ffprobe) if shutil.which(name) is None]
        if missing:
            return False, (
                f"{' and '.join(missing)} not found. Install FFmpeg (macOS: `brew install ffmpeg`, "
                "Ubuntu/Debian: `sudo apt install ffmpeg`, Windows: `winget install Gyan.FFmpeg`) "
                "or set FFMPEG_BINARY / FFPROBE_BINARY in .env, then restart the app."
            )
        return True, "FFmpeg and FFprobe are installed."

    def run(self, args: list[str], *, timeout: int | None = None, what: str = "FFmpeg") -> subprocess.CompletedProcess:
        return run_command(args, timeout=timeout or self.timeout, what=what)


def run_command(args: list[str], *, timeout: int, what: str = "FFmpeg") -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
    except FileNotFoundError as exc:
        raise MediaError(f"{what} is not installed or not on PATH ({args[0]}).") from exc
    except subprocess.TimeoutExpired as exc:
        raise MediaError(f"{what} took longer than {timeout}s and was stopped (FFMPEG_TIMEOUT_SECONDS).") from exc
    if result.returncode != 0:
        raise MediaError(f"{what} failed: {_last_error_line(result.stderr)}")
    return result


def _last_error_line(stderr: str) -> str:
    lines = [line.strip() for line in (stderr or "").splitlines() if line.strip()]
    # FFmpeg prints a banner first; the useful message is near the end.
    return lines[-1][:300] if lines else "unknown error"


# --------------------------------------------------------------------- probe
@dataclass
class MediaInfo:
    duration_seconds: float
    format_name: str
    format_long_name: str
    size_bytes: int
    has_audio: bool
    has_video: bool
    audio_codec: str | None = None
    sample_rate: int | None = None
    channels: int | None = None
    video_codec: str | None = None
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    bit_rate: int | None = None

    @property
    def media_kind(self) -> str:
        return "video" if self.has_video else "audio"

    @property
    def resolution(self) -> str | None:
        return f"{self.width}×{self.height}" if self.width and self.height else None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["media_kind"] = self.media_kind
        data["resolution"] = self.resolution
        return data


def _parse_fps(value: str | None) -> float | None:
    if not value or value in ("0/0", "0"):
        return None
    try:
        if "/" in value:
            num, den = value.split("/", 1)
            return round(float(num) / float(den), 3) if float(den) else None
        return round(float(value), 3)
    except ValueError:
        return None


def parse_probe_output(payload: dict[str, Any], size_bytes: int) -> MediaInfo:
    """Turn `ffprobe -show_format -show_streams` JSON into MediaInfo. Pure function (unit-tested)."""
    streams = payload.get("streams") or []
    fmt = payload.get("format") or {}
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    # Cover art inside an MP3/M4A is reported as a video stream with the attached_pic flag: not real video.
    video = next(
        (
            s for s in streams
            if s.get("codec_type") == "video" and not (s.get("disposition") or {}).get("attached_pic")
        ),
        None,
    )

    def _float(value) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    durations = [_float(fmt.get("duration"))] + [_float(s.get("duration")) for s in (audio, video) if s]
    duration = max((d for d in durations if d), default=0.0)

    return MediaInfo(
        duration_seconds=round(duration, 3),
        format_name=str(fmt.get("format_name") or "unknown"),
        format_long_name=str(fmt.get("format_long_name") or ""),
        size_bytes=size_bytes,
        has_audio=audio is not None,
        has_video=video is not None,
        audio_codec=audio.get("codec_name") if audio else None,
        sample_rate=int(audio["sample_rate"]) if audio and str(audio.get("sample_rate", "")).isdigit() else None,
        channels=audio.get("channels") if audio else None,
        video_codec=video.get("codec_name") if video else None,
        width=video.get("width") if video else None,
        height=video.get("height") if video else None,
        fps=_parse_fps(video.get("avg_frame_rate") or video.get("r_frame_rate")) if video else None,
        bit_rate=int(fmt["bit_rate"]) if str(fmt.get("bit_rate", "")).isdigit() else None,
    )


def probe_media(path: Path, tools: FFmpegTools) -> MediaInfo:
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise MediaError("The file is empty (0 bytes).")
    try:
        result = tools.run(
            [tools.ffprobe, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
            timeout=min(tools.timeout, 120),
            what="FFprobe",
        )
    except MediaError as exc:
        raise MediaError(
            f"FFprobe could not read this file, so it is corrupted or uses an unsupported container/codec. ({exc})"
        ) from exc
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise MediaError("FFprobe returned unreadable output for this file.") from exc
    return parse_probe_output(payload, path.stat().st_size)


def validate_media_info(info: MediaInfo, extension: str, max_duration_seconds: float) -> list[str]:
    """Raise MediaError for unusable media; return non-fatal warnings."""
    warnings: list[str] = []
    if not info.has_audio and not info.has_video:
        raise MediaError("No audio or video stream was found. The file may be corrupted or not a media file.")
    if info.duration_seconds <= 0:
        raise MediaError("The media duration could not be determined (0 seconds). The file may be corrupted.")
    if info.duration_seconds > max_duration_seconds:
        raise MediaError(
            f"The media is {format_timestamp(info.duration_seconds)} long, above the "
            f"{format_timestamp(max_duration_seconds)} limit (MAX_MEDIA_DURATION_MINUTES)."
        )
    if extension in AUDIO_EXTENSIONS - VIDEO_EXTENSIONS and info.has_video:
        warnings.append("This audio file contains a video stream; it will be processed as a video.")
    if extension in VIDEO_EXTENSIONS - AUDIO_EXTENSIONS and not info.has_video:
        warnings.append("No video stream was found in this video file; it will be processed as audio only.")
    if info.has_video and not info.has_audio:
        warnings.append("This video has no audio track: only keyframes will be indexed (no transcript).")
    return warnings


# ------------------------------------------------------------------ uploads
def media_id_from_hash(file_hash: str) -> str:
    return f"media_{file_hash[:16]}"


def check_media_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in MEDIA_EXTENSIONS:
        supported = ", ".join(sorted(MEDIA_EXTENSIONS))
        raise MediaError(f"'{filename}' has an unsupported media type ({extension or 'no extension'}). Supported: {supported}.")
    return extension


def save_stream(source: BinaryIO, target: Path, max_bytes: int) -> tuple[str, int]:
    """Copy an upload to disk in blocks while hashing it. Returns (sha256, size).

    The partial file is removed if anything goes wrong or the size limit is crossed.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    size = 0
    try:
        if hasattr(source, "seek"):
            source.seek(0)
        with open(target, "wb") as handle:
            while block := source.read(READ_BLOCK):
                size += len(block)
                if size > max_bytes:
                    raise MediaError(
                        f"The file is larger than the {max_bytes / 1_048_576:.0f} MB limit (MAX_MEDIA_UPLOAD_SIZE_MB)."
                    )
                digest.update(block)
                handle.write(block)
    except BaseException:
        target.unlink(missing_ok=True)
        raise
    if size == 0:
        target.unlink(missing_ok=True)
        raise MediaError("The file is empty (0 bytes).")
    return digest.hexdigest(), size


# --------------------------------------------------------------- formatting
def format_timestamp(seconds: float | None, *, millis: bool = False) -> str:
    """65.4 -> '00:01:05' (or '00:01:05,400' for SRT)."""
    if seconds is None:
        return "--:--:--"
    seconds = max(0.0, float(seconds))
    whole = int(seconds)
    h, rem = divmod(whole, 3600)
    m, s = divmod(rem, 60)
    text = f"{h:02d}:{m:02d}:{s:02d}"
    if millis:
        text += f",{int(round((seconds - whole) * 1000)) % 1000:03d}"
    return text


def format_time_range(start: float | None, end: float | None) -> str:
    return f"{format_timestamp(start)}–{format_timestamp(end)}"


_TIMESTAMP = re.compile(r"^\s*(?:(\d+):)?(\d{1,2}):(\d{1,2}(?:\.\d+)?)\s*$")


def parse_timestamp(text: str) -> float | None:
    """'00:12:30' / '12:30' / '75' -> seconds, or None if it is not a timestamp."""
    text = (text or "").strip()
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        return float(text)
    match = _TIMESTAMP.match(text)
    if not match:
        return None
    hours, minutes, secs = match.groups()
    return int(hours or 0) * 3600 + int(minutes) * 60 + float(secs)


def format_bytes(size: int | None) -> str:
    if not size:
        return "0 B"
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} GB"


def relative_to_data(path: Path, data_directory: Path) -> str:
    """Show paths relative to the data folder so the UI never reveals the user's home directory."""
    try:
        return str(Path(path).resolve().relative_to(Path(data_directory).resolve()))
    except ValueError:
        return Path(path).name


@dataclass
class StageLog:
    """Status of one processing stage, stored in the media registry so failed jobs can resume."""

    key: str
    name: str
    status: str = "pending"  # pending | running | done | reused | skipped | failed
    message: str = ""
    count: int | None = None
    seconds: float = 0.0
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
