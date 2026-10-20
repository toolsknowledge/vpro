"""Select the vector store implementation from configuration."""

from app.core.config import Settings
from app.vectorstores.base import VectorStore


def create_vector_store(settings: Settings, dimension: int) -> VectorStore:
    """Build the store named by VECTOR_DB. Adapters are imported lazily so unused SDKs are never loaded."""
    match settings.vector_db:
        case "chromadb":
            from app.vectorstores.chroma_store import ChromaVectorStore

            return ChromaVectorStore(settings.chroma_persist_directory, settings.chroma_collection_name, dimension)
        case "faiss":
            from app.vectorstores.faiss_store import FaissVectorStore

            return FaissVectorStore(settings.faiss_index_path, settings.faiss_metadata_path, dimension)
        case "pinecone":
            from app.vectorstores.pinecone_store import PineconeVectorStore

            assert settings.pinecone_api_key and settings.pinecone_index_name  # guaranteed by Settings validation
            return PineconeVectorStore(
                api_key=settings.pinecone_api_key.get_secret_value(),
                index_name=settings.pinecone_index_name,
                namespace=settings.pinecone_namespace,
                dimension=dimension,
            )
    raise ValueError(f"Unsupported VECTOR_DB '{settings.vector_db}'.")
