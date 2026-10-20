import pytest
from pydantic import ValidationError

from tests.conftest import make_settings


def test_defaults_are_valid_without_pinecone_credentials() -> None:
    settings = make_settings()
    assert settings.vector_db == "chromadb"
    assert settings.chunk_size == 800
    assert settings.chunk_overlap == 150
    assert settings.top_k == 4
    assert settings.embedding_model == "sentence-transformers/all-MiniLM-L6-v2"


@pytest.mark.parametrize("vector_db", ["chromadb", "faiss"])
def test_local_databases_do_not_require_pinecone_settings(vector_db: str) -> None:
    assert make_settings(vector_db=vector_db).vector_db == vector_db


def test_vector_db_is_case_insensitive() -> None:
    assert make_settings(vector_db=" FAISS ").vector_db == "faiss"


def test_unknown_vector_db_is_rejected() -> None:
    with pytest.raises(ValidationError):
        make_settings(vector_db="milvus")


@pytest.mark.parametrize(
    "overrides",
    [
        {"pinecone_index_name": "docs"},
        {"pinecone_api_key": "your_pinecone_api_key", "pinecone_index_name": "docs"},
        {"pinecone_api_key": "pc-key"},
    ],
)
def test_pinecone_requires_credentials_and_index(overrides: dict[str, str]) -> None:
    with pytest.raises(ValidationError, match="PINECONE"):
        make_settings(vector_db="pinecone", **overrides)


def test_pinecone_with_credentials_is_valid() -> None:
    settings = make_settings(vector_db="pinecone", pinecone_api_key="pc-key", pinecone_index_name="docs")
    assert settings.pinecone_namespace == "rag-documents"


@pytest.mark.parametrize("key", ["", "your_openai_api_key"])
def test_openai_key_is_required(key: str) -> None:
    with pytest.raises(ValidationError, match="OPENAI_API_KEY"):
        make_settings(openai_api_key=key)


def test_overlap_must_be_smaller_than_chunk_size() -> None:
    with pytest.raises(ValidationError, match="CHUNK_OVERLAP"):
        make_settings(chunk_size=100, chunk_overlap=100)


def test_settings_load_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VECTOR_DB", "faiss")
    monkeypatch.setenv("TOP_K", "7")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:4200, http://example.test")
    settings = make_settings()
    assert settings.vector_db == "faiss"
    assert settings.top_k == 7
    assert settings.cors_origins == ["http://localhost:4200", "http://example.test"]


def test_secrets_are_not_exposed_in_repr() -> None:
    assert "sk-test-key" not in repr(make_settings())
