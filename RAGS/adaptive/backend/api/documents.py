import json

from fastapi import APIRouter, Depends, HTTPException

from config import BACKEND_DIR
from dependencies import get_indexing_service
from schemas.documents import DocumentListResponse
from services.indexing_service import IndexingService

router = APIRouter(prefix="/api", tags=["documents"])

SAMPLE_QUESTIONS_FILE = BACKEND_DIR / "data" / "sample_questions.json"


@router.get("/documents", response_model=DocumentListResponse)
def list_documents(indexing: IndexingService = Depends(get_indexing_service)) -> DocumentListResponse:
    return indexing.list_documents()


@router.get("/sample-questions")
def sample_questions() -> dict:
    """Example questions grouped by the route they are designed to trigger."""
    if not SAMPLE_QUESTIONS_FILE.is_file():
        raise HTTPException(
            status_code=404,
            detail="Sample questions not found. Run: python backend/scripts/create_sample_files.py",
        )
    return json.loads(SAMPLE_QUESTIONS_FILE.read_text(encoding="utf-8"))
