from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class FileIssue(BaseModel):
    filename: str
    reason: str


class IndexingResult(BaseModel):
    mode: Literal["index", "reindex"]
    status: Literal["success", "partial", "failed", "no_documents"]
    message: str
    started_at: datetime
    finished_at: datetime
    duration_seconds: float
    discovered_files: int
    processed_files: int
    unchanged_files: int
    chunks_created: int
    chunks_removed: int
    removed_sources: list[str]
    skipped_files: list[FileIssue]
    errors: list[FileIssue]


class IndexingStatus(BaseModel):
    collection_name: str
    vector_store_ready: bool
    vector_store_error: str | None = None
    openai_configured: bool
    is_indexing: bool
    document_count: int
    chunk_count: int
    last_result: IndexingResult | None
