"""Embedding generation for document chunks and queries."""

from services.openai_service import OpenAIService


class EmbeddingService:
    def __init__(self, openai_service: OpenAIService, batch_size: int) -> None:
        self._openai = openai_service
        self._batch_size = batch_size

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []
        for start in range(0, len(texts), self._batch_size):
            embeddings.extend(self._openai.embed(texts[start : start + self._batch_size]))
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        return self._openai.embed([text])[0]
