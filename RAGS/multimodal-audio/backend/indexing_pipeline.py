"""The indexing pipeline: Upload → Extract → Clean → Chunk → Embed → Store.

`IndexingPipeline.index_file()` runs all six stages for one file and returns a
`FileIndexReport` describing what happened at every stage (status, input,
output, counts, timing). The UI uses these reports for the pipeline view.

Safety rules:
* Everything that can fail slowly (extraction, embedding) happens *before*
  ChromaDB is touched, so a failed re-index leaves the old records intact.
* A file is only marked "indexed" after its vectors are stored.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

from backend.chunker import chunk_sections, get_token_counter
from backend.document_loader import DocumentLoadError, document_id_from_hash, load_document
from backend.document_registry import STATUS_FAILED, STATUS_INDEXED, DocumentRegistry, utc_now
from backend.embeddings import EmbeddingService
from backend.openai_client import OpenAIServiceError
from backend.text_cleaner import clean_sections
from backend.vector_store import VectorStore, VectorStoreError
from config.settings import ConfigError, validate_chunk_settings

STAGES = [
    ("upload", "Upload", "Validate the file type, size and content hash."),
    ("extract", "Extract", "Read text from the file into sections with source metadata."),
    ("clean", "Clean", "Normalise whitespace and characters without losing information."),
    ("chunk", "Chunk", "Split sections into overlapping, token-limited chunks."),
    ("embed", "Embed", "Convert each chunk into a vector with the OpenAI embedding model."),
    ("store", "Store", "Save text, vectors and metadata in the persistent ChromaDB collection."),
]

ProgressCallback = Callable[[str, str], None]  # (stage_key, message)


@dataclass
class StageResult:
    key: str
    name: str
    description: str
    status: str = "pending"  # pending | done | skipped | failed
    input: str = ""
    output: str = ""
    count: int | None = None
    seconds: float = 0.0
    message: str = ""


@dataclass
class FileIndexReport:
    filename: str
    status: str = "pending"  # indexed | duplicate | failed
    document_id: str | None = None
    file_hash: str | None = None
    document_type: str | None = None
    message: str = ""
    warnings: list[str] = field(default_factory=list)
    units: dict[str, int] = field(default_factory=dict)
    sections: int = 0
    chunks: int = 0
    embeddings: int = 0
    dimension: int | None = None
    stored_records: int = 0
    seconds: float = 0.0
    stages: list[StageResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _new_stages() -> list[StageResult]:
    return [StageResult(key, name, description) for key, name, description in STAGES]


class IndexingPipeline:
    def __init__(
        self,
        registry: DocumentRegistry,
        store: VectorStore,
        embedder: EmbeddingService | None,
        max_upload_bytes: int,
    ):
        self.registry = registry
        self.store = store
        self.embedder = embedder
        self.max_upload_bytes = max_upload_bytes

    def index_file(
        self,
        filename: str,
        data: bytes,
        chunk_size: int,
        chunk_overlap: int,
        force: bool = False,
        progress: ProgressCallback | None = None,
    ) -> FileIndexReport:
        report = FileIndexReport(filename=filename, stages=_new_stages())
        stages = {s.key: s for s in report.stages}
        started = time.perf_counter()
        notify = progress or (lambda stage, message: None)

        def run(stage_key: str):
            stage = stages[stage_key]
            stage.status = "running"
            notify(stage_key, f"{stage.name}: {filename}")
            return stage, time.perf_counter()

        def fail(stage: StageResult, t0: float, message: str) -> FileIndexReport:
            stage.status, stage.message, stage.seconds = "failed", message, time.perf_counter() - t0
            for later in report.stages[report.stages.index(stage) + 1 :]:
                later.status = "skipped"
            report.status, report.message = "failed", message
            report.seconds = time.perf_counter() - started
            if report.document_id:
                self._record_failure(report)
            return report

        # 1. Upload ---------------------------------------------------------
        stage, t0 = run("upload")
        try:
            validate_chunk_settings(chunk_size, chunk_overlap)
            if self.embedder is None:
                raise ConfigError("OpenAI is not configured (missing OPENAI_API_KEY), so files cannot be embedded.")
            load = load_document(data, filename, self.max_upload_bytes)
        except (DocumentLoadError, ConfigError) as exc:
            return fail(stage, t0, str(exc))
        report.filename = load.source_file
        report.file_hash = load.file_hash
        report.document_id = document_id_from_hash(load.file_hash)
        report.document_type = load.document_type
        stage.input = f"{filename} ({len(data):,} bytes)"
        stage.output = f"{load.document_type.upper()} file, SHA-256 {load.file_hash[:12]}…"
        stage.count, stage.status, stage.seconds = 1, "done", time.perf_counter() - t0

        existing = self.registry.get(report.document_id)
        in_store = self.store.count_for_document(report.document_id)
        same_settings = bool(
            existing
            and existing.get("chunk_size") == chunk_size
            and existing.get("chunk_overlap") == chunk_overlap
            and existing.get("embedding_model") == self.embedder.model
        )
        if existing and existing.get("status") == STATUS_INDEXED and in_store and same_settings and not force:
            report.status = "duplicate"
            report.message = (
                f"Already indexed as '{existing['filename']}' with the same content and settings "
                f"({in_store} chunks). Tick 'Re-index duplicates' to process it again."
            )
            report.stored_records = in_store
            report.chunks = existing.get("chunk_count", in_store)
            for s in report.stages[1:]:
                s.status, s.message = "skipped", "Duplicate content: already in ChromaDB."
            report.seconds = time.perf_counter() - started
            return report

        # 2. Extract (already done by load_document; recorded as its own stage) --
        stage, t0 = run("extract")
        report.units, report.warnings = load.units, list(load.warnings)
        stage.input = f"{load.source_file}"
        stage.output = f"{len(load.sections)} section(s); " + ", ".join(f"{v} {k}" for k, v in load.units.items())
        stage.count, stage.status, stage.seconds = len(load.sections), "done", time.perf_counter() - t0

        # 3. Clean ----------------------------------------------------------
        stage, t0 = run("clean")
        cleaned = clean_sections(load.sections)
        raw_chars = sum(len(s.text) for s in load.sections)
        clean_chars = sum(len(s.text) for s in cleaned)
        if not cleaned:
            return fail(stage, t0, "Nothing was left after cleaning; the file contains no usable text.")
        report.sections = len(cleaned)
        stage.input = f"{len(load.sections)} section(s), {raw_chars:,} characters"
        stage.output = f"{len(cleaned)} section(s), {clean_chars:,} characters"
        stage.count, stage.status, stage.seconds = len(cleaned), "done", time.perf_counter() - t0

        # 4. Chunk ----------------------------------------------------------
        stage, t0 = run("chunk")
        counter = get_token_counter()
        try:
            chunks = chunk_sections(cleaned, chunk_size, chunk_overlap, counter)
        except (ConfigError, ValueError) as exc:
            return fail(stage, t0, str(exc))
        if not chunks:
            return fail(stage, t0, "No chunks were produced.")
        report.chunks = len(chunks)
        stage.input = f"{len(cleaned)} cleaned section(s)"
        stage.output = (
            f"{len(chunks)} chunk(s), {sum(c.token_count for c in chunks):,} tokens "
            f"(size {chunk_size}, overlap {chunk_overlap}{'' if counter.is_exact else ', approximate token counts'})"
        )
        stage.count, stage.status, stage.seconds = len(chunks), "done", time.perf_counter() - t0

        # 5. Embed ----------------------------------------------------------
        stage, t0 = run("embed")
        try:
            self.store.check_compatible(self.embedder.model)
            result = self.embedder.embed_texts(
                [c.text for c in chunks],
                progress=lambda done, total: notify("embed", f"Embedding {done}/{total} chunks of {load.source_file}"),
            )
        except (OpenAIServiceError, VectorStoreError, ValueError) as exc:
            report.message = str(exc)
            return fail(stage, t0, f"{exc} (0 of {len(chunks)} chunks stored; the document was not indexed.)")
        report.embeddings, report.dimension = len(result.vectors), result.dimension
        stage.input = f"{len(chunks)} chunk(s)"
        stage.output = f"{len(result.vectors)} vector(s) × {result.dimension} dimensions ({result.model})"
        if result.retries:
            stage.message = f"Recovered after {result.retries} retry(ies)."
        stage.count, stage.status, stage.seconds = len(result.vectors), "done", time.perf_counter() - t0

        # 6. Store ----------------------------------------------------------
        stage, t0 = run("store")
        try:
            stored_file = self.registry.save_upload(report.document_id, load.extension, data)
            self.store.replace_document(
                report.document_id,
                ids=[c.chunk_id for c in chunks],
                texts=[c.text for c in chunks],
                metadatas=[c.to_metadata(self.embedder.model) for c in chunks],
                embeddings=result.vectors,
                embedding_model=self.embedder.model,
            )
            stored = self.store.count_for_document(report.document_id)
        except (VectorStoreError, OSError, ValueError) as exc:
            return fail(stage, t0, f"Storing in ChromaDB failed: {exc}")
        if stored != len(chunks):
            return fail(stage, t0, f"Expected {len(chunks)} records in ChromaDB but found {stored}.")
        report.stored_records = stored
        stage.input = f"{len(chunks)} chunk(s) + vectors"
        stage.output = f"{stored} record(s) in collection '{self.store.collection_name}'"
        stage.count, stage.status, stage.seconds = stored, "done", time.perf_counter() - t0

        report.status = "indexed"
        report.seconds = time.perf_counter() - started
        report.message = f"Indexed {len(chunks)} chunk(s) in {report.seconds:.1f}s."

        self.registry.save_trace(
            report.document_id,
            {
                "document_id": report.document_id,
                "source_file": load.source_file,
                "raw_sections": [s.to_dict() for s in load.sections],
                "clean_sections": [s.to_dict() for s in cleaned],
                "chunks": [c.to_dict() for c in chunks],
            },
        )
        self.registry.upsert(
            {
                "document_id": report.document_id,
                "filename": load.source_file,
                "file_hash": load.file_hash,
                "document_type": load.document_type,
                "extension": load.extension,
                "size_bytes": load.size_bytes,
                "stored_file": stored_file,
                "status": STATUS_INDEXED,
                "indexed_at": utc_now(),
                "units": load.units,
                "section_count": len(cleaned),
                "chunk_count": len(chunks),
                "embedding_count": len(result.vectors),
                "embedding_model": self.embedder.model,
                "embedding_dimension": result.dimension,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "processing_seconds": round(report.seconds, 2),
                "warnings": report.warnings,
                "stages": [asdict(s) for s in report.stages],
            }
        )
        return report

    def _record_failure(self, report: FileIndexReport) -> None:
        """Remember a failure without overwriting a previously indexed, still-valid version."""
        existing = self.registry.get(report.document_id)
        if existing and existing.get("status") == STATUS_INDEXED:
            existing = dict(existing)
            existing["last_error"] = report.message
            self.registry.upsert(existing)
            return
        self.registry.upsert(
            {
                "document_id": report.document_id,
                "filename": report.filename,
                "file_hash": report.file_hash,
                "document_type": report.document_type,
                "status": STATUS_FAILED,
                "indexed_at": None,
                "failed_at": utc_now(),
                "last_error": report.message,
                "chunk_count": 0,
                "stages": [asdict(s) for s in report.stages],
            }
        )

    def delete_document(self, document_id: str) -> int:
        """Remove one document from ChromaDB, the registry, traces and uploads."""
        removed = self.store.delete_document(document_id)
        self.registry.remove(document_id)
        return removed

    def rebuild_all(self, chunk_size: int, chunk_overlap: int, progress: ProgressCallback | None = None) -> list[FileIndexReport]:
        """Re-embed every stored document into a fresh collection, then swap it in.

        Used after changing the embedding model. If anything fails, the old
        collection is left untouched.
        """
        documents = [d for d in self.registry.list_documents() if d.get("stored_file")]
        staging = self.store.open_staging()
        staging_pipeline = IndexingPipeline(self.registry, staging, self.embedder, self.max_upload_bytes)
        snapshot = {d["document_id"]: dict(d) for d in documents}
        trace_snapshot = {doc_id: self.registry.load_trace(doc_id) for doc_id in snapshot}
        reports = []
        for doc in documents:
            data = self.registry.read_upload(doc)
            if data is None:
                reports.append(FileIndexReport(filename=doc["filename"], status="failed", message="Original upload file is missing."))
                continue
            reports.append(staging_pipeline.index_file(doc["filename"], data, chunk_size, chunk_overlap, force=True, progress=progress))

        if reports and all(r.status == "indexed" for r in reports):
            self.store.promote_staging(staging)
        else:
            staging.client.delete_collection(staging.collection_name)
            # The old collection is untouched; restore the registry rows and traces that describe it.
            for doc_id, record in snapshot.items():
                self.registry.upsert(record)
                if trace_snapshot.get(doc_id):
                    self.registry.save_trace(doc_id, trace_snapshot[doc_id])
        return reports
