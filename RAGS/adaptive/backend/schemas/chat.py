from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator

MAX_QUESTION_LENGTH = 2000
SESSION_ID_PATTERN = r"^[A-Za-z0-9_-]{8,64}$"


class Route(str, Enum):
    DIRECT = "DIRECT"
    RETRIEVE = "RETRIEVE"
    CLARIFY = "CLARIFY"


class ClassifierOutput(BaseModel):
    """Validated output of the routing LLM. Only data — never executed."""

    route: Route
    reason: str = Field(min_length=1, max_length=300)
    clarifying_question: str | None = Field(default=None, max_length=300)
    search_query: str | None = Field(default=None, max_length=500)

    @field_validator("reason", "clarifying_question", "search_query", mode="before")
    @classmethod
    def _strip(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @model_validator(mode="after")
    def _clarify_needs_question(self) -> "ClassifierOutput":
        if self.route is Route.CLARIFY and not self.clarifying_question:
            raise ValueError("CLARIFY route requires a clarifying_question")
        return self


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=MAX_QUESTION_LENGTH)
    session_id: str | None = Field(
        default=None,
        pattern=SESSION_ID_PATTERN,
        description="Client-generated conversation id. History is kept server-side per session.",
    )

    @field_validator("question")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("question must not be blank")
        return value


class SourceSnippet(BaseModel):
    source: str
    chunk_id: str
    snippet: str
    relevance: float = Field(description="Cosine similarity between the question and this chunk (0..1).")
    chunk_index: int | None = None
    total_chunks: int | None = None
    page: int | None = None
    sheet: str | None = None
    row: int | None = None


class ChatResponse(BaseModel):
    answer: str
    route: Route
    reason: str
    session_id: str
    sources: list[SourceSnippet]
    retrieval_performed: bool
    retrieval_count: int = Field(description="Chunks returned by the vector search (before relevance filtering).")
    relevance_score: float | None = Field(
        description="Highest cosine similarity among retrieved chunks; null when no retrieval ran.",
    )
    relevance_threshold: float | None = Field(
        description="Minimum similarity a chunk needed to be used as context; null when no retrieval ran.",
    )
    grounded: bool = Field(description="True only when the answer was generated from retrieved document context.")
    classifier_fallback: bool = Field(
        description="True when the classifier output was invalid and the documented fallback route was used.",
    )
