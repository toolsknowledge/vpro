"""Plain data containers shared by every pipeline stage."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class Section:
    """One piece of extracted content (a PDF page, an Excel row, a Word section...)."""
    text: str
    source_file: str
    file_hash: str
    document_type: str            # pdf | xlsx | docx | txt
    extraction_method: str
    page_number: Optional[int] = None
    sheet_name: Optional[str] = None
    row_number: Optional[int] = None
    section_title: Optional[str] = None

    def boundary_key(self) -> tuple:
        """Sections with different keys are never merged into the same chunk."""
        return (self.file_hash, self.page_number, self.sheet_name, self.section_title)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    source_file: str
    document_type: str
    token_count: int
    extraction_method: str = ""
    page_number: Optional[int] = None
    sheet_name: Optional[str] = None
    section_title: Optional[str] = None
    row_start: Optional[int] = None
    row_end: Optional[int] = None

    def to_metadata(self) -> dict[str, Any]:
        """ChromaDB metadata: flat values only, and no ``None`` allowed."""
        d = asdict(self)
        d.pop("text")
        return {k: v for k, v in d.items() if v is not None}
