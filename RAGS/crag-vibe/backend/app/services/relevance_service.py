"""The two LLM "judges" of Corrective RAG:

1. evaluate_documents – grades every retrieved chunk as relevant / partially_relevant / irrelevant.
   Following the Corrective RAG paper, retrieval is "correct" (sufficient) when at least one chunk is
   relevant. If chunks are only partially relevant ("ambiguous") or all irrelevant ("incorrect"),
   the workflow corrects the retrieval.
2. rewrite_query – when retrieval was not good enough, produces a better search query.
"""

from app.services.openai_service import chat_json

GRADES = ("relevant", "partially_relevant", "irrelevant")

EVALUATOR_PROMPT = """You are a strict relevance grader in a Corrective RAG system for students.
You judge whether text chunks retrieved from learning materials help answer a student's question.

Grades:
- relevant: the chunk directly answers the question or explains the asked concept.
- partially_relevant: the chunk is on a related topic and contains some useful facts, but not the full answer.
- irrelevant: the chunk does not help answer the question, even if it shares some keywords.

Judge ONLY what each chunk's text contains. Never use outside knowledge to fill gaps.
Judge meaning, not exact wording: a chunk that explains the asked concept under another name
(for example a Python "list" when the student says "array") can be relevant.

Return JSON in exactly this shape:
{"evaluations": [{"chunk": <chunk number>, "grade": "relevant" | "partially_relevant" | "irrelevant",
                  "reason": "<one short sentence>"}],
 "summary": "<one sentence: what the chunks cover and, if the main point is not covered, what is missing>"}"""

REWRITER_PROMPT = """You improve search queries for a vector database of educational PDF documents.
A previous search did not find enough relevant information for a student's question.

Rewrite the question into a better search query:
- expand abbreviations and informal words (e.g. "OOPS" -> "object-oriented programming classes objects"),
- if the student used a synonym or a term from another programming language, translate it into the term this
  subject's beginner textbook would use (e.g. in Python: "array" -> "list", "hashmap" -> "dictionary"),
- use precise technical terms that are likely to appear in a textbook on this subject,
- remove filler words, and keep the student's original meaning – never switch to a different topic,
- keep it short: a focused search phrase of at most 12 words, not a long sentence,
- make the new query clearly different from every previous query.

Return JSON: {"query": "<improved search query>", "reason": "<one sentence explaining what you changed and why>"}"""


def evaluate_documents(question: str, documents: list[dict]) -> dict:
    """Grade each retrieved chunk. Returns the chunks with "relevance" and "reason" added."""
    if not documents:
        return {"documents": [], "sufficient": False, "summary": "No chunks were retrieved for this query."}

    chunk_text = "\n\n".join(
        f"[Chunk {number}] ({doc['document_name']}, page {doc['page_number']})\n{doc['text']}"
        for number, doc in enumerate(documents, start=1)
    )
    result = chat_json(EVALUATOR_PROMPT, f"Student question: {question}\n\nRetrieved chunks:\n\n{chunk_text}")

    grades_by_chunk = {}
    for item in result.get("evaluations") or []:
        if isinstance(item, dict) and item.get("grade") in GRADES:
            grades_by_chunk[item.get("chunk")] = item

    graded = []
    for number, doc in enumerate(documents, start=1):
        evaluation = grades_by_chunk.get(number)
        graded.append({
            **doc,
            # A chunk the grader did not judge is treated as irrelevant – never trusted blindly.
            "relevance": evaluation["grade"] if evaluation else "irrelevant",
            "reason": str(evaluation.get("reason", "")) if evaluation else "The evaluator did not grade this chunk.",
        })

    return {
        "documents": graded,
        "sufficient": any(doc["relevance"] == "relevant" for doc in graded),
        "summary": str(result.get("summary") or "No summary provided by the evaluator."),
    }


def rewrite_query(question: str, previous_queries: list[str], failure_reason: str, document_names: list[str]) -> dict:
    user_prompt = (
        f"Student question: {question}\n"
        f"Available documents: {', '.join(document_names) or 'unknown'}\n"
        f"Previous queries: {previous_queries}\n"
        f"Why the previous retrieval failed: {failure_reason}"
    )
    result = chat_json(REWRITER_PROMPT, user_prompt)
    query = str(result.get("query") or "").strip()
    if not query or query in previous_queries:
        # Fall back to a deterministic variation so the retry still searches differently.
        query = f"{question} explanation definition example"
    return {"query": query, "reason": str(result.get("reason") or "Query reworded for a broader search.")}
