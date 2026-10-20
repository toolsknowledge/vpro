import pytest

from app.rag.chunking import split_text

WORDS = " ".join(f"word{i}" for i in range(400))


def test_short_text_is_a_single_chunk() -> None:
    assert split_text("  A short sentence.  ", chunk_size=100, chunk_overlap=10) == ["A short sentence."]


def test_empty_text_yields_no_chunks() -> None:
    assert split_text("   \n ", chunk_size=100, chunk_overlap=10) == []


def test_chunks_respect_size_and_never_split_words() -> None:
    chunks = split_text(WORDS, chunk_size=120, chunk_overlap=30)

    assert len(chunks) > 1
    assert all(0 < len(chunk) <= 120 for chunk in chunks)
    vocabulary = set(WORDS.split())
    assert all(word in vocabulary for chunk in chunks for word in chunk.split())


def test_consecutive_chunks_overlap() -> None:
    chunks = split_text(WORDS, chunk_size=120, chunk_overlap=30)

    for previous, current in zip(chunks, chunks[1:]):
        assert current.split()[0] in previous.split()


def test_zero_overlap_covers_text_exactly_once() -> None:
    chunks = split_text(WORDS, chunk_size=120, chunk_overlap=0)
    assert " ".join(chunks).split() == WORDS.split()


def test_prefers_paragraph_boundaries() -> None:
    text = "First paragraph sentence.\nSecond paragraph that is longer."
    assert split_text(text, chunk_size=40, chunk_overlap=0) == [
        "First paragraph sentence.",
        "Second paragraph that is longer.",
    ]


def test_text_without_spaces_is_hard_split() -> None:
    chunks = split_text("x" * 250, chunk_size=100, chunk_overlap=20)
    assert all(len(chunk) <= 100 for chunk in chunks)
    assert chunks[-1].endswith("x")


@pytest.mark.parametrize(("size", "overlap"), [(0, 0), (100, 100), (100, -1)])
def test_invalid_parameters_are_rejected(size: int, overlap: int) -> None:
    with pytest.raises(ValueError):
        split_text("text", chunk_size=size, chunk_overlap=overlap)
