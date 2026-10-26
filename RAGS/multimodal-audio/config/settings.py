"""Application configuration.

All settings come from environment variables (optionally loaded from a `.env`
file). Nothing secret is ever printed: use `Settings.public_summary()` when you
need to show configuration to a user.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Project root = the folder that contains app.py
BASE_DIR = Path(__file__).resolve().parent.parent

SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".xlsx": "excel",
    ".xls": "excel",
    ".docx": "word",
    ".txt": "text",
}

# Audio and video containers accepted by the media pipeline. The real content is
# always checked with ffprobe; the extension only decides which uploader accepts it.
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".webm"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
MEDIA_EXTENSIONS = AUDIO_EXTENSIONS | VIDEO_EXTENSIONS

# The OpenAI transcription endpoint rejects files above 25 MB. We stay below it.
TRANSCRIPTION_UPLOAD_LIMIT_BYTES = 24 * 1024 * 1024

# Limits that keep chunking sensible for the embedding model (8191 token input limit).
MIN_CHUNK_SIZE = 50
MAX_CHUNK_SIZE = 8000
MAX_TOP_K = 50


class ConfigError(ValueError):
    """Raised when configuration values are invalid."""


def _resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    return path.resolve()


def _read_int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be a whole number, got {raw!r}.") from exc


def _read_optional_float(name: str, default: float | None) -> float | None:
    raw = os.getenv(name)
    if raw is None:
        return default
    raw = raw.strip()
    if not raw:
        return None  # explicitly blank = "do not send this parameter"
    try:
        return float(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be a number, got {raw!r}.") from exc


def validate_chunk_settings(chunk_size: int, chunk_overlap: int) -> None:
    """Raise ConfigError if chunk size / overlap make no sense."""
    if not MIN_CHUNK_SIZE <= chunk_size <= MAX_CHUNK_SIZE:
        raise ConfigError(
            f"Chunk size must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE} tokens "
            f"(got {chunk_size})."
        )
    if chunk_overlap < 0:
        raise ConfigError("Chunk overlap cannot be negative.")
    if chunk_overlap >= chunk_size // 2:
        raise ConfigError(
            f"Chunk overlap ({chunk_overlap}) must be less than half the chunk size "
            f"({chunk_size}); otherwise chunks would mostly repeat each other."
        )


def validate_top_k(top_k: int) -> None:
    if not 1 <= top_k <= MAX_TOP_K:
        raise ConfigError(f"Top K must be between 1 and {MAX_TOP_K} (got {top_k}).")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = field(repr=False)
    chat_model: str
    embedding_model: str
    chat_temperature: float | None
    chroma_persist_directory: Path
    chroma_collection_name: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    max_upload_size_mb: int
    data_directory: Path
    # ---- audio / video (all have defaults so older callers keep working)
    transcription_model: str = "gpt-4o-mini-transcribe"
    vision_model: str = "gpt-4.1-mini"
    transcription_language: str = ""  # ISO-639-1 hint such as "en"; blank = auto-detect
    transcription_prompt: str = ""  # vocabulary hint, e.g. "VPro Skills, RAG, ChromaDB"
    audio_chunk_seconds: int = 300
    timestamp_fallback_seconds: int = 30
    video_frame_interval_seconds: int = 10
    max_media_upload_size_mb: int = 200
    max_media_duration_minutes: int = 180
    max_frames_per_video: int = 500
    media_top_k: int = 5
    ffmpeg_binary: str = "ffmpeg"
    ffprobe_binary: str = "ffprobe"
    ffmpeg_timeout_seconds: int = 600
    audio_collection_name: str = "vpro_audio_transcripts"
    video_transcript_collection_name: str = "vpro_video_transcripts"
    video_frame_collection_name: str = "vpro_video_frames"

    @property
    def has_api_key(self) -> bool:
        key = self.openai_api_key.strip()
        return bool(key) and key != "your_openai_api_key_here"

    @property
    def uploads_directory(self) -> Path:
        return self.data_directory / "uploads"

    @property
    def traces_directory(self) -> Path:
        return self.data_directory / "traces"

    @property
    def registry_path(self) -> Path:
        return self.data_directory / "document_registry.json"

    @property
    def media_registry_path(self) -> Path:
        return self.data_directory / "media_registry.json"

    @property
    def media_uploads_directory(self) -> Path:
        return self.data_directory / "uploads" / "media"

    @property
    def extracted_audio_directory(self) -> Path:
        return self.data_directory / "extracted_audio"

    @property
    def video_frames_directory(self) -> Path:
        return self.data_directory / "video_frames"

    @property
    def transcripts_directory(self) -> Path:
        return self.data_directory / "transcripts"

    @property
    def max_media_upload_bytes(self) -> int:
        return self.max_media_upload_size_mb * 1024 * 1024

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    def validate(self) -> list[str]:
        """Return a list of human-readable problems (empty list = all good)."""
        problems: list[str] = []
        if not self.has_api_key:
            problems.append(
                "OPENAI_API_KEY is missing. Copy .env.example to .env and paste your "
                "OpenAI API key (API billing is separate from a ChatGPT subscription)."
            )
        if not self.chat_model:
            problems.append("OPENAI_CHAT_MODEL is empty.")
        if not self.embedding_model:
            problems.append("OPENAI_EMBEDDING_MODEL is empty.")
        if not self.chroma_collection_name:
            problems.append("CHROMA_COLLECTION_NAME is empty.")
        try:
            validate_chunk_settings(self.chunk_size, self.chunk_overlap)
        except ConfigError as exc:
            problems.append(str(exc))
        try:
            validate_top_k(self.top_k)
        except ConfigError as exc:
            problems.append(str(exc))
        if self.max_upload_size_mb <= 0:
            problems.append("MAX_UPLOAD_SIZE_MB must be greater than 0.")
        problems.extend(self.validate_media())
        return problems

    def validate_media(self) -> list[str]:
        problems: list[str] = []
        if not self.transcription_model:
            problems.append("OPENAI_TRANSCRIPTION_MODEL is empty.")
        if not self.vision_model:
            problems.append("OPENAI_VISION_MODEL is empty.")
        if not 30 <= self.audio_chunk_seconds <= 1200:
            problems.append("AUDIO_CHUNK_SECONDS must be between 30 and 1200.")
        if not 5 <= self.timestamp_fallback_seconds <= self.audio_chunk_seconds:
            problems.append("TIMESTAMP_FALLBACK_SECONDS must be between 5 and AUDIO_CHUNK_SECONDS.")
        if self.video_frame_interval_seconds < 1:
            problems.append("VIDEO_FRAME_INTERVAL_SECONDS must be at least 1.")
        if self.max_media_upload_size_mb <= 0:
            problems.append("MAX_MEDIA_UPLOAD_SIZE_MB must be greater than 0.")
        if self.max_media_duration_minutes <= 0:
            problems.append("MAX_MEDIA_DURATION_MINUTES must be greater than 0.")
        if self.max_frames_per_video < 1:
            problems.append("MAX_FRAMES_PER_VIDEO must be at least 1.")
        try:
            validate_top_k(self.media_top_k)
        except ConfigError as exc:
            problems.append(f"MEDIA_TOP_K: {exc}")
        names = [self.chroma_collection_name, self.audio_collection_name,
                 self.video_transcript_collection_name, self.video_frame_collection_name]
        if len(set(names)) != len(names):
            problems.append("The four ChromaDB collection names must all be different.")
        return problems

    def public_summary(self) -> dict[str, str]:
        """Configuration that is safe to display. Never includes the API key."""
        return {
            "OpenAI API key": "configured" if self.has_api_key else "missing",
            "Chat model": self.chat_model,
            "Embedding model": self.embedding_model,
            "Chat temperature": "model default" if self.chat_temperature is None else str(self.chat_temperature),
            "Chroma persist directory": str(self.chroma_persist_directory),
            "Chroma collection": self.chroma_collection_name,
            "Default chunk size (tokens)": str(self.chunk_size),
            "Default chunk overlap (tokens)": str(self.chunk_overlap),
            "Default top K": str(self.top_k),
            "Max upload size (MB)": str(self.max_upload_size_mb),
            "Transcription model": self.transcription_model,
            "Vision model": self.vision_model,
            "Transcription language hint": self.transcription_language or "auto-detect",
            "Transcription vocabulary prompt": self.transcription_prompt or "(none)",
            "Audio split length (s)": str(self.audio_chunk_seconds),
            "Timestamp fallback window (s)": str(self.timestamp_fallback_seconds),
            "Video frame interval (s)": str(self.video_frame_interval_seconds),
            "Max media upload (MB)": str(self.max_media_upload_size_mb),
            "Max media duration (min)": str(self.max_media_duration_minutes),
            "Max frames per video": str(self.max_frames_per_video),
            "Media top K": str(self.media_top_k),
            "Media collections": ", ".join(
                [self.audio_collection_name, self.video_transcript_collection_name, self.video_frame_collection_name]
            ),
        }


def load_settings(env_file: Path | None = None, *, use_dotenv: bool = True) -> Settings:
    """Read settings from the environment (and `.env` if present)."""
    if use_dotenv:
        load_dotenv(env_file or BASE_DIR / ".env", override=False)

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        chat_model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini").strip(),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small").strip(),
        chat_temperature=_read_optional_float("OPENAI_CHAT_TEMPERATURE", 0.1),
        chroma_persist_directory=_resolve_path(os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")),
        chroma_collection_name=os.getenv("CHROMA_COLLECTION_NAME", "vpro_document_knowledge").strip(),
        chunk_size=_read_int("CHUNK_SIZE", 800),
        chunk_overlap=_read_int("CHUNK_OVERLAP", 120),
        top_k=_read_int("TOP_K", 5),
        max_upload_size_mb=_read_int("MAX_UPLOAD_SIZE_MB", 20),
        data_directory=_resolve_path(os.getenv("DATA_DIRECTORY", "./data")),
        transcription_model=os.getenv("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe").strip(),
        vision_model=os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini").strip(),
        transcription_language=os.getenv("TRANSCRIPTION_LANGUAGE", "").strip(),
        transcription_prompt=os.getenv("TRANSCRIPTION_PROMPT", "").strip(),
        audio_chunk_seconds=_read_int("AUDIO_CHUNK_SECONDS", 300),
        timestamp_fallback_seconds=_read_int("TIMESTAMP_FALLBACK_SECONDS", 30),
        video_frame_interval_seconds=_read_int("VIDEO_FRAME_INTERVAL_SECONDS", 10),
        max_media_upload_size_mb=_read_int("MAX_MEDIA_UPLOAD_SIZE_MB", 200),
        max_media_duration_minutes=_read_int("MAX_MEDIA_DURATION_MINUTES", 180),
        max_frames_per_video=_read_int("MAX_FRAMES_PER_VIDEO", 500),
        media_top_k=_read_int("MEDIA_TOP_K", 5),
        ffmpeg_binary=os.getenv("FFMPEG_BINARY", "ffmpeg").strip() or "ffmpeg",
        ffprobe_binary=os.getenv("FFPROBE_BINARY", "ffprobe").strip() or "ffprobe",
        ffmpeg_timeout_seconds=_read_int("FFMPEG_TIMEOUT_SECONDS", 600),
        audio_collection_name=os.getenv("CHROMA_AUDIO_COLLECTION", "vpro_audio_transcripts").strip(),
        video_transcript_collection_name=os.getenv("CHROMA_VIDEO_TRANSCRIPT_COLLECTION", "vpro_video_transcripts").strip(),
        video_frame_collection_name=os.getenv("CHROMA_VIDEO_FRAME_COLLECTION", "vpro_video_frames").strip(),
    )
