"""Audio metadata, validation, silence-aware splitting and safe uploads."""

import io

import pytest

from backend.audio_processor import parse_silences, plan_segments, prepare_audio, split_audio
from backend.media_utils import (
    FFmpegTools,
    MediaError,
    check_media_extension,
    format_timestamp,
    parse_probe_output,
    parse_timestamp,
    probe_media,
    save_stream,
    validate_media_info,
)
from tests.conftest import make_tone, needs_ffmpeg

TOOLS = FFmpegTools(timeout=120)


# ------------------------------------------------------------- pure helpers
def test_plan_segments_covers_whole_recording_without_gaps():
    plan = plan_segments(125, 30, silences=[])
    assert plan[0][0] == 0 and plan[-1][1] == 125
    for (_, end, _), (start, _, _) in zip(plan, plan[1:]):
        assert end == start  # no gaps, no overlaps
    assert all(end - start <= 30 for start, end, _ in plan)


def test_plan_segments_moves_cuts_into_pauses():
    plan = plan_segments(100, 30, silences=[(27.0, 28.0), (55.0, 56.0)])
    assert plan[0] == (0.0, 27.5, True)  # cut in the middle of the pause before 30 s
    assert plan[1][0] == 27.5 and plan[1][1] == 55.5 and plan[1][2] is True


def test_plan_segments_merges_tiny_tail():
    plan = plan_segments(60.4, 30, silences=[])
    assert plan[-1][1] == 60.4 and len(plan) == 2


def test_parse_silences_from_ffmpeg_output():
    stderr = """[silencedetect @ 0x1] silence_start: 8.5
[silencedetect @ 0x1] silence_end: 10.0 | silence_duration: 1.5
[silencedetect @ 0x1] silence_start: 18.5
[silencedetect @ 0x1] silence_end: 20 | silence_duration: 1.5"""
    assert parse_silences(stderr) == [(8.5, 10.0), (18.5, 20.0)]


def test_probe_output_ignores_cover_art_as_video():
    payload = {
        "format": {"duration": "61.2", "format_name": "mp3", "bit_rate": "128000"},
        "streams": [
            {"codec_type": "audio", "codec_name": "mp3", "sample_rate": "44100", "channels": 2},
            {"codec_type": "video", "codec_name": "mjpeg", "disposition": {"attached_pic": 1}},
        ],
    }
    info = parse_probe_output(payload, 1000)
    assert info.has_audio and not info.has_video and info.media_kind == "audio"
    assert info.duration_seconds == 61.2 and info.sample_rate == 44100 and info.bit_rate == 128000


def test_validate_rejects_too_long_and_streamless_media():
    long_info = parse_probe_output({"format": {"duration": "7200"}, "streams": [{"codec_type": "audio"}]}, 10)
    with pytest.raises(MediaError, match="limit"):
        validate_media_info(long_info, ".mp3", max_duration_seconds=3600)
    empty = parse_probe_output({"format": {"duration": "10"}, "streams": []}, 10)
    with pytest.raises(MediaError, match="No audio or video stream"):
        validate_media_info(empty, ".mp3", 3600)


def test_unsupported_extension_is_rejected():
    with pytest.raises(MediaError, match="unsupported media type"):
        check_media_extension("lecture.exe")
    assert check_media_extension("Lecture.MP4") == ".mp4"


def test_save_stream_enforces_size_and_rejects_empty(tmp_path):
    with pytest.raises(MediaError, match="limit"):
        save_stream(io.BytesIO(b"x" * 2048), tmp_path / "big.mp3", max_bytes=1024)
    assert not (tmp_path / "big.mp3").exists()  # partial file removed
    with pytest.raises(MediaError, match="empty"):
        save_stream(io.BytesIO(b""), tmp_path / "empty.mp3", max_bytes=1024)
    digest, size = save_stream(io.BytesIO(b"abc"), tmp_path / "ok.mp3", max_bytes=1024)
    assert size == 3 and len(digest) == 64


def test_timestamp_formatting_round_trip():
    assert format_timestamp(750.4) == "00:12:30"
    assert format_timestamp(3.25, millis=True) == "00:00:03,250"
    assert parse_timestamp("00:12:30") == 750 and parse_timestamp("12:30") == 750 and parse_timestamp("90") == 90
    assert parse_timestamp("soon") is None


def test_missing_ffmpeg_is_reported_clearly():
    ok, message = FFmpegTools(ffmpeg="ffmpeg-does-not-exist", ffprobe="ffprobe-nope").available()
    assert not ok and "brew install ffmpeg" in message


# ---------------------------------------------------------------- with FFmpeg
@needs_ffmpeg
def test_audio_metadata_extraction(tmp_path):
    path = make_tone(tmp_path / "tone.wav", seconds=12)
    info = probe_media(path, TOOLS)
    assert info.has_audio and not info.has_video
    assert info.media_kind == "audio"
    assert 11.5 < info.duration_seconds < 12.5
    assert info.audio_codec == "pcm_s16le" and info.sample_rate == 44100


@needs_ffmpeg
def test_corrupted_and_empty_files_get_clear_errors(tmp_path):
    bad = tmp_path / "broken.mp3"
    bad.write_bytes(b"this is not audio at all" * 50)
    with pytest.raises(MediaError, match="corrupted|unsupported"):
        probe_media(bad, TOOLS)
    empty = tmp_path / "empty.mp3"
    empty.write_bytes(b"")
    with pytest.raises(MediaError, match="empty"):
        probe_media(empty, TOOLS)


@needs_ffmpeg
def test_prepare_and_split_preserves_timeline(tmp_path):
    source = make_tone(tmp_path / "lecture.wav", seconds=45, gap_every=10, gap=1.5)
    speech = prepare_audio(source, tmp_path / "work" / "speech.mp3", TOOLS)
    assert source.exists(), "the original recording must be preserved"
    probe = probe_media(speech, TOOLS)
    assert probe.channels == 1 and probe.sample_rate == 16000

    from backend.audio_processor import detect_silences

    silences = detect_silences(speech, TOOLS)
    assert len(silences) >= 3
    plan = plan_segments(probe.duration_seconds, 20, silences)
    pieces = split_audio(speech, plan, tmp_path / "work" / "pieces", TOOLS)
    assert [p.index for p in pieces] == list(range(len(plan)))
    assert pieces[0].start_seconds == 0 and abs(pieces[-1].end_seconds - probe.duration_seconds) < 0.01
    assert any(p.cut_at_silence for p in pieces[:-1])
    for piece in pieces:
        assert abs(probe_media(piece.path, TOOLS).duration_seconds - piece.duration) < 0.3
