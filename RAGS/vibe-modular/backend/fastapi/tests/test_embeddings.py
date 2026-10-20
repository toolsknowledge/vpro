"""Uses the real Sentence Transformers model (downloaded once to the Hugging Face cache)."""

import math

import pytest

from app.core.exceptions import EmbeddingError
from app.embeddings.sentence_transformer import SentenceTransformerEmbedder

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@pytest.fixture(scope="module")
def embedder() -> SentenceTransformerEmbedder:
    return SentenceTransformerEmbedder(MODEL_NAME)


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def test_reports_model_dimension(embedder: SentenceTransformerEmbedder) -> None:
    assert embedder.dimension == 384


def test_embeddings_are_normalized_and_sized(embedder: SentenceTransformerEmbedder) -> None:
    vectors = embedder.embed(["The cat sat on the mat.", "Quarterly revenue grew."])

    assert len(vectors) == 2
    for vector in vectors:
        assert len(vector) == embedder.dimension
        assert math.isclose(math.sqrt(sum(v * v for v in vector)), 1.0, rel_tol=1e-4)


def test_embeddings_are_consistent_between_indexing_and_queries(embedder: SentenceTransformerEmbedder) -> None:
    batch = embedder.embed(["Refund policy details", "Something else"])
    single = embedder.embed(["Refund policy details"])
    assert _cosine(batch[0], single[0]) == pytest.approx(1.0, abs=1e-4)


def test_related_texts_score_higher(embedder: SentenceTransformerEmbedder) -> None:
    query, related, unrelated = embedder.embed(
        ["How do I get my money back?", "Refunds are issued within 14 days.", "The office opens at 9am."]
    )
    assert _cosine(query, related) > _cosine(query, unrelated)


def test_empty_input_returns_empty_list(embedder: SentenceTransformerEmbedder) -> None:
    assert embedder.embed([]) == []


def test_encoding_failure_raises_embedding_error(embedder: SentenceTransformerEmbedder, monkeypatch) -> None:
    def broken_encode(*args, **kwargs):
        raise RuntimeError("device failure")

    monkeypatch.setattr(embedder._model, "encode", broken_encode)
    with pytest.raises(EmbeddingError):
        embedder.embed(["text"])


def test_unknown_model_raises_embedding_error() -> None:
    with pytest.raises(EmbeddingError, match="Could not load"):
        SentenceTransformerEmbedder("./definitely/not/a/model")
