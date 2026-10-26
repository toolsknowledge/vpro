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
    )
