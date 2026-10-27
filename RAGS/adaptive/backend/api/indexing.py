from fastapi import APIRouter, Depends

from dependencies import get_indexing_service
from schemas.common import ErrorResponse
from schemas.indexing import IndexingResult, IndexingStatus
from services.indexing_service import IndexingService

router = APIRouter(prefix="/api/indexing", tags=["indexing"])


@router.get("/status", response_model=IndexingStatus)
def indexing_status(indexing: IndexingService = Depends(get_indexing_service)) -> IndexingStatus:
    return indexing.status()


@router.post("/index", response_model=IndexingResult, responses={409: {"model": ErrorResponse}})
def index_documents(indexing: IndexingService = Depends(get_indexing_service)) -> IndexingResult:
    """Incremental: embed new or modified files, skip unchanged ones."""
    return indexing.run("index")


@router.post("/reindex", response_model=IndexingResult, responses={409: {"model": ErrorResponse}})
def reindex_documents(indexing: IndexingService = Depends(get_indexing_service)) -> IndexingResult:
    """Full refresh: re-embed every file and remove chunks of deleted or unreadable files."""
    return indexing.run("reindex")
