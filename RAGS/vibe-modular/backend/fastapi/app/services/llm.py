"""OpenAI chat completion client."""

import logging

import openai
from openai import OpenAI

from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)


class OpenAIChatClient:
    def __init__(self, api_key: str, model: str, timeout_seconds: float) -> None:
        self._client = OpenAI(api_key=api_key, timeout=timeout_seconds, max_retries=2)
        self._model = model

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
            )
        except openai.APITimeoutError as exc:
            raise LLMError("The language model request timed out. Please try again.") from exc
        except openai.AuthenticationError as exc:
            logger.error("openai_authentication_failed")
            raise LLMError("The language model rejected the configured API key.") from exc
        except openai.RateLimitError as exc:
            raise LLMError("The language model rate limit was reached. Please try again later.") from exc
        except openai.APIError as exc:
            logger.error("openai_request_failed error=%s", type(exc).__name__)
            raise LLMError("The language model request failed.") from exc

        content = response.choices[0].message.content if response.choices else None
        if not content:
            raise LLMError("The language model returned an empty answer.")
        return content.strip()
