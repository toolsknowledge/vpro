"""Application exceptions. Each carries the HTTP status and a client-safe message."""

from http import HTTPStatus


class AppError(Exception):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    code: str = "internal_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class InvalidDocumentError(AppError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    code = "invalid_document"


class UnsupportedFileTypeError(AppError):
    status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    code = "unsupported_file_type"


class FileTooLargeError(AppError):
    status_code = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
    code = "file_too_large"


class DuplicateDocumentError(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "duplicate_document"


class DocumentNotFoundError(AppError):
    status_code = HTTPStatus.NOT_FOUND
    code = "document_not_found"


class EmbeddingError(AppError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    code = "embedding_error"


class VectorStoreError(AppError):
    status_code = HTTPStatus.SERVICE_UNAVAILABLE
    code = "vector_store_error"


class LLMError(AppError):
    status_code = HTTPStatus.BAD_GATEWAY
    code = "llm_error"
