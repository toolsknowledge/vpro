"""Synchronises the documents directory with the ChromaDB collection.

* ``index``   — incremental: new and modified files are embedded, unchanged
  files are skipped (no OpenAI calls), so repeated runs are idempotent.
* ``reindex`` — full refresh: every file is re-embedded and chunks belonging
  to deleted, emptied, or unreadable files are removed.

For each file the new chunks are embedded first, then upserted, and only then
are the file's old chunks deleted, so a failed embedding call never leaves a
document half-indexed. A lock ensures only one indexing run writes at a time.
"""

import json
import logging
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from config import BACKEND_DIR, Settings
from schemas.documents import DocumentInfo, DocumentListResponse
from schemas.indexing import FileIssue, IndexingResult, IndexingStatus
from services.chroma_service import ChromaService, SourceSummary
from services.document_loader import (
    SUPPORTED_EXTENSIONS,
    DocumentLoadError,
    EmptyDocumentError,
    is_supported,
    list_files,
    load_document,
)
from services.document_processor import build_chunks, content_fingerprint
from services.embedding_service import EmbeddingService
from services.openai_service import LLMServiceError

logger = logging.getLogger(__name__)


class IndexingInProgressError(Exception):
    pass


class IndexingService:
    def __init__(self, settings: Settings, chroma: ChromaService, embedder: EmbeddingService) -> None:
        self._settings = settings
        self._chroma = chroma
        self._embedder = embedder
        self._lock = threading.Lock()
        self._last_result: IndexingResult | None = self._load_last_result()

    @property
    def documents_directory(self) -> Path:
        return self._settings.documents_directory

    # ------------------------------------------------------------------ state

    def _load_last_result(self) -> IndexingResult | None:
        path = self._settings.indexing_state_file
        if not path.is_file():
            return None
        try:
            return IndexingResult.model_validate_json(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            logger.warning("Ignoring unreadable indexing state file %s", path.name)
            return None

    def _save_last_result(self, result: IndexingResult) -> None:
        path = self._settings.indexing_state_file
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(result.model_dump(mode="json"), indent=2), encoding="utf-8")
        tmp_path.replace(path)

    # --------------------------------------------------------------- indexing

    def run(self, mode: Literal["index", "reindex"]) -> IndexingResult:
        if not self._lock.acquire(blocking=False):
            raise IndexingInProgressError("An indexing run is already in progress.")
        try:
            result = self._run_locked(mode)
            self._last_result = result
            self._save_last_result(result)
            return result
        finally:
            self._lock.release()

    def _run_locked(self, mode: Literal["index", "reindex"]) -> IndexingResult:
        started_at = datetime.now(timezone.utc)
        timer = time.perf_counter()
        force = mode == "reindex"

        files = list_files(self.documents_directory)
        supported = [path for path in files if is_supported(path)]
        skipped = [
            FileIssue(filename=path.name, reason=f"Unsupported file type '{path.suffix or '(none)'}'")
            for path in files
            if not is_supported(path)
        ]
        errors: list[FileIssue] = []
        removed_sources: list[str] = []
        processed = unchanged = chunks_created = chunks_removed = 0

        existing = self._chroma.source_summaries()
        logger.info("Indexing (%s): %d supported file(s) discovered", mode, len(supported))

        for path in supported:
            previous = existing.get(path.name)
            try:
                document = load_document(path)
            except EmptyDocumentError as exc:
                skipped.append(FileIssue(filename=path.name, reason=str(exc)))
                chunks_removed += self._remove_source(previous, removed_sources)
                continue
            except DocumentLoadError as exc:
                errors.append(FileIssue(filename=path.name, reason=str(exc)))
                chunks_removed += self._remove_source(previous, removed_sources)
                continue

            fingerprint = content_fingerprint(
                document,
                self._settings.chunk_size,
                self._settings.chunk_overlap,
                self._settings.openai_embedding_model,
            )
            if not force and previous is not None and previous.content_hash == fingerprint:
                unchanged += 1
                continue

            chunks = build_chunks(document, self._settings.chunk_size, self._settings.chunk_overlap, fingerprint)
            try:
                embeddings = self._embedder.embed_documents([chunk.text for chunk in chunks])
            except LLMServiceError as exc:
                errors.append(FileIssue(filename=path.name, reason=exc.message))
                continue

            new_ids = [chunk.chunk_id for chunk in chunks]
            self._chroma.add_chunks(
                ids=new_ids,
                embeddings=embeddings,
                documents=[chunk.text for chunk in chunks],
                metadatas=[chunk.metadata for chunk in chunks],
            )
            if previous is not None:
                keep = set(new_ids)
                stale_ids = [chunk_id for chunk_id in previous.chunk_ids if chunk_id not in keep]
                self._chroma.delete_ids(stale_ids)
                chunks_removed += len(stale_ids)
            processed += 1
            chunks_created += len(chunks)
            logger.info("Indexed %s (%d chunks)", path.name, len(chunks))

        if force:
            on_disk = {path.name for path in supported}
            for source, summary in existing.items():
                if source not in on_disk:
                    chunks_removed += self._remove_source(summary, removed_sources)

        status, message = self._summarise(supported, processed, unchanged, errors, chunks_created)
        return IndexingResult(
            mode=mode,
            status=status,
            message=message,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            duration_seconds=round(time.perf_counter() - timer, 3),
            discovered_files=len(files),
            processed_files=processed,
            unchanged_files=unchanged,
            chunks_created=chunks_created,
            chunks_removed=chunks_removed,
            removed_sources=removed_sources,
            skipped_files=skipped,
            errors=errors,
        )

    def _remove_source(self, summary: SourceSummary | None, removed_sources: list[str]) -> int:
        if summary is None:
            return 0
        self._chroma.delete_ids(summary.chunk_ids)
        removed_sources.append(summary.source)
        logger.info("Removed %d stale chunk(s) for %s", len(summary.chunk_ids), summary.source)
        return len(summary.chunk_ids)

    @staticmethod
    def _summarise(
        supported: list[Path], processed: int, unchanged: int, errors: list[FileIssue], chunks_created: int
    ) -> tuple[Literal["success", "partial", "failed", "no_documents"], str]:
        if not supported:
            return "no_documents", "No supported documents were found."
        if errors and processed == 0 and unchanged == 0:
            return "failed", f"Indexing failed for all {len(errors)} file(s)."
        if errors:
            return "partial", (
                f"Indexed {processed} file(s) ({chunks_created} chunks), {unchanged} unchanged, "
                f"{len(errors)} failed."
            )
        return "success", f"Indexed {processed} file(s) ({chunks_created} chunks), {unchanged} unchanged."

    # ---------------------------------------------------------------- queries

    def status(self) -> IndexingStatus:
        ready, error, summaries, chunk_count = True, None, {}, 0
        try:
            summaries = self._chroma.source_summaries()
            chunk_count = self._chroma.count()
        except Exception:  # Report storage problems instead of failing the status endpoint.
            logger.exception("Vector store status check failed")
            ready, error = False, "Vector store could not be opened. Check CHROMA_PERSIST_DIRECTORY."
        return IndexingStatus(
            collection_name=self._chroma.collection_name,
            vector_store_ready=ready,
            vector_store_error=error,
            openai_configured=self._settings.openai_configured,
            is_indexing=self._lock.locked(),
            document_count=len(summaries),
            chunk_count=chunk_count,
            last_result=self._last_result,
        )

    def list_documents(self) -> DocumentListResponse:
        ready = True
        try:
            summaries = self._chroma.source_summaries()
        except Exception:  # Listing files on disk must still work if the store is unavailable.
            logger.exception("Vector store unavailable while listing documents")
            ready, summaries = False, {}

        documents: list[DocumentInfo] = []
        for path in list_files(self.documents_directory):
            summary = summaries.get(path.name)
            documents.append(
                DocumentInfo(
                    filename=path.name,
                    file_type=SUPPORTED_EXTENSIONS.get(path.suffix.lower(), path.suffix.lstrip(".").lower()),
                    supported=is_supported(path),
                    on_disk=True,
                    size_bytes=path.stat().st_size,
                    indexed=summary is not None,
                    chunk_count=summary.chunk_count if summary else 0,
                )
            )
        on_disk = {document.filename for document in documents}
        for source, summary in sorted(summaries.items()):
            if source not in on_disk:
                documents.append(
                    DocumentInfo(
                        filename=source,
                        file_type=summary.file_type,
                        supported=True,
                        on_disk=False,
                        size_bytes=None,
                        indexed=True,
                        chunk_count=summary.chunk_count,
                    )
                )
        try:
            directory_label = str(self.documents_directory.relative_to(BACKEND_DIR.parent))
        except ValueError:
            directory_label = self.documents_directory.name
        return DocumentListResponse(
            documents_directory=directory_label,
            total_files=sum(1 for document in documents if document.on_disk),
            indexed_files=sum(1 for document in documents if document.indexed),
            total_chunks=sum(summary.chunk_count for summary in summaries.values()),
            vector_store_ready=ready,
            documents=documents,
        )
