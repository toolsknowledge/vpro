"""REST endpoints. Handlers only validate HTTP input and delegate to the RAG pipeline."""

from http import HTTPStatus
from pathlib import PurePath
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from app.api.dependencies import get_pipeline, get_settings
from app.core.config import Settings
from app.core.exceptions import FileTooLargeError, InvalidDocumentError, UnsupportedFileTypeError
from app.rag.pipeline import RAGPipeline
from app.schemas.chat import ChatRequest, ChatResponse, SourceReference
from app.schemas.common import ErrorResponse, HealthResponse
from app.schemas.documents import DocumentListResponse, DocumentResponse
from app.utils.files import has_extension

PipelineDep = Annotated[RAGPipeline, Depends(get_pipeline)]
SettingsDep = Annotated[Settings, Depends(get_settings)]

router = APIRouter(prefix="/api", responses={500: {"model": ErrorResponse}})


@router.get("/health", tags=["health"])
def health(settings: SettingsDep) -> HealthResponse:
    return HealthResponse(status="ok", vector_db=settings.vector_db)


@router.post(
    "/documents/upload",
    status_code=HTTPStatus.CREATED,
    tags=["documents"],
    responses={code: {"model": ErrorResponse} for code in (409, 413, 415, 422)},
)
def upload_document(file: UploadFile, pipeline: PipelineDep, settings: SettingsDep) -> DocumentResponse:
    filename = PurePath(file.filename or "").name
    if not has_extension(filename, ".docx"):
        raise UnsupportedFileTypeError("Only .docx files are supported.")

    data = file.file.read(settings.max_upload_size_bytes + 1)
    if len(data) > settings.max_upload_size_bytes:
        raise FileTooLargeError(f"The file exceeds the {settings.max_upload_size_mb} MB upload limit.")
    if not data:
        raise InvalidDocumentError("The uploaded file is empty.")

    document = pipeline.index_document(filename, data)
    return DocumentResponse.model_validate(document)


@router.get("/documents", tags=["documents"])
def list_documents(pipeline: PipelineDep) -> DocumentListResponse:
    documents = [DocumentResponse.model_validate(document) for document in pipeline.list_documents()]
    return DocumentListResponse(documents=documents)


@router.delete(
    "/documents/{document_id}",
    status_code=HTTPStatus.NO_CONTENT,
    tags=["documents"],
    responses={404: {"model": ErrorResponse}},
)
def delete_document(document_id: str, pipeline: PipelineDep) -> None:
    pipeline.delete_document(document_id)


@router.post("/chat", tags=["chat"], responses={422: {"model": ErrorResponse}, 502: {"model": ErrorResponse}})
def chat(request: ChatRequest, pipeline: PipelineDep) -> ChatResponse:
    answer = pipeline.answer(request.question)
    sources = [
        SourceReference(
            document_id=result.chunk.document.document_id,
            filename=result.chunk.document.filename,
            chunk_index=result.chunk.index,
            score=round(result.score, 4),
            text=result.chunk.text,
        )
        for result in answer.sources
    ]
    return ChatResponse(answer=answer.text, sources=sources)
