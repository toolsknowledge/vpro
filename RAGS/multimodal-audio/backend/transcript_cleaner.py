"""Transcript cleaning: tidy the text, never change its meaning.

What it does:
* normalises Unicode look-alikes (non-breaking spaces, zero-width characters);
* collapses runs of spaces/newlines into single spaces;
* removes spaces before punctuation ("word ." -> "word.").

What it deliberately does NOT do: remove filler words, repetitions, numbers,
names or technical terms. Spoken repetitions often carry emphasis, and code
identifiers like `__init__` or `top_k` must survive untouched. Segment IDs and
timestamps are copied unchanged, so every cleaned segment maps 1:1 to a raw one.
"""

from __future__ import annotations

import re
from dataclasses import replace

from backend.transcription_service import TranscriptSegment

_INVISIBLE = dict.fromkeys(map(ord, "​‌‍⁠﻿"), None)
_SPACE_LIKE = dict.fromkeys(map(ord, "   \t\r\n\f\v"), " ")
_MULTI_SPACE = re.compile(r" {2,}")
_SPACE_BEFORE_PUNCT = re.compile(r" +([,.;:!?)](?:\s|$))")


def clean_text(text: str) -> str:
    text = (text or "").translate(_INVISIBLE).translate(_SPACE_LIKE)
    text = "".join(ch for ch in text if ch == " " or ch.isprintable())
    text = _MULTI_SPACE.sub(" ", text)
    text = _SPACE_BEFORE_PUNCT.sub(r"\1", text + " ").strip()
    return text


def clean_segments(segments: list[TranscriptSegment]) -> list[TranscriptSegment]:
    """Return cleaned copies; segments that end up empty are dropped."""
    cleaned = []
    for segment in segments:
        text = clean_text(segment.text)
        if text:
            cleaned.append(replace(segment, text=text))
    return cleaned
