"""Media registry: one JSON row per audio/video file, plus its on-disk artifacts.

It reuses the document registry's atomic JSON storage, and adds the media
folders so that deleting a recording removes *everything* belonging to it:

    data/media_registry.json             one row per media file (status, stages, counts)
    data/uploads/media/<id>.<ext>        the original upload (kept for playback and re-indexing)
    data/transcripts/<id>.json           raw + cleaned transcript segments and chunks
    data/extracted_audio/<id>/           temporary speech MP3 and its pieces (removed after success)
    data/video_frames/<id>/              keyframe JPEGs + frames.json (descriptions)

Every row stores the status of each processing stage, which is how a failed
job can be retried without repeating the stages that already worked.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from backend.document_registry import DocumentRegistry, _atomic_write_json

STATUS_INDEXED = "indexed"
STATUS_PARTIAL = "partial"  # something was indexed, but some stage(s) failed: retry is possible
STATUS_FAILED = "failed"
STATUS_PROCESSING = "processing"


class MediaRegistry(DocumentRegistry):
    def __init__(
        self,
        registry_path: Path,
        transcripts_directory: Path,
        uploads_directory: Path,
        extracted_audio_directory: Path,
        video_frames_directory: Path,
    ):
        super().__init__(registry_path, transcripts_directory, uploads_directory)
        self.extracted_audio_directory = Path(extracted_audio_directory)
        self.video_frames_directory = Path(video_frames_directory)

    # --------------------------------------------------------------- folders
    def _child(self, base: Path, document_id: str) -> Path:
        path = (base / Path(document_id).name).resolve()
        if path.parent != base.resolve():
            raise ValueError("Refusing to use a path outside the media folders.")
        return path

    def audio_dir(self, document_id: str) -> Path:
        return self._child(self.extracted_audio_directory, document_id)

    def frames_dir(self, document_id: str) -> Path:
        return self._child(self.video_frames_directory, document_id)

    def upload_path(self, record: dict[str, Any]) -> Path | None:
        stored = record.get("stored_file")
        if not stored:
            return None
        path = self.uploads_directory / Path(stored).name
        return path if path.exists() else None

    def remove(self, document_id: str) -> None:
        super().remove(document_id)  # registry row, transcript JSON, original upload
        shutil.rmtree(self.audio_dir(document_id), ignore_errors=True)
        shutil.rmtree(self.frames_dir(document_id), ignore_errors=True)

    def find_by_filename(self, filename: str) -> list[dict[str, Any]]:
        return [d for d in self._data["documents"].values() if d.get("filename") == filename]

    # ------------------------------------------------------------- artifacts
    def frames_manifest_path(self, document_id: str) -> Path:
        return self.frames_dir(document_id) / "frames.json"

    def save_frames_manifest(self, document_id: str, manifest: dict[str, Any]) -> None:
        _atomic_write_json(self.frames_manifest_path(document_id), manifest)

    def load_frames_manifest(self, document_id: str) -> dict[str, Any] | None:
        path = self.frames_manifest_path(document_id)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
