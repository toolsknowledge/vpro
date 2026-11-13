import httpx2
import openai
import pytest
from fastapi.testclient import TestClient

from app import config
from app.errors import ServiceError
from app.main import app
from app.services import openai_service

client = TestClient(app)


@pytest.mark.parametrize("payload", [{"question": ""}, {"question": "   "}, {"question": "x" * 501},
                                     {"question": "What is Python?", "extra": 1}, {}])
def test_chat_rejects_invalid_questions(payload):
    response = client.post("/api/chat", json=payload)

    assert response.status_code == 422
    assert "Please enter a question" in response.json()["detail"]


def test_chat_returns_the_documented_schema(monkeypatch):
    from app.api import routes

    monkeypatch.setattr(routes, "answer_question", lambda question: {
        "question": question, "answer": "Python is a language.", "retrieval_status": "relevant",
        "corrective_retrieval_used": False, "correction_attempts": 0, "sources": [],
        "retrieved_documents": [], "attempts": [],
    })

    response = client.post("/api/chat", json={"question": "  What   is Python? "})

    assert response.status_code == 200
    assert response.json()["question"] == "What is Python?"


def test_missing_api_key_gives_clear_error(monkeypatch):
    monkeypatch.setattr(config, "OPENAI_API_KEY", "")

    with pytest.raises(ServiceError) as error:
        openai_service.get_client()
    assert error.value.status_code == 503
    assert "OPENAI_API_KEY" in error.value.message


def test_placeholder_api_key_is_treated_as_missing(monkeypatch):
    monkeypatch.setattr(config, "OPENAI_API_KEY", config.PLACEHOLDER_API_KEY)

    assert config.is_openai_configured() is False


def test_ingest_endpoint_without_pdfs_returns_404():
    response = client.post("/api/documents/ingest")

    assert response.status_code == 404
    assert "No PDF documents" in response.json()["detail"]


def test_chat_with_empty_knowledge_base_returns_friendly_error():
    response = client.post("/api/chat", json={"question": "What is Python?"})

    assert response.status_code == 503
    assert "knowledge base is empty" in response.json()["detail"]


REQUEST = httpx2.Request("POST", "https://api.openai.com/v1/chat/completions")


@pytest.mark.parametrize("error, status_code, text", [
    (openai.AuthenticationError("bad key", response=httpx2.Response(401, request=REQUEST), body=None), 503, "API key"),
    (openai.RateLimitError("slow down", response=httpx2.Response(429, request=REQUEST), body=None), 429, "busy"),
    (openai.APITimeoutError(request=REQUEST), 504, "too long"),
    (openai.APIConnectionError(request=REQUEST), 503, "Could not reach"),
    (openai.NotFoundError("no model", response=httpx2.Response(404, request=REQUEST), body=None), 500, "model"),
])
def test_openai_errors_become_friendly_messages(error, status_code, text, monkeypatch):
    class FailingCompletions:
        def create(self, **kwargs):
            raise error

    class FakeClient:
        chat = type("Chat", (), {"completions": FailingCompletions()})()

    monkeypatch.setattr(openai_service, "get_client", lambda: FakeClient())

    with pytest.raises(ServiceError) as raised:
        openai_service.chat_text("system", "user")
    assert raised.value.status_code == status_code
    assert text in raised.value.message


def test_unexpected_errors_hide_internal_details(monkeypatch):
    from app.api import routes

    def explode(question):
        raise RuntimeError("secret internal stack detail")

    monkeypatch.setattr(routes, "answer_question", explode)
    safe_client = TestClient(app, raise_server_exceptions=False)

    response = safe_client.post("/api/chat", json={"question": "What is Python?"})

    assert response.status_code == 500
    assert "secret internal" not in response.text
