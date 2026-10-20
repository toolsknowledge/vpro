"""Wire concrete components into the RAG pipeline from configuration."""

from app.core.config import Settings
from app.embeddings.sentence_transformer import SentenceTransformerEmbedder
from app.rag.pipeline import RAGPipeline
from app.services.llm import OpenAIChatClient
from app.vectorstores.factory import create_vector_store


def build_pipeline(settings: Settings) -> RAGPipeline:
    embedder = SentenceTransformerEmbedder(settings.embedding_model)
    store = create_vector_store(settings, embedder.dimension)
    llm = OpenAIChatClient(
        api_key=settings.openai_api_key.get_secret_value(),
        model=settings.openai_model,
        timeout_seconds=settings.openai_timeout_seconds,
    )
    return RAGPipeline(
        embedder=embedder,
        store=store,
        llm=llm,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        top_k=settings.top_k,
    )
