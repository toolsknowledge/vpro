"""Video metadata, audio-track extraction and silent videos."""

import pytest

from backend.media_utils import FFmpegTools, MediaError, probe_media, validate_media_info
from backend.video_processor import describe_video, extract_audio_track
from tests.conftest import make_video, needs_ffmpeg

TOOLS = FFmpegTools(timeout=120)

pytestmark = needs_ffmpeg


def test_video_metadata_extraction(tmp_path):
    path = make_video(tmp_path / "lesson.mp4", colors=("red", "blue"), seg_seconds=4)
    info = probe_media(path, TOOLS)
    assert info.has_video and info.has_audio and info.media_kind == "video"
    assert (info.width, info.height) == (320, 240) and info.resolution == "320×240"
    assert info.fps == 5 and 7.5 < info.duration_seconds < 8.5
    summary = describe_video(info)
    assert summary["Resolution"] == "320×240" and summary["Audio"].startswith("yes")


def test_extract_audio_track_keeps_original(tmp_path):
    video = make_video(tmp_path / "lesson.mp4", colors=("red",), seg_seconds=5)
    info = probe_media(video, TOOLS)
    audio = extract_audio_track(video, tmp_path / "out" / "speech.mp3", info, TOOLS)
    assert video.exists() and audio.exists()
    extracted = probe_media(audio, TOOLS)
    assert extracted.has_audio and not extracted.has_video and extracted.sample_rate == 16000


def test_silent_video_has_no_audio_but_is_still_valid(tmp_path):
    video = make_video(tmp_path / "silent.mp4", colors=("red", "green"), seg_seconds=3, audio=False)
    info = probe_media(video, TOOLS)
    assert info.has_video and not info.has_audio
    warnings = validate_media_info(info, ".mp4", 3600)
    assert any("no audio track" in w for w in warnings)
    assert extract_audio_track(video, tmp_path / "speech.mp3", info, TOOLS) is None


def test_audio_extension_with_video_inside_is_treated_as_video(tmp_path):
    video = make_video(tmp_path / "clip.webm.mp4", colors=("red",), seg_seconds=2)
    info = probe_media(video, TOOLS)
    warnings = validate_media_info(info, ".m4a", 3600)
    assert any("processed as a video" in w for w in warnings)


def test_corrupted_video_is_rejected(tmp_path):
    bad = tmp_path / "bad.mp4"
    bad.write_bytes(b"\x00\x00\x00\x18ftypmp42" + b"garbage" * 100)
    with pytest.raises(MediaError):
        probe_media(bad, TOOLS)
