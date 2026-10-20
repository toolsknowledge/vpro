"""RAG pipeline: index DOCX documents and answer questions from retrieved context.

The pipeline depends only on the VectorStore interface, never on a specific database.
"""

import logging
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from app.core.exceptions import DocumentNotFoundError, DuplicateDocumentError, VectorStoreError
from app.document_loaders.docx_loader import load_docx
from app.rag.chunking import split_text
from app.rag.prompts import SYSTEM_PROMPT, build_user_prompt
from app.utils.files import compute_document_id
from app.vectorstores.base import Chunk, DocumentInfo, SearchResult, VectorStore

logger = logging.getLogger(__name__)

NO_CONTEXT_ANSWER = "No indexed document content is available to answer this question. Upload a DOCX document first."


class Embedder(Protocol):
    dimension: int

    def embed(self, texts: list[str]) -> list[list[float]]: ...


class ChatModel(Protocol):
    def complete(self, system_prompt: str, user_prompt: str) -> str: ...


@dataclass(frozen=True)
class Answer:
    text: str
    sources: list[SearchResult]


class RAGPipeline:
    def __init__(
        self,
        embedder: Embedder,
        store: VectorStore,
        llm: ChatModel,
        chunk_size: int,
        chunk_overlap: int,
        top_k: int,
    ) -> None:
        self._embedder = embedder
        self._store = store
        self._llm = llm
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._top_k = top_k
        # Serializes the duplicate check and the write, so concurrent uploads of one file cannot both index.
        self._index_lock = threading.Lock()

    def index_document(self, filename: str, data: bytes) -> DocumentInfo:
        document_id = compute_document_id(data)
        with self._index_lock:
            if self._store.document_exists(document_id):
                raise DuplicateDocumentError(f"'{filename}' has already been indexed.")
            document = self._index_new_document(document_id, filename, data)
        logger.info(
            "document_indexed document_id=%s filename=%r chunks=%d", document_id, filename, document.chunk_count
        )
        return document

    def _index_new_document(self, document_id: str, filename: str, data: bytes) -> DocumentInfo:
        loaded = load_docx(data)
        texts = split_text(loaded.text, self._chunk_size, self._chunk_overlap)
        document = DocumentInfo(
            document_id=document_id,
            filename=filename,
            chunk_count=len(texts),
            uploaded_at=datetime.now(UTC).isoformat(timespec="seconds"),
            title=loaded.title,
            author=loaded.author,
        )
        chunks = [Chunk(document=document, index=index, text=text) for index, text in enumerate(texts)]
        embeddings = self._embedder.embed(texts)
        try:
            self._store.add(chunks, embeddings)
        except VectorStoreError:
            self._remove_partial_document(document_id)
            raise
        return document

    def _remove_partial_document(self, document_id: str) -> None:
        """Best-effort cleanup so a failed upload does not leave orphaned chunks that block a retry."""
        try:
            self._store.delete_document(document_id)
        except DocumentNotFoundError:
            pass
        except VectorStoreError:
            logger.exception("partial_document_cleanup_failed document_id=%s", document_id)

    def answer(self, question: str) -> Answer:
        query_embedding = self._embedder.embed([question])[0]
        results = self._store.search(query_embedding, self._top_k)
        if not results:
            return Answer(text=NO_CONTEXT_ANSWER, sources=[])

        text = self._llm.complete(SYSTEM_PROMPT, build_user_prompt(question, results))
        logger.info("question_answered sources=%d", len(results))
        return Answer(text=text, sources=results)

    def list_documents(self) -> list[DocumentInfo]:
        return sorted(self._store.list_documents(), key=lambda document: document.uploaded_at, reverse=True)

    def delete_document(self, document_id: str) -> None:
        self._store.delete_document(document_id)
        logger.info("document_deleted document_id=%s", document_id)
