"""Document registry: a small JSON file listing every document the app knows about.

ChromaDB holds the chunks; the registry holds one row per *document*:
file name, content hash, status, chunk count, settings used, timings and
warnings. It also stores a "pipeline trace" per document (the extracted,
cleaned and chunked text) so the explorer pages can show real data.
"""

from __future__ import annotations

import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATUS_INDEXED = "indexed"
STATUS_FAILED = "failed"
STATUS_MISSING = "missing from ChromaDB"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _atomic_write_json(path: Path, payload: Any) -> None:
    """Write to a temp file and rename it, so a crash never leaves half a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


class DocumentRegistry:
    def __init__(self, registry_path: Path, traces_directory: Path, uploads_directory: Path):
        self.path = Path(registry_path)
        self.traces_directory = Path(traces_directory)
        self.uploads_directory = Path(uploads_directory)
        self._lock = threading.Lock()
        self._data = self._load()

    def _load(self) -> dict[str, Any]:
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text(encoding="utf-8"))
                data.setdefault("documents", {})
                return data
            except (json.JSONDecodeError, OSError):
                # Keep the broken file for inspection and start fresh.
                self.path.rename(self.path.with_suffix(".corrupt.json"))
        return {"documents": {}, "last_indexed_at": None}

    def _save(self) -> None:
        _atomic_write_json(self.path, self._data)

    def reload(self) -> None:
        with self._lock:
            self._data = self._load()

    # ------------------------------------------------------------- documents
    def list_documents(self) -> list[dict[str, Any]]:
        docs = list(self._data["documents"].values())
        return sorted(docs, key=lambda d: d.get("indexed_at") or "", reverse=True)

    def get(self, document_id: str) -> dict[str, Any] | None:
        return self._data["documents"].get(document_id)

    def find_by_hash(self, file_hash: str) -> dict[str, Any] | None:
        for doc in self._data["documents"].values():
            if doc.get("file_hash") == file_hash:
                return doc
        return None

    def upsert(self, record: dict[str, Any]) -> None:
        with self._lock:
            self._data["documents"][record["document_id"]] = record
            if record.get("status") == STATUS_INDEXED:
                self._data["last_indexed_at"] = record.get("indexed_at") or utc_now()
            self._save()

    def remove(self, document_id: str) -> None:
        """Forget a document and delete its trace and stored upload."""
        with self._lock:
            record = self._data["documents"].pop(document_id, None)
            self._save()
        self.trace_path(document_id).unlink(missing_ok=True)
        if record and record.get("stored_file"):
            (self.uploads_directory / record["stored_file"]).unlink(missing_ok=True)

    def clear(self) -> None:
        for doc_id in list(self._data["documents"]):
            self.remove(doc_id)
        with self._lock:
            self._data["last_indexed_at"] = None
            self._save()

    @property
    def last_indexed_at(self) -> str | None:
        return self._data.get("last_indexed_at")

    def sync_with_store(self, store_document_counts: dict[str, int]) -> list[str]:
        """Mark registry documents whose chunks are no longer in ChromaDB. Returns changed IDs."""
        changed = []
        with self._lock:
            for doc_id, doc in self._data["documents"].items():
                in_store = store_document_counts.get(doc_id, 0)
                if doc.get("status") == STATUS_INDEXED and in_store == 0:
                    doc["status"] = STATUS_MISSING
                    changed.append(doc_id)
                elif doc.get("status") == STATUS_MISSING and in_store > 0:
                    doc["status"] = STATUS_INDEXED
                    changed.append(doc_id)
            if changed:
                self._save()
        return changed

    # ---------------------------------------------------------------- uploads
    def save_upload(self, document_id: str, extension: str, data: bytes) -> str:
        """Store the original file under a generated name (never the user's file name)."""
        self.uploads_directory.mkdir(parents=True, exist_ok=True)
        stored_name = f"{document_id}{extension}"
        target = (self.uploads_directory / stored_name).resolve()
        if target.parent != self.uploads_directory.resolve():
            raise ValueError("Refusing to write outside the uploads directory.")
        target.write_bytes(data)
        return stored_name

    def read_upload(self, record: dict[str, Any]) -> bytes | None:
        stored = record.get("stored_file")
        if not stored:
            return None
        path = self.uploads_directory / Path(stored).name
        return path.read_bytes() if path.exists() else None

    # ----------------------------------------------------------------- traces
    def trace_path(self, document_id: str) -> Path:
        return self.traces_directory / f"{Path(document_id).name}.json"

    def save_trace(self, document_id: str, trace: dict[str, Any]) -> None:
        _atomic_write_json(self.trace_path(document_id), trace)

    def load_trace(self, document_id: str) -> dict[str, Any] | None:
        path = self.trace_path(document_id)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
