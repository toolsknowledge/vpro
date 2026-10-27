"""Final answer generation for the DIRECT and RETRIEVE routes."""

from services.chroma_service import SearchHit
from services.openai_service import OpenAIService

NO_RELEVANT_CONTEXT_MESSAGE = (
    "I couldn't find information about this in the indexed documents, so I can't give a document-based answer. "
    "Try rephrasing the question, asking about a topic covered in the course materials, "
    "or asking it as a general question."
)
EMPTY_INDEX_MESSAGE = (
    "No documents are indexed yet, so I can't answer from the course materials. "
    "Open Indexing Controls and click “Index Documents”, then ask again."
)

DIRECT_PROMPT = """You are the VPRO Skills Adaptive RAG Assistant, a friendly tutor for an EduTech course on
Retrieval-Augmented Generation. Answer concisely and clearly from general knowledge.
You have NOT looked at any course documents for this answer, so never claim or imply that you did.
If the user needs course-specific details, suggest asking about the course documents."""

GROUNDED_PROMPT = """You are the VPRO Skills Adaptive RAG Assistant. Answer the user's question using ONLY the
numbered document excerpts below. Rules:
- Use only facts stated in the excerpts. Do not add outside knowledge.
- Cite the excerpts you used inline as [1], [2], etc.
- If the excerpts do not contain enough information to answer, say so plainly instead of guessing.
- Be concise and well structured; use short lists where helpful.

Document excerpts:
{context}"""


def format_context(hits: list[SearchHit]) -> str:
    blocks = []
    for number, hit in enumerate(hits, start=1):
        location = [f"source: {hit.metadata.get('source', 'unknown')}"]
        for key in ("page", "sheet", "row"):
            if key in hit.metadata:
                location.append(f"{key}: {hit.metadata[key]}")
        blocks.append(f"[{number}] ({', '.join(location)})\n{hit.text}")
    return "\n\n".join(blocks)


class AnswerService:
    def __init__(self, openai_service: OpenAIService, temperature: float) -> None:
        self._openai = openai_service
        self._temperature = temperature

    def answer_direct(self, question: str, history: list[dict[str, str]]) -> str:
        messages = [{"role": "system", "content": DIRECT_PROMPT}, *history, {"role": "user", "content": question}]
        return self._openai.chat(messages, temperature=self._temperature)

    def answer_from_context(self, question: str, history: list[dict[str, str]], hits: list[SearchHit]) -> str:
        messages = [
            {"role": "system", "content": GROUNDED_PROMPT.format(context=format_context(hits))},
            *history,
            {"role": "user", "content": question},
        ]
        return self._openai.chat(messages, temperature=self._temperature)
