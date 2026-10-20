# Backend

FastAPI service that indexes DOCX documents and answers questions with RAG. For setup, see the [project README](../README.md).

## Architecture

```text
app/
├── main.py                 App factory: settings, CORS, error handlers, routes; pipeline built at startup
├── api/                    Routes, dependency injection, centralized exception handlers
├── core/                   Settings (.env validation), exceptions, logging
├── schemas/                Pydantic request/response models
├── document_loaders/       DOCX text + metadata extraction (python-docx)
├── rag/                    Chunking, prompts, RAGPipeline
├── embeddings/             Sentence Transformers embedder (loaded once)
├── vectorstores/           VectorStore interface, Chroma/FAISS/Pinecone adapters, factory
├── services/               OpenAI client, component wiring
└── utils/                  File helpers (document IDs, extension check)
```

`RAGPipeline` depends only on the `VectorStore` interface in `vectorstores/base.py`.
`vectorstores/factory.py` is the only code that knows which adapter `VECTOR_DB` selects.

**Indexing:** DOCX → text (paragraphs and tables, in document order) → overlapping chunks (`CHUNK_SIZE`/`CHUNK_OVERLAP` characters, split on paragraph or word boundaries) → normalized embeddings → vector store.

**Answering:** question → embedding → top `TOP_K` chunks by cosine similarity → prompt → OpenAI → answer and sources.
If nothing is indexed, the API returns a fixed message without calling OpenAI.
The system prompt limits answers to the retrieved context, requires saying when the document lacks the information, and treats document text as untrusted data.

**Document identity:** the document ID is the first 16 hex characters of the file's SHA-256. Re-uploading the same file returns `409`, even under a different name. Chunk IDs are `{document_id}#{index}`.

**Persistence:**
- ChromaDB uses a persistent client.
- FAISS writes the index and a metadata pickle atomically after each change. It refuses to start if one of the files is missing, corrupt, or out of sync with the other.
- Pinecone stores chunk text and metadata with each vector.

## API

All errors use the shape `{"error": {"code": "...", "message": "..."}}`. Responses never include stack traces or secrets.

| Method | Path | Success | Errors |
|---|---|---|---|
| GET | `/api/health` | `200` `{status, vector_db}` | |
| POST | `/api/documents/upload` (multipart `file`) | `201` document | `409` duplicate, `413` too large, `415` not `.docx`, `422` empty/unreadable |
| GET | `/api/documents` | `200` `{documents: [...]}` | |
| DELETE | `/api/documents/{document_id}` | `204` | `404` not found |
| POST | `/api/chat` `{question}` | `200` `{answer, sources: [{document_id, filename, chunk_index, score, text}]}` | `422` invalid question, `502` OpenAI failure |

Vector database failures return `503`.

## Configuration

All settings are read from `fastapi/.env` (see `.env.example`). Invalid settings stop startup with a clear message:

- `OPENAI_API_KEY` is always required.
- `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` are required only when `VECTOR_DB=pinecone`.
- `CHUNK_OVERLAP` must be smaller than `CHUNK_SIZE`.

Two settings are not in the original list:

- `MAX_UPLOAD_SIZE_MB` (default 10)
- `CORS_ORIGINS` (comma-separated, default `http://localhost:4200`)

## macOS note

The faiss-cpu and torch wheels each bundle their own OpenMP runtime. If torch's initializes first, FAISS crashes on its first search.
`app/__init__.py` imports faiss first on macOS to prevent this. Keep that import in place.
