"""Contract tests run against every adapter, plus adapter-specific persistence and validation tests."""

import pickle
from collections.abc import Callable
from pathlib import Path

import pytest

from app.core.exceptions import DocumentNotFoundError, VectorStoreError
from app.vectorstores.base import Chunk, DocumentInfo, VectorStore
from app.vectorstores.chroma_store import ChromaVectorStore
from app.vectorstores.faiss_store import FaissVectorStore
from app.vectorstores.pinecone_store import PineconeVectorStore
from tests.conftest import FakePineconeIndex

DIMENSION = 4


def _unit(axis: int) -> list[float]:
    return [1.0 if i == axis else 0.0 for i in range(DIMENSION)]


def _document(document_id: str, chunk_count: int) -> DocumentInfo:
    return DocumentInfo(
        document_id=document_id,
        filename=f"{document_id}.docx",
        chunk_count=chunk_count,
        uploaded_at="2026-01-01T00:00:00+00:00",
        title="Title" if document_id == "alpha" else None,
    )


def _chunks(document_id: str, texts: list[str]) -> list[Chunk]:
    document = _document(document_id, len(texts))
    return [Chunk(document=document, index=i, text=text) for i, text in enumerate(texts)]


def _chroma(tmp_path: Path) -> VectorStore:
    return ChromaVectorStore(tmp_path / "chroma", "test_collection", DIMENSION)


def _faiss(tmp_path: Path) -> VectorStore:
    return FaissVectorStore(tmp_path / "faiss" / "index.faiss", tmp_path / "faiss" / "metadata.pkl", DIMENSION)


@pytest.fixture(params=["chromadb", "faiss", "pinecone"])
def store(request: pytest.FixtureRequest, tmp_path: Path) -> VectorStore:
    if request.param == "chromadb":
        return _chroma(tmp_path)
    if request.param == "faiss":
        return _faiss(tmp_path)
    request.getfixturevalue("fake_pinecone")(FakePineconeIndex(dimension=DIMENSION))
    return PineconeVectorStore("pc-key", "test-index", "test-namespace", DIMENSION)


def _add_two_documents(store: VectorStore) -> None:
    store.add(_chunks("alpha", ["alpha zero", "alpha one"]), [_unit(0), _unit(1)])
    store.add(_chunks("beta", ["beta zero"]), [_unit(2)])


def test_search_on_empty_store_returns_nothing(store: VectorStore) -> None:
    assert store.search(_unit(0), top_k=3) == []


def test_search_ranks_by_similarity_and_returns_metadata(store: VectorStore) -> None:
    _add_two_documents(store)

    results = store.search([0.1, 0.9, 0.0, 0.0], top_k=2)

    assert [result.chunk.text for result in results] == ["alpha one", "alpha zero"]
    best = results[0]
    assert best.chunk.document.document_id == "alpha"
    assert best.chunk.document.filename == "alpha.docx"
    assert best.chunk.document.title == "Title"
    assert best.chunk.index == 1
    assert best.score > results[1].score


def test_top_k_larger_than_store_returns_all_chunks(store: VectorStore) -> None:
    _add_two_documents(store)
    assert len(store.search(_unit(0), top_k=10)) == 3


def test_list_documents_and_exists(store: VectorStore) -> None:
    _add_two_documents(store)

    documents = {document.document_id: document for document in store.list_documents()}

    assert set(documents) == {"alpha", "beta"}
    assert documents["alpha"].chunk_count == 2
    assert documents["beta"].title is None
    assert store.document_exists("alpha")
    assert not store.document_exists("gamma")


def test_delete_removes_only_the_target_document(store: VectorStore) -> None:
    _add_two_documents(store)

    store.delete_document("alpha")

    assert [document.document_id for document in store.list_documents()] == ["beta"]
    assert not store.document_exists("alpha")
    results = store.search(_unit(0), top_k=10)
    assert [result.chunk.document.document_id for result in results] == ["beta"]


def test_delete_unknown_document_raises(store: VectorStore) -> None:
    with pytest.raises(DocumentNotFoundError):
        store.delete_document("missing")


def test_wrong_dimension_is_rejected(store: VectorStore) -> None:
    with pytest.raises(VectorStoreError, match="dimension"):
        store.add(_chunks("alpha", ["text"]), [[1.0, 0.0]])
    with pytest.raises(VectorStoreError, match="dimension"):
        store.search([1.0, 0.0], top_k=1)


@pytest.mark.parametrize("factory", [_chroma, _faiss], ids=["chromadb", "faiss"])
def test_local_stores_persist_across_restarts(factory: Callable[[Path], VectorStore], tmp_path: Path) -> None:
    first = factory(tmp_path)
    _add_two_documents(first)
    first.delete_document("beta")

    reopened = factory(tmp_path)

    assert [document.document_id for document in reopened.list_documents()] == ["alpha"]
    assert reopened.search(_unit(1), top_k=1)[0].chunk.text == "alpha one"


def test_chroma_rejects_collection_with_other_dimension(tmp_path: Path) -> None:
    _chroma(tmp_path)
    with pytest.raises(VectorStoreError, match="dimension"):
        ChromaVectorStore(tmp_path / "chroma", "test_collection", DIMENSION + 1)


class TestFaissPersistence:
    def test_rejects_corrupt_index(self, tmp_path: Path) -> None:
        _add_two_documents(_faiss(tmp_path))
        (tmp_path / "faiss" / "index.faiss").write_bytes(b"corrupt")
        with pytest.raises(VectorStoreError, match="corrupt"):
            _faiss(tmp_path)

    def test_rejects_missing_metadata_file(self, tmp_path: Path) -> None:
        _add_two_documents(_faiss(tmp_path))
        (tmp_path / "faiss" / "metadata.pkl").unlink()
        with pytest.raises(VectorStoreError, match="out of sync"):
            _faiss(tmp_path)

    def test_rejects_metadata_count_mismatch(self, tmp_path: Path) -> None:
        _add_two_documents(_faiss(tmp_path))
        metadata_path = tmp_path / "faiss" / "metadata.pkl"
        metadata = pickle.loads(metadata_path.read_bytes())
        metadata["chunks"].popitem()
        metadata_path.write_bytes(pickle.dumps(metadata))
        with pytest.raises(VectorStoreError, match="different numbers"):
            _faiss(tmp_path)

    def test_rejects_index_with_other_dimension(self, tmp_path: Path) -> None:
        _add_two_documents(_faiss(tmp_path))
        with pytest.raises(VectorStoreError, match="dimension"):
            FaissVectorStore(tmp_path / "faiss" / "index.faiss", tmp_path / "faiss" / "metadata.pkl", DIMENSION + 1)

    def test_failed_save_keeps_memory_consistent(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        store = _faiss(tmp_path)
        _add_two_documents(store)

        def failing_save() -> None:
            raise OSError("disk full")

        monkeypatch.setattr(store, "_save", failing_save)
        with pytest.raises(VectorStoreError):
            store.delete_document("alpha")
        with pytest.raises(VectorStoreError):
            store.add(_chunks("gamma", ["gamma"]), [_unit(3)])

        assert {document.document_id for document in store.list_documents()} == {"alpha", "beta"}
        assert len(store.search(_unit(0), top_k=10)) == 3


class TestPineconeValidation:
    def test_rejects_index_with_other_dimension(self, fake_pinecone) -> None:
        fake_pinecone(FakePineconeIndex(dimension=DIMENSION + 1))
        with pytest.raises(VectorStoreError, match="dimension"):
            PineconeVectorStore("pc-key", "test-index", "ns", DIMENSION)

    def test_rejects_non_cosine_metric(self, fake_pinecone) -> None:
        fake_pinecone(FakePineconeIndex(dimension=DIMENSION, metric="euclidean"))
        with pytest.raises(VectorStoreError, match="cosine"):
            PineconeVectorStore("pc-key", "test-index", "ns", DIMENSION)

    def test_connection_failure_raises_vector_store_error(self, fake_pinecone) -> None:
        index = fake_pinecone(FakePineconeIndex(dimension=DIMENSION))

        def unreachable() -> None:
            raise ConnectionError("network down")

        index.describe_index_stats = unreachable
        with pytest.raises(VectorStoreError, match="connect"):
            PineconeVectorStore("pc-key", "test-index", "ns", DIMENSION)

    def test_namespaces_are_isolated(self, fake_pinecone) -> None:
        fake_pinecone(FakePineconeIndex(dimension=DIMENSION))
        first = PineconeVectorStore("pc-key", "test-index", "first", DIMENSION)
        second = PineconeVectorStore("pc-key", "test-index", "second", DIMENSION)
        first.add(_chunks("alpha", ["alpha zero"]), [_unit(0)])
        assert second.list_documents() == []
        assert second.search(_unit(0), top_k=1) == []

    def test_lists_and_deletes_documents_across_pages(self, fake_pinecone) -> None:
        fake_pinecone(FakePineconeIndex(dimension=DIMENSION))
        store = PineconeVectorStore("pc-key", "test-index", "ns", DIMENSION)
        texts = [f"chunk {i}" for i in range(250)]
        store.add(_chunks("alpha", texts), [_unit(i % DIMENSION) for i in range(250)])
        store.add(_chunks("beta", ["beta"]), [_unit(0)])

        store.delete_document("alpha")

        assert [document.document_id for document in store.list_documents()] == ["beta"]
