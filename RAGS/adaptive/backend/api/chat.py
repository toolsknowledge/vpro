from fastapi import APIRouter, Depends, Path, Response, status

from dependencies import get_chat_service
from schemas.chat import SESSION_ID_PATTERN, ChatRequest, ChatResponse
from schemas.common import ErrorResponse
from services.chat_service import ChatService

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    responses={422: {"model": ErrorResponse}, 429: {"model": ErrorResponse}, 502: {"model": ErrorResponse},
               503: {"model": ErrorResponse}},
)
def chat(request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    return chat_service.ask(request.question, request.session_id)


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def clear_session(
    session_id: str = Path(pattern=SESSION_ID_PATTERN),
    chat_service: ChatService = Depends(get_chat_service),
) -> Response:
    chat_service.clear_session(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
