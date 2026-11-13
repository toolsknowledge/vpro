"""Step 3 of the indexing pipeline: clean and normalise extracted text.

We are deliberately gentle: we fix whitespace and line breaks but never delete
words, numbers, punctuation or technical terms.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import replace

from backend.models import Section

_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_SPACES = re.compile(r"[ \t   ]+")
_BLANKS = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _CONTROL.sub("", text)
    lines = [_SPACES.sub(" ", ln).strip() for ln in text.split("\n")]
    text = "\n".join(lines)
    text = _BLANKS.sub("\n\n", text)
    return text.strip()


def clean_sections(sections: list[Section]) -> list[Section]:
    """Return cleaned copies; sections that become empty are dropped. Metadata is kept."""
    out = []
    for s in sections:
        cleaned = clean_text(s.text)
        if cleaned:
            out.append(replace(s, text=cleaned))
    return out
