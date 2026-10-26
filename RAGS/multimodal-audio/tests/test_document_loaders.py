"""Extraction tests for PDF, Excel, Word and TXT, including empty and broken files."""

import pytest

from backend.document_loader import (
    DocumentLoadError,
    compute_file_hash,
    load_document,
    sanitize_filename,
    validate_upload,
)
from tests.conftest import make_docx_bytes, make_pdf_bytes, make_xlsx_bytes


# ------------------------------------------------------------------- PDF
def test_pdf_extracts_text_page_by_page():
    data = make_pdf_bytes(["Page one talks about RAG.", "Page two talks about chunking."])
    result = load_document(data, "notes.pdf")
    assert result.document_type == "pdf"
    assert [s.page_number for s in result.sections] == [1, 2]
    assert "RAG" in result.sections[0].text and "chunking" in result.sections[1].text
    assert result.units["pages"] == 2


def test_pdf_with_no_text_is_reported_not_faked():
    data = make_pdf_bytes(["", ""])  # pages with no text layer, like a scanned PDF
    with pytest.raises(DocumentLoadError, match="No extractable text"):
        load_document(data, "scan.pdf")


def test_pdf_skips_blank_pages_with_warning():
    data = make_pdf_bytes(["Real content here.", ""])
    result = load_document(data, "mixed.pdf")
    assert len(result.sections) == 1
    assert any("no extractable text" in w for w in result.warnings)


def test_corrupted_pdf():
    with pytest.raises(DocumentLoadError, match="could not be read"):
        load_document(b"%PDF-1.4 this is not really a pdf", "broken.pdf")


# ----------------------------------------------------------------- Excel
def test_excel_rows_keep_headers_sheet_and_row(course_xlsx):
    result = load_document(course_xlsx, "catalog.xlsx")
    first = result.sections[0]
    assert first.text == "Course: Python Full Stack | Duration: 16 weeks | Fee: 30000"
    assert first.sheet_name == "Course Catalog"
    assert first.row_number == 2  # header is row 1 in Excel
    assert {s.sheet_name for s in result.sections} == {"Course Catalog", "Batches"}
    assert result.units["worksheets"] == 2


def test_excel_missing_values_are_left_out_not_invented(course_xlsx):
    result = load_document(course_xlsx, "catalog.xlsx")
    data_science = next(s for s in result.sections if "Data Science" in s.text)
    assert data_science.text == "Course: Data Science | Duration: 20 weeks"
    assert any("empty cell" in w for w in result.warnings)


def test_excel_each_sheet_has_its_own_group(course_xlsx):
    result = load_document(course_xlsx, "catalog.xlsx")
    keys = {s.sheet_name: s.group_key for s in result.sections}
    assert keys["Course Catalog"] != keys["Batches"]


def test_empty_workbook():
    data = make_xlsx_bytes({"Empty": []})
    with pytest.raises(DocumentLoadError):
        load_document(data, "empty.xlsx")


def test_corrupted_excel():
    with pytest.raises(DocumentLoadError, match="could not be read"):
        load_document(b"PK\x03\x04 not a workbook", "broken.xlsx")


# ------------------------------------------------------------------ Word
def test_word_sections_follow_headings_and_include_tables():
    data = make_docx_bytes(
        [("heading", "Attendance"), ("para", "Attend 80% of sessions."),
         ("heading", "Project assessment"), ("para", "Projects are assessed by a mentor.")],
        table=[("Criterion", "Weight"), ("Functionality", "40%")],
    )
    result = load_document(data, "policy.docx")
    titles = [s.section_title for s in result.sections]
    assert titles == ["Attendance", "Project assessment"]
    assessment = result.sections[1]
    assert "Criterion: Functionality | Weight: 40%" in assessment.text  # table kept with its section
    assert result.units["tables"] == 1


def test_word_title_only_heading_merges_into_next_section():
    data = make_docx_bytes([("heading", "Policy"), ("heading", "Refunds"), ("para", "Refunds within 7 days.")])
    result = load_document(data, "p.docx")
    assert len(result.sections) == 1
    assert result.sections[0].text.startswith("Policy\nRefunds")
    assert result.sections[0].section_title == "Refunds"


def test_empty_word_document():
    with pytest.raises(DocumentLoadError):
        load_document(make_docx_bytes([]), "empty.docx")


def test_corrupted_word_document():
    with pytest.raises(DocumentLoadError, match="could not be opened"):
        load_document(b"definitely not a docx", "broken.docx")


# ------------------------------------------------------------------- TXT
def test_txt_sections_detected_from_headings():
    text = "Course Overview\n\nCourse modules:\n1. Python\n2. RAG\n\n# Support\nSaturdays 10 AM."
    result = load_document(text.encode("utf-8"), "overview.txt")
    titles = [s.section_title for s in result.sections]
    assert titles == ["Course modules", "Support"]
    assert result.sections[0].text.startswith("Course Overview")  # title-only intro merged forward
    assert "2. RAG" in result.sections[0].text


def test_txt_utf8_with_bom_and_non_ascii():
    result = load_document("﻿Fee: ₹30,000 — café".encode("utf-8"), "fees.txt")
    assert "₹30,000" in result.sections[0].text
    assert not result.sections[0].text.startswith("﻿")
    assert result.warnings == []


def test_txt_non_utf8_falls_back_with_warning():
    result = load_document("Caf\xe9 menu".encode("cp1252"), "menu.txt")
    assert "Café" in result.sections[0].text
    assert result.warnings


def test_empty_txt():
    with pytest.raises(DocumentLoadError):
        load_document(b"   \n\n  ", "empty.txt")


def test_binary_file_renamed_to_txt():
    with pytest.raises(DocumentLoadError, match="binary"):
        load_document(b"\x00\x01\x02binary", "image.txt")


# ------------------------------------------------------------ validation
def test_unsupported_extension():
    with pytest.raises(DocumentLoadError, match="unsupported file type"):
        validate_upload("slides.pptx", 100, 1000)


def test_file_too_large():
    with pytest.raises(DocumentLoadError, match="limit"):
        validate_upload("big.pdf", 2_000_000, 1_000_000)


def test_zero_byte_file():
    with pytest.raises(DocumentLoadError, match="empty"):
        validate_upload("x.txt", 0, 1000)


@pytest.mark.parametrize(
    "unsafe, expected",
    [("../../etc/passwd.txt", "passwd.txt"), ("..\\..\\win\\evil.pdf", "evil.pdf"), ("a<b>|c.docx", "a_b_c.docx"), ("", "uploaded_file")],
)
def test_sanitize_filename_blocks_path_traversal(unsafe, expected):
    assert sanitize_filename(unsafe) == expected


def test_hash_identifies_content_not_name():
    assert compute_file_hash(b"same") == compute_file_hash(b"same")
    assert compute_file_hash(b"same") != compute_file_hash(b"different")
    a = load_document(b"Same content", "a.txt")
    b = load_document(b"Same content", "b.txt")
    assert a.file_hash == b.file_hash
