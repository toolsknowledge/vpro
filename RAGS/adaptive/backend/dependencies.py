"""Service wiring. Each service is a process-wide singleton built from settings.

API routes receive services through FastAPI ``Depends`` so tests can replace
any of them with ``app.dependency_overrides``.
"""

from functools import lru_cache

from config import Settings, get_settings
from services.adaptive_router import AdaptiveRouter
from services.answer_service import AnswerService
from services.chat_service import ChatService
from services.chroma_service import ChromaService
from services.embedding_service import EmbeddingService
from services.indexing_service import IndexingService
from services.openai_service import OpenAIService
from services.retrieval_service import RetrievalService
from services.session_store import SessionStore


@lru_cache
def get_openai_service() -> OpenAIService:
    return OpenAIService(get_settings())


@lru_cache
def get_chroma_service() -> ChromaService:
    settings = get_settings()
    return ChromaService(settings.chroma_persist_directory, settings.chroma_collection_name)


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(get_openai_service(), get_settings().embedding_batch_size)


@lru_cache
def get_indexing_service() -> IndexingService:
    return IndexingService(get_settings(), get_chroma_service(), get_embedding_service())


@lru_cache
def get_chat_service() -> ChatService:
    settings: Settings = get_settings()
    openai_service = get_openai_service()
    return ChatService(
        router=AdaptiveRouter(openai_service, settings.classifier_temperature),
        retrieval=RetrievalService(
            get_embedding_service(), get_chroma_service(), settings.top_k, settings.relevance_threshold
        ),
        answers=AnswerService(openai_service, settings.answer_temperature),
        sessions=SessionStore(settings.max_history_turns, settings.max_sessions, settings.session_ttl_minutes),
        chroma=get_chroma_service(),
    )
