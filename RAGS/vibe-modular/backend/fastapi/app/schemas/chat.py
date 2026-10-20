from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

Question = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]


class ChatRequest(BaseModel):
    question: Question


class SourceReference(BaseModel):
    document_id: str
    filename: str
    chunk_index: int
    score: float = Field(description="Cosine similarity between the question and the chunk.")
    text: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
