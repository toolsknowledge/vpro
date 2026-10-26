"""Plain-text (.txt) extraction.

Decodes the bytes (UTF-8 first), then splits the text into sections at lines
that look like headings, so answers can cite "section: Course modules".
Recognised headings:
  * Markdown style:          "# Course modules"
  * Underlined:              "Course modules" followed by "=====" or "-----"
  * Short line ending in ":"  "Course modules:"
  * Short ALL-CAPS line:     "COURSE MODULES"
"""

from __future__ import annotations

import re

from backend.document_loader import DocumentLoadError, ExtractedSection, merge_title_only_sections

_MARKDOWN_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
_UNDERLINE = re.compile(r"^\s*(=+|-+)\s*$")


def decode_text(data: bytes, filename: str) -> tuple[str, str | None]:
    """Return (text, warning). Raises DocumentLoadError for binary data."""
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16"), None
    if b"\x00" in data[:4096]:
        raise DocumentLoadError(f"'{filename}' looks like a binary file, not plain text.")
    try:
        return data.decode("utf-8-sig"), None
    except UnicodeDecodeError:
        # cp1252 (Windows "ANSI") is the most common non-UTF-8 encoding for .txt files.
        try:
            return data.decode("cp1252"), f"'{filename}' is not valid UTF-8; it was decoded as Windows-1252."
        except UnicodeDecodeError:
            return data.decode("latin-1"), f"'{filename}' is not valid UTF-8; it was decoded as Latin-1."


def _heading_text(lines: list[str], i: int) -> str | None:
    """Return the heading text if lines[i] is a heading, else None."""
    line = lines[i].strip()
    if not line:
        return None
    match = _MARKDOWN_HEADING.match(line)
    if match:
        return match.group(1).strip()
    next_line = lines[i + 1] if i + 1 < len(lines) else ""
    if _UNDERLINE.match(next_line) and len(line) <= 80 and not _UNDERLINE.match(line):
        return line
    words = line.split()
    if line.endswith(":") and 1 <= len(words) <= 8:
        return line[:-1].strip()
    # Must start with a letter so list items such as "2. RAG" or "- API" are not headings.
    if line.isupper() and 1 <= len(words) <= 8 and line[0].isalpha() and sum(c.isalpha() for c in line) >= 4:
        return line.title()
    return None


def split_into_sections(text: str) -> list[tuple[str | None, str]]:
    """Split text into (heading, body) pairs. Text before the first heading has heading None."""
    lines = text.splitlines()
    sections: list[tuple[str | None, list[str]]] = [(None, [])]
    skip_next = False
    for i, line in enumerate(lines):
        if skip_next:  # the ==== / ---- underline of a heading
            skip_next = False
            continue
        heading = _heading_text(lines, i)
        if heading is not None:
            if i + 1 < len(lines) and _UNDERLINE.match(lines[i + 1]) and not _MARKDOWN_HEADING.match(line):
                skip_next = True
            sections.append((heading, [heading]))
        else:
            sections[-1][1].append(line)
    return [(title, "\n".join(body).strip()) for title, body in sections if "\n".join(body).strip()]


def extract_text(data: bytes, filename: str, file_hash: str):
    text, warning = decode_text(data, filename)
    if not text.strip():
        raise DocumentLoadError(f"The text file '{filename}' is empty.")

    sections = []
    for number, (title, body) in enumerate(merge_title_only_sections(split_into_sections(text)), start=1):
        sections.append(
            ExtractedSection(
                text=body,
                source_file=filename,
                file_hash=file_hash,
                document_type="text",
                extraction_method="utf-8 text with heading detection",
                section_title=title,
                group_key=f"section:{number}:{title or ''}",
            )
        )

    return sections, [warning] if warning else [], {"sections": len(sections), "characters": len(text)}
