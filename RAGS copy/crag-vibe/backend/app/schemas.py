"""Pydantic request/response models shared by the API routes."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app import config

RelevanceGrade = Literal["relevant", "partially_relevant", "irrelevant"]


class HealthResponse(BaseModel):
    status: str
    app_name: str
    openai_configured: bool
    chat_model: str
    embedding_model: str
    indexed_chunks: int | None = Field(description="Chunks in ChromaDB, or null if the database is unavailable")


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, max_length=config.MAX_QUESTION_LENGTH)

    @field_validator("question")
    @classmethod
    def question_must_have_text(cls, value: str) -> str:
        value = " ".join(value.split())
        if len(value) < 2:
            raise ValueError("Please type a question.")
        return value


class Source(BaseModel):
    chunk_id: str
    document_name: str
    page_number: int
    relevance: RelevanceGrade
    snippet: str


class RetrievedDocument(BaseModel):
    chunk_id: str
    document_name: str
    page_number: int
    text: str
    similarity: float
    relevance: RelevanceGrade
    reason: str
    attempt: int = Field(description="0 = initial retrieval, 1..n = corrective retrieval attempts")
    query: str


class RetrievalAttempt(BaseModel):
    attempt_number: int
    query: str
    rewrite_reason: str | None
    relevant_count: int
    partially_relevant_count: int
    irrelevant_count: int
    sufficient: bool
    evaluation_summary: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    retrieval_status: Literal["relevant", "corrected", "insufficient"]
    corrective_retrieval_used: bool
    correction_attempts: int
    sources: list[Source]
    retrieved_documents: list[RetrievedDocument]
    attempts: list[RetrievalAttempt]


class DocumentInfo(BaseModel):
    document_name: str
    size_kb: float
    page_count: int
    indexed_chunks: int
    indexed: bool


class DocumentListResponse(BaseModel):
    documents: list[DocumentInfo]
    total_chunks: int


class IngestResult(BaseModel):
    document_name: str
    status: Literal["indexed", "already_indexed", "failed"]
    chunks: int
    message: str


class IngestResponse(BaseModel):
    results: list[IngestResult]
    total_chunks: int
