"""Centralised application configuration.

All values come from environment variables (or ``backend/.env``). Relative paths
are resolved against the backend directory so the app behaves the same no matter
which directory it is started from.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent
SAMPLE_DOCUMENTS_DIR = BACKEND_DIR / "data" / "sample_documents"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "VPRO Skills Adaptive RAG Assistant"

    openai_api_key: SecretStr | None = None
    openai_chat_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_timeout_seconds: float = Field(default=60.0, gt=0)
    openai_max_retries: int = Field(default=2, ge=0, le=10)

    chroma_persist_directory: Path = Path("./storage/chroma")
    chroma_collection_name: str = Field(default="vpro_adaptive_rag", min_length=3, max_length=63)
    documents_directory: Path = SAMPLE_DOCUMENTS_DIR
    indexing_state_file: Path = Path("./storage/last_indexing_result.json")

    chunk_size: int = Field(default=800, ge=100, le=8000)
    chunk_overlap: int = Field(default=120, ge=0)
    top_k: int = Field(default=5, ge=1, le=20)
    relevance_threshold: float = Field(default=0.35, ge=0.0, le=1.0)
    embedding_batch_size: int = Field(default=64, ge=1, le=2048)

    answer_temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    classifier_temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    max_history_turns: int = Field(default=6, ge=0, le=20)
    max_sessions: int = Field(default=500, ge=1)
    session_ttl_minutes: int = Field(default=120, ge=1)

    frontend_origin: str = "http://localhost:5173"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    log_level: str = "INFO"

    @field_validator("openai_api_key", mode="before")
    @classmethod
    def _blank_key_is_missing(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("chroma_persist_directory", "documents_directory", "indexing_state_file")
    @classmethod
    def _resolve_path(cls, value: Path) -> Path:
        return value if value.is_absolute() else (BACKEND_DIR / value).resolve()

    @model_validator(mode="after")
    def _check_overlap(self) -> "Settings":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
        return self

    @property
    def openai_configured(self) -> bool:
        return self.openai_api_key is not None

    @property
    def cors_origins(self) -> list[str]:
        """FRONTEND_ORIGIN may hold one origin or a comma-separated list."""
        return [origin.strip().rstrip("/") for origin in self.frontend_origin.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
