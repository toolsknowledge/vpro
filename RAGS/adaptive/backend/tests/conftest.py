"""Shared fixtures. No test in the default suite touches the network or OpenAI.

``FakeOpenAIService`` replaces the real SDK wrapper: chat replies are scripted
per test and embeddings are deterministic hashed bag-of-words vectors, so
cosine similarity behaves sensibly (shared words -> higher similarity).
ChromaDB is real but lives in a per-test temporary directory.
"""

import hashlib
import math
import re
import sys
from collections.abc import Callable
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from config import Settings, get_settings  # noqa: E402
from dependencies import get_chat_service, get_indexing_service  # noqa: E402
from main import app  # noqa: E402
from scripts import create_sample_files  # noqa: E402
from services.adaptive_router import AdaptiveRouter  # noqa: E402
from services.answer_service import AnswerService  # noqa: E402
from services.chat_service import ChatService  # noqa: E402
from services.chroma_service import ChromaService  # noqa: E402
from services.embedding_service import EmbeddingService  # noqa: E402
from services.indexing_service import IndexingService  # noqa: E402
from services.openai_service import OpenAIService  # noqa: E402
from services.retrieval_service import RetrievalService  # noqa: E402
from services.session_store import SessionStore  # noqa: E402

EMBEDDING_DIM = 256


def fake_embedding(text: str) -> list[float]:
    vector = [0.0] * EMBEDDING_DIM
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        if len(token) > 2:
            vector[int(hashlib.md5(token.encode()).hexdigest(), 16) % EMBEDDING_DIM] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


class FakeOpenAIService(OpenAIService):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        self.classifier_reply = '{"route": "DIRECT", "reason": "General question."}'
        self.answer_reply = "Fake generated answer."
        self.chat_error: Exception | None = None
        self.embed_error: Exception | None = None
        self.chat_calls: list[dict] = []
        self.embed_calls: list[list[str]] = []

    def chat(self, messages, *, temperature, json_mode=False, max_tokens=None) -> str:
        self.chat_calls.append({"messages": messages, "json_mode": json_mode, "temperature": temperature})
        if self.chat_error is not None:
            raise self.chat_error
        return self.classifier_reply if json_mode else self.answer_reply

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_calls.append(list(texts))
        if self.embed_error is not None:
            raise self.embed_error
        return [fake_embedding(text) for text in texts]

    @property
    def classifier_calls(self) -> list[dict]:
        return [call for call in self.chat_calls if call["json_mode"]]

    @property
    def answer_calls(self) -> list[dict]:
        return [call for call in self.chat_calls if not call["json_mode"]]


@pytest.fixture
def docs_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "docs"
    directory.mkdir()
    return directory


@pytest.fixture
def make_settings(tmp_path: Path, docs_dir: Path) -> Callable[..., Settings]:
    def factory(**overrides) -> Settings:
        values = {
            "openai_api_key": "sk-test-not-a-real-key",
            "chroma_persist_directory": tmp_path / "chroma",
            "chroma_collection_name": "test_collection",
            "documents_directory": docs_dir,
            "indexing_state_file": tmp_path / "state.json",
            "chunk_size": 400,
            "chunk_overlap": 60,
            "relevance_threshold": 0.35,
        }
        values.update(overrides)
        return Settings(_env_file=None, **values)

    return factory


@pytest.fixture
def settings(make_settings) -> Settings:
    return make_settings()


@pytest.fixture
def fake_openai(settings: Settings) -> FakeOpenAIService:
    return FakeOpenAIService(settings)


@pytest.fixture
def chroma(settings: Settings) -> ChromaService:
    return ChromaService(settings.chroma_persist_directory, settings.chroma_collection_name)


@pytest.fixture
def indexing_service(settings, chroma, fake_openai) -> IndexingService:
    return IndexingService(settings, chroma, EmbeddingService(fake_openai, batch_size=8))


@pytest.fixture
def chat_service(settings, chroma, fake_openai) -> ChatService:
    return ChatService(
        router=AdaptiveRouter(fake_openai, temperature=0.0),
        retrieval=RetrievalService(
            EmbeddingService(fake_openai, batch_size=8), chroma, settings.top_k, settings.relevance_threshold
        ),
        answers=AnswerService(fake_openai, temperature=settings.answer_temperature),
        sessions=SessionStore(max_turns=3, max_sessions=10, ttl_minutes=60),
        chroma=chroma,
    )


@pytest.fixture
def sample_docs(docs_dir: Path) -> Path:
    """Write the real sample documents into the temporary documents directory."""
    create_sample_files.write_txt(docs_dir / "rag_fundamentals.txt")
    create_sample_files.write_md(docs_dir / "adaptive_rag_guide.md")
    create_sample_files.write_docx(docs_dir / "hybrid_vs_advanced_rag.docx")
    create_sample_files.write_pdf(docs_dir / "rag_course_faq.pdf")
    create_sample_files.write_xlsx(docs_dir / "rag_concepts.xlsx")
    return docs_dir


@pytest.fixture
def client(settings, indexing_service, chat_service) -> TestClient:
    app.dependency_overrides[get_settings] = lambda: settings
    app.dependency_overrides[get_indexing_service] = lambda: indexing_service
    app.dependency_overrides[get_chat_service] = lambda: chat_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
