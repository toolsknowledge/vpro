"""Unified retrieval across documents, audio transcripts, video transcripts and frame descriptions.

1. The question is embedded **once** (same model as every collection).
2. Each selected collection is queried with that vector.
3. Because all collections use the same model and the cosine metric, their
   distances are directly comparable, so the hits are merged and the best
   `top_k` overall are kept.
4. Time references in the question ("at 00:12:30", "between 10 and 20
   minutes") become ChromaDB metadata filters on the media timestamps, so
   "what code is visible at 00:12:30?" really looks at that moment.

Citations are built only from metadata stored at indexing time, so a cited
file name or timestamp always exists in the index.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from backend.embeddings import EmbeddingService
from backend.media_utils import format_time_range, format_timestamp, parse_timestamp
from backend.retrieval import RetrievalResult, RetrievedChunk, diagnose, format_citation, keyword_overlap
from backend.transcript_chunker import MEDIA_AUDIO, MEDIA_VIDEO_FRAME, MEDIA_VIDEO_TRANSCRIPT
from backend.vector_store import VectorStore, distance_to_similarity

MEDIA_DOCUMENT = "document"

SCOPES = {
    "all": ("All indexed sources", (MEDIA_DOCUMENT, MEDIA_AUDIO, MEDIA_VIDEO_TRANSCRIPT, MEDIA_VIDEO_FRAME)),
    "documents": ("Documents only", (MEDIA_DOCUMENT,)),
    "audio": ("Audio only", (MEDIA_AUDIO,)),
    "video": ("Video only (transcripts + frames)", (MEDIA_VIDEO_TRANSCRIPT, MEDIA_VIDEO_FRAME)),
    "media": ("All audio and video", (MEDIA_AUDIO, MEDIA_VIDEO_TRANSCRIPT, MEDIA_VIDEO_FRAME)),
}

SOURCE_LABELS = {
    MEDIA_DOCUMENT: "Document",
    MEDIA_AUDIO: "Audio transcript",
    MEDIA_VIDEO_TRANSCRIPT: "Video transcript",
    MEDIA_VIDEO_FRAME: "Video frame",
}


def format_media_citation(metadata: dict[str, Any]) -> str:
    """'Source: Python_Lecture.mp4 | Transcript: 00:12:15–00:13:05' style citations."""
    media_type = metadata.get("media_type")
    source = metadata.get("source_file", "unknown source")
    if media_type == MEDIA_AUDIO:
        text = f"Source: {source} | {format_time_range(metadata.get('start_time_seconds'), metadata.get('end_time_seconds'))}"
    elif media_type == MEDIA_VIDEO_TRANSCRIPT:
        text = f"Source: {source} | Transcript: {format_time_range(metadata.get('start_time_seconds'), metadata.get('end_time_seconds'))}"
    elif media_type == MEDIA_VIDEO_FRAME:
        text = f"Source: {source} | Frame timestamp: {format_timestamp(metadata.get('timestamp_seconds'))}"
        span_end = metadata.get("span_end_seconds")
        if span_end is not None and span_end - float(metadata.get("timestamp_seconds") or 0) >= 1:
            text += f" (same screen until {format_timestamp(span_end)})"
        return text
    else:
        return "Source: " + format_citation(metadata).replace(", page ", " | Page ", 1)
    if metadata.get("timing_source") == "audio_split":
        text += " (approx.)"  # timed by the audio piece, not by the model
    return text


# ------------------------------------------------------------ time windows
@dataclass
class TimeWindow:
    start: float
    end: float
    label: str

    @property
    def is_point(self) -> bool:
        return self.end - self.start < 1


_TS = r"\d{1,2}:\d{2}(?::\d{2})?"
_RANGE_TS = re.compile(rf"(?:between|from)?\s*({_TS})\s*(?:and|to|-|–)\s*({_TS})", re.I)
_RANGE_MIN = re.compile(r"(?:between|from)\s+(\d+(?:\.\d+)?)\s*(?:min(?:ute)?s?)?\s*(?:and|to|-|–)\s*(\d+(?:\.\d+)?)\s*(min(?:ute)?s?|seconds?|secs?)", re.I)
_POINT_TS = re.compile(rf"(?:at|around|near)?\s*({_TS})\b", re.I)
_POINT_MIN = re.compile(r"\b(?:at|around|near)\s+(?:minute\s+(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*(?:min(?:ute)?s?|m)\b)", re.I)


def parse_time_window(question: str) -> TimeWindow | None:
    """Find an explicit time reference in the question. Returns None when there is none."""
    q = question or ""
    if m := _RANGE_TS.search(q):
        a, b = parse_timestamp(m.group(1)), parse_timestamp(m.group(2))
        if a is not None and b is not None and b > a:
            return TimeWindow(a, b, f"{format_timestamp(a)}–{format_timestamp(b)}")
    if m := _RANGE_MIN.search(q):
        factor = 1 if m.group(3).lower().startswith("s") else 60
        a, b = float(m.group(1)) * factor, float(m.group(2)) * factor
        if b > a:
            return TimeWindow(a, b, f"{format_timestamp(a)}–{format_timestamp(b)}")
    if m := _POINT_TS.search(q):
        t = parse_timestamp(m.group(1))
        if t is not None:
            return TimeWindow(t, t, format_timestamp(t))
    if m := _POINT_MIN.search(q):
        t = float(m.group(1) or m.group(2)) * 60
        return TimeWindow(t, t, format_timestamp(t))
    return None


def time_filter(media_type: str, window: TimeWindow, frame_tolerance: float) -> dict | None:
    """ChromaDB `where` clause selecting records that overlap the window."""
    if media_type in (MEDIA_AUDIO, MEDIA_VIDEO_TRANSCRIPT):
        return {"$and": [{"start_time_seconds": {"$lte": window.end}}, {"end_time_seconds": {"$gte": window.start}}]}
    if media_type == MEDIA_VIDEO_FRAME:
        # A kept frame stands for every near-identical frame after it, up to span_end_seconds.
        tol = frame_tolerance / 2 if window.is_point else 0
        return {"$and": [{"span_start_seconds": {"$lte": window.end + tol}}, {"span_end_seconds": {"$gte": window.start - tol}}]}
    return None  # documents have no timeline


def _combine(*clauses: dict | None) -> dict | None:
    clauses = [c for c in clauses if c]
    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    flat = []
    for clause in clauses:
        flat.extend(clause["$and"] if "$and" in clause else [clause])
    return {"$and": flat}


@dataclass
class UnifiedRetrievalResult(RetrievalResult):
    scope: str = "all"
    time_window: TimeWindow | None = None
    searched: dict[str, int] | None = None  # media_type -> records in that collection


class UnifiedRetriever:
    def __init__(self, embedder: EmbeddingService, stores: dict[str, VectorStore], frame_tolerance: float = 10.0):
        self.embedder = embedder
        self.stores = stores  # media_type -> VectorStore (document, audio, video_transcript, video_frame)
        self.frame_tolerance = frame_tolerance

    def retrieve(
        self,
        question: str,
        *,
        scope: str = "all",
        top_k: int = 5,
        min_similarity: float | None = None,
        source_files: list[str] | None = None,
        use_time_filter: bool = True,
        rerank: bool = False,
    ) -> UnifiedRetrievalResult:
        question = (question or "").strip()
        if not question:
            raise ValueError("Please type a question first.")
        if scope not in SCOPES:
            raise ValueError(f"Unknown search scope '{scope}'.")
        if min_similarity is not None and not -1.0 <= min_similarity <= 1.0:
            raise ValueError("The similarity threshold must be between -1 and 1.")

        media_types = [m for m in SCOPES[scope][1] if m in self.stores]
        searched = {m: self.stores[m].count() for m in media_types}
        result = UnifiedRetrievalResult(
            question=question, top_k=top_k, metric="cosine", query_dimension=0,
            embedding_model=self.embedder.model, min_similarity=min_similarity,
            scope=scope, searched=searched,
        )
        if not any(searched.values()):
            result.diagnostics = [f"Nothing is indexed for '{SCOPES[scope][0]}' yet. Upload and index content first."]
            return result

        for media_type in media_types:
            if searched[media_type]:
                self.stores[media_type].check_compatible(self.embedder.model)
        query_vector = self.embedder.embed_query(question)
        result.query_dimension = len(query_vector)
        window = parse_time_window(question) if use_time_filter else None
        result.time_window = window
        file_clause = {"source_file": {"$in": source_files}} if source_files else None

        hits: list[tuple[str, Any]] = []
        for media_type in media_types:
            store = self.stores[media_type]
            if not searched[media_type]:
                continue
            if window and media_type == MEDIA_DOCUMENT:
                continue  # a time question is about recordings; documents have no timestamps
            where = _combine(file_clause, time_filter(media_type, window, self.frame_tolerance) if window else None)
            hits.extend((media_type, h) for h in store.query(query_vector, top_k, where=where))
        if window and not hits:
            result.diagnostics.append(
                f"No indexed media covers {window.label}. Showing the best matches from the whole recordings instead."
            )
            for media_type in media_types:
                if searched[media_type]:
                    hits.extend((media_type, h) for h in self.stores[media_type].query(query_vector, top_k, where=file_clause))

        scored = []
        for media_type, hit in hits:
            similarity = distance_to_similarity(hit.distance, self.stores[media_type].distance_metric)
            overlap = keyword_overlap(question, hit.text)
            score = (similarity or -hit.distance) + (0.1 * overlap if rerank else 0.0)
            scored.append((score, media_type, hit, similarity, overlap))
        scored.sort(key=lambda item: item[0], reverse=True)

        for rank, (_, media_type, hit, similarity, overlap) in enumerate(scored[:top_k], start=1):
            metadata = {**hit.metadata, "collection": self.stores[media_type].collection_name}
            metadata.setdefault("media_type", media_type)
            chunk = RetrievedChunk(
                rank=rank, chunk_id=hit.chunk_id, text=hit.text, metadata=metadata,
                distance=hit.distance, similarity=similarity,
                citation=format_media_citation(metadata), keyword_overlap=overlap,
            )
            if min_similarity is not None and similarity is not None and similarity < min_similarity:
                result.filtered_out.append(chunk)
            else:
                result.chunks.append(chunk)

        if window:
            # For "summarise 10–20 min" questions a chronological context reads far better.
            result.chunks.sort(key=lambda c: (c.metadata.get("source_file", ""), chunk_start(c)))
        result.diagnostics = diagnose(result, sum(searched.values())) + result.diagnostics
        return result


def chunk_start(chunk: RetrievedChunk) -> float:
    meta = chunk.metadata
    return float(meta.get("start_time_seconds", meta.get("timestamp_seconds", 0.0)) or 0.0)
