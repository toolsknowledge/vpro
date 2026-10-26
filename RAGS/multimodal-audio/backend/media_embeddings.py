"""Turn transcript chunks and frame descriptions into ChromaDB-ready records with vectors.

Both kinds of record are *text*: transcript chunks are the spoken words, and
visual records are the vision model's description of a frame. They are
embedded with the same OpenAI text-embedding model as the documents, so the
vector of a frame record represents its description, not the image pixels.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable

from backend.embeddings import EmbeddingService
from backend.frame_analyzer import FrameAnalysis, frame_embedding_text
from backend.frame_extractor import FrameRecord
from backend.transcript_chunker import MEDIA_VIDEO_FRAME, TranscriptChunk


@dataclass
class FrameChunk:
    chunk_id: str
    document_id: str
    source_file: str
    file_hash: str
    timestamp_seconds: float
    frame_path: str
    frame_description: str
    frame_index: int
    extraction_method: str
    vision_model: str
    media_type: str = MEDIA_VIDEO_FRAME
    # Near-duplicate frames are not described again; instead this frame's span grows to cover them,
    # i.e. "the same screen was visible from span_start to span_end".
    span_start_seconds: float | None = None
    span_end_seconds: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def embedding_text(self) -> str:
        frame = FrameRecord(self.chunk_id, self.document_id, self.source_file, self.timestamp_seconds,
                            self.frame_path, self.frame_index, self.extraction_method)
        return frame_embedding_text(frame, self.frame_description)

    def to_metadata(self, embedding_model: str | None = None) -> dict[str, Any]:
        meta = {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "media_type": self.media_type,
            "document_type": self.media_type,
            "source_file": self.source_file,
            "file_hash": self.file_hash,
            "timestamp_seconds": float(self.timestamp_seconds),
            "frame_path": self.frame_path,
            "frame_index": self.frame_index,
            "chunk_index": self.frame_index,
            "extraction_method": self.extraction_method,
            "vision_model": self.vision_model,
            "span_start_seconds": float(self.timestamp_seconds if self.span_start_seconds is None else self.span_start_seconds),
            "span_end_seconds": float(self.timestamp_seconds if self.span_end_seconds is None else self.span_end_seconds),
        }
        if embedding_model:
            meta["embedding_model"] = embedding_model
        return meta


def build_frame_chunks(frames: list[FrameRecord], analyses: list[FrameAnalysis], file_hash: str) -> list[FrameChunk]:
    """One searchable record per successfully described, non-duplicate frame."""
    by_id = {a.frame_id: a for a in analyses}
    span_end: dict[str, float] = {}
    for frame in frames:
        if frame.duplicate_of:
            span_end[frame.duplicate_of] = max(span_end.get(frame.duplicate_of, 0.0), frame.timestamp_seconds)
    chunks = []
    for frame in frames:
        analysis = by_id.get(frame.frame_id)
        if not analysis or analysis.status != "done" or not analysis.description:
            continue
        chunks.append(
            FrameChunk(
                chunk_id=frame.frame_id,  # stable: document id + frame index
                document_id=frame.document_id,
                source_file=frame.source_file,
                file_hash=file_hash,
                timestamp_seconds=frame.timestamp_seconds,
                frame_path=frame.frame_path,
                frame_description=analysis.description,
                frame_index=frame.frame_index,
                extraction_method=frame.extraction_method,
                vision_model=analysis.model,
                span_start_seconds=frame.timestamp_seconds,
                span_end_seconds=max(frame.timestamp_seconds, span_end.get(frame.frame_id, frame.timestamp_seconds)),
            )
        )
    return chunks


@dataclass
class EmbeddedRecords:
    ids: list[str]
    texts: list[str]
    metadatas: list[dict[str, Any]]
    embeddings: list[list[float]]
    dimension: int
    model: str


def embed_records(
    embedder: EmbeddingService,
    records: list[TranscriptChunk] | list[FrameChunk],
    progress: Callable[[int, int], None] | None = None,
) -> EmbeddedRecords:
    texts = [r.embedding_text() for r in records]
    result = embedder.embed_texts(texts, progress=progress)
    return EmbeddedRecords(
        ids=[r.chunk_id for r in records],
        texts=texts,
        metadatas=[r.to_metadata(embedder.model) for r in records],
        embeddings=result.vectors,
        dimension=result.dimension,
        model=result.model,
    )
