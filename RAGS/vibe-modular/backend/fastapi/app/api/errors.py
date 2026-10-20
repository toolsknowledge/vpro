"""Centralized exception handling. Responses never include stack traces or internal details."""

import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppError
from app.schemas.common import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    body = ErrorResponse(error=ErrorDetail(code=code, message=message))
    return JSONResponse(status_code=status_code, content=body.model_dump())


async def _handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    if exc.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        logger.error(
            "request_failed path=%s code=%s message=%r",
            request.url.path,
            exc.code,
            exc.message,
            exc_info=exc.__cause__,
        )
    else:
        logger.warning("request_rejected path=%s code=%s message=%r", request.url.path, exc.code, exc.message)
    return _error_response(exc.status_code, exc.code, exc.message)


async def _handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    messages = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"] if part != "body")
        messages.append(f"{location}: {error['msg']}" if location else error["msg"])
    return _error_response(HTTPStatus.UNPROCESSABLE_ENTITY, "validation_error", "; ".join(messages))


async def _handle_http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return _error_response(exc.status_code, "http_error", str(exc.detail))


async def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unexpected_error path=%s", request.url.path)
    return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "An unexpected error occurred.")


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _handle_app_error)
    app.add_exception_handler(RequestValidationError, _handle_validation_error)
    app.add_exception_handler(StarletteHTTPException, _handle_http_error)
    app.add_exception_handler(Exception, _handle_unexpected_error)
