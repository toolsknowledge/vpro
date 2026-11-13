"""Real-API test. Skipped unless:  RUN_INTEGRATION=1 pytest -m integration  (needs OPENAI_API_KEY in .env)."""
import os

import pytest

from backend.embeddings import OpenAIEmbedder, get_client
from backend.indexer import index_file
from backend.rag_chain import RagChain
from backend.retrieval import Retriever
from config.settings import Settings

pytestmark = [pytest.mark.integration,
              pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="set RUN_INTEGRATION=1 to call the real API")]


def test_end_to_end_with_real_openai(tmp_path, registry, store):
    real = Settings.from_env()
    if not real.has_api_key:
        pytest.skip("OPENAI_API_KEY not configured")
    from backend.vector_store import VectorStore
    store = VectorStore(tmp_path / "chroma", "integration_test", real.embedding_model)
    emb = OpenAIEmbedder(get_client(real), real.embedding_model)
    s = Settings(openai_api_key=real.openai_api_key, data_dir=tmp_path / "data")
    r = index_file("fees.txt", b"Course fees:\nThe Python Full Stack course lasts 16 weeks and costs 30000.",
                   settings=s, registry=registry, store=store, embedder=emb, chunk_size=800, chunk_overlap=100)
    assert r.ok and r.dimension > 0
    res = Retriever(store, emb).retrieve("How long is the Python Full Stack course?", k=2)
    ans = RagChain(get_client(real), real.chat_model).answer("How long is the Python Full Stack course?", res)
    assert "16" in ans.text
