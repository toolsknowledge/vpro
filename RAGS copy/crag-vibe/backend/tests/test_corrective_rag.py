"""Corrective RAG workflow tests. OpenAI chat calls are replaced with scripted fakes."""

import pytest

from app.services import corrective_rag_service as crag
from app.services import pdf_service, relevance_service


@pytest.fixture
def indexed_pdf(sample_pdf):
    pdf_service.ingest_documents()
    return sample_pdf


def grade_all(grade: str):
    def fake_evaluate(question, documents):
        graded = [{**doc, "relevance": grade, "reason": f"Graded {grade}"} for doc in documents]
        return {"documents": graded, "sufficient": grade == "relevant", "summary": f"All chunks {grade}."}
    return fake_evaluate


def test_relevant_retrieval_answers_without_correction(indexed_pdf, monkeypatch):
    monkeypatch.setattr(crag, "evaluate_documents", grade_all("relevant"))
    monkeypatch.setattr(crag, "rewrite_query", lambda *args, **kwargs: pytest.fail("rewrite must not run"))
    monkeypatch.setattr(crag, "chat_text", lambda system, user: "A list is a mutable collection (Page 2).")

    result = crag.answer_question("What is a Python list?")

    assert result["retrieval_status"] == "relevant"
    assert result["corrective_retrieval_used"] is False
    assert result["correction_attempts"] == 0
    assert result["answer"] == "A list is a mutable collection (Page 2)."
    retrieved_ids = {doc["chunk_id"] for doc in result["retrieved_documents"]}
    assert result["sources"] and all(source["chunk_id"] in retrieved_ids for source in result["sources"])


def test_irrelevant_retrieval_triggers_query_correction(indexed_pdf, monkeypatch):
    # The student's wording finds nothing useful; the rewritten textbook query does.
    searched_queries = []
    real_retrieve = crag.retrieval_service.retrieve

    def tracking_retrieve(query, top_k=5):
        searched_queries.append(query)
        return real_retrieve(query, top_k)

    def evaluate(question, documents):
        grade = "relevant" if "except" in searched_queries[-1] else "irrelevant"
        return grade_all(grade)(question, documents)

    rewrite_calls = []

    def fake_rewrite(question, previous_queries, failure_reason, document_names):
        rewrite_calls.append((previous_queries, failure_reason, document_names))
        return {"query": "exception handling try except", "reason": "Used textbook terms."}

    monkeypatch.setattr(crag.retrieval_service, "retrieve", tracking_retrieve)
    monkeypatch.setattr(crag, "evaluate_documents", evaluate)
    monkeypatch.setattr(crag, "rewrite_query", fake_rewrite)
    monkeypatch.setattr(crag, "chat_text", lambda system, user: "Use try and except (Page 3).")

    result = crag.answer_question("how do I stop my code blowing up?")

    assert result["retrieval_status"] == "corrected"
    assert result["corrective_retrieval_used"] is True
    assert result["correction_attempts"] == 1
    assert [attempt["sufficient"] for attempt in result["attempts"]] == [False, True]
    assert result["attempts"][1]["query"] == "exception handling try except"
    assert rewrite_calls == [(["how do I stop my code blowing up?"], "All chunks irrelevant.", ["sample_guide.pdf"])]
    assert {doc["attempt"] for doc in result["retrieved_documents"]} == {0, 1}


def test_unanswerable_question_stops_after_two_corrections(indexed_pdf, monkeypatch):
    monkeypatch.setattr(crag, "evaluate_documents", grade_all("irrelevant"))
    queries = iter(["football world cup winner", "fifa champion 2022"])
    monkeypatch.setattr(crag, "rewrite_query", lambda *args, **kwargs: {"query": next(queries), "reason": "r"})
    monkeypatch.setattr(crag, "chat_text", lambda *args: pytest.fail("must not generate an unsupported answer"))

    result = crag.answer_question("Who won the FIFA World Cup in 2022?")

    assert result["retrieval_status"] == "insufficient"
    assert result["correction_attempts"] == 2
    assert result["answer"] == crag.INSUFFICIENT_ANSWER
    assert result["sources"] == []


def test_generator_refusal_returns_insufficient_answer(indexed_pdf, monkeypatch):
    monkeypatch.setattr(crag, "evaluate_documents", grade_all("relevant"))
    monkeypatch.setattr(crag, "chat_text", lambda *args: crag.INSUFFICIENT_MARKER)

    result = crag.answer_question("What is variable scope?")

    assert result["retrieval_status"] == "insufficient"
    assert result["answer"] == crag.INSUFFICIENT_ANSWER
    assert result["sources"] == []


def test_answer_prompt_contains_only_relevant_context(indexed_pdf, monkeypatch):
    def evaluate(question, documents):
        graded = [{**doc, "relevance": "relevant" if doc["page_number"] == 2 else "irrelevant", "reason": ""}
                  for doc in documents]
        return {"documents": graded, "sufficient": True, "summary": ""}

    prompts = []
    monkeypatch.setattr(crag, "evaluate_documents", evaluate)
    monkeypatch.setattr(crag, "chat_text", lambda system, user: prompts.append(user) or "Answer (Page 2)")

    result = crag.answer_question("What is a list?")

    assert "Page 2" in prompts[0] and "Page 1]" not in prompts[0] and "Page 3]" not in prompts[0]
    assert [source["page_number"] for source in result["sources"]] == [2]


def test_evaluator_grades_chunks_and_distrusts_ungraded_ones(monkeypatch):
    documents = [
        {"chunk_id": "a", "document_name": "d.pdf", "page_number": 1, "text": "lists", "similarity": 0.9},
        {"chunk_id": "b", "document_name": "d.pdf", "page_number": 2, "text": "loops", "similarity": 0.5},
    ]
    monkeypatch.setattr(relevance_service, "chat_json", lambda system, user: {
        "evaluations": [{"chunk": 1, "grade": "partially_relevant", "reason": "Related"}],
        "summary": "Only partly covered.",
    })

    result = relevance_service.evaluate_documents("What is a list?", documents)

    assert [doc["relevance"] for doc in result["documents"]] == ["partially_relevant", "irrelevant"]
    assert result["sufficient"] is False  # only partially relevant -> ambiguous -> correct the retrieval


def test_rewrite_query_never_repeats_a_previous_query(monkeypatch):
    monkeypatch.setattr(relevance_service, "chat_json", lambda system, user: {"query": "what is oops", "reason": ""})

    result = relevance_service.rewrite_query("what is oops", ["what is oops"], "nothing relevant", ["guide.pdf"])

    assert result["query"] != "what is oops"
