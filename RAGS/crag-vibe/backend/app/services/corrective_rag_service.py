"""Corrective RAG workflow:

question -> retrieve top-k chunks -> grade them with the LLM
        -> if not sufficient: rewrite the query and retrieve again (max MAX_CORRECTION_ATTEMPTS times)
        -> answer ONLY from the relevant chunks, or say that the materials do not contain the answer.
"""

import logging

from app import config
from app.services import pdf_service, retrieval_service
from app.services.openai_service import chat_text
from app.services.relevance_service import evaluate_documents, rewrite_query

logger = logging.getLogger("crag.workflow")

INSUFFICIENT_MARKER = "INSUFFICIENT_CONTEXT"
INSUFFICIENT_ANSWER = (
    "I could not find sufficient information in the available learning materials to answer this question "
    "accurately. Please try rephrasing your question or consult your trainer."
)
GRADE_ORDER = {"relevant": 0, "partially_relevant": 1, "irrelevant": 2}
SNIPPET_LENGTH = 350

ANSWER_PROMPT = f"""You are the VPro Skills AI Learning Assistant, a friendly tutor for beginner students.
Answer the student's question using ONLY the information in the context taken from their learning materials.

Rules:
- Use simple English, short paragraphs and a friendly tone. Avoid unnecessary jargon.
- Explain the concept clearly; include a short example (such as Python code from the context) when it helps.
- Format with Markdown: **bold** for key terms, "- " bullet lists, and ```python code blocks.
- After facts you use, mention the page in brackets, for example (Page 4).
- Never add facts that are not in the context.
- If the student uses a different name for a concept that the context explains (for example "array" for a
  Python list), answer about that concept and say which term the learning materials use.
- If the context does not contain enough information to answer, reply with exactly: {INSUFFICIENT_MARKER}"""


def _count(documents: list[dict], grade: str) -> int:
    return sum(1 for doc in documents if doc["relevance"] == grade)


def _select_context(retrieved_documents: list[dict]) -> list[dict]:
    """Best unique relevant/partially relevant chunks from all attempts (relevant first)."""
    best_by_chunk: dict[str, dict] = {}
    for doc in retrieved_documents:
        if doc["relevance"] == "irrelevant":
            continue
        current = best_by_chunk.get(doc["chunk_id"])
        if current is None or GRADE_ORDER[doc["relevance"]] < GRADE_ORDER[current["relevance"]]:
            best_by_chunk[doc["chunk_id"]] = doc
    ranked = sorted(best_by_chunk.values(), key=lambda doc: (GRADE_ORDER[doc["relevance"]], -doc["similarity"]))
    return ranked[:config.MAX_CONTEXT_CHUNKS]


def generate_answer(question: str, context_documents: list[dict]) -> str:
    context = "\n\n".join(
        f"[Source: {doc['document_name']}, Page {doc['page_number']}]\n{doc['text']}" for doc in context_documents
    )
    return chat_text(ANSWER_PROMPT, f"Context:\n\n{context}\n\nStudent question: {question}")


def answer_question(question: str) -> dict:
    attempts: list[dict] = []
    retrieved_documents: list[dict] = []
    query, rewrite_reason = question, None

    for attempt_number in range(config.MAX_CORRECTION_ATTEMPTS + 1):
        if attempt_number > 0:
            rewrite = rewrite_query(
                question,
                previous_queries=[attempt["query"] for attempt in attempts],
                failure_reason=attempts[-1]["evaluation_summary"],
                document_names=[path.name for path in pdf_service.list_pdf_files()],
            )
            query, rewrite_reason = rewrite["query"], rewrite["reason"]

        evaluation = evaluate_documents(question, retrieval_service.retrieve(query))
        graded = [{**doc, "attempt": attempt_number, "query": query} for doc in evaluation["documents"]]
        retrieved_documents.extend(graded)
        attempts.append({
            "attempt_number": attempt_number,
            "query": query,
            "rewrite_reason": rewrite_reason,
            "relevant_count": _count(graded, "relevant"),
            "partially_relevant_count": _count(graded, "partially_relevant"),
            "irrelevant_count": _count(graded, "irrelevant"),
            "sufficient": evaluation["sufficient"],
            "evaluation_summary": evaluation["summary"],
        })
        logger.info("Attempt %d query=%r sufficient=%s", attempt_number, query, evaluation["sufficient"])
        if evaluation["sufficient"]:
            break

    correction_attempts = len(attempts) - 1
    context_documents = _select_context(retrieved_documents)
    answer = INSUFFICIENT_ANSWER
    retrieval_status = "insufficient"

    if attempts[-1]["sufficient"] and context_documents:
        generated = generate_answer(question, context_documents)
        if INSUFFICIENT_MARKER not in generated:
            answer = generated
            retrieval_status = "relevant" if correction_attempts == 0 else "corrected"

    sources = [] if retrieval_status == "insufficient" else [
        {
            "chunk_id": doc["chunk_id"],
            "document_name": doc["document_name"],
            "page_number": doc["page_number"],
            "relevance": doc["relevance"],
            "snippet": doc["text"][:SNIPPET_LENGTH] + ("…" if len(doc["text"]) > SNIPPET_LENGTH else ""),
        }
        for doc in context_documents
    ]

    return {
        "question": question,
        "answer": answer,
        "retrieval_status": retrieval_status,
        "corrective_retrieval_used": correction_attempts > 0,
        "correction_attempts": correction_attempts,
        "sources": sources,
        "retrieved_documents": retrieved_documents,
        "attempts": attempts,
    }
