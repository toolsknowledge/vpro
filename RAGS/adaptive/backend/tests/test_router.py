import json

import pytest

from schemas.chat import Route
from services.adaptive_router import FALLBACK_REASON, AdaptiveRouter
from services.openai_service import LLMServiceError


@pytest.fixture
def router(fake_openai):
    return AdaptiveRouter(fake_openai, temperature=0.0)


def test_direct_route(router, fake_openai):
    fake_openai.classifier_reply = json.dumps({"route": "DIRECT", "reason": "General concept question."})
    decision = router.classify("What is RAG in simple words?", [], ["notes.md"])
    assert decision.route is Route.DIRECT
    assert decision.reason == "General concept question."
    assert decision.fallback is False


def test_retrieve_route_keeps_search_query(router, fake_openai):
    fake_openai.classifier_reply = json.dumps(
        {"route": "RETRIEVE", "reason": "Asks about the notes.", "search_query": "Adaptive RAG definition"}
    )
    decision = router.classify("Explain Adaptive RAG from the course notes.", [], [])
    assert decision.route is Route.RETRIEVE
    assert decision.search_query == "Adaptive RAG definition"
    assert decision.clarifying_question is None


def test_clarify_route(router, fake_openai):
    fake_openai.classifier_reply = json.dumps(
        {"route": "CLARIFY", "reason": "No topic given.", "clarifying_question": "What should I explain?"}
    )
    decision = router.classify("Explain it.", [], [])
    assert decision.route is Route.CLARIFY
    assert decision.clarifying_question == "What should I explain?"


def test_classifier_receives_history_and_sources(router, fake_openai):
    history = [
        {"role": "user", "content": "Compare Hybrid RAG and Advanced RAG"},
        {"role": "assistant", "content": "Hybrid RAG combines... Advanced RAG adds..."},
    ]
    router.classify("What about the second one?", history, ["hybrid_vs_advanced_rag.docx"])
    messages = fake_openai.classifier_calls[0]["messages"]
    assert "hybrid_vs_advanced_rag.docx" in messages[0]["content"]
    assert messages[1:3] == history
    assert messages[-1] == {"role": "user", "content": "What about the second one?"}
    assert fake_openai.classifier_calls[0]["temperature"] == 0.0


@pytest.mark.parametrize("greeting", ["Hi", "hello!", "Thank you.", "Good morning"])
def test_pure_greetings_skip_the_classifier_call(router, fake_openai, greeting):
    decision = router.classify(greeting, [], [])
    assert decision.route is Route.DIRECT
    assert fake_openai.chat_calls == []


@pytest.mark.parametrize(
    "raw",
    [
        "not json at all",
        "[]",
        json.dumps({"route": "SEARCH_WEB", "reason": "x"}),
        json.dumps({"route": "RETRIEVE"}),
        json.dumps({"route": "CLARIFY", "reason": "Ambiguous."}),
        json.dumps({"route": "DIRECT", "reason": "x" * 1000}),
    ],
    ids=["invalid-json", "wrong-type", "unknown-route", "missing-reason", "clarify-without-question", "too-long"],
)
def test_invalid_classifier_output_falls_back_to_retrieve(raw):
    decision = AdaptiveRouter.parse(raw)
    assert decision.route is Route.RETRIEVE
    assert decision.fallback is True
    assert decision.reason == FALLBACK_REASON


def test_api_errors_are_not_masked_by_fallback(router, fake_openai):
    fake_openai.chat_error = LLMServiceError("boom", code="openai_unreachable", status_code=503)
    with pytest.raises(LLMServiceError):
        router.classify("Explain Adaptive RAG", [], [])
