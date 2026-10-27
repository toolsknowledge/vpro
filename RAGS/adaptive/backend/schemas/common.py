from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    """Shape of every non-2xx JSON response."""

    error: ErrorDetail
