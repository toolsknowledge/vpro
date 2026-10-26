"""Chunking tests: size limits, overlap, boundaries and stable IDs."""

import pytest

from backend.chunker import TokenCounter, chunk_sections, find_overlap, make_chunk_id
from backend.document_loader import ExtractedSection, load_document
from backend.text_cleaner import clean_sections, clean_text
from config.settings import ConfigError

COUNTER = TokenCounter()


def _section(text, group="page:1", **kw):
    defaults = dict(source_file="f.pdf", file_hash="a" * 64, document_type="pdf", extraction_method="test")
    defaults.update(kw)
    return ExtractedSection(text=text, group_key=group, **defaults)


LONG_TEXT = " ".join(f"Sentence number {i} explains retrieval augmented generation." for i in range(200))


def test_chunks_respect_chunk_size():
    chunks = chunk_sections([_section(LONG_TEXT)], chunk_size=100, chunk_overlap=20, counter=COUNTER)
    assert len(chunks) > 5
    assert all(c.token_count <= 100 for c in chunks)
    # Every chunk except the last should be reasonably full.
    assert all(c.token_count >= 70 for c in chunks[:-1])


def test_neighbouring_chunks_overlap():
    chunks = chunk_sections([_section(LONG_TEXT)], chunk_size=100, chunk_overlap=20, counter=COUNTER)
    for previous, current in zip(chunks, chunks[1:]):
        shared = find_overlap(previous.text, current.text)
        assert shared, "expected overlapping text between neighbouring chunks"
        assert COUNTER.count(shared) <= 25  # ~chunk_overlap tokens (word boundaries add a little)


def test_zero_overlap_produces_no_shared_text():
    chunks = chunk_sections([_section(LONG_TEXT)], chunk_size=100, chunk_overlap=0, counter=COUNTER)
    joined = " ".join(c.text for c in chunks)
    assert joined.split() == LONG_TEXT.split()


def test_all_text_is_covered():
    chunks = chunk_sections([_section(LONG_TEXT)], chunk_size=80, chunk_overlap=10, counter=COUNTER)
    assert chunks[0].text.startswith("Sentence number 0")
    assert chunks[-1].text.endswith("Sentence number 199 explains retrieval augmented generation.")


def test_pages_are_never_mixed():
    sections = [_section("Page one text.", "page:1", page_number=1), _section("Page two text.", "page:2", page_number=2)]
    chunks = chunk_sections(sections, chunk_size=800, chunk_overlap=100, counter=COUNTER)
    assert [c.page_number for c in chunks] == [1, 2]
    assert "two" not in chunks[0].text


def test_excel_rows_pack_within_sheet_and_track_row_range():
    rows = [
        _section(f"Course: C{i} | Fee: {i}", "sheet:A", document_type="excel", sheet_name="A", row_number=i + 1)
        for i in range(1, 4)
    ] + [_section("Course: X | Fee: 1", "sheet:B", document_type="excel", sheet_name="B", row_number=2)]
    chunks = chunk_sections(rows, chunk_size=800, chunk_overlap=100, counter=COUNTER)
    assert len(chunks) == 2
    assert (chunks[0].sheet_name, chunks[0].row_start, chunks[0].row_end) == ("A", 2, 4)
    assert chunks[0].text.count("\n") == 2  # one row per line
    assert (chunks[1].sheet_name, chunks[1].row_start, chunks[1].row_end) == ("B", 2, 2)


def test_chunk_ids_are_stable_and_unique():
    sections = [_section(LONG_TEXT)]
    first = chunk_sections(sections, 100, 20, counter=COUNTER)
    second = chunk_sections(sections, 100, 20, counter=COUNTER)
    assert [c.chunk_id for c in first] == [c.chunk_id for c in second]
    assert len({c.chunk_id for c in first}) == len(first)
    assert make_chunk_id("doc_x", 0, "a") != make_chunk_id("doc_x", 0, "b")


def test_chunk_indices_are_sequential():
    chunks = chunk_sections([_section(LONG_TEXT)], 100, 20, counter=COUNTER)
    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))


def test_sections_from_two_documents_are_rejected():
    with pytest.raises(ValueError):
        chunk_sections([_section("a"), _section("b", file_hash="b" * 64)], 100, 10, counter=COUNTER)


@pytest.mark.parametrize("size, overlap", [(10, 0), (100, 60), (100, -1), (9000, 10)])
def test_invalid_chunk_settings(size, overlap):
    with pytest.raises(ConfigError):
        chunk_sections([_section("text")], size, overlap, counter=COUNTER)


def test_find_overlap():
    assert find_overlap("RAG retrieves relevant documents and supplies them",
                        "supplies them as context to a language model.") == "supplies them"
    assert find_overlap("abc def", "xyz") == ""


def test_fallback_token_counter_without_tiktoken():
    counter = TokenCounter.__new__(TokenCounter)
    counter.encoding = None
    assert counter.count("abcdefgh") == 2
    assert not counter.is_exact


def test_cleaning_keeps_content_and_fixes_whitespace():
    raw = "Fee:  30,000  INR\r\n\r\n\r\n\r\nembed-\ndings are ﬁne\t\x07"
    assert clean_text(raw) == "Fee: 30,000 INR\n\nembeddings are fine"


def test_clean_sections_drops_empty_and_keeps_metadata():
    sections = [_section("  text  ", page_number=3), _section("   \n ", page_number=4)]
    cleaned = clean_sections(sections)
    assert len(cleaned) == 1 and cleaned[0].page_number == 3 and cleaned[0].text == "text"


def test_txt_end_to_end_chunks_have_sections():
    text = "Intro:\nWelcome.\n\nModules:\nPython and RAG."
    result = load_document(text.encode(), "c.txt")
    chunks = chunk_sections(clean_sections(result.sections), 800, 120, counter=COUNTER)
    assert [c.section_title for c in chunks] == ["Intro", "Modules"]
