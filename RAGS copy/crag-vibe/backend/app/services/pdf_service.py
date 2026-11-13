"""PDF processing pipeline: read PDFs, clean text, split into chunks and index them in ChromaDB.

Only PDF files inside backend/knowledge_base/ are ever read – no file paths come from the user.
"""

import hashlib
import logging
import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app import config
from app.errors import ServiceError
from app.services import retrieval_service

logger = logging.getLogger("crag.pdf")

PAGE_NUMBER_LINE = re.compile(r"^\s*(page\s*)?\d+\s*(of\s*\d+)?\s*$", re.IGNORECASE)


def list_pdf_files() -> list[Path]:
    """PDF files directly inside the knowledge_base folder (no sub-folders, no symlinks outside it)."""
    if not config.KNOWLEDGE_BASE_DIR.is_dir():
        return []
    base = config.KNOWLEDGE_BASE_DIR.resolve()
    return sorted(
        path for path in base.glob("*.pdf")
        if path.is_file() and path.resolve().parent == base
    )


def extract_pages(pdf_path: Path) -> list[dict]:
    """Return [{"page_number": 1, "text": "..."}, ...] for a PDF file."""
    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    if size_mb > config.MAX_PDF_SIZE_MB:
        raise ServiceError(f"'{pdf_path.name}' is larger than {config.MAX_PDF_SIZE_MB} MB.", 413)
    try:
        reader = PdfReader(pdf_path)
        if reader.is_encrypted:
            raise ServiceError(f"'{pdf_path.name}' is password-protected and cannot be read.", 422)
        return [
            {"page_number": number, "text": page.extract_text() or ""}
            for number, page in enumerate(reader.pages, start=1)
        ]
    except ServiceError:
        raise
    except (PdfReadError, ValueError, OSError) as error:
        logger.error("Could not read PDF %s: %s", pdf_path.name, error)
        raise ServiceError(f"'{pdf_path.name}' is not a valid PDF file.", 422) from error


def clean_pages(pages: list[dict]) -> list[dict]:
    """Remove page numbers and running headers/footers, and normalise whitespace."""
    page_lines = [[line.strip() for line in page["text"].splitlines()] for page in pages]

    # A line that appears on most pages (e.g. a running header) adds no meaning to any chunk.
    repeated_lines: set[str] = set()
    if len(pages) >= 3:
        line_counts = Counter(line for lines in page_lines for line in set(lines) if line)
        repeated_lines = {line for line, count in line_counts.items() if count >= len(pages) * 0.6}

    cleaned = []
    for page, lines in zip(pages, page_lines):
        kept = [
            re.sub(r"\s+", " ", line)
            for line in lines
            if line and line not in repeated_lines and not PAGE_NUMBER_LINE.match(line)
        ]
        cleaned.append({"page_number": page["page_number"], "text": "\n".join(kept).strip()})
    return cleaned


def split_text(text: str, chunk_size: int = config.CHUNK_SIZE, overlap: int = config.CHUNK_OVERLAP) -> list[str]:
    """Split text into ~chunk_size character chunks that overlap by ~overlap characters.

    Chunks end at a line break, sentence end or space where possible, so words are not cut in half.
    """
    text = text.strip()
    if len(text) <= chunk_size:
        return [text] if text else []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            search_from = start + chunk_size // 2
            boundary = max(text.rfind("\n", search_from, end), text.rfind(". ", search_from, end))
            if boundary == -1:
                boundary = text.rfind(" ", search_from, end)
            if boundary != -1:
                end = boundary + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        next_start = max(end - overlap, start + 1)
        # Begin the overlap on a new line if possible, otherwise on a whole word.
        boundary = text.find("\n", next_start, end)
        if boundary == -1:
            boundary = text.find(" ", next_start, end)
        start = boundary + 1 if boundary != -1 else next_start
    return chunks


def build_chunks(pdf_path: Path, file_hash: str) -> list[dict]:
    """Extract, clean and split one PDF into chunks with metadata."""
    chunks = []
    for page in clean_pages(extract_pages(pdf_path)):
        for index, text in enumerate(split_text(page["text"])):
            chunk_id = f"{pdf_path.stem}-p{page['page_number']}-c{index}"
            chunks.append({
                "chunk_id": chunk_id,
                "text": text,
                "metadata": {
                    "document_name": pdf_path.name,
                    "page_number": page["page_number"],
                    "chunk_id": chunk_id,
                    "source": f"knowledge_base/{pdf_path.name}",
                    "file_hash": file_hash,
                },
            })
    return chunks


def _file_hash(pdf_path: Path) -> str:
    return hashlib.sha256(pdf_path.read_bytes()).hexdigest()


def ingest_documents() -> dict:
    """Index every PDF in the knowledge base. Unchanged PDFs are skipped; changed ones are re-indexed."""
    pdf_files = list_pdf_files()
    if not pdf_files:
        raise ServiceError("No PDF documents were found in backend/knowledge_base.", 404)

    retrieval_service.reset_collection_if_model_changed()
    results = []
    for pdf_path in pdf_files:
        try:
            file_hash = _file_hash(pdf_path)
            if retrieval_service.get_document_fingerprint(pdf_path.name) == file_hash:
                results.append({"document_name": pdf_path.name, "status": "already_indexed",
                                "chunks": retrieval_service.count_chunks(pdf_path.name),
                                "message": "Document is already indexed and unchanged."})
                continue

            chunks = build_chunks(pdf_path, file_hash)
            if not chunks:
                raise ServiceError(f"'{pdf_path.name}' does not contain any readable text.", 422)
            retrieval_service.delete_document(pdf_path.name)  # remove chunks from an older version
            retrieval_service.store_chunks(chunks)
            logger.info("Indexed %s: %d chunks", pdf_path.name, len(chunks))
            results.append({"document_name": pdf_path.name, "status": "indexed", "chunks": len(chunks),
                            "message": "Document indexed successfully."})
        except ServiceError as error:
            # A bad file (too large / invalid / empty) only fails that document.
            # Any other problem (AI service, database) affects every document, so report it directly.
            if error.status_code not in (413, 422):
                raise
            results.append({"document_name": pdf_path.name, "status": "failed", "chunks": 0,
                            "message": error.message})

    return {"results": results, "total_chunks": retrieval_service.count_chunks()}


def list_documents() -> dict:
    """Describe each PDF in the knowledge base and how many of its chunks are indexed."""
    documents = []
    for pdf_path in list_pdf_files():
        try:
            page_count = len(PdfReader(pdf_path).pages)
        except (PdfReadError, ValueError, OSError):
            page_count = 0
        indexed_chunks = retrieval_service.count_chunks(pdf_path.name)
        documents.append({
            "document_name": pdf_path.name,
            "size_kb": round(pdf_path.stat().st_size / 1024, 1),
            "page_count": page_count,
            "indexed_chunks": indexed_chunks,
            "indexed": indexed_chunks > 0,
        })
    return {"documents": documents, "total_chunks": retrieval_service.count_chunks()}
