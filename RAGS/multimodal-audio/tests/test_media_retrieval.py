"""End-to-end media pipeline with real FFmpeg + real ChromaDB + fake OpenAI, then unified retrieval."""

import httpx
import openai
import pytest

from backend.media_pipeline import MediaOptions
from backend.media_retrieval import (
    MEDIA_DOCUMENT,
    UnifiedRetriever,
    format_media_citation,
    parse_time_window,
    time_filter,
)
from backend.media_vector_store import MediaStores
from backend.unified_rag import NOT_FOUND_MESSAGE, UnifiedRagChain
from backend.vector_store import IncompatibleEmbeddingError, VectorStore
from tests.conftest import FakeMediaChat, FakeMediaClient, FakeTranscriptions, make_tone, make_video, needs_ffmpeg

pytestmark = needs_ffmpeg


def _error(cls, status, code=""):
    response = httpx.Response(status, request=httpx.Request("POST", "https://api.openai.com/v1/x"))
    return cls("error", response=response, body={"error": {"code": code}})


@pytest.fixture
def media_files(tmp_path_factory):
    folder = tmp_path_factory.mktemp("media")
    return {
        "audio": make_tone(folder / "Python_Lecture.mp3", seconds=65),
        "video": make_video(folder / "Python_Lecture.mp4", colors=("red", "red", "blue", "green"), seg_seconds=10),
        "silent": make_video(folder / "Silent_Demo.mp4", colors=("red", "blue"), seg_seconds=10, audio=False),
    }


def _process(m, path, options=None, force=False, name=None):
    with open(path, "rb") as handle:
        return m.pipeline.process(name or path.name, handle, options or MediaOptions(chunk_size=100, chunk_overlap=20,
                                                                                    frame_interval_seconds=10), force=force)


def _retriever(m, docs=None):
    return UnifiedRetriever(m.embedder, {**({MEDIA_DOCUMENT: docs} if docs else {}), **dict(m.stores.items())},
                            frame_tolerance=10)


# ---------------------------------------------------------------- indexing
def test_audio_is_transcribed_chunked_embedded_and_stored(media_factory, media_files):
    m = media_factory()
    report = _process(m, media_files["audio"])
    assert report.status == "indexed", report.errors
    assert report.media_kind == "audio" and report.audio_pieces == 4  # 65 s / 20 s fallback pieces
    assert report.stage("frames").status == "skipped"
    counts = m.stores.counts()
    assert counts["audio"] == report.transcript_chunks > 0 and counts["video_frame"] == 0
    record = m.stores["audio"].get_records()[0]
    assert record.metadata["source_file"] == "Python_Lecture.mp3"
    assert record.metadata["timing_source"] == "audio_split"
    assert record.metadata["start_time_seconds"] == 0.0
    row = m.registry.get(report.document_id)
    assert row["status"] == "indexed" and row["embedding_dimension"] == 64
    trace = m.registry.load_trace(report.document_id)
    assert trace["raw_segments"] and trace["clean_segments"] and trace["chunks"]
    assert not m.registry.audio_dir(report.document_id).exists(), "temporary audio is cleaned up after success"


def test_video_indexes_transcript_and_frames_with_timestamps(media_factory, media_files):
    m = media_factory()
    report = _process(m, media_files["video"])
    assert report.status == "indexed", report.errors
    assert report.frames_extracted == 4 and report.frames_skipped_duplicate == 1 and report.frame_chunks == 3
    assert m.client.chat.vision_calls == 3
    frames = sorted(m.stores["video_frame"].get_records(), key=lambda r: r.metadata["timestamp_seconds"])
    assert [r.metadata["timestamp_seconds"] for r in frames] == [0.5, 20.0, 30.0]
    assert frames[0].metadata["span_end_seconds"] == 10.0
    assert frames[0].text.startswith("Video: Python_Lecture.mp4 | Timestamp: 00:00:00")
    transcript = m.stores["video_transcript"].get_records()[0]
    assert transcript.metadata["media_type"] == "video_transcript"
    assert m.stores["audio"].count() == 0, "video transcripts never land in the audio collection"


def test_silent_video_is_indexed_from_frames_only(media_factory, media_files):
    m = media_factory()
    report = _process(m, media_files["silent"])
    assert report.status == "indexed"
    assert report.stage("transcribe").status == "skipped" and report.frame_chunks == 2
    assert m.client.audio.transcriptions.calls == []


def test_duplicate_media_is_detected_and_reindex_reuses_cache(media_factory, media_files):
    m = media_factory()
    first = _process(m, media_files["video"])
    calls_after_first = (len(m.client.audio.transcriptions.calls), m.client.chat.vision_calls)
    again = _process(m, media_files["video"], name="renamed.mp4")
    assert again.status == "duplicate" and "Python_Lecture.mp4" in again.message
    ids_before = sorted(r.chunk_id for r in m.stores["video_frame"].get_records())

    forced = _process(m, media_files["video"], force=True)
    assert forced.status == "indexed"
    assert (len(m.client.audio.transcriptions.calls), m.client.chat.vision_calls) == calls_after_first, \
        "unchanged media must not be transcribed or analysed again"
    assert forced.stage("transcribe").status == "reused" and forced.stage("vision").status == "reused"
    assert sorted(r.chunk_id for r in m.stores["video_frame"].get_records()) == ids_before, "stable IDs"
    assert m.stores.count_for_document(first.document_id) == {
        "audio": 0, "video_transcript": first.transcript_chunks, "video_frame": first.frame_chunks}


def test_failed_transcription_keeps_frames_and_retry_repeats_only_failed_pieces(media_factory, media_files):
    fake = FakeTranscriptions(fail_pieces={1}, error=_error(openai.BadRequestError, 400))
    m = media_factory(client=FakeMediaClient(transcriptions=fake))
    report = _process(m, media_files["video"])
    assert report.status == "partial"
    assert report.stage("transcribe").status == "partial" and report.frame_chunks == 3
    assert m.registry.get(report.document_id)["status"] == "partial"
    sent_first = [c["piece"] for c in fake.calls]

    fake.fail_pieces.clear()
    retried = m.pipeline.retry(report.document_id)
    assert retried.status == "indexed"
    assert [c["piece"] for c in fake.calls[len(sent_first):]] == [1], "only the failed piece is sent again"


def test_total_transcription_failure_still_indexes_video_frames(media_factory, media_files):
    fake = FakeTranscriptions(fail_pieces={0, 1, 2}, error=_error(openai.RateLimitError, 429, "insufficient_quota"))
    m = media_factory(client=FakeMediaClient(transcriptions=fake))
    report = _process(m, media_files["video"])
    assert report.status == "partial" and report.stage("transcribe").status == "failed"
    assert "credits" in report.message
    assert m.stores["video_frame"].count() == 3 and m.stores["video_transcript"].count() == 0


def test_failed_frame_analysis_keeps_transcript(media_factory, media_files):
    chat = FakeMediaChat(vision_error=_error(openai.AuthenticationError, 401), vision_fail_times=-1)
    m = media_factory(client=FakeMediaClient(chat=chat))
    report = _process(m, media_files["video"])
    assert report.status == "partial" and report.stage("vision").status == "failed"
    assert m.stores["video_transcript"].count() == report.transcript_chunks > 0


def test_unsupported_and_corrupted_uploads_fail_cleanly(media_factory, tmp_path):
    m = media_factory()
    bad = tmp_path / "notes.exe"
    bad.write_bytes(b"MZ")
    assert _process(m, bad).stage("upload").status == "failed"
    corrupt = tmp_path / "broken.mp3"
    corrupt.write_bytes(b"not audio" * 100)
    report = _process(m, corrupt)
    assert report.status == "failed" and report.stage("probe").status == "failed"
    assert not list(m.registry.uploads_directory.glob("*.mp3")), "a corrupted upload is not kept"
    assert m.registry.get(report.document_id)["status"] == "failed"


def test_missing_api_credentials_block_processing(media_factory, media_files):
    m = media_factory()
    m.pipeline.embedder = None
    report = _process(m, media_files["audio"])
    assert report.status == "failed" and "OPENAI_API_KEY" in report.message


def test_delete_removes_records_and_files(media_factory, media_files):
    m = media_factory()
    report = _process(m, media_files["video"])
    frames_dir = m.registry.frames_dir(report.document_id)
    assert frames_dir.exists() and m.registry.load_trace(report.document_id)
    removed = m.pipeline.delete_media(report.document_id)
    assert removed == report.stored_records
    assert m.stores.total() == 0 and m.registry.get(report.document_id) is None
    assert not frames_dir.exists() and m.registry.load_trace(report.document_id) is None
    assert not list(m.registry.uploads_directory.glob("media_*"))


def test_new_version_with_same_name_replaces_old_one(media_factory, media_files, tmp_path):
    m = media_factory()
    old = _process(m, media_files["audio"])
    changed = make_tone(tmp_path / "Python_Lecture.mp3", seconds=30)
    new = _process(m, changed)
    assert new.document_id != old.document_id
    assert m.registry.get(old.document_id) is None and m.stores.count_for_document(old.document_id)["audio"] == 0
    assert any("older version" in w for w in new.warnings)


def test_index_survives_restart(media_factory, media_files):
    m = media_factory()
    report = _process(m, media_files["video"])
    reopened = MediaStores(m.data / "chroma_db", "t_audio", "t_video_transcripts", "t_video_frames")
    assert reopened.count_for_document(report.document_id)["video_frame"] == 3
    assert media_factory(data_dir=m.data).registry.get(report.document_id)["status"] == "indexed"


def test_embedding_model_mismatch_is_refused(media_factory, media_files):
    m = media_factory()
    _process(m, media_files["audio"])
    other = media_factory(embedding_model="another-model", data_dir=m.data)
    report = _process(other, media_files["video"])
    assert report.status == "failed" and "cannot be mixed" in report.message


# --------------------------------------------------------------- retrieval
def test_retrieval_across_media_types_and_scopes(media_factory, media_files, tmp_path):
    m = media_factory()
    _process(m, media_files["audio"])
    _process(m, media_files["video"])
    docs = VectorStore(m.data / "chroma_db", "t_docs")
    text = "ChromaDB architecture notes: vectors are stored on disk."
    docs.add_chunks(["doc_1_c0"], [text], [{"document_id": "doc_1", "source_file": "notes.pdf", "page_number": 1}],
                    [m.embedder.embed_query(text)], m.embedder.model)
    retriever = _retriever(m, docs)

    everything = retriever.retrieve("Where is ChromaDB PersistentClient code shown?", scope="all", top_k=10)
    kinds = {c.metadata["media_type"] for c in everything.chunks}
    assert {"video_frame", "audio", "video_transcript"} <= kinds and "document" in kinds
    assert everything.query_dimension == 64

    audio_only = retriever.retrieve("list comprehensions", scope="audio", top_k=10)
    assert {c.metadata["media_type"] for c in audio_only.chunks} == {"audio"}
    video_only = retriever.retrieve("list comprehensions", scope="video", top_k=10)
    assert {c.metadata["media_type"] for c in video_only.chunks} <= {"video_transcript", "video_frame"}
    docs_only = retriever.retrieve("ChromaDB", scope="documents", top_k=3)
    assert [c.citation for c in docs_only.chunks] == ["Source: notes.pdf | Page 1"]

    only_mp3 = retriever.retrieve("embeddings", scope="all", top_k=10, source_files=["Python_Lecture.mp3"])
    assert {c.metadata["source_file"] for c in only_mp3.chunks} == {"Python_Lecture.mp3"}


def test_time_questions_filter_by_timestamp(media_factory, media_files):
    m = media_factory()
    _process(m, media_files["video"])
    retriever = _retriever(m)
    at = retriever.retrieve("What is on the screen at 00:00:12?", scope="video", top_k=10)
    assert at.time_window.start == 12
    frames = [c for c in at.chunks if c.metadata["media_type"] == "video_frame"]
    # 12 s is covered by the first frame (red screen, 0.5 s, same screen until 10 s, ±5 s tolerance).
    assert [c.metadata["timestamp_seconds"] for c in frames] == [0.5]
    transcripts = [c for c in at.chunks if c.metadata["media_type"] == "video_transcript"]
    assert all(c.metadata["start_time_seconds"] <= 12 <= c.metadata["end_time_seconds"] for c in transcripts)

    window = retriever.retrieve("Summarize the lecture between 0 and 0.5 minutes", scope="video", top_k=10)
    assert (window.time_window.start, window.time_window.end) == (0, 30)
    starts = [c.metadata.get("start_time_seconds", c.metadata.get("timestamp_seconds")) for c in window.chunks]
    assert all(s <= 30 for s in starts)

    nothing = retriever.retrieve("What happens at 02:00:00?", scope="video", top_k=3)
    assert nothing.chunks and any("No indexed media covers" in d for d in nothing.diagnostics)


def test_parse_time_window_variants():
    assert parse_time_window("Summarize the lecture between 10 and 20 minutes").start == 600
    assert parse_time_window("Summarize the lecture between 10 and 20 minutes").end == 1200
    assert parse_time_window("What code is visible at 00:12:30?").start == 750
    assert parse_time_window("from 01:00 to 02:30").end == 150
    assert parse_time_window("at minute 5").start == 300
    assert parse_time_window("What did the instructor say about embeddings?") is None
    assert time_filter("document", parse_time_window("at 00:01:00"), 10) is None


def test_citations_use_only_stored_metadata():
    assert format_media_citation({"media_type": "audio", "source_file": "Python_Lecture.mp3",
                                  "start_time_seconds": 735, "end_time_seconds": 785, "timing_source": "model"}) == \
        "Source: Python_Lecture.mp3 | 00:12:15–00:13:05"
    assert format_media_citation({"media_type": "video_transcript", "source_file": "Python_Lecture.mp4",
                                  "start_time_seconds": 735, "end_time_seconds": 785, "timing_source": "model"}) == \
        "Source: Python_Lecture.mp4 | Transcript: 00:12:15–00:13:05"
    assert format_media_citation({"media_type": "video_frame", "source_file": "Python_Lecture.mp4",
                                  "timestamp_seconds": 740, "span_end_seconds": 740}) == \
        "Source: Python_Lecture.mp4 | Frame timestamp: 00:12:20"
    assert format_media_citation({"source_file": "sample_rag_architecture_notes.pdf", "page_number": 1}) == \
        "Source: sample_rag_architecture_notes.pdf | Page 1"
    assert format_media_citation({"media_type": "audio", "source_file": "a.mp3", "start_time_seconds": 0,
                                  "end_time_seconds": 30, "timing_source": "audio_split"}).endswith("(approx.)")


def test_unified_rag_answers_with_timestamped_citations(media_factory, media_files):
    chat = FakeMediaChat(reply="List comprehensions were explained around 00:00:00 [S1]. Bogus [S99].")
    m = media_factory(client=FakeMediaClient(chat=chat))
    _process(m, media_files["video"])
    rag = UnifiedRagChain(m.client, "fake-chat", _retriever(m), temperature=None)
    answer = rag.ask("When were list comprehensions explained?", scope="video", top_k=3)
    assert "[S99]" not in answer.answer and answer.citations
    assert answer.citations[0].chunk.citation.startswith("Source: Python_Lecture.mp4 |")
    system, user = chat.rag_calls[-1]["messages"]
    assert "Frame timestamp" in system["content"] and "<context>" in user["content"]
    assert "Python_Lecture.mp4" in user["content"]


def test_nothing_indexed_returns_not_found_without_calling_llm(media_factory):
    m = media_factory()
    rag = UnifiedRagChain(m.client, "fake-chat", _retriever(m), temperature=None)
    answer = rag.ask("What is RAG?", scope="media")
    assert answer.answer == NOT_FOUND_MESSAGE and not answer.grounded
    assert m.client.chat.rag_calls == []
