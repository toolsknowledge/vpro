"""Semantic retrieval: question → query embedding → nearest chunks in ChromaDB.

Also contains the citation formatter and simple diagnostics that warn when
the retrieved chunks are probably not relevant to the question.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from backend.embeddings import EmbeddingService
from backend.vector_store import VectorStore, distance_to_similarity

# Below this cosine similarity, OpenAI embeddings are usually only loosely related.
WEAK_SIMILARITY = 0.30

_STOPWORDS = set(
    """a an and are as at be by can could did do does for from has have how i if in into is it its
    me my of on or our please show so than that the their them then there these this to was what
    when where which who why will with would you your about tell give list describe explain""".split()
)


@dataclass
class RetrievedChunk:
    rank: int
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    distance: float
    similarity: float | None
    citation: str
    keyword_overlap: float  # share of the question's keywords that appear in this chunk


@dataclass
class RetrievalResult:
    question: str
    top_k: int
    metric: str
    query_dimension: int
    embedding_model: str
    chunks: list[RetrievedChunk] = field(default_factory=list)  # passed the threshold
    filtered_out: list[RetrievedChunk] = field(default_factory=list)  # below the threshold
    min_similarity: float | None = None
    diagnostics: list[str] = field(default_factory=list)

    @property
    def found_anything(self) -> bool:
        return bool(self.chunks)


def format_citation(metadata: dict[str, Any]) -> str:
    """Build a citation from metadata that was actually recorded at ingestion time."""
    parts = [str(metadata.get("source_file", "unknown source"))]
    if metadata.get("page_number") is not None:
        parts.append(f"page {metadata['page_number']}")
    if metadata.get("sheet_name"):
        parts.append(f"sheet '{metadata['sheet_name']}'")
        start, end = metadata.get("row_start"), metadata.get("row_end")
        if start is not None:
            parts.append(f"row {start}" if start == end or end is None else f"rows {start}–{end}")
    if metadata.get("section_title"):
        parts.append(f"section '{metadata['section_title']}'")
    return ", ".join(parts)


def keywords(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9][a-z0-9+#.\-]*", text.lower())
    return {w.strip(".-") for w in words if w not in _STOPWORDS and len(w) > 2}


def keyword_overlap(question: str, text: str) -> float:
    terms = keywords(question)
    if not terms:
        return 0.0
    haystack = text.lower()
    return sum(1 for t in terms if t in haystack) / len(terms)


def keyword_search(store: VectorStore, question: str, top_k: int) -> list[tuple[int, str, str, dict]]:
    """Plain keyword search for comparison: rank chunks by how many question words they contain.

    Scans every stored chunk, which is fine for a classroom-sized collection.
    Returns (matches, chunk_id, text, metadata).
    """
    terms = keywords(question)
    if not terms:
        return []
    scored = []
    for record in store.get_records():
        lower = record.text.lower()
        hits = sum(1 for t in terms if t in lower)
        if hits:
            scored.append((hits, record.chunk_id, record.text, record.metadata))
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[:top_k]


class Retriever:
    def __init__(self, embedder: EmbeddingService, store: VectorStore):
        self.embedder = embedder
        self.store = store

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        min_similarity: float | None = None,
        where: dict | None = None,
    ) -> RetrievalResult:
        question = (question or "").strip()
        if not question:
            raise ValueError("Please type a question first.")
        if min_similarity is not None and not -1.0 <= min_similarity <= 1.0:
            raise ValueError("The similarity threshold must be between -1 and 1.")

        metric = self.store.distance_metric
        if min_similarity is not None and distance_to_similarity(0.0, metric) is None:
            raise ValueError(f"A similarity threshold cannot be used with the '{metric}' distance metric.")

        # Same model for the question as for the stored chunks, or the vectors are not comparable.
        self.store.check_compatible(self.embedder.model)
        query_vector = self.embedder.embed_query(question)
        hits = self.store.query(query_vector, top_k, where=where)

        result = RetrievalResult(
            question=question,
            top_k=top_k,
            metric=metric,
            query_dimension=len(query_vector),
            embedding_model=self.embedder.model,
            min_similarity=min_similarity,
        )
        for rank, hit in enumerate(hits, start=1):
            similarity = distance_to_similarity(hit.distance, metric)
            chunk = RetrievedChunk(
                rank=rank,
                chunk_id=hit.chunk_id,
                text=hit.text,
                metadata=hit.metadata,
                distance=hit.distance,
                similarity=similarity,
                citation=format_citation(hit.metadata),
                keyword_overlap=keyword_overlap(question, hit.text),
            )
            if min_similarity is not None and similarity is not None and similarity < min_similarity:
                result.filtered_out.append(chunk)
            else:
                result.chunks.append(chunk)

        result.diagnostics = diagnose(result, self.store.count())
        return result


def diagnose(result: RetrievalResult, collection_size: int) -> list[str]:
    """Plain-English warnings about retrieval quality. Empty list = nothing suspicious."""
    notes = []
    if collection_size == 0:
        return ["The ChromaDB collection is empty. Upload and index documents first."]
    if not result.chunks and result.filtered_out:
        best = max(c.similarity or 0 for c in result.filtered_out)
        notes.append(
            f"All {len(result.filtered_out)} retrieved chunks were below the similarity threshold "
            f"{result.min_similarity:.2f} (best was {best:.2f}). Lower the threshold or rephrase the question."
        )
    elif not result.chunks:
        notes.append("No chunks were retrieved.")
    sims = [c.similarity for c in result.chunks if c.similarity is not None]
    if sims and max(sims) < WEAK_SIMILARITY:
        notes.append(
            f"The best match has a low similarity ({max(sims):.2f}). The documents may not cover this "
            "question, so the retrieved chunks are probably not relevant."
        )
    if result.chunks and all(c.keyword_overlap == 0 for c in result.chunks) and keywords(result.question):
        notes.append(
            "None of the retrieved chunks contain any of the question's keywords. That can be fine for "
            "semantic search (synonyms), but check the chunks before trusting the answer."
        )
    return notes
