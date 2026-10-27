import pytest

from services.document_loader import (
    EmptyDocumentError,
    UnsupportedFileTypeError,
    load_document,
)
from services.document_processor import build_chunks, chunk_text, content_fingerprint


@pytest.mark.parametrize(
    ("filename", "file_type", "expected_text"),
    [
        ("rag_fundamentals.txt", "txt", "Retrieval-Augmented Generation"),
        ("adaptive_rag_guide.md", "md", "CLARIFY"),
        ("hybrid_vs_advanced_rag.docx", "docx", "Reciprocal Rank Fusion"),
        ("rag_course_faq.pdf", "pdf", "What is ChromaDB?"),
        ("rag_concepts.xlsx", "xlsx", "Concept: Reranking"),
    ],
)
def test_sample_documents_load(sample_docs, filename, file_type, expected_text):
    document = load_document(sample_docs / filename)
    assert document.source == filename
    assert document.file_type == file_type
    assert expected_text in document.full_text


def test_pdf_and_xlsx_keep_location_metadata(sample_docs):
    pdf = load_document(sample_docs / "rag_course_faq.pdf")
    assert [section.metadata["page"] for section in pdf.sections] == list(range(1, len(pdf.sections) + 1))
    xlsx = load_document(sample_docs / "rag_concepts.xlsx")
    assert len(xlsx.sections) >= 12
    assert xlsx.sections[0].metadata == {"sheet": "Concepts", "row": 2}
    assert "Definition:" in xlsx.sections[0].text and "Example:" in xlsx.sections[0].text


def test_unsupported_extension_is_rejected(tmp_path):
    path = tmp_path / "slides.pptx"
    path.write_bytes(b"not really a pptx")
    with pytest.raises(UnsupportedFileTypeError):
        load_document(path)


@pytest.mark.parametrize("content", ["", "   \n\n  \t"])
def test_empty_document_is_rejected(tmp_path, content):
    path = tmp_path / "empty.txt"
    path.write_text(content)
    with pytest.raises(EmptyDocumentError):
        load_document(path)


def test_chunking_respects_size_and_overlap():
    text = " ".join(f"Sentence number {i} talks about retrieval." for i in range(200))
    chunks = chunk_text(text, chunk_size=300, chunk_overlap=50)
    assert len(chunks) > 1
    assert all(len(chunk) <= 300 for chunk in chunks)
    assert chunks[0][-30:].split()[-1] in chunks[1]  # overlap carries text forward
    joined = " ".join(chunks)
    assert "Sentence number 199" in joined


def test_chunking_rejects_bad_overlap():
    with pytest.raises(ValueError):
        chunk_text("text", chunk_size=100, chunk_overlap=100)


def test_chunk_ids_are_stable_and_unique(sample_docs):
    document = load_document(sample_docs / "rag_fundamentals.txt")
    fingerprint = content_fingerprint(document, 400, 60, "model")
    first = build_chunks(document, 400, 60, fingerprint)
    second = build_chunks(document, 400, 60, fingerprint)
    assert [c.chunk_id for c in first] == [c.chunk_id for c in second]
    assert len({c.chunk_id for c in first}) == len(first)
    assert first[0].metadata["source"] == "rag_fundamentals.txt"
    assert first[-1].metadata["total_chunks"] == len(first)


def test_fingerprint_changes_with_chunking_or_model(sample_docs):
    document = load_document(sample_docs / "rag_fundamentals.txt")
    base = content_fingerprint(document, 400, 60, "model-a")
    assert base != content_fingerprint(document, 500, 60, "model-a")
    assert base != content_fingerprint(document, 400, 60, "model-b")


def test_document_listing_without_api_key(client, sample_docs, fake_openai):
    (sample_docs / "notes.pptx").write_bytes(b"x")
    body = client.get("/api/documents").json()
    files = {doc["filename"]: doc for doc in body["documents"]}
    assert body["total_files"] == 6
    assert body["indexed_files"] == 0
    assert files["rag_course_faq.pdf"]["supported"] is True
    assert files["rag_course_faq.pdf"]["indexed"] is False
    assert files["notes.pptx"]["supported"] is False
    assert fake_openai.embed_calls == []


def test_document_listing_shows_chunk_counts_after_indexing(client, sample_docs, indexing_service):
    result = indexing_service.run("index")
    body = client.get("/api/documents").json()
    assert body["indexed_files"] == 5
    assert body["total_chunks"] == result.chunks_created
    assert all(doc["chunk_count"] > 0 for doc in body["documents"])


def test_sample_questions_endpoint(client):
    body = client.get("/api/sample-questions").json()
    for route in ("DIRECT", "RETRIEVE", "CLARIFY"):
        assert body[route]
