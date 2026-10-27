from fastapi import APIRouter, Depends
from pydantic import BaseModel

from config import Settings, get_settings
from dependencies import get_indexing_service
from services.indexing_service import IndexingService

router = APIRouter(prefix="/api", tags=["health"])


class VectorStoreHealth(BaseModel):
    ready: bool
    collection_name: str
    chunk_count: int
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    app_name: str
    openai_configured: bool
    chat_model: str
    embedding_model: str
    top_k: int
    relevance_threshold: float
    vector_store: VectorStoreHealth


@router.get("/health", response_model=HealthResponse)
def health(
    settings: Settings = Depends(get_settings),
    indexing: IndexingService = Depends(get_indexing_service),
) -> HealthResponse:
    status = indexing.status()
    return HealthResponse(
        status="ok" if status.vector_store_ready else "degraded",
        app_name=settings.app_name,
        openai_configured=settings.openai_configured,
        chat_model=settings.openai_chat_model,
        embedding_model=settings.openai_embedding_model,
        top_k=settings.top_k,
        relevance_threshold=settings.relevance_threshold,
        vector_store=VectorStoreHealth(
            ready=status.vector_store_ready,
            collection_name=status.collection_name,
            chunk_count=status.chunk_count,
            error=status.vector_store_error,
        ),
    )
