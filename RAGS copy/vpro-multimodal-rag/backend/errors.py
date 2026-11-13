"""Friendly, beginner-readable errors.

Every error carries a ``user_message`` that the UI can show directly.
"""
from __future__ import annotations

import openai


class AppError(Exception):
    """Base class: ``str(err)`` is always safe and understandable to show a student."""


class UnsupportedFileError(AppError): ...
class FileTooLargeError(AppError): ...
class DocumentReadError(AppError): ...
class NoExtractableTextError(AppError): ...
class EmbeddingError(AppError): ...
class VectorStoreError(AppError): ...
class EmbeddingModelMismatchError(AppError): ...
class LLMError(AppError): ...
class InvalidChunkSettingsError(AppError): ...
class MissingApiKeyError(AppError): ...


def _is_quota(exc: Exception) -> bool:
    code = getattr(exc, "code", None)
    return code == "insufficient_quota" or "insufficient_quota" in str(exc)


def is_transient(exc: Exception) -> bool:
    """Only these are worth retrying (bounded, with backoff)."""
    if isinstance(exc, openai.RateLimitError):
        return not _is_quota(exc)
    return isinstance(exc, (openai.APIConnectionError, openai.APITimeoutError, openai.InternalServerError))


def translate_openai_error(exc: Exception, kind: type[AppError] = AppError, model: str = "") -> AppError:
    """Convert an OpenAI SDK exception into a friendly AppError."""
    if isinstance(exc, openai.AuthenticationError):
        msg = "OpenAI rejected the API key (invalid or revoked). Check OPENAI_API_KEY in your .env file."
    elif isinstance(exc, openai.PermissionDeniedError):
        msg = f"Your OpenAI account/project is not allowed to use this feature or model ({model or 'unknown'})."
    elif isinstance(exc, openai.RateLimitError) and _is_quota(exc):
        msg = ("OpenAI says your API quota is used up or billing is not set up. "
               "Add credits at platform.openai.com → Billing. (A ChatGPT subscription does not include API credits.)")
    elif isinstance(exc, openai.RateLimitError):
        msg = "OpenAI rate limit reached even after retrying. Wait a minute and try again, or index fewer files at once."
    elif isinstance(exc, openai.NotFoundError):
        msg = (f"The model {model!r} was not found or is not available to your account. "
               "Set OPENAI_CHAT_MODEL / OPENAI_EMBEDDING_MODEL in .env to a supported model and restart.")
    elif isinstance(exc, openai.APITimeoutError):
        msg = "The request to OpenAI timed out. Check your connection and try again."
    elif isinstance(exc, openai.APIConnectionError):
        msg = "Could not connect to OpenAI. Check your internet connection and try again."
    elif isinstance(exc, openai.BadRequestError):
        msg = f"OpenAI rejected the request: {getattr(exc, 'message', exc)}"
    elif isinstance(exc, openai.InternalServerError):
        msg = "OpenAI had a temporary server problem. Please try again shortly."
    else:
        msg = f"Unexpected OpenAI error ({type(exc).__name__}): {exc}"
    return kind(msg)
