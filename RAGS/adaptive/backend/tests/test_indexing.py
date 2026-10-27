import json

import pytest

from services.indexing_service import IndexingInProgressError, IndexingService
from services.openai_service import LLMServiceError


def test_index_all_sample_documents(indexing_service, sample_docs, chroma):
    result = indexing_service.run("index")
    assert result.status == "success"
    assert result.discovered_files == 5
    assert result.processed_files == 5
    assert result.errors == [] and result.skipped_files == []
    assert result.chunks_created == chroma.count() > 0
    assert set(chroma.source_summaries()) == {path.name for path in sample_docs.iterdir()}


def test_indexing_is_idempotent(indexing_service, sample_docs, chroma, fake_openai):
    first = indexing_service.run("index")
    count = chroma.count()
    fake_openai.embed_calls.clear()

    second = indexing_service.run("index")

    assert second.status == "success"
    assert second.processed_files == 0
    assert second.unchanged_files == 5
    assert second.chunks_created == 0
    assert chroma.count() == count == first.chunks_created
    assert fake_openai.embed_calls == []


def test_modified_file_replaces_its_chunks(indexing_service, docs_dir, chroma):
    path = docs_dir / "notes.txt"
    path.write_text("Original content about vector databases. " * 30)
    indexing_service.run("index")
    old_ids = set(chroma.source_summaries()["notes.txt"].chunk_ids)

    path.write_text("Completely new content about reranking models.")
    result = indexing_service.run("index")

    summary = chroma.source_summaries()["notes.txt"]
    assert result.processed_files == 1
    assert result.chunks_removed == len(old_ids)
    assert summary.chunk_count == 1
    assert not old_ids & set(summary.chunk_ids)
    assert chroma.count() == 1


def test_reindex_removes_deleted_files(indexing_service, sample_docs, chroma):
    indexing_service.run("index")
    (sample_docs / "rag_concepts.xlsx").unlink()

    incremental = indexing_service.run("index")
    assert "rag_concepts.xlsx" in chroma.source_summaries()  # incremental index never deletes
    assert incremental.removed_sources == []

    result = indexing_service.run("reindex")
    assert result.mode == "reindex"
    assert result.removed_sources == ["rag_concepts.xlsx"]
    assert result.processed_files == 4
    assert "rag_concepts.xlsx" not in chroma.source_summaries()
    assert chroma.count() == sum(s.chunk_count for s in chroma.source_summaries().values())


def test_reindex_without_changes_keeps_chunk_count(indexing_service, sample_docs, chroma):
    indexing_service.run("index")
    count = chroma.count()
    result = indexing_service.run("reindex")
    assert result.processed_files == 5
    assert chroma.count() == count


def test_empty_and_unsupported_files_are_skipped(indexing_service, docs_dir, chroma):
    (docs_dir / "good.md").write_text("# Title\nUseful content about embeddings.")
    (docs_dir / "empty.txt").write_text("")
    (docs_dir / "image.png").write_bytes(b"\x89PNG")

    result = indexing_service.run("index")

    assert result.status == "success"
    assert result.discovered_files == 3
    assert result.processed_files == 1
    assert {issue.filename for issue in result.skipped_files} == {"empty.txt", "image.png"}
    assert set(chroma.source_summaries()) == {"good.md"}


def test_emptied_file_loses_its_stale_chunks(indexing_service, docs_dir, chroma):
    path = docs_dir / "notes.txt"
    path.write_text("Some indexed content about chunking.")
    indexing_service.run("index")
    path.write_text("")
    result = indexing_service.run("index")
    assert result.removed_sources == ["notes.txt"]
    assert chroma.count() == 0


def test_corrupt_file_does_not_stop_other_files(indexing_service, docs_dir, chroma):
    (docs_dir / "broken.pdf").write_bytes(b"%PDF-1.4 this is not a valid pdf")
    (docs_dir / "good.txt").write_text("Valid text about hybrid retrieval.")

    result = indexing_service.run("index")

    assert result.status == "partial"
    assert [issue.filename for issue in result.errors] == ["broken.pdf"]
    assert result.processed_files == 1
    assert set(chroma.source_summaries()) == {"good.txt"}


def test_embedding_failure_keeps_existing_chunks(indexing_service, docs_dir, chroma, fake_openai):
    path = docs_dir / "notes.txt"
    path.write_text("First version about embeddings.")
    indexing_service.run("index")
    before = chroma.source_summaries()["notes.txt"].chunk_ids

    path.write_text("Second version about embeddings and ChromaDB.")
    fake_openai.embed_error = LLMServiceError("OpenAI unreachable.", code="openai_unreachable", status_code=503)
    result = indexing_service.run("index")

    assert result.status == "failed"
    assert result.errors[0].reason == "OpenAI unreachable."
    assert chroma.source_summaries()["notes.txt"].chunk_ids == before

    fake_openai.embed_error = None
    assert indexing_service.run("index").processed_files == 1  # retried because the hash never changed


def test_no_documents(indexing_service):
    result = indexing_service.run("index")
    assert result.status == "no_documents"
    assert result.discovered_files == 0


def test_concurrent_run_is_rejected(indexing_service):
    indexing_service._lock.acquire()
    try:
        with pytest.raises(IndexingInProgressError):
            indexing_service.run("index")
    finally:
        indexing_service._lock.release()


def test_last_result_is_persisted(indexing_service, sample_docs, settings, chroma, fake_openai):
    from services.embedding_service import EmbeddingService

    result = indexing_service.run("index")
    saved = json.loads(settings.indexing_state_file.read_text())
    assert saved["chunks_created"] == result.chunks_created

    restarted = IndexingService(settings, chroma, EmbeddingService(fake_openai, batch_size=8))
    assert restarted.status().last_result == result


def test_indexing_api_endpoints(client, sample_docs):
    status = client.get("/api/indexing/status").json()
    assert status["chunk_count"] == 0 and status["last_result"] is None

    indexed = client.post("/api/indexing/index")
    assert indexed.status_code == 200
    assert indexed.json()["status"] == "success"

    status = client.get("/api/indexing/status").json()
    assert status["document_count"] == 5
    assert status["chunk_count"] == indexed.json()["chunks_created"]
    assert status["last_result"]["mode"] == "index"

    reindexed = client.post("/api/indexing/reindex").json()
    assert reindexed["mode"] == "reindex"
    assert client.get("/api/indexing/status").json()["chunk_count"] == status["chunk_count"]


def test_indexing_api_reports_conflict(client, indexing_service):
    indexing_service._lock.acquire()
    try:
        response = client.post("/api/indexing/index")
    finally:
        indexing_service._lock.release()
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "indexing_in_progress"


def test_indexing_without_api_key_reports_failure(make_settings, docs_dir, chroma):
    from services.embedding_service import EmbeddingService
    from services.openai_service import OpenAIService

    settings = make_settings(openai_api_key=None)
    (docs_dir / "a.txt").write_text("content about RAG")
    service = IndexingService(settings, chroma, EmbeddingService(OpenAIService(settings), batch_size=8))

    result = service.run("index")

    assert result.status == "failed"
    assert "OPENAI_API_KEY" in result.errors[0].reason
    assert chroma.count() == 0
