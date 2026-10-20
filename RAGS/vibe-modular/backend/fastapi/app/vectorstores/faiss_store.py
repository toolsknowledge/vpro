"""FAISS adapter: an inner-product index with a pickled metadata file, both persisted locally."""

import logging
import os
import pickle
import threading
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from app.core.exceptions import DocumentNotFoundError, VectorStoreError
from app.vectorstores.base import Chunk, DocumentInfo, SearchResult, VectorStore, store_errors

logger = logging.getLogger(__name__)

STORE_NAME = "FAISS"


def _to_matrix(vectors: Sequence[Sequence[float]]) -> np.ndarray:
    return np.asarray(vectors, dtype="float32")


class FaissVectorStore(VectorStore):
    """Vectors live in an IndexIDMap2 so chunks can be removed by ID; metadata maps those IDs to chunks."""

    def __init__(self, index_path: Path, metadata_path: Path, dimension: int) -> None:
        super().__init__(dimension)
        self._index_path = index_path
        self._metadata_path = metadata_path
        self._lock = threading.Lock()
        self._index, self._chunks, self._next_id = self._load()

    def _load(self) -> tuple[faiss.Index, dict[int, dict[str, Any]], int]:
        index_exists, metadata_exists = self._index_path.exists(), self._metadata_path.exists()
        if not index_exists and not metadata_exists:
            return faiss.IndexIDMap2(faiss.IndexFlatIP(self.dimension)), {}, 0
        if index_exists != metadata_exists:
            raise VectorStoreError(
                "The FAISS index and metadata files are out of sync (one is missing). "
                "Restore both files or delete both to start a new index."
            )

        try:
            index = faiss.read_index(str(self._index_path))
            with self._metadata_path.open("rb") as file:
                metadata = pickle.load(file)
            chunks, next_id = metadata["chunks"], metadata["next_id"]
        except Exception as exc:
            raise VectorStoreError("The persisted FAISS index or metadata file is corrupt.") from exc

        if index.d != self.dimension:
            raise VectorStoreError(
                f"The FAISS index has dimension {index.d}, but the embedding model produces {self.dimension}."
            )
        if index.ntotal != len(chunks):
            raise VectorStoreError("The FAISS index and metadata files contain different numbers of chunks.")
        logger.info("faiss_index_loaded chunks=%d", index.ntotal)
        return index, chunks, next_id

    def _save(self) -> None:
        """Write to temporary files and atomically replace, so a crash never leaves a half-written file."""
        self._index_path.parent.mkdir(parents=True, exist_ok=True)
        self._metadata_path.parent.mkdir(parents=True, exist_ok=True)
        index_tmp = self._index_path.with_suffix(self._index_path.suffix + ".tmp")
        metadata_tmp = self._metadata_path.with_suffix(self._metadata_path.suffix + ".tmp")

        faiss.write_index(self._index, str(index_tmp))
        with metadata_tmp.open("wb") as file:
            pickle.dump({"chunks": self._chunks, "next_id": self._next_id}, file)
        os.replace(index_tmp, self._index_path)
        os.replace(metadata_tmp, self._metadata_path)

    def add(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        self._validate_embeddings(chunks, embeddings)
        if not chunks:
            return
        with self._lock, store_errors(STORE_NAME, "add chunks"):
            ids = np.arange(self._next_id, self._next_id + len(chunks), dtype="int64")
            self._index.add_with_ids(_to_matrix(embeddings), ids)
            self._chunks.update({int(i): chunk.to_metadata() for i, chunk in zip(ids, chunks, strict=True)})
            self._next_id += len(chunks)
            try:
                self._save()
            except Exception:
                self._index.remove_ids(ids)
                for i in ids:
                    self._chunks.pop(int(i))
                self._next_id -= len(chunks)
                raise

    def search(self, embedding: Sequence[float], top_k: int) -> list[SearchResult]:
        self._validate_dimension(embedding)
        with self._lock, store_errors(STORE_NAME, "search"):
            if self._index.ntotal == 0:
                return []
            scores, ids = self._index.search(_to_matrix([embedding]), min(top_k, self._index.ntotal))
            return [
                SearchResult(chunk=Chunk.from_metadata(self._chunks[int(i)]), score=float(score))
                for score, i in zip(scores[0], ids[0], strict=True)
                if i != -1
            ]

    def list_documents(self) -> list[DocumentInfo]:
        with self._lock:
            return [
                Chunk.from_metadata(metadata).document
                for metadata in self._chunks.values()
                if metadata["chunk_index"] == 0
            ]

    def document_exists(self, document_id: str) -> bool:
        with self._lock:
            return any(metadata["document_id"] == document_id for metadata in self._chunks.values())

    def delete_document(self, document_id: str) -> None:
        with self._lock, store_errors(STORE_NAME, "delete a document"):
            ids = [i for i, metadata in self._chunks.items() if metadata["document_id"] == document_id]
            if not ids:
                raise DocumentNotFoundError(f"Document '{document_id}' was not found.")
            id_array = np.asarray(ids, dtype="int64")
            vectors = np.vstack([self._index.reconstruct(i) for i in ids])
            removed = {i: self._chunks.pop(i) for i in ids}
            self._index.remove_ids(id_array)
            try:
                self._save()
            except Exception:
                # Restore the in-memory state so it keeps matching the files on disk.
                self._index.add_with_ids(vectors, id_array)
                self._chunks.update(removed)
                raise
