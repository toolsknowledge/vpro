"""Real OpenAI calls. Costs a fraction of a cent. Run explicitly with:

    RUN_OPENAI_INTEGRATION=1 pytest -m integration
"""

import os

import pytest

from backend.document_registry import DocumentRegistry
from backend.embeddings import EmbeddingService
from backend.indexing_pipeline import IndexingPipeline
from backend.openai_client import create_client
from backend.rag_chain import RagChain
from backend.retrieval import Retriever
from backend.vector_store import VectorStore
from config.settings import load_settings

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.getenv("RUN_OPENAI_INTEGRATION") != "1", reason="set RUN_OPENAI_INTEGRATION=1 to run"),
]


def test_end_to_end_with_real_openai(tmp_path):
    settings = load_settings()
    if not settings.has_api_key:
        pytest.skip("OPENAI_API_KEY is not configured")
    client = create_client(settings.openai_api_key)
    embedder = EmbeddingService(client, settings.embedding_model)
    store = VectorStore(tmp_path / "chroma", "integration_test")
    registry = DocumentRegistry(tmp_path / "r.json", tmp_path / "t", tmp_path / "u")
    pipeline = IndexingPipeline(registry, store, embedder, 5 * 1024 * 1024)

    text = b"Course modules:\nThe Python Full Stack course lasts 16 weeks and costs 30000 INR.\n"
    report = pipeline.index_file("course.txt", text, 800, 120)
    assert report.status == "indexed", report.message
    assert report.dimension and report.dimension > 100

    rag = RagChain(client, settings.chat_model, Retriever(embedder, store), settings.chat_temperature)
    answer = rag.ask("How long is the Python Full Stack course?")
    assert "16" in answer.answer
    assert answer.citations and answer.citations[0].chunk.metadata["source_file"] == "course.txt"
