"""Word (.docx) extraction with python-docx.

Paragraphs and tables are read in document order. Headings start a new
section, and every section remembers its heading so answers can cite
"section: Project assessment". Tables are converted to "Header: value" rows.
"""

from __future__ import annotations

import io
import zipfile

from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from docx.table import Table
from docx.text.paragraph import Paragraph

from backend.document_loader import DocumentLoadError, ExtractedSection, merge_title_only_sections


def _is_heading(paragraph: Paragraph) -> bool:
    style = (paragraph.style.name if paragraph.style is not None else "") or ""
    return style.lower().startswith(("heading", "title"))


def _table_to_lines(table: Table) -> list[str]:
    rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
    rows = [r for r in rows if any(r)]
    if not rows:
        return []
    headers = [h or f"Column {i}" for i, h in enumerate(rows[0], start=1)]
    if len(rows) == 1:
        return [" | ".join(rows[0])]
    lines = []
    for row in rows[1:]:
        parts = [f"{h}: {v}" for h, v in zip(headers, row) if v]
        if parts:
            lines.append(" | ".join(parts))
    return lines


def _iter_blocks(document):
    """Yield Paragraph and Table objects in the order they appear in the body."""
    body = document.element.body
    for child in body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            yield Paragraph(child, document)
        elif tag == "tbl":
            yield Table(child, document)


def extract_word(data: bytes, filename: str, file_hash: str):
    try:
        document = Document(io.BytesIO(data))
    except (PackageNotFoundError, zipfile.BadZipFile, KeyError, ValueError) as exc:
        raise DocumentLoadError(
            f"'{filename}' could not be opened as a Word document. It may be corrupted, "
            "password-protected, or an old .doc file (save it as .docx)."
        ) from exc

    parts: list[tuple[str | None, str]] = []  # (heading, text) in document order
    current_title: str | None = None
    current_lines: list[str] = []
    tables = 0

    def flush():
        nonlocal current_lines
        text = "\n".join(current_lines).strip()
        if text:
            parts.append((current_title, text))
        current_lines = []

    for block in _iter_blocks(document):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if not text:
                continue
            if _is_heading(block):
                flush()
                current_title = text
                current_lines = [text]  # keep the heading inside the chunk text, too
            else:
                current_lines.append(text)
        else:
            tables += 1
            current_lines.extend(_table_to_lines(block))
    flush()

    sections = [
        ExtractedSection(
            text=text,
            source_file=filename,
            file_hash=file_hash,
            document_type="word",
            extraction_method="python-docx paragraphs and tables",
            section_title=title,
            group_key=f"section:{number}:{title or ''}",
        )
        for number, (title, text) in enumerate(merge_title_only_sections(parts), start=1)
    ]

    if not sections:
        raise DocumentLoadError(f"The Word document '{filename}' contains no text.")

    warnings = []
    if document.inline_shapes:
        warnings.append(f"{len(document.inline_shapes)} embedded image(s) were ignored (no OCR in this app).")

    return sections, warnings, {"sections": len(sections), "tables": tables}
