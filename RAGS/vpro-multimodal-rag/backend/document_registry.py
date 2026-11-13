"""A small JSON registry of indexed documents (identity = SHA-256 content hash).

It also stores a per-document *trace* (raw + cleaned extracted text and stage
statistics) so the explorer pages can show what happened, even after a restart.
"""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from backend.errors import AppError


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


class DocumentRegistry:
    def __init__(self, registry_path: Path, processed_dir: Path, uploads_dir: Path):
        self.path, self.processed_dir, self.uploads_dir = Path(registry_path), Path(processed_dir), Path(uploads_dir)
        for d in (self.path.parent, self.processed_dir, self.uploads_dir):
            d.mkdir(parents=True, exist_ok=True)

    # ---- registry ----
    def _read(self) -> dict[str, dict]:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _write(self, data: dict[str, dict]) -> None:
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, self.path)
        except OSError as exc:
            Path(tmp).unlink(missing_ok=True)
            raise AppError(f"Could not save the document registry: {exc}") from exc

    def all(self) -> list[dict[str, Any]]:
        return sorted(self._read().values(), key=lambda r: r.get("indexed_at", ""), reverse=True)

    def get(self, document_id: str) -> Optional[dict]:
        return self._read().get(document_id)

    def has(self, document_id: str) -> bool:
        return document_id in self._read()

    def upsert(self, record: dict[str, Any]) -> None:
        data = self._read()
        data[record["document_id"]] = record
        self._write(data)

    def remove(self, document_id: str) -> None:
        data = self._read()
        rec = data.pop(document_id, None)
        self._write(data)
        self.trace_path(document_id).unlink(missing_ok=True)
        if rec and rec.get("stored_path"):
            p = Path(rec["stored_path"])
            if p.parent.resolve() == self.uploads_dir.resolve():
                p.unlink(missing_ok=True)

    def clear(self) -> None:
        for rec in self.all():
            self.remove(rec["document_id"])

    def last_indexed_at(self) -> Optional[str]:
        recs = self.all()
        return recs[0]["indexed_at"] if recs else None

    # ---- traces ----
    def trace_path(self, document_id: str) -> Path:
        return self.processed_dir / f"{document_id}.json"

    def save_trace(self, document_id: str, trace: dict) -> None:
        self.trace_path(document_id).write_text(json.dumps(trace, ensure_ascii=False), encoding="utf-8")

    def load_trace(self, document_id: str) -> Optional[dict]:
        p = self.trace_path(document_id)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
