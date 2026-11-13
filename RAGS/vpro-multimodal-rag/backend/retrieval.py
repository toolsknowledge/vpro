"""Question → query embedding → ChromaDB search → ranked chunks (+ diagnostics)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

from backend.errors import AppError, EmbeddingError
from backend.vector_store import VectorStore


@dataclass
class RetrievedChunk:
    rank: int
    chunk_id: str
    text: str
    metadata: dict
    distance: float
    similarity: Optional[float]

    @property
    def citation(self) -> str:
        return citation_label(self.metadata)


@dataclass
class RetrievalResult:
    query: str
    embedding_dim: int
    k_requested: int
    metric: str
    threshold: Optional[float]
    hits: list[RetrievedChunk] = field(default_factory=list)
    dropped_by_threshold: int = 0
    candidates: int = 0


def distance_to_similarity(distance: float, metric: str) -> Optional[float]:
    """Chroma returns *distances*.  cosine: d = 1 − cos_sim.  ip: d = 1 − dot.  l2 has no bounded similarity."""
    if metric in ("cosine", "ip"):
        return 1.0 - distance
    return None


def validate_threshold(threshold: Optional[float], metric: str) -> Optional[float]:
    if threshold is None:
        return None
    if metric != "cosine":
        raise AppError(f"A similarity threshold is only supported for the cosine metric (collection uses {metric}).")
    if not 0.0 <= threshold <= 1.0:
        raise AppError("The similarity threshold must be between 0.0 and 1.0 for cosine similarity.")
    return float(threshold)


def citation_label(md: dict) -> str:
    """Build a citation using ONLY location fields that exist in the metadata."""
    parts = [md.get("source_file", "unknown source")]
    if md.get("page_number") is not None:
        parts.append(f"page {md['page_number']}")
    if md.get("sheet_name"):
        parts.append(f"sheet `{md['sheet_name']}`")
    r0, r1 = md.get("row_start"), md.get("row_end")
    if r0 is not None:
        parts.append(f"row {r0}" if r0 == r1 or r1 is None else f"rows {r0}–{r1}")
    if md.get("section_title") and md.get("document_type") in ("docx", "txt"):
        parts.append(f"section `{md['section_title']}`")
    return ", ".join(parts)


def format_context(hits: Sequence[RetrievedChunk]) -> str:
    blocks = [f"[{h.rank}] Source: {h.citation}\n{h.text}" for h in hits]
    return "\n\n---\n\n".join(blocks)


class Retriever:
    def __init__(self, store: VectorStore, embedder):
        self.store, self.embedder = store, embedder

    def retrieve(self, query: str, k: int = 5, threshold: Optional[float] = None,
                 source_files: Optional[Sequence[str]] = None) -> RetrievalResult:
        query = (query or "").strip()
        if not query:
            raise EmbeddingError("Please type a question first.")
        if k <= 0:
            raise AppError("Top K must be at least 1.")
        self.store.assert_compatible()
        metric = self.store.distance_metric
        threshold = validate_threshold(threshold, metric)
        vec = self.embedder.embed_query(query)
        stored_dim = self.store.stored_dimension()
        if stored_dim is not None and stored_dim != len(vec):
            from backend.errors import EmbeddingModelMismatchError
            raise EmbeddingModelMismatchError(
                f"Query vector has {len(vec)} dimensions but the database has {stored_dim}. Re-index your documents.")
        where = None
        if source_files:
            where = {"source_file": source_files[0]} if len(source_files) == 1 else {"source_file": {"$in": list(source_files)}}
        raw = self.store.query(vec, k, where=where)
        hits, dropped = [], 0
        for r in raw:
            sim = distance_to_similarity(r["distance"], metric)
            if threshold is not None and sim is not None and sim < threshold:
                dropped += 1
                continue
            hits.append(RetrievedChunk(rank=len(hits) + 1, chunk_id=r["id"], text=r["document"],
                                       metadata=r["metadata"], distance=r["distance"], similarity=sim))
        return RetrievalResult(query=query, embedding_dim=len(vec), k_requested=k, metric=metric,
                               threshold=threshold, hits=hits, dropped_by_threshold=dropped, candidates=len(raw))


def diagnose(result: RetrievalResult, weak_similarity: float = 0.25) -> list[tuple[str, str]]:
    """Honest, beginner-friendly notes: list of (level, message) where level is ok|warning|error."""
    notes: list[tuple[str, str]] = []
    if result.candidates == 0:
        notes.append(("error", "ChromaDB returned nothing: the collection is empty (or the source filter matched no documents). Index a document first."))
        return notes
    if not result.hits:
        notes.append(("warning", f"All {result.dropped_by_threshold} candidate chunk(s) were below the similarity threshold "
                                 f"({result.threshold}). Lower the threshold or rephrase the question."))
        return notes
    best = result.hits[0].similarity
    if best is not None and best < weak_similarity:
        notes.append(("warning", f"The best match has a low similarity ({best:.2f}). The retrieved chunks are probably NOT relevant; "
                                 "the documents may not contain an answer, or the question should be rephrased with terms used in the documents."))
    else:
        notes.append(("ok", "The top results look reasonably close in meaning. Always read the chunks to confirm they really contain the answer; "
                            "a high score means *similar*, not *correct*."))
    if len(result.hits) < result.k_requested and result.dropped_by_threshold:
        notes.append(("ok", f"{result.dropped_by_threshold} chunk(s) were filtered out by the similarity threshold."))
    if len({h.metadata.get("source_file") for h in result.hits}) == 1 and len(result.hits) > 1:
        notes.append(("ok", "All results come from one file. For comparison questions, increase Top K."))
    return notes
