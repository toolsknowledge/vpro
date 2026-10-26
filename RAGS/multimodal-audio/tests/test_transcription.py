"""Transcription capabilities, response parsing, failure handling, cleaning and export."""

from types import SimpleNamespace

import httpx
import openai
import pytest

from backend.audio_processor import AudioPiece
from backend.openai_client import OpenAIServiceError, create_client
from backend.transcript_cleaner import clean_segments, clean_text
from backend.transcript_export import ExportError, srt_supported, to_srt, to_txt
from backend.transcription_service import (
    TIMING_AUDIO_SPLIT,
    TIMING_MODEL,
    TranscriptionService,
    TranscriptSegment,
    capabilities_for,
    parse_transcription_response,
)
from tests.conftest import FakeMediaClient, FakeTranscriptions

PIECE = AudioPiece(index=2, start_seconds=60.0, end_seconds=90.0, path="piece_0002.mp3")


def _error(cls, status, code=""):
    response = httpx.Response(status, request=httpx.Request("POST", "https://api.openai.com/v1/audio/transcriptions"))
    return cls("error", response=response, body={"error": {"code": code}})


def test_capabilities_match_the_api():
    assert capabilities_for("whisper-1").request_kwargs() == {
        "response_format": "verbose_json", "timestamp_granularities": ["segment"]}
    diarize = capabilities_for("gpt-4o-transcribe-diarize")
    assert diarize.speakers and diarize.request_kwargs()["chunking_strategy"] == "auto" and not diarize.accepts_prompt
    mini = capabilities_for("gpt-4o-mini-transcribe")
    assert mini.response_format == "json" and not mini.segment_timestamps and not mini.speakers


def test_verbose_segments_are_shifted_by_the_piece_offset():
    response = SimpleNamespace(text="a b", language="english", segments=[
        SimpleNamespace(start=1.0, end=4.5, text=" first "), SimpleNamespace(start=4.5, end=40.0, text="second")])
    segments = parse_transcription_response(response, PIECE, capabilities_for("whisper-1"))
    assert [(s.start_seconds, s.end_seconds) for s in segments] == [(61.0, 64.5), (64.5, 90.0)]  # clamped to piece end
    assert all(s.timing_source == TIMING_MODEL and s.language == "english" for s in segments)
    assert segments[0].text == "first"


def test_text_only_models_get_piece_timing_not_invented_timestamps():
    segments = parse_transcription_response(SimpleNamespace(text="Hello class."), PIECE, capabilities_for("gpt-4o-mini-transcribe"))
    assert len(segments) == 1
    seg = segments[0]
    assert (seg.start_seconds, seg.end_seconds) == (60.0, 90.0)
    assert seg.timing_source == TIMING_AUDIO_SPLIT and seg.speaker is None and seg.language is None


def test_diarized_speakers_are_kept_and_never_fabricated():
    response = SimpleNamespace(text="x", segments=[SimpleNamespace(start=0, end=2, text="Hi", speaker="A")])
    diarized = parse_transcription_response(response, PIECE, capabilities_for("gpt-4o-transcribe-diarize"))
    assert diarized[0].speaker == "A"
    whisper = parse_transcription_response(response, PIECE, capabilities_for("whisper-1"))
    assert whisper[0].speaker is None  # whisper does not label speakers


def test_split_length_depends_on_timestamp_support():
    assert TranscriptionService(None, "whisper-1").split_seconds(300, 30) == 300
    assert TranscriptionService(None, "gpt-4o-mini-transcribe").split_seconds(300, 30) == 30


def test_request_sends_language_and_prompt_only_when_supported(tmp_path):
    audio = tmp_path / "piece_0000.mp3"
    audio.write_bytes(b"fake")
    piece = AudioPiece(0, 0, 10, str(audio))
    client = FakeMediaClient()
    TranscriptionService(client, "gpt-4o-mini-transcribe", "en", prompt="VPro, RAG").transcribe_piece(piece, audio)
    TranscriptionService(client, "gpt-4o-transcribe-diarize", prompt="VPro").transcribe_piece(piece, audio)
    first, second = client.audio.transcriptions.calls
    assert first["language"] == "en" and first["prompt"] == "VPro, RAG" and first["response_format"] == "json"
    assert "prompt" not in second and second["response_format"] == "diarized_json"


def test_failed_piece_is_recorded_and_others_continue(tmp_path):
    pieces = []
    for i in range(3):
        (tmp_path / f"piece_{i:04d}.mp3").write_bytes(b"fake")
        pieces.append(AudioPiece(i, i * 10, i * 10 + 10, str(tmp_path / f"piece_{i:04d}.mp3")))
    fake = FakeTranscriptions(fail_pieces={1}, error=_error(openai.BadRequestError, 400))
    service = TranscriptionService(FakeMediaClient(transcriptions=fake), "gpt-4o-mini-transcribe")
    result = service.transcribe_pieces(pieces, resolve_path=lambda p: p.path)
    assert [f.piece_index for f in result.failures] == [1]
    assert sorted({s.piece_index for s in result.segments}) == [0, 2]


def test_fatal_error_stops_after_first_piece(tmp_path):
    pieces = []
    for i in range(3):
        (tmp_path / f"piece_{i:04d}.mp3").write_bytes(b"fake")
        pieces.append(AudioPiece(i, i * 10, i * 10 + 10, str(tmp_path / f"piece_{i:04d}.mp3")))
    fake = FakeTranscriptions(fail_pieces={0, 1, 2}, error=_error(openai.AuthenticationError, 401))
    result = TranscriptionService(FakeMediaClient(transcriptions=fake), "whisper-1").transcribe_pieces(
        pieces, resolve_path=lambda p: p.path)
    assert len(fake.calls) == 1, "a wrong API key must not be retried for every piece"
    assert len(result.failures) == 3 and "API key" in result.failures[0].error


def test_cached_pieces_are_not_sent_again(tmp_path):
    (tmp_path / "piece_0001.mp3").write_bytes(b"fake")
    pieces = [AudioPiece(0, 0, 10, "unused"), AudioPiece(1, 10, 20, str(tmp_path / "piece_0001.mp3"))]
    cached = {0: [TranscriptSegment("p0000s0000", 0, 0, 10, "cached words", TIMING_AUDIO_SPLIT)]}
    fake = FakeTranscriptions()
    result = TranscriptionService(FakeMediaClient(transcriptions=fake), "gpt-4o-mini-transcribe").transcribe_pieces(
        pieces, resolve_path=lambda p: p.path, cached=cached)
    assert [c["piece"] for c in fake.calls] == [1]
    assert result.segments[0].text == "cached words"


def test_missing_api_credentials_are_reported():
    with pytest.raises(OpenAIServiceError, match="No OpenAI API key"):
        create_client("")
    with pytest.raises(OpenAIServiceError):
        create_client("your_openai_api_key_here")


def test_cleaning_keeps_meaning_terms_and_timestamps():
    raw = TranscriptSegment("p0s0", 0, 12.5, 15.0, "  the  top_k value is 5 , and __init__ runs  twice twice .", TIMING_MODEL)
    cleaned = clean_segments([raw, TranscriptSegment("p0s1", 0, 15, 16, " ​ ", TIMING_MODEL)])
    assert len(cleaned) == 1
    assert cleaned[0].text == "the top_k value is 5, and __init__ runs twice twice."
    assert (cleaned[0].start_seconds, cleaned[0].end_seconds, cleaned[0].segment_id) == (12.5, 15.0, "p0s0")
    assert clean_text("Text-embedding-3-small: 1536 dims") == "Text-embedding-3-small: 1536 dims"


def test_srt_only_for_model_timestamps():
    model = [TranscriptSegment("a", 0, 1.0, 3.25, "Hello", TIMING_MODEL, speaker="A")]
    srt = to_srt(model)
    assert "00:00:01,000 --> 00:00:03,250" in srt and "A: Hello" in srt
    approx = [TranscriptSegment("b", 0, 0, 30, "Hello", TIMING_AUDIO_SPLIT)]
    assert not srt_supported(approx)
    with pytest.raises(ExportError, match="misleading"):
        to_srt(approx)
    txt = to_txt(approx, "lecture.mp3", "gpt-4o-mini-transcribe")
    assert "approximate" in txt and "[00:00:00–00:00:30] Hello" in txt
