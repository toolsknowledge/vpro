"""Transcript chunking: timestamps, overlap, size limits, stable IDs, metadata."""

import pytest

from backend.chunker import TokenCounter
from backend.transcript_chunker import MEDIA_AUDIO, MEDIA_VIDEO_TRANSCRIPT, chunk_transcript
from backend.transcription_service import TIMING_AUDIO_SPLIT, TIMING_MODEL, TranscriptSegment

COUNTER = TokenCounter()


def _segments(n=60, seconds=5.0, words=6):
    return [
        TranscriptSegment(f"p0000s{i:04d}", 0, i * seconds, (i + 1) * seconds,
                          " ".join(f"word{i}_{w}" for w in range(words)) + ".", TIMING_MODEL, language="english")
        for i in range(n)
    ]


def _chunk(segments, size=200, overlap=40, media_type=MEDIA_AUDIO):
    return chunk_transcript(segments, document_id="media_abc", source_file="lecture.mp3", file_hash="f" * 64,
                            media_type=media_type, transcription_model="whisper-1",
                            chunk_size=size, chunk_overlap=overlap, counter=COUNTER)


def test_chunks_preserve_timestamps_of_their_segments():
    segments = _segments()
    by_id = {s.segment_id: s for s in segments}
    for chunk in _chunk(segments):
        covered = [by_id[i] for i in chunk.transcript_segment_ids]
        assert chunk.start_time_seconds == covered[0].start_seconds
        assert chunk.end_time_seconds == covered[-1].end_seconds
        assert chunk.timing_source == TIMING_MODEL and chunk.language == "english"
        assert "[00:00:" in chunk.timed_text or "[00:0" in chunk.timed_text


def test_chunks_respect_size_and_overlap_with_whole_segments():
    chunks = _chunk(_segments())
    assert len(chunks) > 3
    assert all(c.token_count <= 200 for c in chunks)
    for prev, cur in zip(chunks, chunks[1:]):
        shared = set(prev.transcript_segment_ids) & set(cur.transcript_segment_ids)
        assert shared, "neighbouring chunks should overlap by whole segments"
        assert cur.start_time_seconds < prev.end_time_seconds
    all_ids = {i for c in chunks for i in c.transcript_segment_ids}
    assert all_ids == {s.segment_id for s in _segments()}  # nothing lost


def test_chunk_ids_are_stable_and_unique():
    first, second = _chunk(_segments()), _chunk(_segments())
    assert [c.chunk_id for c in first] == [c.chunk_id for c in second]
    assert len({c.chunk_id for c in first}) == len(first)
    assert first[0].chunk_id.startswith("media_abc_a0000_")
    video = _chunk(_segments(), media_type=MEDIA_VIDEO_TRANSCRIPT)
    assert video[0].chunk_id.startswith("media_abc_t0000_")


def test_long_text_only_segment_is_split_but_keeps_its_time_range():
    long_text = " ".join(f"Sentence number {i} explains embeddings in detail." for i in range(80))
    segments = [TranscriptSegment("p0003s0000", 3, 90.0, 120.0, long_text, TIMING_AUDIO_SPLIT)]
    chunks = _chunk(segments, size=120, overlap=20)
    assert len(chunks) > 2
    assert all((c.start_time_seconds, c.end_time_seconds) == (90.0, 120.0) for c in chunks)
    assert all(c.timing_source == TIMING_AUDIO_SPLIT and c.token_count <= 120 for c in chunks)


def test_metadata_is_chroma_safe_and_complete():
    chunk = _chunk(_segments(n=3))[0]
    meta = chunk.to_metadata("text-embedding-3-small")
    required = {"chunk_id", "document_id", "media_type", "source_file", "chunk_index", "start_time_seconds",
                "end_time_seconds", "transcript_segment_ids", "transcription_model", "language"}
    assert required <= set(meta)
    assert all(v is not None and isinstance(v, (str, int, float, bool)) for v in meta.values())
    assert chunk.embedding_text().startswith("Audio: lecture.mp3 | 00:00:00–00:00:15")


def test_speakers_are_listed_only_when_the_model_provided_them():
    segs = [TranscriptSegment("a", 0, 0, 2, "Hello.", TIMING_MODEL, speaker="A"),
            TranscriptSegment("b", 0, 2, 4, "Hi.", TIMING_MODEL, speaker="B")]
    chunk = _chunk(segs)[0]
    assert chunk.speakers == ["A", "B"] and "A: Hello." in chunk.timed_text
    assert _chunk(_segments(n=2))[0].speakers == []


def test_invalid_settings_and_types_are_rejected():
    with pytest.raises(Exception):
        _chunk(_segments(), size=100, overlap=60)
    with pytest.raises(ValueError):
        _chunk(_segments(), media_type="video_frame")
    assert _chunk([]) == []
