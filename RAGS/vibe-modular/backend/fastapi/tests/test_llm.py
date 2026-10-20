from types import SimpleNamespace

import httpx
import openai
import pytest

from app.core.exceptions import LLMError
from app.services.llm import OpenAIChatClient

REQUEST = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")


@pytest.fixture
def client() -> OpenAIChatClient:
    return OpenAIChatClient(api_key="sk-test", model="gpt-test", timeout_seconds=5)


def _stub_create(client: OpenAIChatClient, monkeypatch: pytest.MonkeyPatch, result=None, error=None) -> list[dict]:
    calls: list[dict] = []

    def create(**kwargs):
        calls.append(kwargs)
        if error:
            raise error
        return result

    monkeypatch.setattr(client._client.chat.completions, "create", create)
    return calls


def _completion(content: str | None) -> SimpleNamespace:
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


def test_sends_system_and_user_prompts_to_configured_model(client, monkeypatch) -> None:
    calls = _stub_create(client, monkeypatch, result=_completion("  An answer.  "))

    assert client.complete("system rules", "user question") == "An answer."
    assert calls[0]["model"] == "gpt-test"
    assert calls[0]["messages"] == [
        {"role": "system", "content": "system rules"},
        {"role": "user", "content": "user question"},
    ]


@pytest.mark.parametrize(
    ("error", "message"),
    [
        (openai.APITimeoutError(request=REQUEST), "timed out"),
        (openai.APIConnectionError(request=REQUEST), "request failed"),
        (
            openai.AuthenticationError("bad key", response=httpx.Response(401, request=REQUEST), body=None),
            "API key",
        ),
        (openai.RateLimitError("slow down", response=httpx.Response(429, request=REQUEST), body=None), "rate limit"),
    ],
)
def test_api_errors_become_llm_errors(client, monkeypatch, error: Exception, message: str) -> None:
    _stub_create(client, monkeypatch, error=error)
    with pytest.raises(LLMError, match=message):
        client.complete("system", "user")


def test_empty_completion_is_an_error(client, monkeypatch) -> None:
    _stub_create(client, monkeypatch, result=_completion(None))
    with pytest.raises(LLMError, match="empty"):
        client.complete("system", "user")
