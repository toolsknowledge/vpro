"""Optional smoke test against the real OpenAI API.

Deselected by default. Run from backend/ with a real key in backend/.env:
    ../.venv/bin/python -m pytest -m live
It indexes the sample documents into a temporary ChromaDB directory (your real
index is untouched) and makes a handful of small, inexpensive API calls.
"""

import pytest

from config import Settings
from schemas.chat import Route
from services.adaptive_router import AdaptiveRouter
from services.answer_service import AnswerService
from services.chat_service import ChatService
from services.chroma_service import ChromaService
from services.embedding_service import EmbeddingService
from services.indexing_service import IndexingService
from services.openai_service import OpenAIService
from services.retrieval_service import RetrievalService
from services.session_store import SessionStore

pytestmark = pytest.mark.live


@pytest.fixture
def live_chat(tmp_path, sample_docs):
    settings = Settings(
        chroma_persist_directory=tmp_path / "chroma",
        documents_directory=sample_docs,
        indexing_state_file=tmp_path / "state.json",
    )
    if not settings.openai_configured:
        pytest.skip("OPENAI_API_KEY is not configured")
    openai_service = OpenAIService(settings)
    chroma = ChromaService(settings.chroma_persist_directory, "live_smoke_test")
    embedder = EmbeddingService(openai_service, settings.embedding_batch_size)
    result = IndexingService(settings, chroma, embedder).run("index")
    assert result.status == "success", result.errors
    return ChatService(
        router=AdaptiveRouter(openai_service, settings.classifier_temperature),
        retrieval=RetrievalService(embedder, chroma, settings.top_k, settings.relevance_threshold),
        answers=AnswerService(openai_service, settings.answer_temperature),
        sessions=SessionStore(settings.max_history_turns, 10, 60),
        chroma=chroma,
    )


def test_live_routes(live_chat):
    direct = live_chat.ask("Hi, how are you?", "live-session-1")
    assert direct.route is Route.DIRECT and not direct.retrieval_performed

    retrieve = live_chat.ask("Explain Adaptive RAG from the course notes.", "live-session-2")
    assert retrieve.route is Route.RETRIEVE
    assert retrieve.grounded and retrieve.sources

    clarify = live_chat.ask("Compare these two.", "live-session-3")
    assert clarify.route is Route.CLARIFY and not clarify.retrieval_performed
