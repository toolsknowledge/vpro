"""Thin wrapper around the OpenAI SDK.

The client is created lazily so the API can start (health checks, document
listing, UI) without a key. SDK errors are translated into ``LLMServiceError``
with user-safe messages; the API key is never included in messages or logs.
"""

import logging
from typing import Any

import openai

from config import Settings

logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """An OpenAI operation failed. ``message`` is safe to show to end users."""

    def __init__(self, message: str, *, code: str, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class OpenAIConfigurationError(LLMServiceError):
    def __init__(self) -> None:
        super().__init__(
            "OpenAI API key is not configured. Set OPENAI_API_KEY in backend/.env and restart the backend.",
            code="openai_not_configured",
            status_code=503,
        )


def _translate_error(exc: openai.OpenAIError) -> LLMServiceError:
    if isinstance(exc, openai.AuthenticationError):
        return LLMServiceError(
            "OpenAI rejected the API key. Check OPENAI_API_KEY in backend/.env.",
            code="openai_auth_failed",
            status_code=502,
        )
    if isinstance(exc, openai.PermissionDeniedError):
        return LLMServiceError(
            "The OpenAI API key does not have access to the configured model.",
            code="openai_permission_denied",
            status_code=502,
        )
    if isinstance(exc, openai.RateLimitError):
        return LLMServiceError(
            "OpenAI rate limit or quota exceeded. Wait a moment and try again, or check your billing.",
            code="openai_rate_limited",
            status_code=429,
        )
    if isinstance(exc, openai.APITimeoutError):
        return LLMServiceError(
            "The request to OpenAI timed out. Please try again.",
            code="openai_timeout",
            status_code=504,
        )
    if isinstance(exc, openai.APIConnectionError):
        return LLMServiceError(
            "Could not connect to OpenAI. Check your network connection.",
            code="openai_unreachable",
            status_code=503,
        )
    if isinstance(exc, openai.NotFoundError):
        return LLMServiceError(
            "The configured OpenAI model was not found. Check OPENAI_CHAT_MODEL / OPENAI_EMBEDDING_MODEL.",
            code="openai_model_not_found",
            status_code=502,
        )
    if isinstance(exc, openai.APIStatusError):
        return LLMServiceError(
            f"OpenAI returned an error (HTTP {exc.status_code}).",
            code="openai_api_error",
            status_code=502,
        )
    return LLMServiceError("The OpenAI request failed.", code="openai_error", status_code=502)


class OpenAIService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client: openai.OpenAI | None = None

    @property
    def configured(self) -> bool:
        return self._settings.openai_configured

    def _get_client(self) -> openai.OpenAI:
        if self._settings.openai_api_key is None:
            raise OpenAIConfigurationError()
        if self._client is None:
            self._client = openai.OpenAI(
                api_key=self._settings.openai_api_key.get_secret_value(),
                timeout=self._settings.openai_timeout_seconds,
                max_retries=self._settings.openai_max_retries,
            )
        return self._client

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float,
        json_mode: bool = False,
        max_tokens: int | None = None,
    ) -> str:
        """Run a chat completion and return the assistant text."""
        client = self._get_client()
        kwargs: dict[str, Any] = {
            "model": self._settings.openai_chat_model,
            "messages": messages,
            "temperature": temperature,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        try:
            response = client.chat.completions.create(**kwargs)
        except openai.OpenAIError as exc:
            logger.warning("OpenAI chat completion failed: %s", type(exc).__name__)
            raise _translate_error(exc) from exc
        content = response.choices[0].message.content if response.choices else None
        if not content:
            raise LLMServiceError(
                "OpenAI returned an empty response.", code="openai_empty_response", status_code=502
            )
        return content

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts, preserving input order."""
        client = self._get_client()
        try:
            response = client.embeddings.create(model=self._settings.openai_embedding_model, input=texts)
        except openai.OpenAIError as exc:
            logger.warning("OpenAI embedding request failed: %s", type(exc).__name__)
            raise _translate_error(exc) from exc
        ordered = sorted(response.data, key=lambda item: item.index)
        return [list(item.embedding) for item in ordered]
