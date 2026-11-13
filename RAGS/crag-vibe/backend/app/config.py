"""Application settings loaded from environment variables (backend/.env)."""

import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini").strip()
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small").strip()
OPENAI_TIMEOUT_SECONDS = 30

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if origin.strip()
]

# Knowledge base and vector database
KNOWLEDGE_BASE_DIR = BACKEND_DIR / "knowledge_base"
CHROMA_DB_DIR = BACKEND_DIR / "chroma_db"
CHROMA_COLLECTION_NAME = "vpro_corrective_rag"
MAX_PDF_SIZE_MB = 20

# RAG settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 5
MAX_CORRECTION_ATTEMPTS = 2
MAX_CONTEXT_CHUNKS = 6
MAX_QUESTION_LENGTH = 500

PLACEHOLDER_API_KEY = "your_openai_api_key"


def is_openai_configured() -> bool:
    """True when a real-looking OpenAI API key is present (never logs the key itself)."""
    return bool(OPENAI_API_KEY) and OPENAI_API_KEY != PLACEHOLDER_API_KEY
