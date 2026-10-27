"""Persistent ChromaDB access.

Embeddings are always supplied by the application (OpenAI), so the collection
is created without Chroma's default embedding function — Chroma never
downloads a local model. The collection uses cosine distance, so
``relevance = 1 - distance`` is the cosine similarity of query and chunk.
"""

import logging
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.config import Settings as ChromaSettings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SearchHit:
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    relevance: float


@dataclass
class SourceSummary:
    source: str
    file_type: str
    content_hash: str
    chunk_count: int = 0
    chunk_ids: list[str] = field(default_factory=list)


class ChromaService:
    def __init__(self, persist_directory: Path, collection_name: str) -> None:
        self._persist_directory = persist_directory
        self._collection_name = collection_name
        self._collection: Collection | None = None
        self._init_lock = threading.Lock()

    @property
    def collection_name(self) -> str:
        return self._collection_name

    @property
    def persist_directory(self) -> Path:
        return self._persist_directory

    def _get_collection(self) -> Collection:
        with self._init_lock:
            if self._collection is None:
                self._persist_directory.mkdir(parents=True, exist_ok=True)
                client = chromadb.PersistentClient(
                    path=str(self._persist_directory),
                    settings=ChromaSettings(anonymized_telemetry=False),
                )
                self._collection = client.get_or_create_collection(
                    name=self._collection_name,
                    configuration={"hnsw": {"space": "cosine"}},
                    embedding_function=None,
                )
                logger.info("ChromaDB collection '%s' ready at %s", self._collection_name, self._persist_directory)
            return self._collection

    def count(self) -> int:
        return self._get_collection().count()

    def add_chunks(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict[str, Any]],
    ) -> None:
        if ids:
            self._get_collection().upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    def delete_ids(self, ids: list[str]) -> None:
        if ids:
            self._get_collection().delete(ids=ids)

    def source_summaries(self) -> dict[str, SourceSummary]:
        """Group stored chunks by source file (used for change detection and listings)."""
        collection = self._get_collection()
        if collection.count() == 0:
            return {}
        records = collection.get(include=["metadatas"])
        summaries: dict[str, SourceSummary] = {}
        for chunk_id, metadata in zip(records["ids"], records["metadatas"] or []):
            metadata = metadata or {}
            source = str(metadata.get("source", "unknown"))
            summary = summaries.setdefault(
                source,
                SourceSummary(
                    source=source,
                    file_type=str(metadata.get("file_type", "")),
                    content_hash=str(metadata.get("content_hash", "")),
                ),
            )
            summary.chunk_count += 1
            summary.chunk_ids.append(chunk_id)
            if summary.content_hash != str(metadata.get("content_hash", "")):
                # Mixed hashes mean a previous update was interrupted; force a refresh.
                summary.content_hash = ""
        return summaries

    def query(self, embedding: list[float], top_k: int) -> list[SearchHit]:
        collection = self._get_collection()
        if collection.count() == 0:
            return []
        result = collection.query(
            query_embeddings=[embedding],
            n_results=min(top_k, collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        hits: list[SearchHit] = []
        for chunk_id, text, metadata, distance in zip(
            result["ids"][0],
            (result["documents"] or [[]])[0],
            (result["metadatas"] or [[]])[0],
            (result["distances"] or [[]])[0],
        ):
            hits.append(
                SearchHit(
                    chunk_id=chunk_id,
                    text=text or "",
                    metadata=dict(metadata or {}),
                    relevance=round(max(0.0, min(1.0, 1.0 - float(distance))), 4),
                )
            )
        return hits
