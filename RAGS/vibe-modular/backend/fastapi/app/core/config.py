"""Central application configuration loaded from environment variables and `.env`."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal, Self

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

VectorDbName = Literal["chromadb", "faiss", "pinecone"]

PLACEHOLDER_PREFIX = "your_"


def _is_missing(secret: SecretStr | None) -> bool:
    if secret is None:
        return True
    value = secret.get_secret_value().strip()
    return not value or value.startswith(PLACEHOLDER_PREFIX)


class Settings(BaseSettings):
    # hide_input_in_errors keeps secrets out of validation error messages and startup logs.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", hide_input_in_errors=True
    )

    openai_api_key: SecretStr
    openai_model: str = "gpt-4.1-mini"
    openai_timeout_seconds: float = Field(default=30.0, gt=0)

    vector_db: VectorDbName = "chromadb"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    chunk_size: int = Field(default=800, gt=0)
    chunk_overlap: int = Field(default=150, ge=0)
    top_k: int = Field(default=4, ge=1, le=20)

    chroma_persist_directory: Path = Path("./data/chroma")
    chroma_collection_name: str = "rag_documents"

    faiss_index_path: Path = Path("./data/faiss/index.faiss")
    faiss_metadata_path: Path = Path("./data/faiss/metadata.pkl")

    pinecone_api_key: SecretStr | None = None
    pinecone_index_name: str | None = None
    pinecone_namespace: str = "rag-documents"

    max_upload_size_mb: int = Field(default=10, gt=0)
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:4200"]

    @field_validator("vector_db", mode="before")
    @classmethod
    def _normalize_vector_db(cls, value: object) -> object:
        return value.strip().lower() if isinstance(value, str) else value

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def _validate_settings(self) -> Self:
        if _is_missing(self.openai_api_key):
            raise ValueError("OPENAI_API_KEY must be set to a real OpenAI API key.")
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE.")
        if self.vector_db == "pinecone":
            if _is_missing(self.pinecone_api_key):
                raise ValueError("PINECONE_API_KEY is required when VECTOR_DB=pinecone.")
            if not self.pinecone_index_name or self.pinecone_index_name.startswith(PLACEHOLDER_PREFIX):
                raise ValueError("PINECONE_INDEX_NAME is required when VECTOR_DB=pinecone.")
        return self

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
