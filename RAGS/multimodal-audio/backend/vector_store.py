"""Persistent vector storage with ChromaDB.

ChromaDB stores, for every chunk: its ID, its text, its embedding vector and
its metadata (source file, page, sheet, ...). `PersistentClient` writes to disk
automatically, so the data survives application restarts. No manual
`persist()` call is needed (that API is obsolete).

The collection remembers which embedding model filled it. Vectors from two
different models live in different "spaces" and cannot be compared, so adding
vectors from another model is refused until the collection is rebuilt.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb

DISTANCE_METRIC = "cosine"


class VectorStoreError(Exception):
    """A user-facing ChromaDB problem."""


class IncompatibleEmbeddingError(VectorStoreError):
    """The collection holds vectors from a different embedding model or dimension."""


@dataclass
class StoredRecord:
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    embedding: list[float] | None = None


@dataclass
class QueryHit:
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    distance: float


def distance_to_similarity(distance: float, metric: str) -> float | None:
    """Convert a raw Chroma distance into a similarity score where that is meaningful.

    * cosine: Chroma returns 1 - cosine_similarity, so similarity = 1 - distance.
    * ip (inner product): Chroma returns 1 - dot product; for normalised vectors
      such as OpenAI embeddings this equals 1 - cosine similarity.
    * l2: squared Euclidean distance has no fixed similarity scale -> None.
    """
    if metric in ("cosine", "ip"):
        return 1.0 - distance
    return None


class VectorStore:
    def __init__(self, persist_directory: Path, collection_name: str):
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        try:
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            self.client = chromadb.PersistentClient(path=str(self.persist_directory))
            self.collection = self._get_or_create(collection_name)
        except Exception as exc:
            raise VectorStoreError(f"Could not open ChromaDB at '{self.persist_directory}': {exc}") from exc

    # ----------------------------------------------------------- collection info
    def _get_or_create(self, name: str):
        # embedding_function=None: we always supply our own OpenAI vectors.
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=None,
            configuration={"hnsw": {"space": DISTANCE_METRIC}},
        )

    @property
    def distance_metric(self) -> str:
        try:
            hnsw = (self.collection.configuration or {}).get("hnsw") or {}
            return hnsw.get("space") or DISTANCE_METRIC
        except Exception:
            return (self.collection.metadata or {}).get("hnsw:space", "l2")

    @property
    def stored_embedding_model(self) -> str | None:
        return (self.collection.metadata or {}).get("embedding_model")

    @property
    def stored_dimension(self) -> int | None:
        value = (self.collection.metadata or {}).get("embedding_dimension")
        return int(value) if value is not None else None

    def count(self) -> int:
        return self.collection.count()

    def check_compatible(self, embedding_model: str, dimension: int | None = None) -> None:
        """Raise IncompatibleEmbeddingError if new vectors would not match stored ones."""
        if self.count() == 0:
            return
        stored_model, stored_dim = self.stored_embedding_model, self.stored_dimension
        if stored_model and stored_model != embedding_model:
            raise IncompatibleEmbeddingError(
                f"The collection was built with '{stored_model}' but the app is configured for "
                f"'{embedding_model}'. Vectors from different models cannot be mixed. Use "
                "'Rebuild index with current model' in System Settings, or switch the model back."
            )
        if dimension is not None and stored_dim is not None and stored_dim != dimension:
            raise IncompatibleEmbeddingError(
                f"New vectors have {dimension} dimensions but the collection stores {stored_dim}-dimensional vectors."
            )

    def _record_model(self, embedding_model: str, dimension: int) -> None:
        metadata = dict(self.collection.metadata or {})
        if metadata.get("embedding_model") != embedding_model or metadata.get("embedding_dimension") != dimension:
            metadata.update({"embedding_model": embedding_model, "embedding_dimension": dimension})
            metadata.pop("hnsw:space", None)  # legacy key; the metric is set through `configuration`
            self.collection.modify(metadata=metadata)

    # ------------------------------------------------------------------ writes
    def add_chunks(self, ids: list[str], texts: list[str], metadatas: list[dict], embeddings: list[list[float]], embedding_model: str) -> None:
        if not (len(ids) == len(texts) == len(metadatas) == len(embeddings)):
            raise VectorStoreError("ids, texts, metadatas and embeddings must have the same length.")
        if not ids:
            return
        dimension = len(embeddings[0])
        if any(len(e) != dimension for e in embeddings):
            raise VectorStoreError("All embeddings in one add() call must have the same dimension.")
        self.check_compatible(embedding_model, dimension)

        batch = max(1, self.client.get_max_batch_size())
        try:
            for start in range(0, len(ids), batch):
                end = start + batch
                self.collection.upsert(
                    ids=ids[start:end],
                    documents=texts[start:end],
                    metadatas=metadatas[start:end],
                    embeddings=embeddings[start:end],
                )
        except Exception as exc:
            # Remove whatever part of this call was written so no half-document remains.
            try:
                self.collection.delete(ids=ids)
            except Exception:
                pass
            raise VectorStoreError(f"Saving vectors to ChromaDB failed: {exc}") from exc
        self._record_model(embedding_model, dimension)

    def replace_document(self, document_id: str, ids, texts, metadatas, embeddings, embedding_model: str) -> None:
        """Swap a document's records for new ones; on failure, restore the old records."""
        self.check_compatible(embedding_model, len(embeddings[0]) if embeddings else None)
        old = self.get_records(where={"document_id": document_id}, include_embeddings=True)
        self.delete_document(document_id)
        try:
            self.add_chunks(ids, texts, metadatas, embeddings, embedding_model)
        except Exception:
            if old:
                self.collection.upsert(
                    ids=[r.chunk_id for r in old],
                    documents=[r.text for r in old],
                    metadatas=[r.metadata for r in old],
                    embeddings=[r.embedding for r in old],
                )
            raise

    def delete_document(self, document_id: str) -> int:
        """Delete every chunk of one document. Returns how many records were removed."""
        try:
            existing = self.collection.get(where={"document_id": document_id}, include=[])
            ids = existing["ids"]
            if ids:
                self.collection.delete(ids=ids)
            return len(ids)
        except Exception as exc:
            raise VectorStoreError(f"Deleting document '{document_id}' from ChromaDB failed: {exc}") from exc

    def reset_collection(self) -> None:
        """Delete the whole collection and create an empty one with the same name."""
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.collection = self._get_or_create(self.collection_name)

    def open_staging(self, suffix: str = "rebuild") -> "VectorStore":
        """An empty side collection used to rebuild the index safely."""
        staging_name = f"{self.collection_name}__{suffix}"
        try:
            self.client.delete_collection(staging_name)
        except Exception:
            pass
        return VectorStore(self.persist_directory, staging_name)

    def promote_staging(self, staging: "VectorStore") -> None:
        """Replace this collection with a fully built staging collection."""
        self.client.delete_collection(self.collection_name)
        staging.collection.modify(name=self.collection_name)
        self.collection = self.client.get_collection(self.collection_name, embedding_function=None)

    # ------------------------------------------------------------------- reads
    def document_ids(self) -> set[str]:
        records = self.collection.get(include=["metadatas"])
        return {m.get("document_id") for m in records["metadatas"] or [] if m}

    def count_for_document(self, document_id: str) -> int:
        return len(self.collection.get(where={"document_id": document_id}, include=[])["ids"])

    def get_records(
        self,
        where: dict | None = None,
        limit: int | None = None,
        offset: int | None = None,
        include_embeddings: bool = False,
    ) -> list[StoredRecord]:
        include = ["documents", "metadatas"] + (["embeddings"] if include_embeddings else [])
        result = self.collection.get(where=where, limit=limit, offset=offset, include=include)
        embeddings = result.get("embeddings") if include_embeddings else None
        records = []
        for i, chunk_id in enumerate(result["ids"]):
            vector = None
            if embeddings is not None and len(embeddings) > i:
                vector = [float(x) for x in embeddings[i]]
            records.append(StoredRecord(chunk_id, result["documents"][i], result["metadatas"][i] or {}, vector))
        return records

    def query(self, query_embedding: list[float], top_k: int, where: dict | None = None) -> list[QueryHit]:
        total = self.count()
        if total == 0:
            return []
        if self.stored_dimension and len(query_embedding) != self.stored_dimension:
            raise IncompatibleEmbeddingError(
                f"The question vector has {len(query_embedding)} dimensions but the collection stores "
                f"{self.stored_dimension}. Was the embedding model changed?"
            )
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, total),
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        return [
            QueryHit(chunk_id, result["documents"][0][i], result["metadatas"][0][i] or {}, float(result["distances"][0][i]))
            for i, chunk_id in enumerate(result["ids"][0])
        ]
