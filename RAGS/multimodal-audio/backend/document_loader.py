"""Document loading: validate an upload and turn it into extracted sections.

Every file type (PDF, Excel, Word, TXT) is converted into the same internal
representation, a list of `ExtractedSection` objects. The rest of the pipeline
(cleaning, chunking, embedding) never needs to know which format a file was.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import PurePath
from typing import Any

from config.settings import SUPPORTED_EXTENSIONS


class DocumentLoadError(Exception):
    """A friendly, user-facing problem with an uploaded file."""


@dataclass
class ExtractedSection:
    """One piece of extracted content plus where it came from."""

    text: str
    source_file: str
    file_hash: str
    document_type: str
    extraction_method: str
    page_number: int | None = None
    sheet_name: str | None = None
    row_number: int | None = None
    section_title: str | None = None
    # Sections that share a group_key may be packed into the same chunk.
    # Different keys are never mixed (e.g. two worksheets, two PDF pages).
    group_key: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LoadResult:
    """Everything the loader learned about one file."""

    source_file: str
    file_hash: str
    document_type: str
    extension: str
    size_bytes: int
    sections: list[ExtractedSection]
    warnings: list[str] = field(default_factory=list)
    # Human-friendly counts, e.g. {"pages": 3} or {"worksheets": 2, "rows": 40}
    units: dict[str, int] = field(default_factory=dict)


def compute_file_hash(data: bytes) -> str:
    """SHA-256 of the file bytes: identifies a document *version*, whatever its name."""
    return hashlib.sha256(data).hexdigest()


def document_id_from_hash(file_hash: str) -> str:
    return f"doc_{file_hash[:16]}"


_UNSAFE_CHARS = re.compile(r"[^A-Za-z0-9._ ()\-]+")


def sanitize_filename(filename: str) -> str:
    """Return a display-safe file name with no directory parts.

    `../../etc/passwd` becomes `passwd`; odd characters become `_`.
    The result is only used for display and metadata. Files are saved to disk
    under a generated name (the document ID), never under the user's name.
    """
    name = unicodedata.normalize("NFKC", filename or "")
    # Strip any directory components, for both / and \ separators.
    name = PurePath(name.replace("\\", "/")).name
    name = _UNSAFE_CHARS.sub("_", name).strip(" .")
    if not name:
        name = "uploaded_file"
    return name[:150]


def get_extension(filename: str) -> str:
    return PurePath(filename).suffix.lower()


def validate_upload(filename: str, size_bytes: int, max_bytes: int) -> tuple[str, str]:
    """Check name and size. Returns (safe_filename, extension) or raises DocumentLoadError."""
    safe_name = sanitize_filename(filename)
    extension = get_extension(safe_name)
    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise DocumentLoadError(
            f"'{safe_name}' has an unsupported file type ({extension or 'no extension'}). "
            f"Supported types: {supported}."
        )
    if size_bytes == 0:
        raise DocumentLoadError(f"'{safe_name}' is empty (0 bytes).")
    if size_bytes > max_bytes:
        raise DocumentLoadError(
            f"'{safe_name}' is {size_bytes / 1_048_576:.1f} MB, which is above the "
            f"{max_bytes / 1_048_576:.0f} MB limit (MAX_UPLOAD_SIZE_MB)."
        )
    return safe_name, extension


def merge_title_only_sections(sections: list[tuple[str | None, str]]) -> list[tuple[str | None, str]]:
    """Fold sections that hold nothing but a heading (e.g. a document title) into the next section.

    Without this, "Training Policy" followed directly by "Attendance" would
    become a tiny chunk containing only the words "Training Policy".
    """
    merged: list[tuple[str | None, str]] = []
    pending: list[str] = []
    for title, body in sections:
        body = body.strip()
        single_line = "\n" not in body
        if single_line and (body == title or (title is None and len(body.split()) <= 12)):
            pending.append(body)
            continue
        if pending:
            body = "\n".join(pending + [body])
            pending = []
        merged.append((title, body))
    if pending:
        merged.append((sections[-1][0], "\n".join(pending)))
    return merged


def load_document(data: bytes, filename: str, max_bytes: int = 20 * 1024 * 1024) -> LoadResult:
    """Validate and extract one file. Raises DocumentLoadError on any failure."""
    # Imported here so each processor module stays independent and easy to read.
    from backend import excel_processor, pdf_processor, text_processor, word_processor

    safe_name, extension = validate_upload(filename, len(data), max_bytes)
    file_hash = compute_file_hash(data)
    document_type = SUPPORTED_EXTENSIONS[extension]

    processors = {
        "pdf": pdf_processor.extract_pdf,
        "excel": excel_processor.extract_excel,
        "word": word_processor.extract_word,
        "text": text_processor.extract_text,
    }
    extract = processors[document_type]
    if document_type == "excel":
        sections, warnings, units = extract(data, safe_name, file_hash, extension)
    else:
        sections, warnings, units = extract(data, safe_name, file_hash)

    if not any(s.text.strip() for s in sections):
        raise DocumentLoadError(f"No extractable text was found in '{safe_name}'.")

    return LoadResult(
        source_file=safe_name,
        file_hash=file_hash,
        document_type=document_type,
        extension=extension,
        size_bytes=len(data),
        sections=sections,
        warnings=warnings,
        units=units,
    )
