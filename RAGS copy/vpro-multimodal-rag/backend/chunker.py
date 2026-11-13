"""Step 4: token-aware chunking with overlap.

* Chunks never cross a *source boundary* (different file, PDF page, worksheet or
  document section), so unrelated content is never mixed.
* Excel rows are kept whole (a row is never cut in half) and use no overlap.
* Every chunk carries metadata and a stable, unique ID.
"""
from __future__ import annotations

import hashlib
import math
import re
from functools import lru_cache
from itertools import groupby

from backend.errors import InvalidChunkSettingsError
from backend.models import Chunk, Section

_UNIT = re.compile(r"\S+\s*")


class Tokenizer:
    """Counts tokens with tiktoken; falls back to a rough 4-chars-per-token estimate offline."""

    def __init__(self):
        self.name = "approx-4-chars-per-token"
        self._enc = None
        try:
            import tiktoken
            self._enc = tiktoken.get_encoding("cl100k_base")
            self.name = "tiktoken-cl100k_base"
        except Exception:
            pass

    def count(self, text: str) -> int:
        if not text:
            return 0
        if self._enc is not None:
            return len(self._enc.encode(text, disallowed_special=()))
        return max(1, math.ceil(len(text) / 4))


@lru_cache(maxsize=1)
def get_tokenizer() -> Tokenizer:
    return Tokenizer()


def validate_chunk_settings(chunk_size: int, chunk_overlap: int) -> None:
    if chunk_size <= 0:
        raise InvalidChunkSettingsError("Chunk size must be greater than 0.")
    if chunk_overlap < 0:
        raise InvalidChunkSettingsError("Chunk overlap cannot be negative.")
    if chunk_overlap >= chunk_size:
        raise InvalidChunkSettingsError("Chunk overlap must be smaller than the chunk size.")


def _windows(counts: list[int], size: int, overlap: int) -> list[tuple[int, int]]:
    """Sliding windows over units. Returns [start, end) index pairs; always makes progress."""
    n, i, out = len(counts), 0, []
    while i < n:
        total, j = 0, i
        while j < n and (j == i or total + counts[j] <= size):
            total += counts[j]
            j += 1
        out.append((i, j))
        if j >= n:
            break
        k, back = j, 0
        while k > i + 1 and back + counts[k - 1] <= overlap:
            k -= 1
            back += counts[k]
        i = k
    return out


def make_chunk_id(file_hash: str, chunk_index: int, text: str) -> str:
    """Deterministic: same file + position + text => same ID on every run."""
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    return f"{file_hash[:12]}-{chunk_index:05d}-{digest}"


def _header_for(first: Section) -> str:
    if first.sheet_name:
        return f"Sheet: {first.sheet_name}"
    if first.section_title:
        return f"Section: {first.section_title}"
    return ""


def chunk_sections(sections: list[Section], chunk_size: int = 800, chunk_overlap: int = 120) -> list[Chunk]:
    validate_chunk_settings(chunk_size, chunk_overlap)
    tok = get_tokenizer()
    chunks: list[Chunk] = []

    for _, grp in groupby(sections, key=lambda s: s.boundary_key()):
        group = list(grp)
        first = group[0]
        tabular = first.row_number is not None
        header = _header_for(first)
        header_tokens = tok.count(header + "\n") if header else 0
        eff = chunk_size - header_tokens
        if eff < max(chunk_size // 2, 1):
            eff = max(chunk_size // 2, 1)

        if tabular:
            units = [f"Row {s.row_number}: {s.text}\n" for s in group]
            rows = [s.row_number for s in group]
            counts = [tok.count(u) for u in units]
            wins = _windows(counts, eff, 0)
            pieces = []
            for a, b in wins:
                pieces.append(("".join(units[a:b]).strip(), rows[a], rows[b - 1]))
        else:
            text = "\n\n".join(s.text for s in group)
            units = _UNIT.findall(text)
            counts = [tok.count(u) for u in units]
            wins = _windows(counts, eff, chunk_overlap)
            pieces = [("".join(units[a:b]).strip(), None, None) for a, b in wins]

        for body, r0, r1 in pieces:
            if not body:
                continue
            text = f"{header}\n{body}" if header else body
            idx = len(chunks)
            chunks.append(Chunk(
                chunk_id=make_chunk_id(first.file_hash, idx, text), document_id=first.file_hash,
                chunk_index=idx, text=text, source_file=first.source_file, document_type=first.document_type,
                token_count=tok.count(text), extraction_method=first.extraction_method,
                page_number=first.page_number, sheet_name=first.sheet_name, section_title=first.section_title,
                row_start=r0, row_end=r1))
    return chunks


def strip_header(text: str) -> str:
    """Remove the 'Sheet: x' / 'Section: x' context line (used when comparing overlaps)."""
    first, _, rest = text.partition("\n")
    return rest if first.startswith(("Sheet: ", "Section: ")) and rest else text


def find_overlap(prev_text: str, cur_text: str) -> str:
    """Longest suffix of ``prev`` that is also a prefix of ``cur`` (shown to students as 'overlap')."""
    a, b = strip_header(prev_text), strip_header(cur_text)
    for i in range(len(a)):
        if b.startswith(a[i:]):
            return a[i:]
    return ""
