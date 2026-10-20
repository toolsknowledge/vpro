"""Pinecone adapter. The index must already exist with the embedding dimension and cosine metric."""

from collections.abc import Iterator, Sequence
from itertools import batched

from pinecone import Pinecone

from app.core.exceptions import DocumentNotFoundError, VectorStoreError
from app.vectorstores.base import Chunk, DocumentInfo, SearchResult, VectorStore, store_errors

STORE_NAME = "Pinecone"
UPSERT_BATCH_SIZE = 100
FETCH_BATCH_SIZE = 100
DELETE_BATCH_SIZE = 1000
FIRST_CHUNK_SUFFIX = "#0"


class PineconeVectorStore(VectorStore):
    def __init__(self, api_key: str, index_name: str, namespace: str, dimension: int) -> None:
        super().__init__(dimension)
        self._namespace = namespace
        with store_errors(STORE_NAME, f"connect to index '{index_name}'"):
            self._index = Pinecone(api_key=api_key).Index(name=index_name)
            stats = self._index.describe_index_stats()

        if stats.dimension != dimension:
            raise VectorStoreError(
                f"Pinecone index '{index_name}' has dimension {stats.dimension}, "
                f"but the embedding model produces {dimension}."
            )
        if stats.metric and stats.metric != "cosine":
            raise VectorStoreError(f"Pinecone index '{index_name}' must use the cosine metric, not '{stats.metric}'.")

    def add(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        self._validate_embeddings(chunks, embeddings)
        vectors = [
            {"id": chunk.id, "values": list(vector), "metadata": chunk.to_metadata()}
            for chunk, vector in zip(chunks, embeddings, strict=True)
        ]
        with store_errors(STORE_NAME, "add chunks"):
            for batch in batched(vectors, UPSERT_BATCH_SIZE):
                self._index.upsert(vectors=list(batch), namespace=self._namespace, show_progress=False)

    def search(self, embedding: Sequence[float], top_k: int) -> list[SearchResult]:
        self._validate_dimension(embedding)
        with store_errors(STORE_NAME, "search"):
            response = self._index.query(
                vector=list(embedding),
                top_k=top_k,
                namespace=self._namespace,
                include_metadata=True,
            )
        return [
            SearchResult(chunk=Chunk.from_metadata(match.metadata), score=float(match.score))
            for match in response.matches
            if match.metadata
        ]

    def _list_ids(self, prefix: str | None = None) -> Iterator[str]:
        for page in self._index.list(prefix=prefix, namespace=self._namespace):
            yield from (item.id for item in page.vectors)

    def list_documents(self) -> list[DocumentInfo]:
        with store_errors(STORE_NAME, "list documents"):
            first_chunk_ids = [vector_id for vector_id in self._list_ids() if vector_id.endswith(FIRST_CHUNK_SUFFIX)]
            documents = []
            for batch in batched(first_chunk_ids, FETCH_BATCH_SIZE):
                response = self._index.fetch(ids=list(batch), namespace=self._namespace)
                documents.extend(
                    Chunk.from_metadata(vector.metadata).document
                    for vector in response.vectors.values()
                    if vector.metadata
                )
        return documents

    def document_exists(self, document_id: str) -> bool:
        with store_errors(STORE_NAME, "look up a document"):
            response = self._index.fetch(ids=[document_id + FIRST_CHUNK_SUFFIX], namespace=self._namespace)
        return bool(response.vectors)

    def delete_document(self, document_id: str) -> None:
        with store_errors(STORE_NAME, "delete a document"):
            ids = list(self._list_ids(prefix=f"{document_id}#"))
            if not ids:
                raise DocumentNotFoundError(f"Document '{document_id}' was not found.")
            for batch in batched(ids, DELETE_BATCH_SIZE):
                self._index.delete(ids=list(batch), namespace=self._namespace)
