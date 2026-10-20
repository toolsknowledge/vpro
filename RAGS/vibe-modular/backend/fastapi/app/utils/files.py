"""File helpers for uploaded documents."""

import hashlib
from pathlib import PurePath

DOCUMENT_ID_LENGTH = 16


def compute_document_id(data: bytes) -> str:
    """Derive a stable ID from file content, so re-uploading the same file is detected as a duplicate."""
    return hashlib.sha256(data).hexdigest()[:DOCUMENT_ID_LENGTH]


def has_extension(filename: str, extension: str) -> bool:
    return PurePath(filename).suffix.lower() == extension
