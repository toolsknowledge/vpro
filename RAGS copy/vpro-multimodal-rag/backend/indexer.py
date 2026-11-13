"""The indexing pipeline orchestrator:  Upload → Extract → Clean → Chunk → Embed → Store.

Safety rules implemented here:
* A file is registered as "indexed" only after every step succeeded.
* Embeddings are computed *before* anything is written, so a failure never
  leaves half-written or lost data; old records are replaced only on success.
* Identity is the SHA-256 of the file content, not its name.
"""
from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Optional

from backend.chunker import chunk_sections, get_tokenizer, validate_chunk_settings
from backend.document_loader import compute_hash, document_type_for, extract_document, safe_filename, validate_upload
from backend.document_registry import DocumentRegistry, now_iso
from backend.errors import AppError
from backend.models import Chunk, Section
from backend.text_cleaner import clean_sections
from backend.vector_store import VectorStore

Progress = Callable[[str, float], None]
UNIT_LABELS = {"pdf": "pages", "xlsx": "worksheets", "docx": "sections", "txt": "sections"}


@dataclass
class FileIndexResult:
    filename: str
    status: str                    # indexed | reindexed | skipped_duplicate | failed
    message: str = ""
    document_id: str = ""
    document_type: str = ""
    units: int = 0
    unit_label: str = "sections"
    sections: int = 0
    chunks: int = 0
    embeddings: int = 0
    dimension: int = 0
    stored: int = 0
    seconds: float = 0.0
    retries: int = 0

    @property
    def ok(self) -> bool:
        return self.status in ("indexed", "reindexed", "skipped_duplicate")

    def to_dict(self) -> dict:
        return asdict(self)


def count_units(sections: list[Section]) -> int:
    return len({(s.page_number, s.sheet_name, s.section_title) for s in sections})


def _prepare(filename: str, data: bytes, file_hash: str, embedder, chunk_size: int, chunk_overlap: int,
             progress: Optional[Progress] = None):
    """Extract → clean → chunk → embed.  Nothing is written anywhere."""
    p = progress or (lambda stage, f: None)
    p("Extract", 0.0)
    raw = extract_document(filename, data, file_hash)
    p("Clean", 0.0)
    cleaned = clean_sections(raw)
    p("Chunk", 0.0)
    chunks = chunk_sections(cleaned, chunk_size, chunk_overlap)
    if not chunks:
        from backend.errors import NoExtractableTextError
        raise NoExtractableTextError(f"'{filename}' produced no text after cleaning.")
    p("Embed", 0.0)
    vectors = embedder.embed_texts([c.text for c in chunks], progress=lambda d, t: p("Embed", d / t))
    return raw, cleaned, chunks, vectors


def _build_trace(filename, doc_type, raw, cleaned, chunks, vectors, embedder, chunk_size, chunk_overlap, stored):
    return {
        "filename": filename, "document_type": doc_type, "created_at": now_iso(),
        "tokenizer": get_tokenizer().name, "embedding_model": embedder.model,
        "chunk_size": chunk_size, "chunk_overlap": chunk_overlap,
        "raw_sections": [s.to_dict() for s in raw], "cleaned_sections": [s.to_dict() for s in cleaned],
        "stages": {"extracted_sections": len(raw), "cleaned_sections": len(cleaned), "chunks": len(chunks),
                   "embeddings": len(vectors), "dimension": len(vectors[0]) if vectors else 0, "stored": stored,
                   "units": count_units(cleaned), "unit_label": UNIT_LABELS.get(doc_type, "sections")},
    }


def index_file(filename: str, data: bytes, *, settings, registry: DocumentRegistry, store: VectorStore, embedder,
               chunk_size: int, chunk_overlap: int, force: bool = False,
               progress: Optional[Progress] = None) -> FileIndexResult:
    t0 = time.perf_counter()
    name = safe_filename(filename)
    res = FileIndexResult(filename=name, status="failed")
    p = progress or (lambda stage, f: None)
    retries_before = getattr(embedder, "retries", 0)
    try:
        p("Upload", 0.0)
        validate_upload(filename, data, settings.max_upload_bytes)
        validate_chunk_settings(chunk_size, chunk_overlap)
        store.assert_compatible()
        file_hash = compute_hash(data)
        res.document_id, res.document_type = file_hash, document_type_for(name)
        res.unit_label = UNIT_LABELS.get(res.document_type, "sections")

        existing = registry.get(file_hash)
        old_ids = store.ids_for_document(file_hash) if existing else []
        if existing and old_ids and not force:
            res.status = "skipped_duplicate"
            res.message = (f"Already indexed (same content as '{existing['filename']}', "
                           f"{len(old_ids)} chunks). Tick 'Re-index existing' to rebuild it.")
            res.chunks = res.stored = len(old_ids)
            return res

        raw, cleaned, chunks, vectors = _prepare(name, data, file_hash, embedder, chunk_size, chunk_overlap, progress)

        p("Store", 0.0)
        store.add_chunks(chunks, vectors)
        stale = [i for i in old_ids if i not in {c.chunk_id for c in chunks}]
        store.delete_ids(stale)

        stored_path = settings.uploads_dir / f"{file_hash[:12]}_{name}"
        stored_path.parent.mkdir(parents=True, exist_ok=True)
        stored_path.write_bytes(data)
        n_stored = len(store.ids_for_document(file_hash))
        others = [r["filename"] for r in registry.all() if r["filename"] == name and r["document_id"] != file_hash]

        registry.upsert({
            "document_id": file_hash, "filename": name, "document_type": res.document_type, "size_bytes": len(data),
            "stored_path": str(stored_path), "indexed_at": now_iso(), "status": "indexed",
            "sections": len(cleaned), "units": count_units(cleaned), "unit_label": res.unit_label,
            "chunks": len(chunks), "dimension": len(vectors[0]), "embedding_model": embedder.model,
            "chunk_size": chunk_size, "chunk_overlap": chunk_overlap,
            "processing_seconds": round(time.perf_counter() - t0, 2)})
        registry.save_trace(file_hash, _build_trace(name, res.document_type, raw, cleaned, chunks, vectors,
                                                    embedder, chunk_size, chunk_overlap, n_stored))
        res.status = "reindexed" if existing else "indexed"
        res.sections, res.units = len(cleaned), count_units(cleaned)
        res.chunks, res.embeddings, res.dimension, res.stored = len(chunks), len(vectors), len(vectors[0]), n_stored
        res.message = "Indexed successfully."
        if others:
            res.message += f" Note: a different version named '{name}' is also in the index; remove the old one if unwanted."
    except AppError as exc:
        res.status, res.message = "failed", str(exc)
    except Exception as exc:  # never let one bad file crash a batch
        res.status, res.message = "failed", f"Unexpected error while indexing '{name}': {type(exc).__name__}: {exc}"
    finally:
        res.seconds = round(time.perf_counter() - t0, 2)
        res.retries = getattr(embedder, "retries", 0) - retries_before
    return res


def delete_document(document_id: str, *, registry: DocumentRegistry, store: VectorStore) -> int:
    """Remove vectors, registry entry, trace and stored upload for one document."""
    n = store.delete_document(document_id)
    registry.remove(document_id)
    return n


def clear_everything(*, registry: DocumentRegistry, store: VectorStore) -> None:
    store.clear()
    registry.clear()


def reindex_all(*, settings, registry: DocumentRegistry, store: VectorStore, embedder, chunk_size: int,
                chunk_overlap: int, progress: Optional[Progress] = None) -> list[FileIndexResult]:
    """Rebuild every document (e.g. after changing the embedding model).

    All embedding happens first.  Only if *every* file succeeds do we replace the
    collection, so a failure leaves the existing index untouched.
    """
    validate_chunk_settings(chunk_size, chunk_overlap)
    records = registry.all()
    prepared, results = [], []
    for i, rec in enumerate(records):
        t0 = time.perf_counter()
        path = Path(rec.get("stored_path", ""))
        if not path.is_file():
            raise AppError(f"The stored copy of '{rec['filename']}' is missing, so re-indexing was cancelled "
                           "and nothing was changed. Re-upload that file or remove it from the registry first.")
        data = path.read_bytes()
        raw, cleaned, chunks, vectors = _prepare(rec["filename"], data, rec["document_id"], embedder,
                                                 chunk_size, chunk_overlap,
                                                 progress=lambda s, f, i=i: (progress or (lambda *_: None))(
                                                     f"{rec['filename']} · {s}", (i + f) / max(len(records), 1)))
        prepared.append((rec, raw, cleaned, chunks, vectors, time.perf_counter() - t0))
    store.clear(new_model=embedder.model)
    for rec, raw, cleaned, chunks, vectors, secs in prepared:
        store.add_chunks(chunks, vectors)
        rec.update({"indexed_at": now_iso(), "chunks": len(chunks), "dimension": len(vectors[0]),
                    "embedding_model": embedder.model, "chunk_size": chunk_size, "chunk_overlap": chunk_overlap,
                    "sections": len(cleaned), "units": count_units(cleaned), "processing_seconds": round(secs, 2)})
        registry.upsert(rec)
        registry.save_trace(rec["document_id"], _build_trace(rec["filename"], rec["document_type"], raw, cleaned,
                                                             chunks, vectors, embedder, chunk_size, chunk_overlap,
                                                             len(chunks)))
        results.append(FileIndexResult(filename=rec["filename"], status="reindexed", document_id=rec["document_id"],
                                       document_type=rec["document_type"], chunks=len(chunks),
                                       embeddings=len(vectors), dimension=len(vectors[0]), stored=len(chunks),
                                       seconds=round(secs, 2), message="Re-indexed."))
    return results
