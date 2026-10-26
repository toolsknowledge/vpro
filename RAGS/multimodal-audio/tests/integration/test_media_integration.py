"""Real OpenAI + real FFmpeg on the generated sample media. Costs a few cents. Run explicitly with:

    python scripts/generate_sample_media.py
    RUN_OPENAI_INTEGRATION=1 pytest -m integration
"""

import os
from pathlib import Path

import pytest

from backend.media_pipeline import MediaOptions
from backend.services import build_services
from config.settings import load_settings
from tests.conftest import needs_ffmpeg

SAMPLE = Path(__file__).resolve().parents[2] / "sample_files" / "Python_Lecture.mp4"

pytestmark = [
    pytest.mark.integration,
    needs_ffmpeg,
    pytest.mark.skipif(os.getenv("RUN_OPENAI_INTEGRATION") != "1", reason="set RUN_OPENAI_INTEGRATION=1 to run"),
]


def test_video_rag_end_to_end(tmp_path, monkeypatch):
    if not SAMPLE.exists():
        pytest.skip("run scripts/generate_sample_media.py first")
    monkeypatch.setenv("DATA_DIRECTORY", str(tmp_path))
    monkeypatch.setenv("CHROMA_PERSIST_DIRECTORY", str(tmp_path / "chroma_db"))
    settings = load_settings()
    if not settings.has_api_key:
        pytest.skip("OPENAI_API_KEY is not configured")
    services = build_services(settings)

    with open(SAMPLE, "rb") as handle:
        report = services.media_pipeline.process(SAMPLE.name, handle, MediaOptions(frame_interval_seconds=10))
    assert report.status == "indexed", report.errors
    assert report.transcript_chunks >= 1 and report.frame_chunks >= 3

    answer = services.unified_rag.ask("Which timestamp shows the slide explaining ChromaDB?", scope="video")
    assert answer.grounded and answer.citations
    assert any(c.chunk.metadata["media_type"] == "video_frame" for c in answer.citations)
