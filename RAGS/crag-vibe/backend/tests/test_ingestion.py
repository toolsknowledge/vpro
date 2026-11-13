import pytest

from app.errors import ServiceError
from app.services import pdf_service, retrieval_service
from tests.conftest import write_pdf


def test_ingestion_stores_chunks_in_chromadb(sample_pdf):
    result = pdf_service.ingest_documents()

    assert result["results"][0]["status"] == "indexed"
    assert result["total_chunks"] == 3
    stored = retrieval_service.get_collection().get(include=["metadatas"])
    assert {meta["page_number"] for meta in stored["metadatas"]} == {1, 2, 3}
    assert all(meta["document_name"] == "sample_guide.pdf" for meta in stored["metadatas"])


def test_reingesting_does_not_duplicate_chunks(sample_pdf):
    pdf_service.ingest_documents()
    second = pdf_service.ingest_documents()

    assert second["results"][0]["status"] == "already_indexed"
    assert retrieval_service.count_chunks() == 3


def test_changed_pdf_is_reindexed(sample_pdf):
    pdf_service.ingest_documents()
    write_pdf(sample_pdf, ["Only one page about Python sets now."])

    result = pdf_service.ingest_documents()

    assert result["results"][0]["status"] == "indexed"
    assert retrieval_service.count_chunks() == 1


def test_list_documents_reports_index_status(sample_pdf):
    before = pdf_service.list_documents()
    pdf_service.ingest_documents()
    after = pdf_service.list_documents()

    assert before["documents"][0]["indexed"] is False
    assert after["documents"][0] == {
        "document_name": "sample_guide.pdf",
        "size_kb": after["documents"][0]["size_kb"],
        "page_count": 3,
        "indexed_chunks": 3,
        "indexed": True,
    }


def test_missing_pdf_raises_not_found():
    with pytest.raises(ServiceError) as error:
        pdf_service.ingest_documents()
    assert error.value.status_code == 404


def test_pdf_without_text_is_reported_as_failed(isolated_environment):
    write_pdf(isolated_environment / "blank.pdf", ["", ""], header="")

    result = pdf_service.ingest_documents()

    assert result["results"][0]["status"] == "failed"
    assert "readable text" in result["results"][0]["message"]


def test_retrieval_returns_the_most_relevant_page(sample_pdf):
    pdf_service.ingest_documents()

    results = retrieval_service.retrieve("exception error try except blocks", top_k=2)

    assert results[0]["page_number"] == 3
    assert results[0]["similarity"] > results[1]["similarity"]
    assert set(results[0]) == {"chunk_id", "document_name", "page_number", "text", "similarity"}


def test_retrieval_on_empty_collection_gives_friendly_error():
    with pytest.raises(ServiceError) as error:
        retrieval_service.retrieve("What is Python?")
    assert error.value.status_code == 503
    assert "knowledge base is empty" in error.value.message
