"""Word (.docx) extraction: paragraphs, heading context and tables, in document order."""
from __future__ import annotations

from io import BytesIO

from backend.errors import DocumentReadError, NoExtractableTextError
from backend.models import Section


def _table_text(table) -> str:
    rows = [[c.text.strip().replace("\n", " ") for c in r.cells] for r in table.rows]
    rows = [r for r in rows if any(r)]
    if not rows:
        return ""
    if len(rows) == 1:
        return " | ".join(v for v in rows[0] if v)
    headers = [h or f"Column {i}" for i, h in enumerate(rows[0], 1)]
    return "\n".join(" | ".join(f"{h}: {v}" for h, v in zip(headers, r) if v) for r in rows[1:])


def extract_docx(data: bytes, filename: str, file_hash: str) -> list[Section]:
    try:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
        doc = Document(BytesIO(data))
        body = list(doc.element.body.iterchildren())
    except Exception as exc:
        raise DocumentReadError(f"'{filename}' could not be read as a Word document (corrupted?): {exc}") from exc

    sections: list[Section] = []
    title: str | None = None
    buf: list[str] = []

    def flush():
        text = "\n".join(buf).strip()
        if text:
            sections.append(Section(text=text, source_file=filename, file_hash=file_hash, document_type="docx",
                                    extraction_method="python-docx", section_title=title))
        buf.clear()

    for el in body:
        tag = el.tag.rsplit("}", 1)[-1]
        if tag == "p":
            p = Paragraph(el, doc)
            text = p.text.strip()
            style = (p.style.name if p.style is not None else "") or ""
            if text and (style.lower().startswith("heading") or style.lower() == "title"):
                flush()
                title = text
            elif text:
                buf.append(text)
        elif tag == "tbl":
            t = _table_text(Table(el, doc))
            if t:
                buf.append(t)
    flush()
    if not sections:
        raise NoExtractableTextError(f"'{filename}' is a Word file but contains no text.")
    return sections
