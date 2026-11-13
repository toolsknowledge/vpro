import pytest

from backend.chunker import chunk_sections, find_overlap, get_tokenizer, make_chunk_id
from backend.errors import InvalidChunkSettingsError
from backend.models import Section


def sec(text, **kw):
    base = dict(source_file="f.txt", file_hash="a" * 64, document_type="txt", extraction_method="t")
    base.update(kw)
    return Section(text=text, **base)


LONG = " ".join(f"word{i}" for i in range(600))


def test_size_and_overlap_respected():
    tok = get_tokenizer()
    chunks = chunk_sections([sec(LONG)], chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 3
    assert all(c.token_count <= 110 for c in chunks)          # small slack for tokenizer re-counting at joins
    ov = find_overlap(chunks[0].text, chunks[1].text)
    assert ov and 5 <= tok.count(ov) <= 22
    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))


def test_everything_is_covered():
    chunks = chunk_sections([sec(LONG)], 100, 20)
    joined = " ".join(c.text for c in chunks)
    assert all(f"word{i} " in joined + " " for i in (0, 299, 599))


def test_invalid_settings():
    for size, ov in ((0, 0), (100, 100), (100, -1), (50, 80)):
        with pytest.raises(InvalidChunkSettingsError):
            chunk_sections([sec("x")], size, ov)


def test_stable_ids_and_uniqueness():
    a = chunk_sections([sec(LONG)], 100, 20)
    b = chunk_sections([sec(LONG)], 100, 20)
    assert [c.chunk_id for c in a] == [c.chunk_id for c in b]
    assert len({c.chunk_id for c in a}) == len(a)
    assert make_chunk_id("h" * 64, 3, "t") == make_chunk_id("h" * 64, 3, "t") != make_chunk_id("h" * 64, 3, "u")


def test_source_boundaries_never_mixed():
    secs = [sec("page one text", document_type="pdf", page_number=1), sec("page two text", document_type="pdf", page_number=2),
            sec("other", section_title="B")]
    chunks = chunk_sections(secs, 800, 100)
    assert len(chunks) == 3
    assert [c.page_number for c in chunks[:2]] == [1, 2] and chunks[2].section_title == "B"
    assert "two" not in chunks[0].text


def test_excel_rows_whole_with_row_range_and_sheet_header():
    rows = [sec(f"Course: C{i} | Fee: {i}", document_type="xlsx", sheet_name="S", row_number=i + 2) for i in range(40)]
    chunks = chunk_sections(rows, chunk_size=120, chunk_overlap=50)
    assert len(chunks) > 1
    for c in chunks:
        assert c.text.startswith("Sheet: S\n") and c.row_start <= c.row_end and c.sheet_name == "S"
    assert chunks[0].row_start == 2 and chunks[-1].row_end == 41
    assert all(len(l.split("|")) == 2 for c in chunks for l in c.text.splitlines()[1:])   # no row cut in half


def test_metadata_has_no_none_values():
    md = chunk_sections([sec("hello")], 100, 10)[0].to_metadata()
    assert None not in md.values() and "page_number" not in md and md["source_file"] == "f.txt"
