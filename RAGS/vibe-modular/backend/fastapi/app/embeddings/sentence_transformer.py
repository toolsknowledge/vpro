"""Sentence Transformers embedding model, loaded once and reused for indexing and queries."""

import logging

from sentence_transformers import SentenceTransformer

from app.core.exceptions import EmbeddingError

logger = logging.getLogger(__name__)


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str) -> None:
        logger.info("loading_embedding_model model=%s", model_name)
        try:
            self._model = SentenceTransformer(model_name)
        except Exception as exc:
            raise EmbeddingError(f"Could not load embedding model '{model_name}'.") from exc

        dimension = self._model.get_embedding_dimension()
        if not dimension:
            raise EmbeddingError(f"Embedding model '{model_name}' does not report a fixed dimension.")
        self.dimension: int = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return L2-normalized embeddings so dot product equals cosine similarity in every store."""
        if not texts:
            return []
        try:
            vectors = self._model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
        except Exception as exc:
            logger.exception("embedding_failed count=%d", len(texts))
            raise EmbeddingError("Failed to generate embeddings.") from exc
        return vectors.tolist()
