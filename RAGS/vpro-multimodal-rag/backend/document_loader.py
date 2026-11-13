"""Step 1 & 2: validate an upload and dispatch to the right extractor."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from backend.errors import FileTooLargeError, UnsupportedFileError, DocumentReadError
from backend.excel_processor import extract_excel
from backend.models import Section
from backend.pdf_processor import extract_pdf
from backend.text_processor import extract_txt
from backend.word_processor import extract_docx
from config.settings import SUPPORTED_EXTENSIONS

_EXTRACTORS = {
    ".pdf": ("pdf", extract_pdf),
    ".xlsx": ("xlsx", extract_excel),
    ".xls": ("xlsx", extract_excel),
    ".docx": ("docx", extract_docx),
    ".txt": ("txt", extract_txt),
}
_MAGIC = {".pdf": (b"%PDF",), ".xlsx": (b"PK",), ".docx": (b"PK",), ".xls": (b"\xd0\xcf\x11\xe0",)}


def safe_filename(filename: str) -> str:
    """Strip any directory part and unsafe characters (prevents path traversal)."""
    name = Path(filename.replace("\\", "/")).name
    name = re.sub(r"[^A-Za-z0-9._ -]", "_", name).strip(" .")
    return name or "unnamed_file"


def file_extension(filename: str) -> str:
    return Path(safe_filename(filename)).suffix.lower()


def compute_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def document_type_for(filename: str) -> str:
    return _EXTRACTORS[file_extension(filename)][0]


def validate_upload(filename: str, data: bytes, max_bytes: int) -> str:
    """Return the lower-case extension, or raise a friendly error."""
    ext = file_extension(filename)
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileError(
            f"'{filename}' has an unsupported type ({ext or 'no extension'}). "
            f"Supported: {', '.join(SUPPORTED_EXTENSIONS)}.")
    if len(data) == 0:
        raise DocumentReadError(f"'{filename}' is empty (0 bytes).")
    if len(data) > max_bytes:
        raise FileTooLargeError(
            f"'{filename}' is {len(data) / 1_048_576:.1f} MB; the limit is {max_bytes / 1_048_576:.0f} MB "
            "(change MAX_UPLOAD_SIZE_MB in .env).")
    magic = _MAGIC.get(ext)
    if magic and not data.startswith(magic):
        raise DocumentReadError(f"'{filename}' does not look like a real {ext} file (wrong file signature).")
    return ext


def extract_document(filename: str, data: bytes, file_hash: str) -> list[Section]:
    ext = file_extension(filename)
    if ext not in _EXTRACTORS:
        raise UnsupportedFileError(f"Unsupported file type: {ext}")
    return _EXTRACTORS[ext][1](data, safe_filename(filename), file_hash)
