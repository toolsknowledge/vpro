"""FastAPI application entry point.

Run from the project root:   uvicorn main:app --app-dir backend --reload
or from backend/:            python main.py
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api import chat, documents, health, indexing
from config import get_settings
from services.indexing_service import IndexingInProgressError
from services.openai_service import LLMServiceError

settings = get_settings()

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
)
# The OpenAI SDK's HTTP client logs request URLs at INFO; keep it quiet.
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("adaptive_rag")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if not settings.openai_configured:
        logger.warning("OPENAI_API_KEY is not set: the UI and health checks work, but chat and indexing will fail.")
    logger.info(
        "Chat model=%s, embedding model=%s, collection=%s",
        settings.openai_chat_model,
        settings.openai_embedding_model,
        settings.chroma_collection_name,
    )
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
    version="1.0.0",
    description="Adaptive RAG API: routes each question to DIRECT, RETRIEVE, or CLARIFY.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
)


def _error(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": {"code": code, "message": message}})


@app.exception_handler(LLMServiceError)
async def handle_llm_error(_: Request, exc: LLMServiceError) -> JSONResponse:
    return _error(exc.status_code, exc.code, exc.message)


@app.exception_handler(IndexingInProgressError)
async def handle_indexing_in_progress(_: Request, exc: IndexingInProgressError) -> JSONResponse:
    return _error(409, "indexing_in_progress", str(exc))


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    problems = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error.get("loc", ()) if part != "body")
        problems.append(f"{location}: {error.get('msg')}" if location else str(error.get("msg")))
    return _error(422, "validation_error", "; ".join(problems) or "Invalid request.")


@app.exception_handler(StarletteHTTPException)
async def handle_http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    return _error(exc.status_code, "http_error", str(exc.detail))


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return _error(500, "internal_error", "An unexpected server error occurred. Check the backend logs.")


app.include_router(health.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(indexing.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.api_host, port=settings.api_port, reload=False)
