"""FastAPI application factory. Run with: uvicorn app.main:create_app --factory"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import register_exception_handlers
from app.api.routes import router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging
from app.rag.pipeline import RAGPipeline
from app.services.container import build_pipeline

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = app.state.settings
    if getattr(app.state, "pipeline", None) is None:
        logger.info("starting vector_db=%s embedding_model=%s", settings.vector_db, settings.embedding_model)
        app.state.pipeline = build_pipeline(settings)
    logger.info("ready vector_db=%s", settings.vector_db)
    yield


def create_app(settings: Settings | None = None, pipeline: RAGPipeline | None = None) -> FastAPI:
    """Create the app. Settings are validated here, so a misconfigured `.env` fails at startup."""
    configure_logging()
    settings = settings or get_settings()

    app = FastAPI(title="RAGS Vibe Modular", lifespan=lifespan)
    app.state.settings = settings
    app.state.pipeline = pipeline

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["Content-Type"],
    )
    register_exception_handlers(app)
    app.include_router(router)
    return app
