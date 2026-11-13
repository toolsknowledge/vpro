"""HTTP API routes. All endpoints are mounted under /api in main.py.

Routes are plain `def` functions: FastAPI runs them in a thread pool, so the blocking
OpenAI and ChromaDB calls do not freeze the server.
"""

from fastapi import APIRouter

from app import config
from app.errors import ServiceError
from app.schemas import ChatRequest, ChatResponse, DocumentListResponse, HealthResponse, IngestResponse
from app.services import pdf_service, retrieval_service
from app.services.corrective_rag_service import answer_question

router = APIRouter()

APP_NAME = "VPro Skills – Corrective RAG Student Assistant"


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    try:
        indexed_chunks = retrieval_service.count_chunks()
    except ServiceError:
        indexed_chunks = None
    return HealthResponse(
        status="ok",
        app_name=APP_NAME,
        openai_configured=config.is_openai_configured(),
        chat_model=config.OPENAI_CHAT_MODEL,
        embedding_model=config.OPENAI_EMBEDDING_MODEL,
        indexed_chunks=indexed_chunks,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> dict:
    return answer_question(request.question)


@router.get("/documents", response_model=DocumentListResponse)
def list_documents() -> dict:
    return pdf_service.list_documents()


@router.post("/documents/ingest", response_model=IngestResponse)
def ingest_documents() -> dict:
    return pdf_service.ingest_documents()
