from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.core.exceptions import DuplicateDocumentError, InvalidDocumentError, VectorStoreError
from app.rag.pipeline import NO_CONTEXT_ANSWER, RAGPipeline
from app.rag.prompts import SYSTEM_PROMPT
from app.vectorstores.faiss_store import FaissVectorStore
from tests.conftest import FAKE_DIMENSION, FakeChatModel, FakeEmbedder, make_docx

GUIDE = [
    "Refund policy: customers can request a refund within 14 days of purchase.",
    "Shipping: orders ship from the Berlin warehouse every weekday.",
]


@pytest.fixture
def store(tmp_path: Path) -> FaissVectorStore:
    return FaissVectorStore(tmp_path / "index.faiss", tmp_path / "metadata.pkl", FAKE_DIMENSION)


@pytest.fixture
def llm() -> FakeChatModel:
    return FakeChatModel("Refunds are available within 14 days [1].")


@pytest.fixture
def pipeline(store: FaissVectorStore, llm: FakeChatModel) -> RAGPipeline:
    return RAGPipeline(FakeEmbedder(), store, llm, chunk_size=80, chunk_overlap=10, top_k=1)


def test_index_document_stores_chunks_with_metadata(pipeline: RAGPipeline) -> None:
    document = pipeline.index_document("guide.docx", make_docx(GUIDE, title="Store Guide"))

    assert document.filename == "guide.docx"
    assert document.chunk_count == 2
    assert document.title == "Store Guide"
    assert pipeline.list_documents() == [document]


def test_answer_retrieves_context_and_calls_llm(pipeline: RAGPipeline, llm: FakeChatModel) -> None:
    pipeline.index_document("guide.docx", make_docx(GUIDE))

    answer = pipeline.answer("How many days do I have to request a refund?")

    assert answer.text == "Refunds are available within 14 days [1]."
    assert [source.chunk.text for source in answer.sources] == [GUIDE[0]]
    system_prompt, user_prompt = llm.prompts[0]
    assert system_prompt == SYSTEM_PROMPT
    assert GUIDE[0] in user_prompt
    assert "How many days do I have to request a refund?" in user_prompt


def test_answer_without_indexed_documents_skips_llm(pipeline: RAGPipeline, llm: FakeChatModel) -> None:
    answer = pipeline.answer("Anything?")
    assert answer.text == NO_CONTEXT_ANSWER
    assert answer.sources == []
    assert llm.prompts == []


def test_duplicate_upload_is_rejected_before_embedding(pipeline: RAGPipeline) -> None:
    data = make_docx(GUIDE)
    pipeline.index_document("guide.docx", data)
    with pytest.raises(DuplicateDocumentError):
        pipeline.index_document("renamed.docx", data)
    assert len(pipeline.list_documents()) == 1


def test_invalid_document_is_not_indexed(pipeline: RAGPipeline) -> None:
    with pytest.raises(InvalidDocumentError):
        pipeline.index_document("broken.docx", b"not a docx")
    assert pipeline.list_documents() == []


def test_failed_store_write_cleans_up_partial_chunks(llm: FakeChatModel) -> None:
    store = MagicMock()
    store.document_exists.return_value = False
    store.add.side_effect = VectorStoreError("write failed")
    pipeline = RAGPipeline(FakeEmbedder(), store, llm, chunk_size=80, chunk_overlap=10, top_k=1)

    with pytest.raises(VectorStoreError):
        pipeline.index_document("guide.docx", make_docx(GUIDE))

    store.delete_document.assert_called_once()


def test_delete_document_keeps_other_documents(pipeline: RAGPipeline) -> None:
    first = pipeline.index_document("guide.docx", make_docx(GUIDE))
    second = pipeline.index_document("other.docx", make_docx(["Office hours are 9 to 5."]))

    pipeline.delete_document(first.document_id)

    assert [document.document_id for document in pipeline.list_documents()] == [second.document_id]


def test_system_prompt_treats_context_as_untrusted() -> None:
    assert "untrusted" in SYSTEM_PROMPT
    assert "does not contain enough information" in SYSTEM_PROMPT
