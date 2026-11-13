import pytest

from app.errors import ServiceError
from app.services import pdf_service


def test_extract_pages_reads_every_page(sample_pdf):
    pages = pdf_service.extract_pages(sample_pdf)

    assert [page["page_number"] for page in pages] == [1, 2, 3]
    assert "variable is a name" in pages[0]["text"]


def test_clean_pages_removes_headers_and_page_numbers(sample_pdf):
    cleaned = pdf_service.clean_pages(pdf_service.extract_pages(sample_pdf))

    for page in cleaned:
        assert "VPro Skills Test Guide" not in page["text"]
        assert "Page " not in page["text"]
        assert "  " not in page["text"]
    assert "Python Lists" in cleaned[1]["text"]


def test_split_text_respects_size_and_overlap():
    text = " ".join(f"word{number}" for number in range(600))  # ~4,500 characters

    chunks = pdf_service.split_text(text, chunk_size=800, overlap=150)

    assert len(chunks) > 5
    assert all(len(chunk) <= 800 for chunk in chunks)
    assert chunks[0].split()[-1] in chunks[1]  # consecutive chunks overlap
    assert all(not chunk.startswith("ord") for chunk in chunks)  # no words cut in half


def test_split_text_keeps_short_text_as_one_chunk():
    assert pdf_service.split_text("Short page.") == ["Short page."]
    assert pdf_service.split_text("   ") == []


def test_build_chunks_adds_metadata(sample_pdf):
    chunks = pdf_service.build_chunks(sample_pdf, file_hash="abc")

    first = chunks[0]
    assert first["chunk_id"] == "sample_guide-p1-c0"
    assert first["metadata"] == {
        "document_name": "sample_guide.pdf",
        "page_number": 1,
        "chunk_id": "sample_guide-p1-c0",
        "source": "knowledge_base/sample_guide.pdf",
        "file_hash": "abc",
    }


def test_invalid_pdf_is_rejected(isolated_environment):
    broken = isolated_environment / "broken.pdf"
    broken.write_bytes(b"this is not a pdf")

    with pytest.raises(ServiceError) as error:
        pdf_service.extract_pages(broken)
    assert error.value.status_code == 422
