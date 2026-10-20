from fastapi import Request

from app.core.config import Settings
from app.rag.pipeline import RAGPipeline


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_pipeline(request: Request) -> RAGPipeline:
    return request.app.state.pipeline
