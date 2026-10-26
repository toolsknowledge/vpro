"""Keyframe planning, extraction, duplicate skipping and frame analysis."""

import httpx
import openai
import pytest

from backend.frame_analyzer import FrameAnalysis, FrameAnalyzer, build_description, frame_embedding_text
from backend.frame_extractor import (
    METHOD_INTERVAL,
    METHOD_SCENE,
    FrameRecord,
    detect_scene_changes,
    extract_frames,
    parse_scene_times,
    plan_frame_timestamps,
)
from backend.media_embeddings import build_frame_chunks
from backend.media_utils import FFmpegTools, probe_media
from tests.conftest import FakeMediaChat, FakeMediaClient, make_video, needs_ffmpeg

TOOLS = FFmpegTools(timeout=120)


def _error(cls, status, code=""):
    response = httpx.Response(status, request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
    return cls("error", response=response, body={"error": {"code": code}})


def test_plan_every_interval_seconds():
    plan, warnings = plan_frame_timestamps(35, 10, 500)
    assert [t for t, _ in plan] == [0.5, 10.0, 20.0, 30.0] and not warnings
    assert all(m == METHOD_INTERVAL for _, m in plan)


def test_plan_respects_max_frames_and_explains_it():
    plan, warnings = plan_frame_timestamps(3600, 10, 50)
    assert len(plan) == 50 and warnings and "MAX_FRAMES_PER_VIDEO" in warnings[0]
    assert plan[0][0] > 0 and plan[-1][0] < 3600


def test_plan_merges_scene_changes_without_near_duplicates():
    plan, _ = plan_frame_timestamps(30, 10, 100, extra=[10.5, 14.0, 29.0])
    times = dict(plan)
    assert 14.0 in times and times[14.0] == METHOD_SCENE
    assert 10.5 not in times  # too close to the 10 s interval frame


def test_parse_scene_times():
    stderr = ("[Parsed_showinfo_1 @ 0x1] n:   0 pts:  51200 pts_time:4       duration: 512\n"
              "[Parsed_showinfo_1 @ 0x1] n:   1 pts: 102400 pts_time:8.2 duration: 512\n")
    assert parse_scene_times(stderr) == [4.0, 8.2]


@needs_ffmpeg
def test_extract_frames_records_metadata_and_skips_duplicates(tmp_path):
    video = make_video(tmp_path / "v.mp4", colors=("red", "red", "blue", "green"), seg_seconds=5, audio=False)
    info = probe_media(video, TOOLS)
    plan, _ = plan_frame_timestamps(info.duration_seconds, 5, 100)
    frames = extract_frames(video, tmp_path / "data" / "video_frames" / "media_x", document_id="media_x",
                            source_file="v.mp4", plan=plan, tools=TOOLS, data_directory=tmp_path / "data")
    assert [f.frame_index for f in frames] == list(range(len(frames)))
    assert [f.timestamp_seconds for f in frames] == [0.5, 5.0, 10.0, 15.0]
    assert frames[0].frame_id == "media_x_f0000"
    assert not frames[0].frame_path.startswith("/"), "frame paths must be relative, never absolute"
    assert (tmp_path / "data" / frames[0].frame_path).exists()
    # red, red(dup), blue, green
    assert [f.duplicate_of for f in frames] == [None, "media_x_f0000", None, None]


@needs_ffmpeg
def test_scene_detection_finds_colour_changes(tmp_path):
    video = make_video(tmp_path / "v.mp4", colors=("red", "blue", "green"), seg_seconds=3, audio=False)
    times = detect_scene_changes(video, TOOLS, threshold=0.3)
    assert any(abs(t - 3) < 0.5 for t in times) and any(abs(t - 6) < 0.5 for t in times)


def _frames(tmp_path, n=3):
    frames = []
    for i in range(n):
        (tmp_path / f"frame_{i:04d}.jpg").write_bytes(b"\xff\xd8fakejpeg")
        frames.append(FrameRecord(f"media_x_f{i:04d}", "media_x", "v.mp4", i * 10.0, f"frame_{i:04d}.jpg", i, METHOD_INTERVAL))
    return frames


def test_analyzer_describes_frames_and_skips_duplicates(tmp_path):
    frames = _frames(tmp_path)
    frames[1].duplicate_of = frames[0].frame_id
    chat = FakeMediaChat()
    analyses = FrameAnalyzer(FakeMediaClient(chat=chat), "vision-model").analyze_frames(frames, lambda f: tmp_path / f.frame_path)
    assert [a.status for a in analyses] == ["done", "skipped_duplicate", "done"]
    assert chat.vision_calls == 2
    assert "Code on screen: client = chromadb.PersistentClient" in analyses[0].description
    chunks = build_frame_chunks(frames, analyses, "f" * 64)
    assert [c.chunk_id for c in chunks] == ["media_x_f0000", "media_x_f0002"]
    assert chunks[0].span_end_seconds == 10.0  # it also stands for the duplicate at 10 s
    assert chunks[0].embedding_text().startswith("Video: v.mp4 | Timestamp: 00:00:00 | Frame description:")


def test_analyzer_continues_after_a_failed_frame_and_uses_cache(tmp_path):
    frames = _frames(tmp_path)
    chat = FakeMediaChat(vision_error=_error(openai.BadRequestError, 400), vision_fail_times=1)
    analyzer = FrameAnalyzer(FakeMediaClient(chat=chat), "vision-model")
    first = analyzer.analyze_frames(frames, lambda f: tmp_path / f.frame_path)
    assert [a.status for a in first] == ["failed", "done", "done"]
    second = analyzer.analyze_frames(frames, lambda f: tmp_path / f.frame_path, cached={a.frame_id: a for a in first})
    assert [a.status for a in second] == ["done", "done", "done"]
    assert chat.vision_calls == 4, "only the failed frame is sent again"


def test_analyzer_stops_calling_after_fatal_error(tmp_path):
    frames = _frames(tmp_path, n=4)
    chat = FakeMediaChat(vision_error=_error(openai.AuthenticationError, 401), vision_fail_times=-1)
    analyses = FrameAnalyzer(FakeMediaClient(chat=chat), "vision-model").analyze_frames(frames, lambda f: tmp_path / f.frame_path)
    assert chat.vision_calls == 1 and all(a.status == "failed" for a in analyses)


def test_description_separates_observed_and_uncertain():
    text, observed, uncertain = build_description(
        {"summary": "A slide.", "slide_title": "RAG", "code": "", "uncertain": "The small footer text is unreadable."})
    assert text.splitlines()[0] == "A slide." and "Slide title: RAG" in text
    assert "Uncertain (model's interpretation): The small footer" in text
    assert observed["code"] == "" and uncertain.startswith("The small")
    frame = FrameRecord("f", "d", "Python_Lecture.mp4", 130, "x.jpg", 0, METHOD_INTERVAL)
    assert frame_embedding_text(frame, "A slide.") == (
        "Video: Python_Lecture.mp4 | Timestamp: 00:02:10 | Frame description: A slide.")
