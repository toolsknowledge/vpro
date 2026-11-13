"""PDF extraction: text page by page, keeping page numbers.

Limitation: this reads the PDF's *text layer*.  Scanned PDFs (images of text)
have no text layer; OCR is NOT implemented, so we report that clearly.
"""
from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from backend.errors import DocumentReadError, NoExtractableTextError
from backend.models import Section


def extract_pdf(data: bytes, filename: str, file_hash: str) -> list[Section]:
    try:
        reader = PdfReader(BytesIO(data))
        if reader.is_encrypted:
            try:
                ok = reader.decrypt("")
            except Exception:
                ok = 0
            if not ok:
                raise DocumentReadError(f"'{filename}' is password-protected. Remove the password and upload again.")
        pages = list(reader.pages)
    except DocumentReadError:
        raise
    except (PdfReadError, ValueError, KeyError, OSError, Exception) as exc:  # corrupted file
        raise DocumentReadError(f"'{filename}' could not be read as a PDF (it may be corrupted): {exc}") from exc

    sections: list[Section] = []
    for number, page in enumerate(pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            sections.append(Section(text=text, source_file=filename, file_hash=file_hash, document_type="pdf",
                                    extraction_method="pypdf-text", page_number=number))
    if not sections:
        raise NoExtractableTextError(
            f"No extractable text found in '{filename}' ({len(pages)} page(s)). It is probably a scanned/image-only PDF. "
            "OCR is not implemented in this app, so this file cannot be indexed."
        )
    return sections
