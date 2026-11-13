"""Application settings.

All configuration comes from environment variables (optionally loaded from a
local ``.env`` file).  Nothing secret is hard-coded, and the API key is never
included in ``repr()`` so it cannot leak into logs by accident.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Optional

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER_KEY = "your_openai_api_key_here"

APP_NAME = "VPro Skills EduTech — Smart Document RAG Assistant"
SUPPORTED_EXTENSIONS = (".pdf", ".xlsx", ".xls", ".docx", ".txt")


class ConfigError(Exception):
    """Raised when a configuration value is invalid."""


def _int(env: Mapping[str, str], name: str, default: int) -> int:
    raw = env.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be a whole number, got {raw!r}.") from exc


def _path(raw: str) -> Path:
    p = Path(raw).expanduser()
    return p if p.is_absolute() else (PROJECT_ROOT / p).resolve()


@dataclass(frozen=True)
class Settings:
    openai_api_key: Optional[str] = field(default=None, repr=False)
    chat_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    chroma_dir: Path = PROJECT_ROOT / "data" / "chroma_db"
    collection_name: str = "vpro_document_knowledge"
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 5
    max_upload_mb: int = 20
    data_dir: Path = PROJECT_ROOT / "data"

    @property
    def uploads_dir(self) -> Path:
        return self.data_dir / "uploads"

    @property
    def processed_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def registry_path(self) -> Path:
        return self.data_dir / "document_registry.json"

    @property
    def sample_dir(self) -> Path:
        return PROJECT_ROOT / "sample_files"

    @property
    def has_api_key(self) -> bool:
        key = (self.openai_api_key or "").strip()
        return bool(key) and key != PLACEHOLDER_KEY

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @classmethod
    def from_env(cls, environ: Optional[Mapping[str, str]] = None, load_env_file: bool = True) -> "Settings":
        if environ is None:
            if load_env_file:
                load_dotenv(PROJECT_ROOT / ".env", override=False)
            environ = os.environ
        s = cls(
            openai_api_key=environ.get("OPENAI_API_KEY") or None,
            chat_model=environ.get("OPENAI_CHAT_MODEL", "").strip() or "gpt-4.1-mini",
            embedding_model=environ.get("OPENAI_EMBEDDING_MODEL", "").strip() or "text-embedding-3-small",
            chroma_dir=_path(environ.get("CHROMA_PERSIST_DIRECTORY", "").strip() or "./data/chroma_db"),
            collection_name=environ.get("CHROMA_COLLECTION_NAME", "").strip() or "vpro_document_knowledge",
            chunk_size=_int(environ, "CHUNK_SIZE", 800),
            chunk_overlap=_int(environ, "CHUNK_OVERLAP", 120),
            top_k=_int(environ, "TOP_K", 5),
            max_upload_mb=_int(environ, "MAX_UPLOAD_SIZE_MB", 20),
            data_dir=_path(environ.get("DATA_DIRECTORY", "").strip() or "./data"),
        )
        return s

    def problems(self) -> list[str]:
        """Human-readable configuration problems (empty list == healthy)."""
        out: list[str] = []
        if not self.has_api_key:
            out.append(
                "OPENAI_API_KEY is missing. Copy `.env.example` to `.env`, paste your OpenAI API key "
                "(created at platform.openai.com → API keys) and restart the app. "
                "Note: API billing is separate from a ChatGPT subscription."
            )
        if self.chunk_size <= 0:
            out.append("CHUNK_SIZE must be greater than 0.")
        if not (0 <= self.chunk_overlap < max(self.chunk_size, 1)):
            out.append("CHUNK_OVERLAP must be at least 0 and smaller than CHUNK_SIZE.")
        if self.top_k <= 0:
            out.append("TOP_K must be greater than 0.")
        if self.max_upload_mb <= 0:
            out.append("MAX_UPLOAD_SIZE_MB must be greater than 0.")
        if not self.collection_name or len(self.collection_name) < 3:
            out.append("CHROMA_COLLECTION_NAME must be at least 3 characters.")
        return out

    def ensure_dirs(self) -> None:
        for d in (self.data_dir, self.uploads_dir, self.processed_dir, self.chroma_dir):
            d.mkdir(parents=True, exist_ok=True)
