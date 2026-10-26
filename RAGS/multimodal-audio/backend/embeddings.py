"""Embeddings: turn text into vectors with the OpenAI embeddings API.

An embedding is a list of numbers (1536 of them for text-embedding-3-small)
that captures the *meaning* of a text. Texts with similar meaning get vectors
that point in similar directions, which is what semantic search relies on.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from backend.openai_client import OpenAIServiceError, call_with_retries

# OpenAI accepts up to 2048 inputs per request; smaller batches fail more gracefully.
DEFAULT_BATCH_SIZE = 64


@dataclass
class EmbeddingBatchResult:
    vectors: list[list[float]]
    model: str
    dimension: int
    retries: int = 0
    retry_messages: list[str] = field(default_factory=list)


class EmbeddingService:
    def __init__(self, client, model: str, batch_size: int = DEFAULT_BATCH_SIZE, max_attempts: int = 3):
        self.client = client
        self.model = model
        self.batch_size = batch_size
        self.max_attempts = max_attempts

    def _embed_batch(self, texts: list[str], on_retry) -> list[list[float]]:
        response = call_with_retries(
            lambda: self.client.embeddings.create(model=self.model, input=texts),
            model=self.model,
            max_attempts=self.max_attempts,
            on_retry=on_retry,
        )
        # The API returns items with an `index`; sort to be sure the order matches `texts`.
        items = sorted(response.data, key=lambda item: item.index)
        if len(items) != len(texts):
            raise OpenAIServiceError(f"OpenAI returned {len(items)} embeddings for {len(texts)} texts.")
        return [list(item.embedding) for item in items]

    def embed_texts(
        self, texts: list[str], progress: Callable[[int, int], None] | None = None
    ) -> EmbeddingBatchResult:
        """Embed many texts in batches. Raises OpenAIServiceError if any batch fails.

        All-or-nothing on purpose: a document is only stored when *every* chunk
        has a vector, so a half-embedded document is never marked as indexed.
        """
        if not texts:
            return EmbeddingBatchResult(vectors=[], model=self.model, dimension=0)
        if any(not t.strip() for t in texts):
            raise ValueError("Cannot embed empty text.")

        retry_messages: list[str] = []

        def on_retry(attempt: int, error: OpenAIServiceError):
            retry_messages.append(f"Attempt {attempt} failed ({error}); retrying…")

        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            vectors.extend(self._embed_batch(batch, on_retry))
            if progress:
                progress(len(vectors), len(texts))

        dimensions = {len(v) for v in vectors}
        if len(dimensions) != 1:
            raise OpenAIServiceError(f"Embeddings came back with inconsistent dimensions: {sorted(dimensions)}")
        return EmbeddingBatchResult(
            vectors=vectors,
            model=self.model,
            dimension=dimensions.pop(),
            retries=len(retry_messages),
            retry_messages=retry_messages,
        )

    def embed_query(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("The question is empty.")
        return self._embed_batch([text.strip()], on_retry=None)[0]
