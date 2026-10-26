"""Metadata preservation, citation formatting and configuration validation."""

import pytest

from backend.chunker import chunk_sections
from backend.document_loader import load_document
from backend.retrieval import format_citation
from backend.text_cleaner import clean_sections
from config.settings import load_settings
from tests.conftest import make_docx_bytes, make_pdf_bytes

REQUIRED_KEYS = {"chunk_id", "document_id", "chunk_index", "source_file", "file_hash", "document_type", "token_count"}


def _chunks(data, name):
    result = load_document(data, name)
    return chunk_sections(clean_sections(result.sections), 800, 120)


def test_pdf_chunk_metadata(tmp_path):
    chunks = _chunks(make_pdf_bytes(["Alpha page.", "Beta page."]), "notes.pdf")
    meta = chunks[1].to_metadata("text-embedding-3-small")
    assert REQUIRED_KEYS <= meta.keys()
    assert meta["page_number"] == 2 and meta["source_file"] == "notes.pdf"
    assert meta["embedding_model"] == "text-embedding-3-small"
    assert "text" not in meta


def test_excel_chunk_metadata(course_xlsx):
    chunks = _chunks(course_xlsx, "catalog.xlsx")
    meta = chunks[0].to_metadata()
    assert meta["sheet_name"] == "Course Catalog" and meta["row_start"] == 2 and meta["row_end"] == 3
    assert "page_number" not in meta


def test_metadata_has_no_none_values_for_chroma():
    chunks = _chunks(b"Plain text without headings.", "a.txt")
    assert all(v is not None for v in chunks[0].to_metadata().values())


def test_document_id_is_derived_from_content_hash():
    a = _chunks(b"Same text", "one.txt")[0]
    b = _chunks(b"Same text", "two.txt")[0]
    assert a.document_id == b.document_id and a.chunk_id == b.chunk_id
    assert a.source_file == "one.txt" and b.source_file == "two.txt"


@pytest.mark.parametrize(
    "meta, expected",
    [
        ({"source_file": "notes.pdf", "page_number": 1}, "notes.pdf, page 1"),
        ({"source_file": "c.xlsx", "sheet_name": "Course Catalog", "row_start": 2, "row_end": 2}, "c.xlsx, sheet 'Course Catalog', row 2"),
        ({"source_file": "c.xlsx", "sheet_name": "S", "row_start": 2, "row_end": 6}, "c.xlsx, sheet 'S', rows 2–6"),
        ({"source_file": "p.docx", "section_title": "Project assessment"}, "p.docx, section 'Project assessment'"),
        ({"source_file": "o.txt"}, "o.txt"),
    ],
)
def test_format_citation_uses_only_available_metadata(meta, expected):
    assert format_citation(meta) == expected


def test_word_chunk_has_section_title():
    data = make_docx_bytes([("heading", "Project assessment"), ("para", "Mentors grade projects.")])
    assert _chunks(data, "p.docx")[0].section_title == "Project assessment"


# ---------------------------------------------------------------- settings
def _clear_env(monkeypatch):
    for name in ["OPENAI_API_KEY", "OPENAI_CHAT_MODEL", "OPENAI_EMBEDDING_MODEL", "CHUNK_SIZE", "CHUNK_OVERLAP", "TOP_K",
                 "MAX_UPLOAD_SIZE_MB", "CHROMA_PERSIST_DIRECTORY", "CHROMA_COLLECTION_NAME", "OPENAI_CHAT_TEMPERATURE"]:
        monkeypatch.delenv(name, raising=False)


def test_missing_api_key_is_reported(monkeypatch):
    _clear_env(monkeypatch)
    settings = load_settings(use_dotenv=False)
    assert not settings.has_api_key
    assert any("OPENAI_API_KEY" in p for p in settings.validate())


def test_placeholder_api_key_counts_as_missing(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "your_openai_api_key_here")
    assert not load_settings(use_dotenv=False).has_api_key


def test_defaults_and_secret_never_in_public_summary(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-SECRET123")
    settings = load_settings(use_dotenv=False)
    assert settings.validate() == []
    assert (settings.chunk_size, settings.chunk_overlap, settings.top_k) == (800, 120, 5)
    assert settings.embedding_model == "text-embedding-3-small"
    assert "SECRET123" not in str(settings.public_summary()) and "SECRET123" not in repr(settings)


def test_invalid_chunk_config_is_reported(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("CHUNK_SIZE", "100")
    monkeypatch.setenv("CHUNK_OVERLAP", "90")
    assert any("overlap" in p.lower() for p in load_settings(use_dotenv=False).validate())


def test_blank_temperature_means_model_default(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("OPENAI_CHAT_TEMPERATURE", "")
    assert load_settings(use_dotenv=False).chat_temperature is None
