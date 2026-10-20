"""ChromaDB adapter with on-disk persistence."""

from collections.abc import Sequence
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.exceptions import DocumentNotFoundError, VectorStoreError
from app.vectorstores.base import Chunk, DocumentInfo, SearchResult, VectorStore, store_errors

STORE_NAME = "ChromaDB"


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_directory: Path, collection_name: str, dimension: int) -> None:
        super().__init__(dimension)
        with store_errors(STORE_NAME, "open the persistent collection"):
            client = chromadb.PersistentClient(
                path=str(persist_directory),
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            self._collection = client.get_or_create_collection(
                name=collection_name,
                configuration={"hnsw": {"space": "cosine"}},
                metadata={"dimension": dimension},
                embedding_function=None,
            )

        stored_dimension = (self._collection.metadata or {}).get("dimension")
        if stored_dimension is not None and stored_dimension != dimension:
            raise VectorStoreError(
                f"ChromaDB collection '{collection_name}' has dimension {stored_dimension}, "
                f"but the embedding model produces {dimension}. Use a new collection name."
            )

    def add(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        self._validate_embeddings(chunks, embeddings)
        if not chunks:
            return
        with store_errors(STORE_NAME, "add chunks"):
            self._collection.add(
                ids=[chunk.id for chunk in chunks],
                embeddings=[list(vector) for vector in embeddings],
                metadatas=[chunk.to_metadata() for chunk in chunks],
            )

    def search(self, embedding: Sequence[float], top_k: int) -> list[SearchResult]:
        self._validate_dimension(embedding)
        with store_errors(STORE_NAME, "search"):
            count = self._collection.count()
            if count == 0:
                return []
            result = self._collection.query(
                query_embeddings=[list(embedding)],
                n_results=min(top_k, count),
                include=["metadatas", "distances"],
            )
        metadatas = (result["metadatas"] or [[]])[0]
        distances = (result["distances"] or [[]])[0]
        # Chroma returns cosine distance; convert to similarity to match the other stores.
        return [
            SearchResult(chunk=Chunk.from_metadata(metadata), score=1.0 - distance)
            for metadata, distance in zip(metadatas, distances, strict=True)
        ]

    def list_documents(self) -> list[DocumentInfo]:
        with store_errors(STORE_NAME, "list documents"):
            result = self._collection.get(where={"chunk_index": 0}, include=["metadatas"])
        return [Chunk.from_metadata(metadata).document for metadata in result["metadatas"] or []]

    def document_exists(self, document_id: str) -> bool:
        with store_errors(STORE_NAME, "look up a document"):
            result = self._collection.get(where={"document_id": document_id}, limit=1, include=[])
        return bool(result["ids"])

    def delete_document(self, document_id: str) -> None:
        with store_errors(STORE_NAME, "delete a document"):
            result = self._collection.delete(where={"document_id": document_id})
        if not result or not result.get("deleted"):
            raise DocumentNotFoundError(f"Document '{document_id}' was not found.")
