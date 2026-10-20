"""Extract text and metadata from DOCX files."""

import io
import zipfile
from dataclasses import dataclass

from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from docx.table import Table

from app.core.exceptions import InvalidDocumentError


@dataclass(frozen=True)
class LoadedDocument:
    text: str
    title: str | None
    author: str | None


def _table_lines(table: Table) -> list[str]:
    lines = []
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        line = " | ".join(cell for cell in cells if cell)
        if line:
            lines.append(line)
    return lines


def load_docx(data: bytes) -> LoadedDocument:
    """Return the text of paragraphs and tables in document order, plus core metadata."""
    try:
        document = Document(io.BytesIO(data))
    except (PackageNotFoundError, zipfile.BadZipFile, KeyError, ValueError) as exc:
        raise InvalidDocumentError("The file is not a readable DOCX document.") from exc

    parts: list[str] = []
    for block in document.iter_inner_content():
        if isinstance(block, Table):
            parts.extend(_table_lines(block))
        elif text := block.text.strip():
            parts.append(text)

    text = "\n".join(parts)
    if not text:
        raise InvalidDocumentError("The DOCX document contains no extractable text.")

    properties = document.core_properties
    return LoadedDocument(
        text=text,
        title=properties.title or None,
        author=properties.author or None,
    )
