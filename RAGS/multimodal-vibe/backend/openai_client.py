"""Shared OpenAI helpers: client creation, friendly error messages, bounded retries.

Only *transient* problems (rate limits, timeouts, connection drops, 5xx errors)
are retried. Wrong keys, missing billing or unknown models fail immediately
with an explanation, because retrying them cannot help.
"""

from __future__ import annotations

import random
import time
from typing import Callable, TypeVar

import openai

T = TypeVar("T")


class OpenAIServiceError(Exception):
    """A user-facing OpenAI problem. `retryable` tells whether it was transient."""

    def __init__(self, message: str, *, retryable: bool = False, attempts: int = 1):
        super().__init__(message)
        self.retryable = retryable
        self.attempts = attempts


def create_client(api_key: str, timeout: float = 60.0) -> openai.OpenAI:
    if not api_key or api_key == "your_openai_api_key_here":
        raise OpenAIServiceError(
            "No OpenAI API key is configured. Add OPENAI_API_KEY to your .env file and restart the app."
        )
    # The SDK has its own retry logic; we disable it so retries are visible and bounded here.
    return openai.OpenAI(api_key=api_key, timeout=timeout, max_retries=0)


def _error_code(exc: Exception) -> str:
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        error = body.get("error", body)
        if isinstance(error, dict):
            return str(error.get("code") or error.get("type") or "")
    return str(getattr(exc, "code", "") or "")


def explain_openai_error(exc: Exception, model: str | None = None) -> OpenAIServiceError:
    """Translate an OpenAI SDK exception into a clear message for students."""
    code = _error_code(exc)
    model_hint = f" '{model}'" if model else ""

    if isinstance(exc, openai.AuthenticationError):
        return OpenAIServiceError(
            "OpenAI rejected the API key (invalid or revoked). Check OPENAI_API_KEY in your .env file."
        )
    if isinstance(exc, openai.PermissionDeniedError):
        return OpenAIServiceError(
            f"Your OpenAI project is not allowed to use model{model_hint}. Choose another model in .env "
            "or enable it for your project on platform.openai.com."
        )
    if isinstance(exc, openai.RateLimitError):
        if code == "insufficient_quota":
            return OpenAIServiceError(
                "Your OpenAI account has no remaining API credits (insufficient_quota). API usage is billed "
                "separately from ChatGPT plans. Add billing at platform.openai.com → Billing."
            )
        return OpenAIServiceError("OpenAI rate limit reached. Wait a moment and try again.", retryable=True)
    if isinstance(exc, openai.NotFoundError) or code == "model_not_found":
        return OpenAIServiceError(
            f"The model{model_hint} was not found or is not available to your account. Set a supported model "
            "name in .env (e.g. OPENAI_CHAT_MODEL=gpt-4.1-mini, OPENAI_EMBEDDING_MODEL=text-embedding-3-small)."
        )
    if isinstance(exc, openai.BadRequestError):
        return OpenAIServiceError(f"OpenAI rejected the request: {getattr(exc, 'message', exc)}")
    if isinstance(exc, (openai.APITimeoutError, openai.APIConnectionError)):
        return OpenAIServiceError(
            "Could not reach OpenAI (network problem or timeout). Check your internet connection.", retryable=True
        )
    if isinstance(exc, openai.InternalServerError):
        return OpenAIServiceError("OpenAI had a temporary server error. Please try again.", retryable=True)
    if isinstance(exc, openai.APIStatusError) and getattr(exc, "status_code", 0) >= 500:
        return OpenAIServiceError("OpenAI is temporarily unavailable. Please try again.", retryable=True)
    if isinstance(exc, OpenAIServiceError):
        return exc
    return OpenAIServiceError(f"Unexpected error while calling OpenAI: {type(exc).__name__}: {exc}")


def call_with_retries(
    func: Callable[[], T],
    *,
    model: str | None = None,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    on_retry: Callable[[int, OpenAIServiceError], None] | None = None,
    sleep: Callable[[float], None] | None = None,
) -> T:
    """Run `func`, retrying transient OpenAI errors with exponential backoff and jitter."""
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001 - every error is translated below
            error = explain_openai_error(exc, model)
            error.attempts = attempt
            if not error.retryable or attempt == max_attempts:
                raise error from exc
            if on_retry:
                on_retry(attempt, error)
            (sleep or time.sleep)(base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.25))
    raise AssertionError("unreachable")
