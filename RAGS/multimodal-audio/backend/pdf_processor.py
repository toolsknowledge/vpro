"""PDF extraction with pypdf, one section per page so page numbers are preserved.

pypdf only reads the text layer of a PDF. Scanned pages (images of text) have
no text layer, and this app does not run OCR, so such pages are reported as
having no extractable text rather than being silently skipped.
"""

from __future__ import annotations

import io

from pypdf import PdfReader
from pypdf.errors import FileNotDecryptedError, PdfReadError

from backend.document_loader import DocumentLoadError, ExtractedSection


def extract_pdf(data: bytes, filename: str, file_hash: str):
    try:
        reader = PdfReader(io.BytesIO(data))
        if reader.is_encrypted:
            # Some PDFs are "encrypted" with an empty password (copy protection only).
            try:
                if not reader.decrypt(""):
                    raise DocumentLoadError(f"'{filename}' is password-protected. Remove the password and upload it again.")
            except (FileNotDecryptedError, NotImplementedError) as exc:
                raise DocumentLoadError(f"'{filename}' is password-protected or uses unsupported encryption.") from exc
        pages = list(reader.pages)
    except DocumentLoadError:
        raise
    except (PdfReadError, ValueError, OSError) as exc:
        raise DocumentLoadError(f"'{filename}' could not be read as a PDF. It may be corrupted.") from exc

    sections: list[ExtractedSection] = []
    empty_pages: list[int] = []
    for page_number, page in enumerate(pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:  # pypdf can fail on individual malformed pages
            text = ""
        if not text.strip():
            empty_pages.append(page_number)
            continue
        sections.append(
            ExtractedSection(
                text=text,
                source_file=filename,
                file_hash=file_hash,
                document_type="pdf",
                extraction_method="pypdf text layer",
                page_number=page_number,
                group_key=f"page:{page_number}",
            )
        )

    if not sections:
        raise DocumentLoadError(
            f"No extractable text was found in '{filename}' ({len(pages)} page(s)). "
            "It is probably a scanned PDF. This app does not perform OCR."
        )

    warnings = []
    if empty_pages:
        listed = ", ".join(map(str, empty_pages[:20])) + ("…" if len(empty_pages) > 20 else "")
        warnings.append(f"{len(empty_pages)} page(s) had no extractable text (scanned or image-only?): {listed}")

    return sections, warnings, {"pages": len(pages), "pages_with_text": len(sections)}
