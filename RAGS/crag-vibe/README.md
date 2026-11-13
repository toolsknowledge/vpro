# VPro Skills – Corrective RAG Student Assistant

> **Learn Smarter with AI-Powered Knowledge Retrieval**

A working, educational **Corrective RAG** (Retrieval-Augmented Generation) application built for
[VPro Skills EduTech](https://www.vproskills.com/). Students ask questions about their Python learning
materials (PDF). The assistant retrieves matching passages, **checks whether they are actually relevant**,
**corrects the search** when they are not, and only then answers – with the source PDF and page numbers.
If the materials do not contain the answer, it says so instead of guessing.

---

## Table of contents

1. [Project overview](#1-project-overview)
2. [How Corrective RAG works](#2-how-corrective-rag-works)
3. [Architecture](#3-architecture)
4. [Technology stack](#4-technology-stack)
5. [Folder structure](#5-folder-structure)
6. [Prerequisites](#6-prerequisites)
7. [Installation](#7-installation)
8. [Environment configuration](#8-environment-configuration)
9. [Start the backend](#9-start-the-backend)
10. [Start the frontend](#10-start-the-frontend)
11. [PDF ingestion](#11-pdf-ingestion)
12. [API reference](#12-api-reference)
13. [Testing](#13-testing)
14. [Demo questions for class](#14-demo-questions-for-class)
15. [Common errors and solutions](#15-common-errors-and-solutions)

---

## 1. Project overview

| Feature | Description |
|---|---|
| Student chat | Ask questions in plain English; answers are simple, student-friendly and include examples. |
| PDF knowledge base | A 11-page *Python Programming – Student Learning Guide* is generated with ReportLab and indexed automatically. |
| Relevance evaluation | The LLM grades every retrieved chunk as **Relevant**, **Partially Relevant** or **Irrelevant**. |
| Corrective retrieval | If no chunk is relevant, the question is rewritten and ChromaDB is searched again (max **2** corrections). |
| Safe answers | Answers use only retrieved text. Unanswerable questions get a polite "not enough information" message. |
| Sources | Every answer lists the PDF name, page number and the exact text snippet used. |
| Workflow visualisation | The "How Corrective RAG Works" panel shows all six stages, every retrieval attempt and every graded chunk. |
| Responsive UI | Desktop: chat + side panel. Mobile: chat with a collapsible workflow section. |

---

## 2. How Corrective RAG works

A normal ("naive") RAG system trusts whatever the vector database returns. **Corrective RAG does not.**

```
 Student question
        │
        ▼
 1. Question Received ── FastAPI validates the question (2–500 characters)
        │
        ▼
 2. Query Processing ─── OpenAI embeddings turn the question into a vector
        │
        ▼
 3. Initial Retrieval ── ChromaDB returns the top 5 most similar PDF chunks
        │
        ▼
 4. Relevance Evaluation ── LLM grades each chunk: relevant / partially relevant / irrelevant
        │
        ├── at least one chunk is RELEVANT  ("Correct") ─────────────────────┐
        │                                                                     │
        └── only partial or irrelevant chunks ("Ambiguous" / "Incorrect")     │
                 │                                                            │
                 ▼                                                            │
 5. Corrective Retrieval (max 2 times)                                        │
        • LLM explains what is missing and rewrites the query                 │
          (e.g. "OOPS" → "object-oriented programming classes objects")       │
        • ChromaDB is searched again and the new chunks are graded            │
        • stops as soon as a relevant chunk is found ────────────────────────┤
        • after 2 failed corrections → safe "not enough information" answer   │
                                                                              ▼
 6. Final Answer Generation ── LLM answers ONLY from relevant chunks, with page references.
                               If the chunks still do not contain the answer, it refuses.
```

The decision rule follows the original *Corrective Retrieval Augmented Generation* paper:
retrieval is **Correct** when at least one document is relevant, otherwise it is corrected.

There are **two safety checks** against made-up answers:

1. The **evaluator** must find a relevant chunk, otherwise the query is corrected or the question is refused.
2. The **answer generator** is instructed to reply `INSUFFICIENT_CONTEXT` if the chunks do not contain the
   answer; the backend then returns the friendly refusal instead.

---

## 3. Architecture

```
┌──────────────────────────────┐         HTTP (JSON)          ┌──────────────────────────────────────┐
│  React + Vite (port 5173)    │ ───────────────────────────▶ │  FastAPI + Uvicorn (port 8000)        │
│                              │ ◀─────────────────────────── │                                      │
│  Header · Welcome · Chat     │   /api/chat                  │  api/routes.py                       │
│  Sources · Workflow panel    │   /api/documents             │    │                                 │
│  axios (src/api.js)          │   /api/documents/ingest      │    ▼                                 │
└──────────────────────────────┘   /api/health                │  corrective_rag_service.py           │
                                                              │    ├─ retrieval_service.py ──▶ ChromaDB (backend/chroma_db)
         The OpenAI API key lives ONLY in backend/.env        │    ├─ relevance_service.py ──▶ OpenAI chat (grade + rewrite)
         and is never sent to the browser.                    │    └─ openai_service.py ─────▶ OpenAI embeddings + chat
                                                              │  pdf_service.py ──▶ knowledge_base/*.pdf
                                                              └──────────────────────────────────────┘
```

| Backend module | Responsibility |
|---|---|
| `app/main.py` | Creates the FastAPI app, CORS, error handlers, auto-indexes the PDF on first start. |
| `app/config.py` | Reads `backend/.env`; all tunable settings (chunk size, top-k, max corrections…). |
| `app/schemas.py` | Pydantic request/response models. |
| `app/errors.py` | `ServiceError` – a friendly message + HTTP status code. |
| `app/api/routes.py` | The four API endpoints. |
| `app/services/openai_service.py` | Every OpenAI call, with friendly handling of key/rate-limit/timeout/network/model errors. |
| `app/services/pdf_service.py` | Read PDF → clean text → split into chunks → index; list documents. |
| `app/services/retrieval_service.py` | ChromaDB: store chunk vectors, similarity search. |
| `app/services/relevance_service.py` | LLM relevance grader and LLM query rewriter. |
| `app/services/corrective_rag_service.py` | The full Corrective RAG loop and the final answer. |

---

## 4. Technology stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite 6, JavaScript, HTML5, CSS3 (CSS variables, no UI library), Axios |
| Backend | Python 3.10+, FastAPI, Uvicorn, Pydantic, python-dotenv |
| AI | OpenAI chat model (`gpt-4o-mini`) and embeddings (`text-embedding-3-small`) |
| Vector database | ChromaDB (persistent, cosine similarity) |
| PDF | pypdf (reading), ReportLab (generating the sample guide) |
| Tests | pytest + FastAPI TestClient (backend), Vitest + Testing Library (frontend) |

---

## 5. Folder structure

```
crag-vibe/
├── README.md
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI app, CORS, error handlers, auto-ingestion
│   │   ├── config.py                   # settings from .env
│   │   ├── errors.py                   # ServiceError
│   │   ├── schemas.py                  # Pydantic models
│   │   ├── api/routes.py               # /api endpoints
│   │   └── services/
│   │       ├── openai_service.py       # OpenAI embeddings + chat
│   │       ├── pdf_service.py          # PDF extraction, cleaning, chunking, ingestion
│   │       ├── retrieval_service.py    # ChromaDB storage + search
│   │       ├── relevance_service.py    # relevance grading + query rewriting
│   │       └── corrective_rag_service.py
│   ├── knowledge_base/
│   │   └── python_learning_guide.pdf   # generated sample PDF (11 pages)
│   ├── scripts/generate_sample_pdf.py  # re-creates the sample PDF with ReportLab
│   ├── chroma_db/                      # vector database (created automatically)
│   ├── tests/                          # pytest suite (no paid API calls)
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                            # your secrets – never commit
└── frontend/
    ├── public/logo.jpeg                # VPro Skills logo
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx                     # page layout and chat state
    │   ├── api.js                      # axios calls + friendly error messages
    │   ├── workflow.js                 # builds the 6 Corrective RAG stages from a response
    │   ├── index.css                   # complete theme and responsive styles
    │   ├── components/                 # Header, WelcomeScreen, ChatMessage, ChatInput,
    │   │                               # WorkflowPanel, FormattedText, Icons
    │   └── test/                       # Vitest tests
    ├── index.html
    ├── vite.config.js
    ├── package.json
    ├── .env.example
    └── .env
```

---

## 6. Prerequisites

| Tool | Version | Check |
|---|---|---|
| Python | 3.10 or newer (tested with 3.12) | `python --version` (Windows) / `python3 --version` (macOS) |
| Node.js | 18 or newer (tested with 22) | `node --version` |
| npm | 9 or newer | `npm --version` |
| OpenAI API key | with access to `gpt-4o-mini` and `text-embedding-3-small` | <https://platform.openai.com/api-keys> |

---

## 7. Installation

### Backend

**Windows (Command Prompt / PowerShell)**

```bat
cd crag-vibe\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux**

```bash
cd crag-vibe/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend (Windows and macOS)

```bash
cd crag-vibe/frontend
npm install
```

---

## 8. Environment configuration

### Backend – `backend/.env`

Copy the example file and add your key:

```bash
# macOS
cp .env.example .env
# Windows
copy .env.example .env
```

```ini
OPENAI_API_KEY=sk-...your key...
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Frontend addresses allowed to call the API (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

The API key is only read by the backend. It is never logged and never sent to the browser.

### Frontend – `frontend/.env`

```ini
VITE_API_BASE_URL=http://localhost:8000/api
```

Change this if the backend runs on a different port (see [Common errors](#15-common-errors-and-solutions)).
Restart `npm run dev` after editing `.env`.

---

## 9. Start the backend

**Windows**

```bat
cd crag-vibe\backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**macOS**

```bash
cd crag-vibe/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

* API: <http://localhost:8000/api/health>
* Interactive API docs (Swagger): <http://localhost:8000/docs>

On the **first start** the backend automatically indexes every PDF in `backend/knowledge_base/` into ChromaDB
(you will see `Indexed python_learning_guide.pdf: 25 chunks` in the terminal).

---

## 10. Start the frontend

Open a **second terminal** (keep the backend running):

```bash
cd crag-vibe/frontend
npm run dev
```

Open <http://localhost:5173>. The header shows **Backend connected** when the API is reachable.

---

## 11. PDF ingestion

### Pipeline

1. Read every `*.pdf` file in `backend/knowledge_base/` (max 20 MB, password-protected or broken PDFs are reported).
2. Extract text page by page with pypdf.
3. Clean the text: remove running headers/footers and page numbers, normalise whitespace.
4. Split each page into chunks of ~**800** characters with ~**150** characters overlap
   (chunks end at a line or sentence boundary, so words are never cut).
5. Create an embedding for every chunk with OpenAI.
6. Store chunk text, embedding and metadata in the ChromaDB collection **`vpro_corrective_rag`**.

Metadata saved with each chunk: `document_name`, `page_number`, `chunk_id`, `source`, `file_hash`.

### No duplicates

* Chunk ids are deterministic (`python_learning_guide-p6-c0`) and stored with `upsert`.
* The SHA-256 hash of each PDF is stored. Unchanged PDFs are skipped; a changed PDF is re-indexed (old chunks removed first).
* If you change `OPENAI_EMBEDDING_MODEL`, the collection is rebuilt automatically on the next ingestion.

### Add your own PDF

1. Copy the PDF into `backend/knowledge_base/`.
2. Run ingestion:
   ```bash
   # macOS / Linux
   curl -X POST http://localhost:8000/api/documents/ingest
   # Windows PowerShell
   Invoke-RestMethod -Method Post http://localhost:8000/api/documents/ingest
   ```
   or use **POST /api/documents/ingest → Try it out** at <http://localhost:8000/docs>.

### Re-create the sample PDF

```bash
cd backend
python scripts/generate_sample_pdf.py      # Windows (venv active)
python3 scripts/generate_sample_pdf.py     # macOS (or "python" inside the venv)
```

### Rebuild the vector database from scratch

Stop the backend, delete the `backend/chroma_db/` folder, start the backend again – it re-indexes automatically.

---

## 12. API reference

All endpoints are under `/api`. Errors always return `{"detail": "<friendly message>"}`.

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Backend status, whether OpenAI is configured, model names, number of indexed chunks. |
| POST | `/api/chat` | Ask a question; runs the full Corrective RAG workflow. |
| GET | `/api/documents` | PDFs in the knowledge base with page count and indexed chunk count. |
| POST | `/api/documents/ingest` | Index new or changed PDFs. |

### `POST /api/chat`

Request:

```json
{ "question": "What is the difference between List and Tuple?" }
```

Response (shortened):

```json
{
  "question": "What is the difference between List and Tuple?",
  "answer": "A **list** is mutable ... (Page 6)",
  "retrieval_status": "relevant",
  "corrective_retrieval_used": false,
  "correction_attempts": 0,
  "sources": [
    { "chunk_id": "python_learning_guide-p6-c1", "document_name": "python_learning_guide.pdf",
      "page_number": 6, "relevance": "relevant", "snippet": "Difference between List and Tuple ..." }
  ],
  "retrieved_documents": [
    { "chunk_id": "...", "document_name": "...", "page_number": 6, "text": "...", "similarity": 0.62,
      "relevance": "relevant", "reason": "Directly lists the differences.", "attempt": 0, "query": "..." }
  ],
  "attempts": [
    { "attempt_number": 0, "query": "...", "rewrite_reason": null, "relevant_count": 1,
      "partially_relevant_count": 3, "irrelevant_count": 1, "sufficient": true,
      "evaluation_summary": "..." }
  ]
}
```

| Field | Meaning |
|---|---|
| `retrieval_status` | `relevant` (first retrieval was good), `corrected` (good after correction), `insufficient` (refused). |
| `attempts` | One entry per retrieval: `0` = initial, `1`–`2` = corrections, with the query used and grade counts. |
| `retrieved_documents` | Every chunk retrieved in every attempt with its similarity score, grade and reason. |
| `sources` | The chunks actually given to the LLM to write the answer (empty when refused). |

| Status code | When |
|---|---|
| 422 | Empty question, longer than 500 characters, or unknown fields. |
| 429 | OpenAI rate limit / quota reached. |
| 503 | API key missing or invalid, OpenAI unreachable, or the knowledge base is empty. |
| 504 | OpenAI timed out. |

---

## 13. Testing

### Backend (39 tests, no OpenAI calls, no real database touched)

```bash
cd backend
# activate the venv first (see above)
python -m pytest -v
```

The tests use a temporary ChromaDB folder, a small generated test PDF and a deterministic fake embedding,
and replace the OpenAI chat calls with scripted fakes. They cover: health check, PDF extraction, cleaning,
chunking, invalid/empty PDFs, ingestion and duplicate prevention, ChromaDB storage, relevant retrieval,
irrelevant retrieval, query correction, retry limits, final answer generation, refusal handling,
input validation, missing configuration and OpenAI error handling.

### Frontend (15 tests)

```bash
cd frontend
npm test
```

Covers: rendering (logo, welcome screen, sample questions), backend status, disabled send button,
question submission with Enter, loading state, answers with sources, sample-card submission,
corrected and insufficient workflows, network and backend error messages with retry, clearing the chat,
and safe rendering of answer text.

### Lint

```bash
cd frontend
npm run lint
```

---

## 14. Demo questions for class

Results come from a real LLM, so they can vary slightly between runs.

| Question | What students will usually see |
|---|---|
| What is the difference between List and Tuple? | **Relevant** – answered from the first retrieval, sources on page 6. |
| how do i keep stuff in pairs like name and value | **Relevant** – informal wording still finds *Dictionaries* (page 7). |
| What is a hashmap in Python? | **Relevant** – the answer explains it as a Python *dictionary*. |
| Who won the FIFA World Cup in 2022? | **Insufficient** – 2 corrections are tried (rewritten queries are shown), then a safe refusal. |
| How do I connect Python to a MySQL database? | **Insufficient** – the topic is not in the PDF, so nothing is invented. |
| explain PEP-style naming for vars | **Corrective retrieval is triggered** – the first search finds only partial matches, so the panel shows the rewritten queries (e.g. "PEP 8 variable naming conventions"). The guide never mentions PEP 8, so it ends in a safe refusal instead of an invented answer. |

Open **View workflow** under any answer to walk through the six stages, the retrieval attempts and every graded chunk.

---

## 15. Common errors and solutions

| Problem | Solution |
|---|---|
| Header shows **Backend offline** | Start the backend (`uvicorn app.main:app --reload`) and check `VITE_API_BASE_URL` in `frontend/.env` matches its port. Restart `npm run dev` after changing `.env`. |
| `[Errno 48] Address already in use` / port 8000 busy (e.g. Docker) | Run on another port: `uvicorn app.main:app --reload --port 8010` and set `VITE_API_BASE_URL=http://localhost:8010/api` in `frontend/.env`. |
| "The AI service is not configured yet…" | `OPENAI_API_KEY` is missing or still `your_openai_api_key` in `backend/.env`. Set it and restart the backend. |
| "The AI service rejected the API key…" | The key is invalid or revoked – create a new key on the OpenAI dashboard. |
| "The AI service is busy or the usage limit was reached…" | Rate limit or no remaining credit on the OpenAI account. Wait or add billing. |
| "The AI model configuration is invalid…" | Check `OPENAI_CHAT_MODEL` / `OPENAI_EMBEDDING_MODEL` spelling and that your account can use them. |
| "The knowledge base is empty…" | Indexing has not run (e.g. the key was missing at startup). Click **Index now** on the welcome screen or `POST /api/documents/ingest`. |
| "No PDF documents were found…" | Put at least one `.pdf` file in `backend/knowledge_base/` (or regenerate the sample PDF). |
| "The embedding model changed…" | You changed `OPENAI_EMBEDDING_MODEL`. Run ingestion again to rebuild the collection. |
| CORS error in the browser console | Add the frontend address (e.g. `http://localhost:5174`) to `CORS_ORIGINS` in `backend/.env` and restart the backend. |
| `venv\Scripts\activate` is blocked in PowerShell | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt. |
| `python3: command not found` on Windows | Use `python` instead of `python3` on Windows. |
| `pip install` fails building `chromadb` | Upgrade pip first: `python -m pip install --upgrade pip`, and use Python 3.10–3.12. |
| Answers changed after editing the PDF | Run ingestion again – changed PDFs are re-indexed automatically. |

---

© VPro Skills EduTech · <https://www.vproskills.com/>
