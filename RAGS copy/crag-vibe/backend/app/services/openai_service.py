"""All calls to OpenAI (embeddings and chat) go through this module.

OpenAI errors are translated into ServiceError with messages students can understand.
Technical details are written to the server log only.
"""

import json
import logging
from functools import lru_cache

import openai
from openai import OpenAI

from app import config
from app.errors import ServiceError

logger = logging.getLogger("crag.openai")

EMBEDDING_BATCH_SIZE = 100


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    if not config.is_openai_configured():
        raise ServiceError(
            "The AI service is not configured yet. Please set OPENAI_API_KEY in backend/.env and restart the backend.",
            503,
        )
    return OpenAI(api_key=config.OPENAI_API_KEY, timeout=config.OPENAI_TIMEOUT_SECONDS, max_retries=2)


def _to_service_error(error: Exception) -> ServiceError:
    """Map OpenAI SDK exceptions to friendly messages (order matters: timeout is a connection error)."""
    logger.error("OpenAI request failed: %s: %s", type(error).__name__, error)
    if isinstance(error, openai.AuthenticationError):
        return ServiceError("The AI service rejected the API key. Please check OPENAI_API_KEY in backend/.env.", 503)
    if isinstance(error, openai.PermissionDeniedError):
        return ServiceError("The API key does not have permission to use this AI model.", 503)
    if isinstance(error, openai.RateLimitError):
        return ServiceError("The AI service is busy or the usage limit was reached. Please wait a moment and try again.", 429)
    if isinstance(error, openai.APITimeoutError):
        return ServiceError("The AI service took too long to respond. Please try again.", 504)
    if isinstance(error, openai.APIConnectionError):
        return ServiceError("Could not reach the AI service. Please check the internet connection and try again.", 503)
    if isinstance(error, (openai.NotFoundError, openai.BadRequestError)):
        return ServiceError("The AI model configuration is invalid. Please check the model names in backend/.env.", 500)
    return ServiceError("The AI service returned an error. Please try again.", 502)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Create one embedding vector per text using the configured embedding model."""
    client = get_client()
    vectors: list[list[float]] = []
    try:
        for start in range(0, len(texts), EMBEDDING_BATCH_SIZE):
            batch = texts[start:start + EMBEDDING_BATCH_SIZE]
            response = client.embeddings.create(model=config.OPENAI_EMBEDDING_MODEL, input=batch)
            vectors.extend(item.embedding for item in sorted(response.data, key=lambda item: item.index))
    except openai.OpenAIError as error:
        raise _to_service_error(error) from error
    if len(vectors) != len(texts):
        raise ServiceError("The AI service returned an incomplete embedding response. Please try again.", 502)
    return vectors


def _chat(system_prompt: str, user_prompt: str, temperature: float, json_mode: bool) -> str:
    client = get_client()
    try:
        response = client.chat.completions.create(
            model=config.OPENAI_CHAT_MODEL,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            **({"response_format": {"type": "json_object"}} if json_mode else {}),
        )
    except openai.OpenAIError as error:
        raise _to_service_error(error) from error
    content = response.choices[0].message.content if response.choices else None
    if not content or not content.strip():
        raise ServiceError("The AI service returned an empty response. Please try again.", 502)
    return content.strip()


def chat_text(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    return _chat(system_prompt, user_prompt, temperature, json_mode=False)


def chat_json(system_prompt: str, user_prompt: str) -> dict:
    content = _chat(system_prompt, user_prompt, temperature=0, json_mode=True)
    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        logger.error("OpenAI returned invalid JSON: %s", content[:300])
        raise ServiceError("The AI service returned an unexpected response. Please try again.", 502) from error
    if not isinstance(data, dict):
        raise ServiceError("The AI service returned an unexpected response. Please try again.", 502)
    return data
