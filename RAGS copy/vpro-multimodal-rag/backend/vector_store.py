"""Step 6: persistent ChromaDB storage.

The collection uses *cosine* distance (``hnsw:space = cosine``).  For cosine,
Chroma returns ``distance = 1 - cosine_similarity`` (0 = identical direction).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence

import chromadb

from backend.errors import EmbeddingModelMismatchError, VectorStoreError
from backend.models import Chunk

DISTANCE_METRIC = "cosine"


class VectorStore:
    def __init__(self, persist_dir: Path, collection_name: str, embedding_model: str):
        self.persist_dir = Path(persist_dir)
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        try:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=str(self.persist_dir))
            self._collection = self._open()
        except Exception as exc:
            raise VectorStoreError(f"Could not open the ChromaDB database at {self.persist_dir}: {exc}") from exc

    def _open(self):
        return self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": DISTANCE_METRIC, "embedding_model": self.embedding_model},
            embedding_function=None,  # we always supply our own OpenAI vectors
        )

    @property
    def collection(self):
        return self._collection

    # ---- info ----
    @property
    def distance_metric(self) -> str:
        return (self._collection.metadata or {}).get("hnsw:space", DISTANCE_METRIC)

    @property
    def stored_model(self) -> str:
        return (self._collection.metadata or {}).get("embedding_model", "")

    def count(self) -> int:
        return self._collection.count()

    def stored_dimension(self) -> Optional[int]:
        if self.count() == 0:
            return None
        got = self._collection.get(limit=1, include=["embeddings"])
        emb = got.get("embeddings")
        return int(len(emb[0])) if emb is not None and len(emb) else None

    def compatibility_problem(self) -> Optional[str]:
        """None if the stored vectors were made with the configured model, else an explanation."""
        if self.count() > 0 and self.stored_model and self.stored_model != self.embedding_model:
            return (f"The database holds vectors made with '{self.stored_model}', but the app is configured for "
                    f"'{self.embedding_model}'. Mixing them would give wrong search results. Go to System Settings → "
                    "Re-index all documents (or switch OPENAI_EMBEDDING_MODEL back).")
        return None

    def assert_compatible(self) -> None:
        problem = self.compatibility_problem()
        if problem:
            raise EmbeddingModelMismatchError(problem)

    # ---- write ----
    def add_chunks(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]], batch: int = 200) -> int:
        if len(chunks) != len(vectors):
            raise VectorStoreError("Number of chunks and vectors differ.")
        if not chunks:
            return 0
        dims = {len(v) for v in vectors}
        if len(dims) != 1:
            raise VectorStoreError(f"Vectors have inconsistent dimensions: {sorted(dims)}.")
        self.assert_compatible()
        existing = self.stored_dimension()
        if existing is not None and existing != dims.pop():
            raise EmbeddingModelMismatchError(
                f"New vectors have a different dimension than stored vectors ({existing}). Re-index everything.")
        try:
            for i in range(0, len(chunks), batch):
                part = chunks[i:i + batch]
                self._collection.upsert(
                    ids=[c.chunk_id for c in part],
                    embeddings=[list(map(float, v)) for v in vectors[i:i + batch]],
                    documents=[c.text for c in part],
                    metadatas=[c.to_metadata() for c in part])
        except Exception as exc:
            raise VectorStoreError(f"Could not write to ChromaDB: {exc}") from exc
        return len(chunks)

    def ids_for_document(self, document_id: str) -> list[str]:
        return self._collection.get(where={"document_id": document_id}, include=[])["ids"]

    def delete_ids(self, ids: Sequence[str]) -> None:
        if ids:
            try:
                self._collection.delete(ids=list(ids))
            except Exception as exc:
                raise VectorStoreError(f"Could not delete records: {exc}") from exc

    def delete_document(self, document_id: str) -> int:
        ids = self.ids_for_document(document_id)
        self.delete_ids(ids)
        return len(ids)

    def clear(self, new_model: Optional[str] = None) -> None:
        """Delete the whole collection and create a fresh empty one (optionally for a new model)."""
        try:
            self._client.delete_collection(self.collection_name)
            if new_model:
                self.embedding_model = new_model
            self._collection = self._open()
        except Exception as exc:
            raise VectorStoreError(f"Could not clear the collection: {exc}") from exc

    # ---- read ----
    def get_records(self, where: Optional[dict] = None, limit: Optional[int] = None, offset: int = 0,
                    include_embeddings: bool = False) -> list[dict[str, Any]]:
        inc = ["documents", "metadatas"] + (["embeddings"] if include_embeddings else [])
        try:
            got = self._collection.get(where=where, limit=limit, offset=offset, include=inc)
        except Exception as exc:
            raise VectorStoreError(f"Could not read from ChromaDB: {exc}") from exc
        embs = got.get("embeddings") if include_embeddings else None
        rows = []
        for i, cid in enumerate(got["ids"]):
            row = {"id": cid, "document": got["documents"][i], "metadata": got["metadatas"][i] or {}}
            if embs is not None:
                row["embedding"] = [float(x) for x in embs[i]]
            rows.append(row)
        rows.sort(key=lambda r: (r["metadata"].get("source_file", ""), r["metadata"].get("chunk_index", 0)))
        return rows

    def query(self, embedding: Sequence[float], k: int, where: Optional[dict] = None) -> list[dict[str, Any]]:
        n = self.count()
        if n == 0:
            return []
        try:
            res = self._collection.query(query_embeddings=[list(map(float, embedding))], n_results=min(k, n),
                                         where=where, include=["documents", "metadatas", "distances"])
        except Exception as exc:
            raise VectorStoreError(f"ChromaDB search failed: {exc}") from exc
        return [{"id": res["ids"][0][i], "document": res["documents"][0][i],
                 "metadata": res["metadatas"][0][i] or {}, "distance": float(res["distances"][0][i])}
                for i in range(len(res["ids"][0]))]
