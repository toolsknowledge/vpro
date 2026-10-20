from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: str
    filename: str
    chunk_count: int
    uploaded_at: datetime
    title: str | None = None
    author: str | None = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
