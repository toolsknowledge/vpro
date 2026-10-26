"""Builds all backend objects from Settings in one place.

The UI asks for `AppServices` once; every page then uses the same registry,
vector store, embedder, retriever and RAG chain.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.document_registry import DocumentRegistry
from backend.embeddings import EmbeddingService
from backend.indexing_pipeline import IndexingPipeline
from backend.openai_client import OpenAIServiceError, create_client
from backend.rag_chain import RagChain
from backend.retrieval import Retriever
from backend.vector_store import VectorStore
from config.settings import Settings


@dataclass
class AppServices:
    settings: Settings
    registry: DocumentRegistry
    store: VectorStore
    pipeline: IndexingPipeline
    embedder: EmbeddingService | None = None
    retriever: Retriever | None = None
    rag: RagChain | None = None
    openai_error: str | None = None  # why OpenAI features are unavailable, if they are

    @property
    def openai_ready(self) -> bool:
        return self.embedder is not None

    def sync_registry(self) -> None:
        """Bring the registry in line with what is really stored in ChromaDB."""
        counts: dict[str, int] = {}
        for record in self.store.get_records():
            doc_id = record.metadata.get("document_id")
            if doc_id:
                counts[doc_id] = counts.get(doc_id, 0) + 1
        self.registry.sync_with_store(counts)


def build_services(settings: Settings, client=None) -> AppServices:
    registry = DocumentRegistry(settings.registry_path, settings.traces_directory, settings.uploads_directory)
    store = VectorStore(settings.chroma_persist_directory, settings.chroma_collection_name)

    embedder = retriever = rag = None
    openai_error = None
    try:
        client = client or create_client(settings.openai_api_key)
        embedder = EmbeddingService(client, settings.embedding_model)
        retriever = Retriever(embedder, store)
        rag = RagChain(client, settings.chat_model, retriever, settings.chat_temperature)
    except OpenAIServiceError as exc:
        openai_error = str(exc)

    pipeline = IndexingPipeline(registry, store, embedder, settings.max_upload_bytes)
    return AppServices(settings, registry, store, pipeline, embedder, retriever, rag, openai_error)
