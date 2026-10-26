"""Transcript chunking: group timed segments into ~800-token chunks with ~120 tokens overlap.

Unlike document chunking (which cuts between words), transcript chunks are
built from whole transcript segments, so every chunk has an honest time range:
its start is the first segment's start, its end the last segment's end.

* A chunk never mixes two recordings (one call = one media file).
* Overlap is made of whole trailing segments from the previous chunk.
* A single segment that is longer than the chunk size (common with text-only
  models, where one segment = one 30 s audio piece) is split at sentence
  boundaries. The parts keep the segment's time range, because the model did
  not tell us when inside the segment each sentence was spoken.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from typing import Any

from backend.chunker import TokenCounter, get_token_counter
from backend.media_utils import format_time_range
from backend.transcription_service import TranscriptSegment
from config.settings import validate_chunk_settings

MEDIA_AUDIO = "audio"
MEDIA_VIDEO_TRANSCRIPT = "video_transcript"
MEDIA_VIDEO_FRAME = "video_frame"

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


@dataclass
class TranscriptChunk:
    chunk_id: str
    document_id: str
    media_type: str
    source_file: str
    chunk_index: int
    text: str
    start_time_seconds: float
    end_time_seconds: float
    transcript_segment_ids: list[str]
    transcription_model: str
    timing_source: str
    token_count: int
    file_hash: str
    language: str | None = None
    speakers: list[str] = field(default_factory=list)
    # The same words with a [start–end] marker per transcript segment. These markers come from the
    # recorded segment times, so the answer model can cite a narrower range than the whole chunk.
    timed_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def embedding_text(self) -> str:
        """Text stored in ChromaDB and embedded: a one-line header plus the spoken words.

        The header lets questions like "which session discusses RAG evaluation?"
        match the recording's file name as well as its content.
        """
        kind = "Audio" if self.media_type == MEDIA_AUDIO else "Video transcript"
        speakers = f" | Speakers: {', '.join(self.speakers)}" if self.speakers else ""
        return (
            f"{kind}: {self.source_file} | {format_time_range(self.start_time_seconds, self.end_time_seconds)}"
            f"{speakers}\n{self.timed_text or self.text}"
        )

    def to_metadata(self, embedding_model: str | None = None) -> dict[str, Any]:
        """ChromaDB metadata: scalar values only, no None."""
        meta = {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "media_type": self.media_type,
            "source_file": self.source_file,
            "file_hash": self.file_hash,
            "chunk_index": self.chunk_index,
            "start_time_seconds": float(self.start_time_seconds),
            "end_time_seconds": float(self.end_time_seconds),
            "transcript_segment_ids": ",".join(self.transcript_segment_ids),
            "transcription_model": self.transcription_model,
            "timing_source": self.timing_source,
            "token_count": self.token_count,
            "document_type": self.media_type,
        }
        if self.language:
            meta["language"] = self.language
        if self.speakers:
            meta["speakers"] = ",".join(self.speakers)
        if embedding_model:
            meta["embedding_model"] = embedding_model
        return meta


def make_media_chunk_id(document_id: str, kind: str, index: int, text: str) -> str:
    """Stable ID: same media + same position + same text => same ID on every re-index."""
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]
    return f"{document_id}_{kind}{index:04d}_{digest}"


def _split_long_segment(segment: TranscriptSegment, chunk_size: int, counter: TokenCounter) -> list[TranscriptSegment]:
    if counter.count(segment.text) <= chunk_size:
        return [segment]
    sentences = [s for s in _SENTENCE_END.split(segment.text) if s.strip()]
    parts: list[str] = []
    current = ""
    for sentence in sentences:
        candidate = f"{current} {sentence}".strip()
        if current and counter.count(candidate) > chunk_size:
            parts.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        parts.append(current)
    # A single sentence longer than chunk_size: hard-split by words as a last resort.
    final: list[str] = []
    for part in parts:
        if counter.count(part) <= chunk_size:
            final.append(part)
            continue
        words, buf = part.split(" "), []
        for word in words:
            if buf and counter.count(" ".join(buf + [word])) > chunk_size:
                final.append(" ".join(buf))
                buf = []
            buf.append(word)
        if buf:
            final.append(" ".join(buf))
    return [
        TranscriptSegment(
            segment_id=f"{segment.segment_id}.{i}",
            piece_index=segment.piece_index,
            start_seconds=segment.start_seconds,
            end_seconds=segment.end_seconds,
            text=text,
            timing_source=segment.timing_source,
            speaker=segment.speaker,
            language=segment.language,
        )
        for i, text in enumerate(final)
    ]


def chunk_transcript(
    segments: list[TranscriptSegment],
    *,
    document_id: str,
    source_file: str,
    file_hash: str,
    media_type: str,
    transcription_model: str,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    counter: TokenCounter | None = None,
) -> list[TranscriptChunk]:
    validate_chunk_settings(chunk_size, chunk_overlap)
    if media_type not in (MEDIA_AUDIO, MEDIA_VIDEO_TRANSCRIPT):
        raise ValueError(f"Unknown transcript media type: {media_type}")
    counter = counter or get_token_counter()

    units: list[TranscriptSegment] = []
    for segment in sorted(segments, key=lambda s: (s.start_seconds, s.segment_id)):
        if segment.text.strip():
            units.extend(_split_long_segment(segment, chunk_size, counter))
    if not units:
        return []
    sizes = [counter.count(u.text) for u in units]

    chunks: list[TranscriptChunk] = []
    start = 0
    while start < len(units):
        end, total = start, 0
        while end < len(units) and (total + sizes[end] <= chunk_size or end == start):
            total += sizes[end]
            end += 1
        window = units[start:end]
        text = " ".join(u.text for u in window)
        timing = {u.timing_source for u in window}
        speakers = sorted({u.speaker for u in window if u.speaker})
        timed_text = "\n".join(
            f"[{format_time_range(u.start_seconds, u.end_seconds)}]{f' {u.speaker}:' if u.speaker else ''} {u.text}"
            for u in window
        )
        languages = [u.language for u in window if u.language]
        index = len(chunks)
        kind = "a" if media_type == MEDIA_AUDIO else "t"
        chunks.append(
            TranscriptChunk(
                chunk_id=make_media_chunk_id(document_id, kind, index, text),
                document_id=document_id,
                media_type=media_type,
                source_file=source_file,
                chunk_index=index,
                text=text,
                start_time_seconds=min(u.start_seconds for u in window),
                end_time_seconds=max(u.end_seconds for u in window),
                transcript_segment_ids=[u.segment_id for u in window],
                transcription_model=transcription_model,
                timing_source=timing.pop() if len(timing) == 1 else "mixed",
                token_count=counter.count(text),
                file_hash=file_hash,
                language=languages[0] if languages else None,
                speakers=speakers,
                timed_text=timed_text,
            )
        )
        if end >= len(units):
            break
        next_start, overlap = end, 0
        while next_start > start + 1 and overlap + sizes[next_start - 1] <= chunk_overlap:
            next_start -= 1
            overlap += sizes[next_start]
        start = next_start
    return chunks
