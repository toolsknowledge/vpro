from pydantic import BaseModel


class DocumentInfo(BaseModel):
    filename: str
    file_type: str
    supported: bool
    on_disk: bool
    size_bytes: int | None
    indexed: bool
    chunk_count: int


class DocumentListResponse(BaseModel):
    documents_directory: str
    total_files: int
    indexed_files: int
    total_chunks: int
    vector_store_ready: bool
    documents: list[DocumentInfo]
