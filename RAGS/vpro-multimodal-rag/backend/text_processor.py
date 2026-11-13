"""TXT extraction: UTF-8 first, with a clearly-labelled fallback; simple heading detection."""
from __future__ import annotations

import re

from backend.errors import DocumentReadError, NoExtractableTextError
from backend.models import Section

_MD_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*$")
_UNDERLINE = re.compile(r"^(=+|-+)\s*$")


def decode_text(data: bytes, filename: str) -> tuple[str, str]:
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16"), "utf-16"
    try:
        return data.decode("utf-8-sig"), "utf-8"
    except UnicodeDecodeError:
        pass
    try:
        return data.decode("cp1252"), "cp1252-fallback"
    except UnicodeDecodeError as exc:
        raise DocumentReadError(f"'{filename}' is not valid UTF-8 text (is it a binary file?).") from exc


def _heading(line: str, next_line: str | None) -> str | None:
    s = line.strip()
    if not s or len(s) > 70:
        return None
    m = _MD_HEADING.match(s)
    if m:
        return m.group(1).strip()
    if next_line is not None and _UNDERLINE.match(next_line.strip()) and len(next_line.strip()) >= 3:
        return s
    if s.endswith(":") and len(s) > 2 and not s.endswith("::"):
        return s.rstrip(":").strip()
    if len(s) > 3 and s.upper() == s and re.search(r"[A-Z]", s) and not re.search(r"[.!?]$", s):
        return s.title()
    return None


def extract_txt(data: bytes, filename: str, file_hash: str) -> list[Section]:
    text, enc = decode_text(data, filename)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        raise NoExtractableTextError(f"'{filename}' is empty.")
    lines = text.split("\n")
    sections: list[Section] = []
    title: str | None = None
    buf: list[str] = []
    method = f"text-{enc}"

    def flush():
        body = "\n".join(buf).strip()
        if body:
            sections.append(Section(text=body, source_file=filename, file_hash=file_hash, document_type="txt",
                                    extraction_method=method, section_title=title))
        buf.clear()

    i = 0
    while i < len(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else None
        h = _heading(lines[i], nxt)
        if h and not _UNDERLINE.match(lines[i].strip()):
            flush()
            title = h
            if nxt is not None and _UNDERLINE.match(nxt.strip()):
                i += 1  # skip the underline row
        else:
            buf.append(lines[i])
        i += 1
    flush()
    return sections
