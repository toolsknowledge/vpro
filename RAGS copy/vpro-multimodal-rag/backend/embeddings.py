"""Step 5: turn text into vectors with the OpenAI embeddings API.

An *embedding* is a list of numbers (a vector) that captures the meaning of a
piece of text.  Texts with similar meaning get vectors that point in similar
directions, which is what makes semantic search possible.
"""
from __future__ import annotations

import time
from typing import Callable, Optional, Sequence

from openai import OpenAI

from backend.errors import EmbeddingError, MissingApiKeyError, is_transient, translate_openai_error
from config.settings import Settings


def get_client(settings: Settings) -> OpenAI:
    if not settings.has_api_key:
        raise MissingApiKeyError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env, add your key, and restart the app.")
    return OpenAI(api_key=settings.openai_api_key, timeout=60.0, max_retries=0)  # we do our own bounded retries


class OpenAIEmbedder:
    def __init__(self, client, model: str, batch_size: int = 64, max_attempts: int = 4,
                 base_delay: float = 1.0, sleep: Callable[[float], None] = time.sleep):
        self.client, self.model = client, model
        self.batch_size, self.max_attempts, self.base_delay, self._sleep = batch_size, max_attempts, base_delay, sleep
        self.retries = 0
        self.retry_log: list[str] = []

    def _embed_batch(self, batch: list[str]) -> list[list[float]]:
        for attempt in range(1, self.max_attempts + 1):
            try:
                resp = self.client.embeddings.create(model=self.model, input=batch)
                data = sorted(resp.data, key=lambda d: d.index)
                if len(data) != len(batch):
                    raise EmbeddingError("OpenAI returned a different number of vectors than texts sent.")
                return [list(d.embedding) for d in data]
            except EmbeddingError:
                raise
            except Exception as exc:
                if is_transient(exc) and attempt < self.max_attempts:
                    self.retries += 1
                    delay = self.base_delay * (2 ** (attempt - 1))
                    self.retry_log.append(f"{type(exc).__name__}: retry {attempt}/{self.max_attempts - 1} in {delay:.0f}s")
                    self._sleep(delay)
                    continue
                raise translate_openai_error(exc, EmbeddingError, self.model) from exc
        raise EmbeddingError("Embedding failed.")  # pragma: no cover

    def embed_texts(self, texts: Sequence[str], progress: Optional[Callable[[int, int], None]] = None) -> list[list[float]]:
        """Embed all texts in batches. Raises EmbeddingError if any batch fails (no partial results)."""
        texts = list(texts)
        if any(not t.strip() for t in texts):
            raise EmbeddingError("Cannot embed empty text.")
        out: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            out.extend(self._embed_batch(texts[i:i + self.batch_size]))
            if progress:
                progress(len(out), len(texts))
        return out

    def embed_query(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise EmbeddingError("The question is empty.")
        return self._embed_batch([text.strip()])[0]
