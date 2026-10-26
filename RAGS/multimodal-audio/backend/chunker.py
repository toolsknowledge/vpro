"""Token-aware chunking.

How it works:
1. Sections are grouped by `group_key` (one PDF page, one Word/TXT section,
   one Excel worksheet). Groups are never mixed, so a chunk always comes from
   exactly one page / section / worksheet of exactly one document.
2. Inside a group the text is split into words. Words are added to the
   current chunk until the next word would exceed `chunk_size` tokens.
3. The next chunk starts `chunk_overlap` tokens *before* the previous chunk
   ended, so a sentence cut at a boundary still appears whole in one chunk.

Tokens are counted with tiktoken (the tokenizer OpenAI embedding models use).
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from backend.document_loader import ExtractedSection, document_id_from_hash
from config.settings import validate_chunk_settings

# Leading whitespace stays attached to each word (" the"), matching how tiktoken splits text.
_WORD_PIECES = re.compile(r"\s*\S+")


class TokenCounter:
    """Counts tokens with tiktoken; falls back to ~4 characters per token if unavailable."""

    def __init__(self, encoding_name: str = "cl100k_base"):
        self.encoding = None
        try:
            import tiktoken

            self.encoding = tiktoken.get_encoding(encoding_name)
        except Exception:  # tiktoken downloads its vocabulary on first use; may fail offline
            self.encoding = None

    @property
    def is_exact(self) -> bool:
        return self.encoding is not None

    def count(self, text: str) -> int:
        if self.encoding is not None:
            return len(self.encoding.encode_ordinary(text))
        return max(1, math.ceil(len(text) / 4)) if text else 0

    def count_many(self, texts: list[str]) -> list[int]:
        if self.encoding is not None:
            return [len(t) for t in self.encoding.encode_ordinary_batch(texts)]
        return [self.count(t) for t in texts]


@lru_cache(maxsize=1)
def get_token_counter() -> TokenCounter:
    return TokenCounter()


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    source_file: str
    file_hash: str
    document_type: str
    extraction_method: str
    token_count: int
    page_number: int | None = None
    sheet_name: str | None = None
    section_title: str | None = None
    row_start: int | None = None
    row_end: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_metadata(self, embedding_model: str | None = None) -> dict[str, Any]:
        """Metadata for ChromaDB. Chroma rejects None values, so those are left out."""
        meta = {k: v for k, v in self.to_dict().items() if k != "text" and v is not None}
        if embedding_model:
            meta["embedding_model"] = embedding_model
        return meta


def make_chunk_id(document_id: str, chunk_index: int, text: str) -> str:
    """Stable ID: same document + same position + same text => same ID, every time."""
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]
    return f"{document_id}_c{chunk_index:04d}_{digest}"


def _group_sections(sections: list[ExtractedSection]) -> list[list[ExtractedSection]]:
    """Group consecutive sections with the same group_key (never across documents)."""
    groups: list[list[ExtractedSection]] = []
    for section in sections:
        key = (section.file_hash, section.group_key)
        if groups and (groups[-1][0].file_hash, groups[-1][0].group_key) == key:
            groups[-1].append(section)
        else:
            groups.append([section])
    return groups


def _split_group(
    group: list[ExtractedSection], chunk_size: int, chunk_overlap: int, counter: TokenCounter
) -> list[tuple[str, list[int]]]:
    """Split one group into (chunk_text, [indices of sections it covers]) windows."""
    pieces: list[str] = []
    owner: list[int] = []  # which section each word piece came from
    for section_index, section in enumerate(group):
        words = _WORD_PIECES.findall(section.text)
        if words and pieces:
            words[0] = "\n" + words[0].lstrip()  # each section (row, paragraph) starts on a new line
        pieces.extend(words)
        owner.extend([section_index] * len(words))
    if not pieces:
        return []

    sizes = counter.count_many(pieces)
    windows: list[tuple[str, list[int]]] = []
    start = 0
    while start < len(pieces):
        end, total = start, 0
        while end < len(pieces) and (total + sizes[end] <= chunk_size or end == start):
            total += sizes[end]
            end += 1
        text = "".join(pieces[start:end]).strip()
        if text:
            windows.append((text, sorted(set(owner[start:end]))))
        if end >= len(pieces):
            break
        # Step back from `end` until we have ~chunk_overlap tokens of overlap.
        next_start, overlap = end, 0
        while next_start > start + 1 and overlap + sizes[next_start - 1] <= chunk_overlap:
            next_start -= 1
            overlap += sizes[next_start]
        start = next_start
    return windows


def chunk_sections(
    sections: list[ExtractedSection],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    counter: TokenCounter | None = None,
) -> list[Chunk]:
    """Turn cleaned sections of ONE document into chunks with full metadata."""
    validate_chunk_settings(chunk_size, chunk_overlap)
    counter = counter or get_token_counter()
    if not sections:
        return []
    if len({s.file_hash for s in sections}) > 1:
        raise ValueError("chunk_sections expects the sections of a single document.")

    document_id = document_id_from_hash(sections[0].file_hash)
    chunks: list[Chunk] = []
    for group in _group_sections(sections):
        first = group[0]
        for text, covered in _split_group(group, chunk_size, chunk_overlap, counter):
            rows = [group[i].row_number for i in covered if group[i].row_number is not None]
            index = len(chunks)
            chunks.append(
                Chunk(
                    chunk_id=make_chunk_id(document_id, index, text),
                    document_id=document_id,
                    chunk_index=index,
                    text=text,
                    source_file=first.source_file,
                    file_hash=first.file_hash,
                    document_type=first.document_type,
                    extraction_method=first.extraction_method,
                    token_count=counter.count(text),
                    page_number=first.page_number,
                    sheet_name=first.sheet_name,
                    section_title=first.section_title,
                    row_start=min(rows) if rows else None,
                    row_end=max(rows) if rows else None,
                )
            )
    return chunks


def find_overlap(previous_text: str, current_text: str, min_chars: int = 3) -> str:
    """Return the longest text that ends `previous_text` and starts `current_text`.

    Used by the Chunk Explorer to highlight overlap between neighbouring chunks.
    """
    previous_text, current_text = previous_text.strip(), current_text.strip()
    longest = min(len(previous_text), len(current_text))
    for size in range(longest, min_chars - 1, -1):
        if previous_text.endswith(current_text[:size]):
            return current_text[:size]
    return ""
