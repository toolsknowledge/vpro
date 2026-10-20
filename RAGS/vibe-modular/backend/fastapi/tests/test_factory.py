from pathlib import Path

import pytest

from app.vectorstores.chroma_store import ChromaVectorStore
from app.vectorstores.factory import create_vector_store
from app.vectorstores.faiss_store import FaissVectorStore
from app.vectorstores.pinecone_store import PineconeVectorStore
from tests.conftest import FAKE_DIMENSION, make_settings


def _settings(vector_db: str, tmp_path: Path, **overrides):
    return make_settings(
        vector_db=vector_db,
        chroma_persist_directory=tmp_path / "chroma",
        faiss_index_path=tmp_path / "faiss" / "index.faiss",
        faiss_metadata_path=tmp_path / "faiss" / "metadata.pkl",
        **overrides,
    )


@pytest.mark.parametrize(("vector_db", "expected"), [("chromadb", ChromaVectorStore), ("faiss", FaissVectorStore)])
def test_selects_local_store_from_settings(vector_db: str, expected: type, tmp_path: Path) -> None:
    store = create_vector_store(_settings(vector_db, tmp_path), FAKE_DIMENSION)
    assert type(store) is expected
    assert store.dimension == FAKE_DIMENSION


def test_selects_pinecone_from_settings(tmp_path: Path, fake_pinecone) -> None:
    settings = _settings("pinecone", tmp_path, pinecone_api_key="pc-key", pinecone_index_name="docs")
    store = create_vector_store(settings, FAKE_DIMENSION)
    assert type(store) is PineconeVectorStore
