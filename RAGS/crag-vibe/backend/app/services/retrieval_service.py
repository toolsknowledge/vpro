"""ChromaDB access: storing chunk embeddings and searching for similar chunks."""

import logging
from functools import lru_cache

import chromadb
from chromadb.config import Settings

from app import config
from app.errors import ServiceError
from app.services.openai_service import embed_texts

logger = logging.getLogger("crag.retrieval")


@lru_cache(maxsize=1)
def _get_client():
    try:
        config.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
        return chromadb.PersistentClient(
            path=str(config.CHROMA_DB_DIR), settings=Settings(anonymized_telemetry=False)
        )
    except Exception as error:
        logger.exception("Could not open ChromaDB at %s", config.CHROMA_DB_DIR)
        raise ServiceError("The knowledge database could not be opened. Please check the backend logs.", 503) from error


def get_collection():
    """Return the collection, creating it (cosine similarity) if it does not exist yet."""
    try:
        return _get_client().get_or_create_collection(
            name=config.CHROMA_COLLECTION_NAME,
            configuration={"hnsw": {"space": "cosine"}},
            metadata={"embedding_model": config.OPENAI_EMBEDDING_MODEL},
            embedding_function=None,  # we always supply OpenAI embeddings ourselves
        )
    except ServiceError:
        raise
    except Exception as error:
        logger.exception("Could not open ChromaDB collection")
        raise ServiceError("The knowledge database could not be opened. Please check the backend logs.", 503) from error


def reset_collection_if_model_changed() -> None:
    """Vectors from different embedding models cannot be compared, so rebuild when the model changes."""
    collection = get_collection()
    indexed_model = (collection.metadata or {}).get("embedding_model")
    if indexed_model != config.OPENAI_EMBEDDING_MODEL:
        logger.warning("Embedding model changed (%s -> %s); clearing collection", indexed_model,
                       config.OPENAI_EMBEDDING_MODEL)
        _get_client().delete_collection(config.CHROMA_COLLECTION_NAME)


def count_chunks(document_name: str | None = None) -> int:
    collection = get_collection()
    if document_name is None:
        return collection.count()
    return len(collection.get(where={"document_name": document_name}, include=[])["ids"])


def get_document_fingerprint(document_name: str) -> str | None:
    """File hash stored when the document was indexed, or None if it is not indexed."""
    result = get_collection().get(where={"document_name": document_name}, limit=1, include=["metadatas"])
    return result["metadatas"][0].get("file_hash") if result["ids"] else None


def delete_document(document_name: str) -> None:
    get_collection().delete(where={"document_name": document_name})


def store_chunks(chunks: list[dict]) -> None:
    """Embed and store chunks. upsert with deterministic ids means restarts never create duplicates."""
    embeddings = embed_texts([chunk["text"] for chunk in chunks])
    try:
        get_collection().upsert(
            ids=[chunk["chunk_id"] for chunk in chunks],
            documents=[chunk["text"] for chunk in chunks],
            metadatas=[chunk["metadata"] for chunk in chunks],
            embeddings=embeddings,
        )
    except Exception as error:
        logger.exception("Failed to store chunks in ChromaDB")
        raise ServiceError("Could not save the document in the knowledge database.", 500) from error


def retrieve(query: str, top_k: int = config.TOP_K) -> list[dict]:
    """Return the top_k most similar chunks with metadata and a 0–1 similarity score."""
    collection = get_collection()
    if collection.count() == 0:
        raise ServiceError(
            "The knowledge base is empty. Please index the learning materials first (POST /api/documents/ingest).",
            503,
        )
    if (collection.metadata or {}).get("embedding_model") != config.OPENAI_EMBEDDING_MODEL:
        raise ServiceError("The embedding model changed. Please re-index the learning materials.", 409)

    query_embedding = embed_texts([query])[0]
    try:
        result = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, collection.count()),
            include=["documents", "metadatas", "distances"],
        )
    except Exception as error:
        logger.exception("ChromaDB query failed")
        raise ServiceError("Searching the learning materials failed. Please try again.", 500) from error

    return [
        {
            "chunk_id": chunk_id,
            "document_name": metadata["document_name"],
            "page_number": metadata["page_number"],
            "text": text,
            "similarity": round(max(0.0, 1 - distance), 4),  # cosine distance -> similarity
        }
        for chunk_id, text, metadata, distance in zip(
            result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]
