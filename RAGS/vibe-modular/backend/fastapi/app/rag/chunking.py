"""Split text into overlapping chunks that end on paragraph or word boundaries."""


def _find_break(text: str, start: int, end: int) -> int:
    """Return the best break position in text[start:end], preferring the latter half."""
    midpoint = start + (end - start) // 2
    for separator in ("\n", " "):
        position = text.rfind(separator, midpoint, end)
        if position != -1:
            return position
    return end


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Split text into chunks of at most `chunk_size` characters with roughly `chunk_overlap` overlap."""
    if chunk_size <= 0 or not 0 <= chunk_overlap < chunk_size:
        raise ValueError("chunk_size must be positive and chunk_overlap must be in [0, chunk_size).")

    text = text.strip()
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            end = _find_break(text, start, end)

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        if chunk_overlap == 0:
            start = end
            continue

        next_start = max(end - chunk_overlap, start + 1)
        # Begin the next chunk at a word boundary so the overlap never starts mid-word.
        space = text.find(" ", next_start, end)
        start = space + 1 if space != -1 else next_start
    return chunks
