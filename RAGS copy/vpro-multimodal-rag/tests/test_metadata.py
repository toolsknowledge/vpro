import pytest

from backend.chunker import chunk_sections
from backend.document_loader import compute_hash
from backend.errors import AppError, EmbeddingModelMismatchError, InvalidChunkSettingsError
from backend.indexer import delete_document, index_file, reindex_all
from backend.text_cleaner import clean_text
from config.settings import Settings


def run(name, data, settings, registry, store, embedder, **kw):
    return index_file(name, data, settings=settings, registry=registry, store=store, embedder=embedder,
                      chunk_size=kw.pop("chunk_size", 800), chunk_overlap=kw.pop("chunk_overlap", 100), **kw)


def test_clean_text_preserves_content():
    out = clean_text("  Fee:\t 30000 \r\n\r\n\r\n\r\nPython  (v3.12) rocks ")
    assert out == "Fee: 30000\n\nPython (v3.12) rocks"


def test_metadata_preserved_into_chroma(settings, registry, store, embedder, make_xlsx):
    data = make_xlsx({"Course Catalog": [["Course", "Fee"], ["Python", 100], ["Java", 200]]})
    r = run("c.xlsx", data, settings, registry, store, embedder)
    assert r.status == "indexed" and r.stored == r.chunks == store.count() >= 1
    rec = store.get_records()[0]
    md = rec["metadata"]
    assert md["source_file"] == "c.xlsx" and md["sheet_name"] == "Course Catalog" and md["row_start"] == 2
    assert md["document_id"] == compute_hash(data) and rec["id"] == md["chunk_id"]
    assert store.stored_dimension() == 64


def test_duplicate_detection_by_content_not_name(settings, registry, store, embedder):
    run("a.txt", b"Hello world, this is some content.", settings, registry, store, embedder)
    n = store.count()
    dup = run("renamed.txt", b"Hello world, this is some content.", settings, registry, store, embedder)
    assert dup.status == "skipped_duplicate" and store.count() == n and len(registry.all()) == 1
    forced = run("a.txt", b"Hello world, this is some content.", settings, registry, store, embedder, force=True)
    assert forced.status == "reindexed" and store.count() == n
    changed = run("a.txt", b"Hello world, this is NEW content.", settings, registry, store, embedder)
    assert changed.status == "indexed" and len(registry.all()) == 2 and "different version" in changed.message


def test_delete_only_target_document(settings, registry, store, embedder):
    a = run("a.txt", b"alpha alpha alpha", settings, registry, store, embedder)
    b = run("b.txt", b"beta beta beta", settings, registry, store, embedder)
    path = registry.get(a.document_id)["stored_path"]
    assert delete_document(a.document_id, registry=registry, store=store) == a.chunks
    assert store.count() == b.chunks and registry.get(a.document_id) is None
    assert registry.load_trace(a.document_id) is None
    from pathlib import Path
    assert not Path(path).exists() and registry.has(b.document_id)


def test_failed_file_is_not_registered(settings, registry, store, embedder, make_pdf):
    r = run("scan.pdf", make_pdf([None]), settings, registry, store, embedder)
    assert r.status == "failed" and "OCR" in r.message
    assert registry.all() == [] and store.count() == 0
    assert run("x.exe", b"abc", settings, registry, store, embedder).status == "failed"
    assert run("big.txt", b"a" * 50, Settings(openai_api_key="k", max_upload_mb=1, data_dir=settings.data_dir),
               registry, store, embedder).status == "indexed"


def test_embedding_failure_keeps_existing_records(settings, registry, store, embedder):
    ok = run("a.txt", b"alpha beta gamma", settings, registry, store, embedder)

    class Boom(type(embedder)):
        def embed_texts(self, *a, **k):
            raise AppError("API down")
    r = run("a.txt", b"alpha beta gamma", settings, registry, store, Boom(), force=True)
    assert r.status == "failed" and "API down" in r.message
    assert store.count() == ok.chunks and registry.has(ok.document_id)


def test_invalid_chunk_settings_reported(settings, registry, store, embedder):
    r = run("a.txt", b"hello there", settings, registry, store, embedder, chunk_size=10, chunk_overlap=10)
    assert r.status == "failed" and "overlap" in r.message.lower()


def test_model_mismatch_blocks_mixing(settings, registry, store, embedder):
    run("a.txt", b"hello there friend", settings, registry, store, embedder)
    from backend.vector_store import VectorStore
    other = VectorStore(settings.chroma_dir, "test_collection", "different-model")
    assert "different-model" in other.compatibility_problem()
    with pytest.raises(EmbeddingModelMismatchError):
        other.add_chunks(chunk_sections([__import__("backend.models", fromlist=["Section"]).Section(
            "x y", "f", "h" * 64, "txt", "t")]), [[0.1] * 64])


def test_reindex_all_replaces_collection(settings, registry, store, embedder):
    run("a.txt", b"alpha beta gamma delta", settings, registry, store, embedder)
    res = reindex_all(settings=settings, registry=registry, store=store, embedder=embedder, chunk_size=200, chunk_overlap=20)
    assert len(res) == 1 and store.count() == res[0].chunks
