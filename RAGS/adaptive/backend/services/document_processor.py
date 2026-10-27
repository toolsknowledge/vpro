"""Chunking and stable chunk identities."""

import hashlib
import re
from dataclasses import dataclass
from typing import Any

from services.document_loader import LoadedDocument

_BREAK_PATTERNS = ("\n\n", "\n", ". ", "? ", "! ", "; ", ", ", " ")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    metadata: dict[str, Any]


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Split text into overlapping chunks of at most ``chunk_size`` characters.

    Chunks end at the most natural boundary (paragraph, line, sentence, word)
    found in the second half of the window, so sentences are rarely cut.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    text = normalize_text(text)
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            window_floor = start + chunk_size // 2
            for pattern in _BREAK_PATTERNS:
                position = text.rfind(pattern, window_floor, end)
                if position != -1:
                    end = position + len(pattern)
                    break
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        next_start = max(end - chunk_overlap, start + 1)
        # Start the overlap on a word boundary instead of mid-word.
        if next_start < end and not text[next_start - 1].isspace():
            space = text.find(" ", next_start, end)
            if space != -1:
                next_start = space + 1
        start = next_start
    return chunks


def content_fingerprint(document: LoadedDocument, chunk_size: int, chunk_overlap: int, embedding_model: str) -> str:
    """Hash of everything that determines the stored chunks and vectors.

    Hashing the extracted text (not file bytes) means regenerating an identical
    sample file does not trigger re-embedding, while any content, chunking, or
    embedding-model change does.
    """
    digest = hashlib.sha256()
    digest.update(f"{chunk_size}|{chunk_overlap}|{embedding_model}|".encode())
    for section in document.sections:
        digest.update(repr(sorted(section.metadata.items())).encode())
        digest.update(section.text.encode("utf-8"))
    return digest.hexdigest()


def build_chunks(document: LoadedDocument, chunk_size: int, chunk_overlap: int, content_hash: str) -> list[Chunk]:
    source_key = hashlib.sha256(document.source.encode("utf-8")).hexdigest()[:12]
    pieces: list[tuple[str, dict[str, Any]]] = []
    for section in document.sections:
        for piece in chunk_text(section.text, chunk_size, chunk_overlap):
            pieces.append((piece, section.metadata))
    total = len(pieces)
    return [
        Chunk(
            chunk_id=f"{source_key}-{content_hash[:12]}-{index:04d}",
            text=piece,
            metadata={
                **section_metadata,
                "source": document.source,
                "file_type": document.file_type,
                "content_hash": content_hash,
                "chunk_index": index,
                "total_chunks": total,
            },
        )
        for index, (piece, section_metadata) in enumerate(pieces)
    ]
