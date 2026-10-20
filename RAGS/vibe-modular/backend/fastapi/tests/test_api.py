from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.exceptions import LLMError
from app.main import create_app
from app.rag.pipeline import RAGPipeline
from app.vectorstores.faiss_store import FaissVectorStore
from tests.conftest import FAKE_DIMENSION, FakeChatModel, FakeEmbedder, make_docx, make_settings

DOCX_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@pytest.fixture
def llm() -> FakeChatModel:
    return FakeChatModel("The warehouse is in Berlin.")


@pytest.fixture
def client(tmp_path: Path, llm: FakeChatModel) -> TestClient:
    settings = make_settings(vector_db="faiss", max_upload_size_mb=1)
    store = FaissVectorStore(tmp_path / "index.faiss", tmp_path / "metadata.pkl", FAKE_DIMENSION)
    pipeline = RAGPipeline(FakeEmbedder(), store, llm, chunk_size=200, chunk_overlap=20, top_k=2)
    with TestClient(create_app(settings, pipeline), raise_server_exceptions=False) as test_client:
        yield test_client


def _upload(client: TestClient, data: bytes, filename: str = "guide.docx"):
    return client.post("/api/documents/upload", files={"file": (filename, data, DOCX_TYPE)})


def test_health_reports_vector_db(client: TestClient) -> None:
    assert client.get("/api/health").json() == {"status": "ok", "vector_db": "faiss"}


def test_upload_indexes_document(client: TestClient) -> None:
    response = _upload(client, make_docx(["Orders ship from the Berlin warehouse."]))

    assert response.status_code == 201
    body = response.json()
    assert body["filename"] == "guide.docx"
    assert body["chunk_count"] == 1
    assert len(body["document_id"]) == 16


def test_upload_strips_client_path_from_filename(client: TestClient) -> None:
    response = _upload(client, make_docx(["Text"]), filename="../../etc/guide.docx")
    assert response.json()["filename"] == "guide.docx"


@pytest.mark.parametrize(
    ("filename", "data", "status", "code"),
    [
        ("notes.pdf", b"%PDF-1.7", 415, "unsupported_file_type"),
        ("notes", b"data", 415, "unsupported_file_type"),
        ("empty.docx", b"", 422, "invalid_document"),
        ("fake.docx", b"not really a docx", 422, "invalid_document"),
        ("huge.docx", b"x" * (1024 * 1024 + 1), 413, "file_too_large"),
    ],
)
def test_upload_validation(client: TestClient, filename: str, data: bytes, status: int, code: str) -> None:
    response = _upload(client, data, filename)
    assert response.status_code == status
    assert response.json()["error"]["code"] == code


def test_upload_without_file_is_rejected(client: TestClient) -> None:
    response = client.post("/api/documents/upload")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_duplicate_upload_returns_conflict(client: TestClient) -> None:
    data = make_docx(["Same content."])
    assert _upload(client, data).status_code == 201
    response = _upload(client, data, "copy.docx")
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "duplicate_document"


def test_list_and_delete_documents(client: TestClient) -> None:
    keep = _upload(client, make_docx(["Keep this document."]), "keep.docx").json()
    remove = _upload(client, make_docx(["Remove this document."]), "remove.docx").json()

    assert client.delete(f"/api/documents/{remove['document_id']}").status_code == 204

    documents = client.get("/api/documents").json()["documents"]
    assert [document["document_id"] for document in documents] == [keep["document_id"]]
    missing = client.delete(f"/api/documents/{remove['document_id']}")
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "document_not_found"


def test_chat_returns_answer_and_sources(client: TestClient) -> None:
    document = _upload(client, make_docx(["Orders ship from the Berlin warehouse."])).json()

    response = client.post("/api/chat", json={"question": "  Where do orders ship from?  "})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "The warehouse is in Berlin."
    source = body["sources"][0]
    assert source["document_id"] == document["document_id"]
    assert source["filename"] == "guide.docx"
    assert source["chunk_index"] == 0
    assert "Berlin" in source["text"]


def test_chat_without_documents_returns_no_context_message(client: TestClient, llm: FakeChatModel) -> None:
    response = client.post("/api/chat", json={"question": "Anything?"})
    assert response.status_code == 200
    assert response.json()["sources"] == []
    assert llm.prompts == []


@pytest.mark.parametrize("payload", [{}, {"question": ""}, {"question": "   "}, {"question": "x" * 2001}])
def test_chat_validation(client: TestClient, payload: dict) -> None:
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_llm_failure_returns_bad_gateway(client: TestClient, llm: FakeChatModel, monkeypatch) -> None:
    _upload(client, make_docx(["Some content."]))

    def failing_complete(system_prompt: str, user_prompt: str) -> str:
        raise LLMError("The language model request failed.")

    monkeypatch.setattr(llm, "complete", failing_complete)
    response = client.post("/api/chat", json={"question": "Some?"})
    assert response.status_code == 502
    assert response.json() == {"error": {"code": "llm_error", "message": "The language model request failed."}}


def test_unexpected_errors_do_not_leak_details(client: TestClient, llm: FakeChatModel, monkeypatch) -> None:
    _upload(client, make_docx(["Some content."]))

    def crashing_complete(system_prompt: str, user_prompt: str) -> str:
        raise RuntimeError("secret sk-live-123 in stack trace")

    monkeypatch.setattr(llm, "complete", crashing_complete)
    response = client.post("/api/chat", json={"question": "Some?"})
    assert response.status_code == 500
    assert "sk-live-123" not in response.text
    assert response.json()["error"]["code"] == "internal_error"


def test_cors_allows_angular_dev_server(client: TestClient) -> None:
    response = client.options(
        "/api/chat",
        headers={"Origin": "http://localhost:4200", "Access-Control-Request-Method": "POST"},
    )
    assert response.headers["access-control-allow-origin"] == "http://localhost:4200"
