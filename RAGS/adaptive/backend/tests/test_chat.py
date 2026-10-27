import json

import pytest

from schemas.chat import MAX_QUESTION_LENGTH
from services.answer_service import EMPTY_INDEX_MESSAGE, NO_RELEVANT_CONTEXT_MESSAGE
from services.openai_service import LLMServiceError, OpenAIConfigurationError

SESSION = "test-session-0001"


def route_reply(route: str, **extra) -> str:
    return json.dumps({"route": route, "reason": f"{route} chosen for test.", **extra})


@pytest.fixture
def indexed(sample_docs, indexing_service):
    result = indexing_service.run("index")
    assert result.status == "success"
    return result


def test_direct_route_skips_retrieval(client, fake_openai, indexed):
    fake_openai.classifier_reply = route_reply("DIRECT")
    fake_openai.embed_calls.clear()

    body = client.post("/api/chat", json={"question": "What is RAG in simple words?", "session_id": SESSION}).json()

    assert body["route"] == "DIRECT"
    assert body["answer"] == "Fake generated answer."
    assert body["sources"] == []
    assert body["retrieval_performed"] is False
    assert body["retrieval_count"] == 0
    assert body["relevance_score"] is None
    assert body["grounded"] is False
    assert fake_openai.embed_calls == []


def test_retrieve_route_answers_from_relevant_context(client, fake_openai, indexed):
    fake_openai.classifier_reply = route_reply("RETRIEVE", search_query="What is ChromaDB vector database")
    fake_openai.embed_calls.clear()

    body = client.post(
        "/api/chat", json={"question": "What is ChromaDB according to the sample documents?", "session_id": SESSION}
    ).json()

    assert body["route"] == "RETRIEVE"
    assert body["retrieval_performed"] is True
    assert body["grounded"] is True
    assert body["retrieval_count"] >= len(body["sources"]) > 0
    assert all(source["relevance"] >= body["relevance_threshold"] for source in body["sources"])
    assert body["relevance_score"] == max(source["relevance"] for source in body["sources"])
    assert any("ChromaDB" in source["snippet"] for source in body["sources"])
    # The search used the classifier's standalone query, embedded exactly once.
    assert fake_openai.embed_calls == [["What is ChromaDB vector database"]]
    # The answer prompt contains the retrieved context and grounding instructions.
    system_prompt = fake_openai.answer_calls[-1]["messages"][0]["content"]
    assert "ONLY" in system_prompt
    assert body["sources"][0]["snippet"][:40] in system_prompt


def test_retrieve_with_low_relevance_does_not_generate(client, fake_openai, indexed):
    fake_openai.classifier_reply = route_reply("RETRIEVE")

    body = client.post(
        "/api/chat", json={"question": "zebra xylophone quokka marmalade", "session_id": SESSION}
    ).json()

    assert body["route"] == "RETRIEVE"
    assert body["retrieval_performed"] is True
    assert body["grounded"] is False
    assert body["sources"] == []
    assert body["answer"] == NO_RELEVANT_CONTEXT_MESSAGE
    assert body["relevance_score"] is not None and body["relevance_score"] < body["relevance_threshold"]
    assert fake_openai.answer_calls == []


def test_retrieve_with_empty_index(client, fake_openai):
    fake_openai.classifier_reply = route_reply("RETRIEVE")

    body = client.post("/api/chat", json={"question": "Explain Adaptive RAG from the notes."}).json()

    assert body["answer"] == EMPTY_INDEX_MESSAGE
    assert body["retrieval_count"] == 0
    assert body["sources"] == []
    assert fake_openai.embed_calls == []  # nothing to search, so no embedding call
    assert fake_openai.answer_calls == []


def test_clarify_route_asks_follow_up_without_retrieval(client, fake_openai, indexed):
    fake_openai.classifier_reply = route_reply("CLARIFY", clarifying_question="What would you like me to explain?")
    fake_openai.embed_calls.clear()

    body = client.post("/api/chat", json={"question": "Explain it.", "session_id": SESSION}).json()

    assert body["route"] == "CLARIFY"
    assert body["answer"] == "What would you like me to explain?"
    assert body["retrieval_performed"] is False
    assert fake_openai.embed_calls == []
    assert fake_openai.answer_calls == []


def test_invalid_classifier_output_uses_fallback_route(client, fake_openai, indexed):
    fake_openai.classifier_reply = "definitely not json"

    body = client.post(
        "/api/chat", json={"question": "What is ChromaDB vector database?", "session_id": SESSION}
    ).json()

    assert body["route"] == "RETRIEVE"
    assert body["classifier_fallback"] is True
    assert body["retrieval_performed"] is True


def test_history_is_bounded_and_isolated_per_session(client, fake_openai):
    fake_openai.classifier_reply = route_reply("DIRECT")
    for number in range(5):
        client.post("/api/chat", json={"question": f"question {number}", "session_id": SESSION})
    client.post("/api/chat", json={"question": "other session", "session_id": "another-session-01"})

    last_classifier_messages = fake_openai.classifier_calls[-1]["messages"]
    assert [m["content"] for m in last_classifier_messages[1:]] == ["other session"]

    fake_openai.chat_calls.clear()
    client.post("/api/chat", json={"question": "follow up", "session_id": SESSION})
    history = fake_openai.classifier_calls[0]["messages"][1:-1]
    assert len(history) == 6  # max_turns=3 -> 3 question/answer pairs
    assert history[0]["content"] == "question 2"


def test_clearing_a_session_forgets_history(client, fake_openai):
    fake_openai.classifier_reply = route_reply("DIRECT")
    client.post("/api/chat", json={"question": "remember me", "session_id": SESSION})
    assert client.delete(f"/api/chat/sessions/{SESSION}").status_code == 204

    fake_openai.chat_calls.clear()
    client.post("/api/chat", json={"question": "anything?", "session_id": SESSION})
    assert len(fake_openai.classifier_calls[0]["messages"]) == 2


def test_server_generates_session_id_when_missing(client, fake_openai):
    body = client.post("/api/chat", json={"question": "What is RAG?"}).json()
    assert len(body["session_id"]) >= 8


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"question": ""},
        {"question": "   "},
        {"question": "x" * (MAX_QUESTION_LENGTH + 1)},
        {"question": 42},
        {"question": "ok", "session_id": "bad id with spaces"},
        {"question": "ok", "session_id": "short"},
    ],
    ids=["missing", "empty", "blank", "too-long", "wrong-type", "bad-session-chars", "short-session"],
)
def test_invalid_requests_are_rejected(client, fake_openai, payload):
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    assert fake_openai.chat_calls == []


def test_missing_api_key_returns_helpful_503(client, fake_openai):
    fake_openai.chat_error = OpenAIConfigurationError()
    response = client.post("/api/chat", json={"question": "Explain Adaptive RAG"})
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "openai_not_configured"
    assert "OPENAI_API_KEY" in response.json()["error"]["message"]


def test_openai_failure_is_reported_not_fabricated(client, fake_openai):
    fake_openai.chat_error = LLMServiceError("Rate limited.", code="openai_rate_limited", status_code=429)
    response = client.post("/api/chat", json={"question": "Explain Adaptive RAG"})
    assert response.status_code == 429
    assert response.json() == {"error": {"code": "openai_rate_limited", "message": "Rate limited."}}


def test_unexpected_errors_hide_internals(settings, chat_service, monkeypatch):
    from fastapi.testclient import TestClient

    from dependencies import get_chat_service
    from main import app

    def explode(*_args, **_kwargs):
        raise RuntimeError("secret internal detail")

    monkeypatch.setattr(chat_service, "ask", explode)
    app.dependency_overrides[get_chat_service] = lambda: chat_service
    try:
        with TestClient(app, raise_server_exceptions=False) as test_client:
            response = test_client.post("/api/chat", json={"question": "hi there friend"})
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "internal_error"
    assert "secret internal detail" not in response.text
