"""Vector store interface shared by every database adapter."""

from abc import ABC, abstractmethod
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from typing import Any

from app.core.exceptions import AppError, VectorStoreError

MetadataValue = str | int


@dataclass(frozen=True)
class DocumentInfo:
    document_id: str
    filename: str
    chunk_count: int
    uploaded_at: str
    title: str | None = None
    author: str | None = None


@dataclass(frozen=True)
class Chunk:
    document: DocumentInfo
    index: int
    text: str

    @property
    def id(self) -> str:
        """Chunk IDs share the document ID as prefix, which lets stores list and delete by prefix."""
        return f"{self.document.document_id}#{self.index}"

    def to_metadata(self) -> dict[str, MetadataValue]:
        metadata = {key: value for key, value in asdict(self.document).items() if value is not None}
        return metadata | {"chunk_index": self.index, "text": self.text}

    @classmethod
    def from_metadata(cls, metadata: Mapping[str, Any]) -> "Chunk":
        document = DocumentInfo(
            document_id=str(metadata["document_id"]),
            filename=str(metadata["filename"]),
            chunk_count=int(metadata["chunk_count"]),
            uploaded_at=str(metadata["uploaded_at"]),
            title=metadata.get("title"),
            author=metadata.get("author"),
        )
        return cls(document=document, index=int(metadata["chunk_index"]), text=str(metadata["text"]))


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


@contextmanager
def store_errors(store_name: str, operation: str) -> Iterator[None]:
    """Convert unexpected database errors into a client-safe VectorStoreError."""
    try:
        yield
    except AppError:
        raise
    except Exception as exc:
        raise VectorStoreError(f"{store_name} failed to {operation}.") from exc


class VectorStore(ABC):
    """Operations the RAG pipeline needs. Implementations own all database-specific details."""

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension

    @abstractmethod
    def add(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        """Store chunks with their embeddings."""

    @abstractmethod
    def search(self, embedding: Sequence[float], top_k: int) -> list[SearchResult]:
        """Return up to `top_k` chunks ranked by cosine similarity; empty when the store is empty."""

    @abstractmethod
    def list_documents(self) -> list[DocumentInfo]:
        """Return metadata for every indexed document."""

    @abstractmethod
    def document_exists(self, document_id: str) -> bool:
        """Return True if any chunk of the document is stored."""

    @abstractmethod
    def delete_document(self, document_id: str) -> None:
        """Delete every chunk of the document; raise DocumentNotFoundError if it is absent."""

    def _validate_embeddings(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise VectorStoreError("The number of chunks and embeddings does not match.")
        for vector in embeddings:
            self._validate_dimension(vector)

    def _validate_dimension(self, vector: Sequence[float]) -> None:
        if len(vector) != self.dimension:
            raise VectorStoreError(
                f"Embedding dimension {len(vector)} does not match the vector store dimension {self.dimension}."
            )
