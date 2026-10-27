"""LLM-based query router: DIRECT, RETRIEVE, or CLARIFY.

The classifier sees the question, a bounded slice of conversation history and
the names of the indexed documents, and must reply with JSON matching
``ClassifierOutput``. Its output is treated purely as data and validated.

Fallback policy (documented in the README): if the classifier reply is not
valid JSON or fails schema validation, the query is routed to RETRIEVE. That
route is protected by the retrieval relevance gate, so a misroute can at worst
produce an honest "the documents do not cover this" reply — never an
ungrounded answer presented as coming from the documents. Errors from the
OpenAI API itself are *not* masked; they propagate to the caller.
"""

import json
import logging
import re
from dataclasses import dataclass

from pydantic import ValidationError

from schemas.chat import ClassifierOutput, Route
from services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

FALLBACK_REASON = (
    "The router's output could not be validated, so the question was sent to document retrieval "
    "(protected by the relevance check)."
)

# Pure greetings are unambiguous; answering them directly avoids one LLM call.
# Everything else goes through the LLM classifier.
_GREETINGS = {
    "hi", "hello", "hey", "hiya", "good morning", "good afternoon", "good evening",
    "thanks", "thank you", "thank you so much", "thanks a lot", "bye", "goodbye",
}

_HISTORY_CHAR_LIMIT = 600

CLASSIFIER_PROMPT = """You are the routing component of an Adaptive RAG learning assistant for VPRO Skills EduTech.
Decide how the latest user message should be handled. Choose exactly one route:

DIRECT — greetings, small talk, thanks, questions about the assistant, or general-knowledge questions
that the user does NOT tie to the course documents and that can be answered well without them
(e.g. "Hi", "How are you?", "What is RAG in simple words?").

RETRIEVE — the user asks about the course notes, uploaded/indexed documents, "our" materials,
"according to the notes/documents", or asks for course-specific details the knowledge base is likely to contain.

CLARIFY — the message cannot be understood or answered without missing information: unresolved references
("it", "the second one", "these two") that the conversation history does NOT resolve, or a request too vague
to act on. If the history makes the reference clear, do NOT clarify; route the resolved question instead.

Indexed documents: {sources}

Respond with a single JSON object and nothing else:
{{"route": "DIRECT" | "RETRIEVE" | "CLARIFY",
  "reason": "<one short sentence explaining the choice>",
  "clarifying_question": "<concise follow-up question; required for CLARIFY, otherwise null>",
  "search_query": "<for RETRIEVE: a self-contained search query with references from history resolved; otherwise null>"}}"""


@dataclass(frozen=True)
class RouteDecision:
    route: Route
    reason: str
    clarifying_question: str | None = None
    search_query: str | None = None
    fallback: bool = False


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z ]", "", text.lower()).strip()


class AdaptiveRouter:
    def __init__(self, openai_service: OpenAIService, temperature: float) -> None:
        self._openai = openai_service
        self._temperature = temperature

    def classify(self, question: str, history: list[dict[str, str]], sources: list[str]) -> RouteDecision:
        if _normalise(question) in _GREETINGS:
            return RouteDecision(route=Route.DIRECT, reason="Simple greeting or courtesy; no documents needed.")

        messages = [
            {
                "role": "system",
                "content": CLASSIFIER_PROMPT.format(sources=", ".join(sources) if sources else "(none indexed yet)"),
            }
        ]
        for message in history:
            messages.append({"role": message["role"], "content": message["content"][:_HISTORY_CHAR_LIMIT]})
        messages.append({"role": "user", "content": question})

        raw = self._openai.chat(messages, temperature=self._temperature, json_mode=True, max_tokens=300)
        return self.parse(raw)

    @staticmethod
    def parse(raw: str) -> RouteDecision:
        """Validate raw classifier text, applying the documented fallback on bad output."""
        try:
            output = ClassifierOutput.model_validate(json.loads(raw))
        except (json.JSONDecodeError, ValidationError, TypeError) as exc:
            logger.warning("Invalid classifier output (%s); falling back to RETRIEVE", type(exc).__name__)
            return RouteDecision(route=Route.RETRIEVE, reason=FALLBACK_REASON, fallback=True)
        return RouteDecision(
            route=output.route,
            reason=output.reason,
            clarifying_question=output.clarifying_question if output.route is Route.CLARIFY else None,
            search_query=output.search_query if output.route is Route.RETRIEVE else None,
        )
