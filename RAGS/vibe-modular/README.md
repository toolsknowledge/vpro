# RAGS — Vibe Modular

A modular Retrieval-Augmented Generation app. Upload DOCX documents, then ask questions that OpenAI answers from the retrieved document content, with source references.

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI |
| Frontend | Angular 21 |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`, 384 dimensions) |
| LLM | OpenAI Chat Completions |
| Vector database | ChromaDB, FAISS or Pinecone, selected by `VECTOR_DB` in `.env` |

```text
vibe-modular/
├── backend/
│   ├── README.md          Backend architecture and API reference
│   └── fastapi/           FastAPI application, tests, requirements.txt, .env.example
└── frontend/              Angular application
```

## Prerequisites

- Python 3.12
- Node.js 20.19+ (or 22.12+) and npm
- An OpenAI API key
- A Pinecone API key and index, only if you use Pinecone

## Run the backend

```bash
cd backend/fastapi
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then set OPENAI_API_KEY in .env
uvicorn app.main:create_app --factory --port 8000
```

Run the commands from `backend/fastapi`: `.env` and the relative `./data/...` paths are resolved from there.
The first start downloads the embedding model (about 90 MB) to the Hugging Face cache.
The API docs are at http://localhost:8000/docs.

## Run the frontend

```bash
cd frontend
npm install
npm start                     # http://localhost:4200
```

The backend URL is set in `frontend/src/environments/environment*.ts` (default `http://localhost:8000/api`).
If you serve the frontend from another origin, add that origin to `CORS_ORIGINS` in the backend `.env`.

## Switch vector databases

Change one line in `backend/fastapi/.env` and restart the backend:

```env
VECTOR_DB=chromadb   # persistent local store in CHROMA_PERSIST_DIRECTORY
VECTOR_DB=faiss      # local index + metadata files in FAISS_INDEX_PATH / FAISS_METADATA_PATH
VECTOR_DB=pinecone   # managed index; needs PINECONE_API_KEY and PINECONE_INDEX_NAME
```

No code changes are needed: a factory builds the selected adapter, and the RAG pipeline and Angular app only use the common interface.
Each database keeps its own data. Documents indexed in one are not visible after switching to another, so re-upload them.

### Pinecone setup

Create a **dense** index with **dimension 384** (matching `all-MiniLM-L6-v2`) and the **cosine** metric. Do this in the Pinecone console, or with:

```bash
python -c "
from pinecone import Pinecone, ServerlessSpec
Pinecone(api_key='YOUR_KEY').create_index(
    name='rag-documents', dimension=384, metric='cosine',
    spec=ServerlessSpec(cloud='aws', region='us-east-1'))"
```

Then set `PINECONE_API_KEY`, `PINECONE_INDEX_NAME` and optionally `PINECONE_NAMESPACE`.
At startup the backend checks that the index exists, that its dimension matches the embedding model, and that it uses cosine.
Pinecone is eventually consistent, so a document can take a few seconds to show up in the list after upload.

If you change `EMBEDDING_MODEL` to one with a different dimension, use a new Chroma collection, new FAISS paths or a new Pinecone index. The backend refuses to start if they don't match.

## Tests

```bash
cd backend/fastapi && source .venv/bin/activate && pytest   # 106 tests
cd frontend && npm test -- --watch=false                    # 15 tests
```

The backend tests use mocks for OpenAI and Pinecone, so they need no credentials and make no paid calls.
The embedding tests use the real Sentence Transformers model; it is downloaded on first run.
