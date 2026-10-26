"""Text cleaning and normalisation.

The goal is *tidy, not lossy*: fix whitespace and odd characters, but keep
every word, number, punctuation mark and table value that could answer a question.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import replace

from backend.document_loader import ExtractedSection

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_SPACES = re.compile(r"[ \t  -​　]+")
_MANY_NEWLINES = re.compile(r"\n{3,}")
# A word broken across lines by a hyphen, e.g. "embed-\ndings" (common in PDFs).
_HYPHEN_BREAK = re.compile(r"(\w)-\n(\w)")


def clean_text(text: str) -> str:
    if not text:
        return ""
    # NFKC turns ligatures ("ﬁ") and full-width characters into ordinary ones.
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _CONTROL_CHARS.sub("", text)
    text = _HYPHEN_BREAK.sub(r"\1\2", text)
    lines = [_SPACES.sub(" ", line).strip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = _MANY_NEWLINES.sub("\n\n", text)
    return text.strip()


def clean_sections(sections: list[ExtractedSection]) -> list[ExtractedSection]:
    """Clean every section and drop the ones that end up empty. Metadata is kept as-is."""
    cleaned = []
    for section in sections:
        text = clean_text(section.text)
        if text:
            cleaned.append(replace(section, text=text))
    return cleaned
