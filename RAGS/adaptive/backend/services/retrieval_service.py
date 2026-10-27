"""Vector search with a relevance gate."""

from dataclasses import dataclass

from services.chroma_service import ChromaService, SearchHit
from services.embedding_service import EmbeddingService


@dataclass(frozen=True)
class RetrievalResult:
    hits: list[SearchHit]
    relevant_hits: list[SearchHit]
    threshold: float

    @property
    def top_score(self) -> float | None:
        return max((hit.relevance for hit in self.hits), default=None)

    @property
    def has_relevant_context(self) -> bool:
        return bool(self.relevant_hits)


class RetrievalService:
    def __init__(self, embedder: EmbeddingService, chroma: ChromaService, top_k: int, threshold: float) -> None:
        self._embedder = embedder
        self._chroma = chroma
        self._top_k = top_k
        self._threshold = threshold

    def retrieve(self, query: str) -> RetrievalResult:
        # An empty collection cannot answer anything; skip the embedding call.
        if self._chroma.count() == 0:
            return RetrievalResult(hits=[], relevant_hits=[], threshold=self._threshold)
        hits = self._chroma.query(self._embedder.embed_query(query), self._top_k)
        relevant = [hit for hit in hits if hit.relevance >= self._threshold]
        return RetrievalResult(hits=hits, relevant_hits=relevant, threshold=self._threshold)
