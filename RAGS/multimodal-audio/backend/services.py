"""Builds all backend objects from Settings in one place.

The UI asks for `AppServices` once; every page then uses the same registry,
vector store, embedder, retriever and RAG chain.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.document_registry import DocumentRegistry
from backend.embeddings import EmbeddingService
from backend.frame_analyzer import FrameAnalyzer
from backend.indexing_pipeline import IndexingPipeline
from backend.media_pipeline import MediaIndexingPipeline
from backend.media_registry import MediaRegistry
from backend.media_retrieval import MEDIA_DOCUMENT, UnifiedRetriever
from backend.media_utils import FFmpegTools
from backend.media_vector_store import MediaStores
from backend.openai_client import OpenAIServiceError, create_client
from backend.rag_chain import RagChain
from backend.retrieval import Retriever
from backend.transcription_service import TranscriptionService
from backend.unified_rag import UnifiedRagChain
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
    # ---- audio / video
    media_registry: MediaRegistry | None = None
    media_stores: MediaStores | None = None
    media_pipeline: MediaIndexingPipeline | None = None
    ffmpeg: FFmpegTools | None = None
    unified_retriever: UnifiedRetriever | None = None
    unified_rag: UnifiedRagChain | None = None

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

    media_registry = MediaRegistry(
        settings.media_registry_path,
        settings.transcripts_directory,
        settings.media_uploads_directory,
        settings.extracted_audio_directory,
        settings.video_frames_directory,
    )
    media_stores = MediaStores(
        settings.chroma_persist_directory,
        settings.audio_collection_name,
        settings.video_transcript_collection_name,
        settings.video_frame_collection_name,
    )
    ffmpeg = FFmpegTools(settings.ffmpeg_binary, settings.ffprobe_binary, settings.ffmpeg_timeout_seconds)
    transcriber = analyzer = unified_retriever = unified_rag = None
    if embedder is not None:
        transcriber = TranscriptionService(
            client, settings.transcription_model, settings.transcription_language, prompt=settings.transcription_prompt
        )
        analyzer = FrameAnalyzer(client, settings.vision_model)
        unified_retriever = UnifiedRetriever(
            embedder,
            {MEDIA_DOCUMENT: store, **dict(media_stores.items())},
            frame_tolerance=settings.video_frame_interval_seconds,
        )
        unified_rag = UnifiedRagChain(client, settings.chat_model, unified_retriever, settings.chat_temperature)
    media_pipeline = MediaIndexingPipeline(
        media_registry,
        media_stores,
        ffmpeg,
        embedder,
        transcriber,
        analyzer,
        settings.data_directory,
        max_upload_bytes=settings.max_media_upload_bytes,
        max_duration_seconds=settings.max_media_duration_minutes * 60,
        audio_chunk_seconds=settings.audio_chunk_seconds,
        timestamp_fallback_seconds=settings.timestamp_fallback_seconds,
    )
    return AppServices(
        settings, registry, store, pipeline, embedder, retriever, rag, openai_error,
        media_registry, media_stores, media_pipeline, ffmpeg, unified_retriever, unified_rag,
    )
