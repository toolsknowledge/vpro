"""FastAPI entry point. Run with: uvicorn app.main:app --reload"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import config
from app.api.routes import router
from app.errors import ServiceError
from app.services import pdf_service, retrieval_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
for noisy_logger in ("httpx", "httpx2"):  # keep OpenAI request lines out of the log
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)
logger = logging.getLogger("crag")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """On first start, index the sample PDF automatically so the assistant works out of the box."""
    if not config.is_openai_configured():
        logger.warning("OPENAI_API_KEY is not set in backend/.env – chat and ingestion will not work until it is.")
    else:
        try:
            if retrieval_service.count_chunks() == 0:
                logger.info("Knowledge base is empty – indexing PDFs from %s", config.KNOWLEDGE_BASE_DIR)
                pdf_service.ingest_documents()
        except ServiceError as error:
            logger.error("Automatic ingestion skipped: %s", error.message)
    yield


app = FastAPI(title="VPro Skills Corrective RAG API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(router, prefix="/api")


@app.exception_handler(ServiceError)
async def service_error_handler(_request: Request, exc: ServiceError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.info("Rejected invalid request: %s", exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": f"Please enter a question between 2 and {config.MAX_QUESTION_LENGTH} characters."},
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    # Full details go to the server log only; students see a friendly message.
    logger.exception("Unexpected error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong on the server. Please try again in a moment."},
    )
