"""Adaptive RAG pipeline: route → (retrieve → relevance gate) → answer."""

import logging
import uuid

from schemas.chat import ChatResponse, Route, SourceSnippet
from services.adaptive_router import AdaptiveRouter
from services.answer_service import EMPTY_INDEX_MESSAGE, NO_RELEVANT_CONTEXT_MESSAGE, AnswerService
from services.chroma_service import ChromaService, SearchHit
from services.retrieval_service import RetrievalService
from services.session_store import SessionStore

logger = logging.getLogger(__name__)

_SNIPPET_CHARS = 600


def _to_snippet(hit: SearchHit) -> SourceSnippet:
    metadata = hit.metadata
    text = hit.text if len(hit.text) <= _SNIPPET_CHARS else hit.text[:_SNIPPET_CHARS].rstrip() + "…"
    return SourceSnippet(
        source=str(metadata.get("source", "unknown")),
        chunk_id=hit.chunk_id,
        snippet=text,
        relevance=hit.relevance,
        chunk_index=metadata.get("chunk_index"),
        total_chunks=metadata.get("total_chunks"),
        page=metadata.get("page"),
        sheet=metadata.get("sheet"),
        row=metadata.get("row"),
    )


class ChatService:
    def __init__(
        self,
        router: AdaptiveRouter,
        retrieval: RetrievalService,
        answers: AnswerService,
        sessions: SessionStore,
        chroma: ChromaService,
    ) -> None:
        self._router = router
        self._retrieval = retrieval
        self._answers = answers
        self._sessions = sessions
        self._chroma = chroma

    def clear_session(self, session_id: str) -> bool:
        return self._sessions.clear(session_id)

    def ask(self, question: str, session_id: str | None) -> ChatResponse:
        session_id = session_id or uuid.uuid4().hex
        history = self._sessions.get_history(session_id)
        sources = sorted(self._chroma.source_summaries())

        decision = self._router.classify(question, history, sources)
        logger.info("Route=%s fallback=%s", decision.route.value, decision.fallback)

        retrieval_performed = False
        retrieval_count = 0
        relevance_score: float | None = None
        relevance_threshold: float | None = None
        snippets: list[SourceSnippet] = []
        grounded = False

        if decision.route is Route.CLARIFY:
            answer = decision.clarifying_question or "Could you give me a bit more detail about what you mean?"
        elif decision.route is Route.DIRECT:
            answer = self._answers.answer_direct(question, history)
        else:
            result = self._retrieval.retrieve(decision.search_query or question)
            retrieval_performed = True
            retrieval_count = len(result.hits)
            relevance_score = result.top_score
            relevance_threshold = result.threshold
            if result.has_relevant_context:
                answer = self._answers.answer_from_context(question, history, result.relevant_hits)
                snippets = [_to_snippet(hit) for hit in result.relevant_hits]
                grounded = True
            elif not sources:
                answer = EMPTY_INDEX_MESSAGE
            else:
                answer = NO_RELEVANT_CONTEXT_MESSAGE
            logger.info(
                "Retrieved %d chunk(s), %d above threshold %.2f (top=%s)",
                retrieval_count,
                len(result.relevant_hits),
                result.threshold,
                relevance_score,
            )

        self._sessions.append_turn(session_id, question, answer)
        return ChatResponse(
            answer=answer,
            route=decision.route,
            reason=decision.reason,
            session_id=session_id,
            sources=snippets,
            retrieval_performed=retrieval_performed,
            retrieval_count=retrieval_count,
            relevance_score=relevance_score,
            relevance_threshold=relevance_threshold,
            grounded=grounded,
            classifier_fallback=decision.fallback,
        )
