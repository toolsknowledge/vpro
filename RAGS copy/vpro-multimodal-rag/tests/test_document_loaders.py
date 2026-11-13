import pytest

from backend.document_loader import extract_document, safe_filename, validate_upload
from backend.errors import (DocumentReadError, FileTooLargeError, NoExtractableTextError, UnsupportedFileError)


def test_pdf_pages_and_numbers(make_pdf):
    secs = extract_document("a.pdf", make_pdf(["First page text", "Second page text"]), "h")
    assert [s.page_number for s in secs] == [1, 2]
    assert "Second page" in secs[1].text and secs[0].document_type == "pdf"


def test_pdf_without_text_is_reported_not_faked(make_pdf):
    with pytest.raises(NoExtractableTextError, match="OCR"):
        extract_document("scan.pdf", make_pdf([None, None]), "h")


def test_corrupted_pdf():
    with pytest.raises(DocumentReadError):
        extract_document("bad.pdf", b"%PDF-1.4 garbage", "h")


def test_excel_rows_keep_headers_and_sheets(make_xlsx):
    data = make_xlsx({"Course Catalog": [["Course", "Duration", "Fee"], ["Python Full Stack", "16 weeks", 30000.0],
                                          [None, None, None], ["Java", None, 25000]],
                      "Batches": [["Course", "Seats"], ["Python Full Stack", 25]]})
    secs = extract_document("c.xlsx", data, "h")
    assert secs[0].text == "Course: Python Full Stack | Duration: 16 weeks | Fee: 30000"
    assert (secs[0].sheet_name, secs[0].row_number) == ("Course Catalog", 2)
    assert secs[1].text == "Course: Java | Fee: 25000" and secs[1].row_number == 4   # blank row skipped, missing value skipped
    assert {s.sheet_name for s in secs} == {"Course Catalog", "Batches"}


def test_excel_empty_sheet(make_xlsx):
    with pytest.raises(NoExtractableTextError):
        extract_document("e.xlsx", make_xlsx({"S": [["only header"]]}), "h")


def test_docx_headings_and_tables(make_docx):
    data = make_docx([("Heading 1", "Project assessment"), ("Normal", "Projects are graded."), ("Heading 1", "Refunds"),
                      ("Normal", "Within 7 days.")], table=[["Item", "Weight"], ["Project", "50%"]])
    secs = extract_document("p.docx", data, "h")
    assert [s.section_title for s in secs] == ["Project assessment", "Refunds"]
    assert "Item: Project | Weight: 50%" in secs[1].text


def test_docx_empty(make_docx):
    with pytest.raises(NoExtractableTextError):
        extract_document("e.docx", make_docx([]), "h")


def test_txt_sections_and_encoding():
    text = "Intro line.\n\nCourse modules:\nModule 1 and 2.\n"
    secs = extract_document("a.txt", text.encode(), "h")
    assert [s.section_title for s in secs] == [None, "Course modules"]
    assert secs[0].extraction_method == "text-utf-8"
    latin = extract_document("b.txt", "café ☕".encode("utf-8"), "h")
    assert "café" in latin[0].text


def test_txt_empty():
    with pytest.raises(NoExtractableTextError):
        extract_document("e.txt", b"  \n ", "h")


def test_validation():
    with pytest.raises(UnsupportedFileError):
        validate_upload("x.exe", b"abc", 100)
    with pytest.raises(FileTooLargeError):
        validate_upload("x.txt", b"a" * 200, 100)
    with pytest.raises(DocumentReadError):
        validate_upload("x.pdf", b"not a pdf", 100)
    assert validate_upload("ok.TXT", b"hi", 100) == ".txt"


def test_safe_filename_blocks_traversal():
    assert safe_filename("../../etc/passwd") == "passwd"
    assert safe_filename("..\\..\\evil.txt") == "evil.txt"
    assert "/" not in safe_filename("a/b/c<>.txt")
