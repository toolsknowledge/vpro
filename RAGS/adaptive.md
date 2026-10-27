# MASTER PROMPT: Build a Complete Adaptive RAG Application for VPRO Skills EduTech

## 1. Your Role

Act as a senior AI engineer, Python backend engineer, React developer, software architect, QA engineer, and UI/UX designer.

Build a complete, working, production-style educational Adaptive RAG application from scratch.

Do not merely explain the implementation or provide partial snippets. Create the actual project files, implement every required module, generate sample documents, install dependencies where possible, run the application checks, fix errors, and provide clear startup instructions.

Prioritize correctness, simplicity, maintainability, and reliable execution.

## 2. Project Location

Create the project at exactly:

`vpro/RAGS/adaptive/`

Use the current working directory as the parent directory. Inspect the current directory before creating files. Do not overwrite unrelated existing projects.

All backend, frontend, data, configuration, documentation, and test files must be inside the `adaptive` project directory.

## 3. Technology Stack

### Backend
- Python 3.11 or a compatible supported Python version
- FastAPI
- Uvicorn
- OpenAI Python SDK
- ChromaDB with persistent local storage
- OpenAI embeddings using `text-embedding-3-small`
- Pydantic and pydantic-settings
- python-dotenv
- PyPDF for PDF ingestion
- python-docx for DOCX ingestion
- openpyxl for XLSX ingestion
- pytest and FastAPI TestClient for testing

Use a consistent, compatible dependency set. Pin tested versions in `requirements.txt` and avoid unnecessary dependencies.

### Frontend
- React
- Vite
- JavaScript
- React Hooks
- Plain CSS or CSS Modules
- Fetch API for backend communication
- Lucide React icons, if useful

Do not introduce Redux, Next.js, Tailwind, or other frameworks unless absolutely necessary.

### AI and Storage
- OpenAI LLM for question routing and final answer generation
- ChromaDB for persistent vector storage
- OpenAI embeddings for document chunks
- Local sample documents
- Local ChromaDB persistence directory

All model names, API configuration, thresholds, and storage paths must be configurable using environment variables.

## 4. Adaptive RAG: Correct Functional Behavior

Implement genuine adaptive routing, not a fixed retrieval pipeline.

The application must classify each user query into one of the following routes:

### Route A: DIRECT

For greetings, simple conversational messages, and general questions that do not require the uploaded knowledge base.

Examples:
- Hi
- Hello
- How are you?
- What is RAG in simple words?

Behavior:
1. Classify the query.
2. Skip ChromaDB retrieval.
3. Generate a concise answer using the configured OpenAI LLM.
4. Return the answer with route `DIRECT`.
5. Return an empty sources array.

Do not claim that a general answer came from uploaded documents.

### Route B: RETRIEVE

For questions that require information from the indexed documents.

Examples:
- What is Adaptive RAG according to the course notes?
- Explain the concepts covered in the uploaded RAG document.
- What is the difference between Hybrid RAG and Advanced RAG in our notes?

Behavior:
1. Classify the query.
2. Generate an embedding for the query.
3. Retrieve relevant document chunks from ChromaDB.
4. Evaluate whether retrieved results meet the configured relevance threshold.
5. If relevant context exists, pass the context to the answer-generation LLM.
6. Instruct the LLM to answer only from the supplied document context.
7. Include document filenames and available source metadata.
8. Return the route, retrieved source snippets, and answer.

If no relevant context exists, do not invent an answer from the documents. Return a clear message explaining that the indexed documents do not contain sufficient information.

### Route C: CLARIFY

For incomplete, ambiguous, or underspecified questions.

Examples:
- Explain it.
- What about the second one?
- Compare these two.

The classifier must consider conversation history when deciding whether clarification is necessary.

Behavior:
1. Identify what information is missing.
2. Ask a concise follow-up question.
3. Do not perform unnecessary document retrieval.
4. Return the route `CLARIFY`.

Maintain a short, bounded conversation history per frontend session so follow-up questions can be interpreted. Do not store secrets or share history across different sessions.

### Adaptive Routing Rules

- Use a structured Pydantic schema for the classifier output.
- The classifier should return `route`, `reason`, and, where appropriate, `clarifying_question`.
- Validate every classifier response.
- If the classifier produces invalid output, handle it safely with a documented fallback.
- Never let classifier output execute code, SQL, shell commands, or arbitrary tools.
- Apply retrieval relevance checks before generating document-grounded answers.
- Do not run retrieval for every query.
- Do not use a fixed keyword-only router as the primary implementation.
- Make the routing decision observable in the API response and UI.
- Use bounded conversation history.
- Use a configurable low-temperature answer-generation setting.
- Avoid additional LLM calls when a simpler validated operation is sufficient.

## 5. Sample Documents: Create Them Automatically

Generate useful sample files inside:

`backend/data/sample_documents/`

Create these files with meaningful, non-empty content:

1. `rag_fundamentals.txt`
   - What RAG is
   - Indexing and retrieval
   - Embeddings and chunks
   - Advantages and limitations

2. `adaptive_rag_guide.md`
   - Adaptive RAG definition
   - DIRECT, RETRIEVE, and CLARIFY routing
   - Query classification
   - Retrieval relevance checks
   - Example routing scenarios

3. `hybrid_vs_advanced_rag.docx`
   - Hybrid RAG
   - Advanced RAG
   - Sparse and dense retrieval
   - Query rewriting and reranking
   - Differences and practical examples

4. `rag_course_faq.pdf`
   - At least 10 useful questions and answers covering RAG fundamentals, Adaptive RAG, Hybrid RAG, ChromaDB, embeddings, and OpenAI

5. `rag_concepts.xlsx`
   - A worksheet named `Concepts`
   - Columns: Concept, Definition, Example
   - At least 12 meaningful records

Use Python scripts with the appropriate libraries to generate the DOCX, PDF, and XLSX files. Ensure that the files are actually created and readable. Do not create fake documents with incorrect extensions.

Also create a `sample_questions.json` file containing example questions categorized by DIRECT, RETRIEVE, and CLARIFY.

Include a few out-of-scope questions that should produce a low-relevance retrieval result or a clarification response as appropriate.

The backend must support indexing these sample file types:
- TXT
- MD
- PDF
- DOCX
- XLSX

Do not require users to upload a file to test the initial application.

## 6. Document Ingestion and Indexing

Implement a reusable document ingestion module.

Requirements:

1. Read supported document types.
2. Extract text correctly from each format.
3. Preserve source filename and useful metadata.
4. Split extracted text into configurable chunks.
5. Use a configurable chunk size and overlap.
6. Generate embeddings through the OpenAI embeddings API.
7. Store chunk text, embeddings, unique IDs, and metadata in ChromaDB.
8. Use a persistent ChromaDB directory.
9. Use a configurable collection name.
10. Avoid duplicate records when indexing the same unchanged file repeatedly.
11. Detect modified files and update their indexed chunks safely.
12. Report the number of discovered files, processed files, chunks created, skipped files, and errors.
13. Handle empty files and extraction failures without crashing the entire indexing operation.
14. Provide an indexing status endpoint.
15. Provide a reindex endpoint that updates the index without leaving stale chunks from modified or deleted files.

Do not make the application download documents from the internet.

Do not use an in-memory-only vector database.

## 7. OpenAI and Environment Configuration

Create:

- `backend/.env.example`
- `backend/.env` only if safe to create without overwriting existing secrets
- `backend/config.py`

The environment example must contain:

OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
CHROMA_PERSIST_DIRECTORY=./storage/chroma
CHROMA_COLLECTION_NAME=vpro_adaptive_rag
CHUNK_SIZE=800
CHUNK_OVERLAP=120
TOP_K=5
RELEVANCE_THRESHOLD=0.35
FRONTEND_ORIGIN=http://localhost:5173
API_HOST=127.0.0.1
API_PORT=8000

You may adjust model names or defaults if necessary for current SDK compatibility, but keep all configuration centralized and documented.

Never hardcode an API key in source code.

Never print the API key in logs, API responses, or exception messages.

Validate required configuration at startup or when an OpenAI operation is first invoked, and return a helpful error when the key is missing.

Do not create or invent an API key.

Provide `.gitignore` entries for `.env`, Python caches, virtual environments, frontend dependencies, build output, logs, and local ChromaDB storage.

## 8. Backend Directory Structure

Create a clean structure similar to:

adaptive/
├── README.md
├── .gitignore
├── requirements.txt
├── start.sh
├── start.bat
├── backend/
│   ├── .env.example
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── api/
│   │   ├── health.py
│   │   ├── chat.py
│   │   ├── documents.py
│   │   └── indexing.py
│   ├── schemas/
│   │   ├── chat.py
│   │   ├── documents.py
│   │   └── indexing.py
│   ├── services/
│   │   ├── adaptive_router.py
│   │   ├── openai_service.py
│   │   ├── embedding_service.py
│   │   ├── chroma_service.py
│   │   ├── document_loader.py
│   │   ├── document_processor.py
│   │   ├── retrieval_service.py
│   │   ├── answer_service.py
│   │   └── indexing_service.py
│   ├── data/
│   │   └── sample_documents/
│   ├── scripts/
│   │   ├── create_sample_files.py
│   │   └── index_documents.py
│   ├── storage/
│   │   └── .gitkeep
│   └── tests/
│       ├── conftest.py
│       ├── test_health.py
│       ├── test_router.py
│       ├── test_chat.py
│       ├── test_documents.py
│       └── test_indexing.py
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    ├── .env.example
    ├── public/
    │   └── logo.png
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── api/
        │   └── client.js
        ├── components/
        │   ├── Header.jsx
        │   ├── Sidebar.jsx
        │   ├── ChatWindow.jsx
        │   ├── ChatMessage.jsx
        │   ├── ChatInput.jsx
        │   ├── RouteBadge.jsx
        │   ├── SourcePanel.jsx
        │   ├── SampleQuestions.jsx
        │   ├── StatusCard.jsx
        │   └── LoadingIndicator.jsx
        ├── hooks/
        │   └── useChat.js
        ├── styles/
        │   ├── global.css
        │   ├── layout.css
        │   ├── chat.css
        │   └── components.css
        └── utils/
            └── formatters.js

You may refine the structure if there is a clear architectural reason. Every imported module must exist. Do not leave empty placeholder modules, TODO comments, pseudocode, or unused duplicate implementations.

## 9. Backend API Requirements

Implement and document these endpoints:

### GET /api/health
Return application status, configuration status without secrets, and vector database initialization status.

### GET /api/indexing/status
Return collection name, document count, chunk count where available, and the last indexing result.

### POST /api/indexing/index
Index all supported sample documents.

### POST /api/indexing/reindex
Refresh the index and remove stale chunks safely.

### GET /api/documents
List indexed source documents with filenames and chunk counts.

### POST /api/chat
Accept a request with:
- `question`
- `session_id`
- `history` or a validated server-managed conversation reference, depending on your chosen session design

Return:
- `answer`
- `route`
- `reason`
- `sources`
- `session_id`
- `retrieval_performed`
- `retrieval_count`
- `confidence` or a documented relevance score when available

Do not return fabricated confidence values.

Use consistent JSON response schemas.

Configure CORS for the frontend origin using environment variables.

Validate request lengths and data types.

Use appropriate HTTP status codes.

Add useful error handling and structured logs without exposing sensitive information.

Keep API routes thin. Business logic belongs in service modules.

## 10. React Application Design

Create a professional, responsive AI learning assistant dashboard for VPRO Skills EduTech.

Use the uploaded VPRO Skills logo as the official brand asset.

Copy the supplied image into:

`frontend/public/logo.png`

Use the exact supplied logo. Do not replace it with a generated logo or a text-only approximation.

### Visual Theme

- Professional edtech SaaS dashboard
- Orange accent inspired by the logo
- Black and charcoal typography
- White or very light neutral background
- Subtle borders and shadows
- Rounded cards
- Clear visual hierarchy
- Consistent spacing
- Responsive desktop, tablet, and mobile layouts
- Accessible contrast and visible keyboard focus
- Avoid excessive gradients, animation, and visual clutter

### Header

Include:
- VPRO Skills logo
- Product name: Adaptive RAG Assistant
- Subtitle: Intelligent document question answering
- Backend connection indicator
- Indexing status indicator

### Sidebar

Include:
- New Chat
- Overview
- Sample Questions
- Indexed Documents
- Indexing Controls

Make these controls functional. Do not add non-working navigation items.

### Main Chat Area

Include:
- Welcome message
- Example questions
- Chat message history
- User and assistant message styling
- Input textarea
- Send button
- Enter-to-send and Shift+Enter for a newline
- Loading indicator
- Disabled send button while a request is pending
- Clear error messages
- Retry option where appropriate
- Copy-answer action
- Scroll management for new messages

### Route Visibility

Display an easy-to-understand badge for each answer:

DIRECT — Answered without document retrieval.

RETRIEVE — Answered using relevant indexed documents.

CLARIFY — Asked for more information.

Also display a brief explanation of why that route was selected.

Never claim that retrieval happened when it did not.

### Source Panel

For RETRIEVE responses, display:
- Source filename
- Relevant text snippet
- Relevance score when available
- Chunk metadata when useful

Use expandable source cards.

Display a clear empty state when no sources were retrieved.

### Indexing Controls

Show:
- Indexed file count
- Chunk count
- Collection status
- Last indexing result
- Index Documents button
- Reindex Documents button

Show progress, errors, and success messages. Refresh the status after indexing.

### Sample Questions

Provide selectable example questions for all three routes.

Examples:
- "Hi, how are you?"
- "Explain Adaptive RAG from the course notes."
- "What is the difference between Hybrid RAG and Advanced RAG in our documents?"
- "Explain it."
- "What is ChromaDB according to the sample documents?"
- "What are embeddings?"

Do not label a sample question as guaranteed to follow a particular route if the classifier may reasonably choose another route. Clearly distinguish expected behavior from actual observed routing.

### Responsive Behavior

- Desktop: sidebar and main chat panel
- Tablet: compact sidebar
- Mobile: collapsible navigation and full-width chat
- No horizontal page overflow
- Input must remain usable on small screens
- Source cards must wrap long filenames and text

### Logo

The logo must load from `/logo.png`. Use meaningful alt text and preserve its aspect ratio.

## 11. Frontend API Integration

Create one reusable API client with a configurable backend URL:

`VITE_API_BASE_URL=http://127.0.0.1:8000`

Requirements:
- Centralize HTTP requests.
- Handle JSON parsing and non-2xx responses.
- Handle backend offline errors.
- Avoid duplicating fetch logic across components.
- Prevent stale chat responses from overwriting newer state.
- Prevent duplicate submission while a request is pending.
- Keep conversation state predictable.
- Do not place API keys in frontend environment variables.
- Do not hardcode backend URLs in multiple files.

## 12. Reliability and Error Handling

Follow these rules strictly:

1. No undefined variables.
2. No missing imports.
3. No circular imports.
4. No duplicate implementations of the same functionality.
5. No redundant code snippets or unused modules.
6. No hardcoded API secrets.
7. No fake API responses presented as real AI responses.
8. No unimplemented buttons.
9. No unsupported claims about successful indexing.
10. No hidden dependency on a developer's global Python or Node installation beyond documented requirements.
11. Use pathlib for filesystem paths.
12. Make path resolution independent of the current shell directory.
13. Make indexing idempotent.
14. Use stable, unique chunk IDs.
15. Handle ChromaDB persistence correctly.
16. Handle OpenAI rate limits, connection failures, and invalid credentials with useful messages.
17. Never silently convert a failed OpenAI call into a fabricated answer.
18. Do not expose stack traces or secrets to frontend users.
19. Avoid unnecessary concurrent writes to the same ChromaDB collection.
20. Avoid broad exception handling that silently hides programming errors.
21. Ensure temporary files are cleaned up.
22. Keep generated storage and `.env` out of version control.
23. Ensure all scripts and commands work from the documented directory.
24. Use consistent naming conventions throughout the project.
25. Ensure sample documents can be recreated deterministically.

If the OpenAI API key is missing, the UI should still start and display a clear configuration warning. Health checks, UI rendering, sample-document listing, and offline unit tests must work without an API key.

Live LLM responses and real embedding generation require a valid OpenAI API key and network access.

## 13. Testing Requirements

Create meaningful automated tests.

Tests that do not require external services must use mocks or dependency injection.

Test at least:

- Health endpoint
- Valid and invalid request schemas
- DIRECT routing
- RETRIEVE routing
- CLARIFY routing
- Invalid classifier output fallback
- Retrieval skipped for DIRECT queries
- Retrieval executed for RETRIEVE queries
- Empty retrieval result
- Answer generation with retrieved context
- No-context answer behavior
- Document listing
- Unsupported file extensions
- Empty documents
- Indexing failures
- Idempotent indexing behavior
- API error handling

Do not make ordinary unit tests call the real OpenAI API.

Add a separate optional smoke-test command for a real OpenAI API key.

## 14. Single-Shot Setup and Startup

Provide scripts and commands that work from the project root.

### Linux/macOS

`bash start.sh`

The script should:
1. Check Python and Node.js availability.
2. Create a Python virtual environment if needed.
3. Install backend dependencies.
4. Generate missing sample documents.
5. Install frontend dependencies.
6. Check whether `.env` exists.
7. Create `.env` from `.env.example` only when it does not exist.
8. Preserve existing user configuration and API keys.
9. Run backend tests.
10. Run frontend production build checks.
11. Start the backend and frontend using a reliable process-management approach.
12. Clearly explain how to stop both processes.

Do not run dependency installation repeatedly when avoidable. Report any failure and stop rather than continuing as if successful.

If a dependency installation or test fails, show the relevant error and provide the exact corrective action.

### Windows

Provide a corresponding `start.bat` with equivalent setup behavior where practical.

### Manual Setup

Document commands for:
- Creating and activating a virtual environment
- Installing Python dependencies
- Creating `.env`
- Generating sample documents
- Indexing sample documents
- Starting FastAPI
- Installing React dependencies
- Starting Vite
- Running tests
- Building the React production bundle

Use separate terminal commands where necessary. Do not claim that two long-running development servers can both be started in a single foreground process without appropriate process management.

## 15. Documentation

Create a complete `README.md` containing:

1. Project overview
2. Adaptive RAG explained in simple English
3. Architecture diagram using Mermaid
4. Complete directory structure
5. Prerequisites
6. Installation instructions
7. Environment configuration
8. Sample document generation
9. Document indexing
10. API endpoints with request and response examples
11. Frontend usage
12. How DIRECT, RETRIEVE, and CLARIFY work
13. Example questions to test each route
14. ChromaDB persistence location
15. Troubleshooting
16. Security considerations
17. Test commands
18. Known limitations

Clearly explain that OpenAI API usage may incur charges.

## 16. Development Workflow

Follow this exact sequence:

Phase 1: Inspect the workspace and verify the logo asset is available.

Phase 2: Create the directory structure and configuration.

Phase 3: Implement deterministic sample-document generation.

Phase 4: Implement document loading, chunking, embeddings, and ChromaDB persistence.

Phase 5: Implement the adaptive classifier, retrieval logic, and answer generation.

Phase 6: Implement validated FastAPI endpoints.

Phase 7: Build the complete React interface and integrate the supplied logo.

Phase 8: Add automated tests and startup scripts.

Phase 9: Install dependencies if network access permits.

Phase 10: Generate sample documents and run tests.

Phase 11: Build the React production bundle.

Phase 12: Fix errors and rerun all relevant checks.

Phase 13: Review the final directory tree and README.

Do not stop after creating a plan. Continue implementing the project.

Do not ask me to create files manually when you can create them yourself.

If an operation cannot be completed because of missing credentials, unavailable network access, or environment restrictions, finish all independent work and state exactly what remains.

## 17. Final Acceptance Criteria

The project is complete only when:

- The full directory structure exists.
- All source files contain complete implementations.
- The VPRO Skills logo is displayed correctly.
- Sample documents are generated in the correct formats.
- ChromaDB uses persistent local storage.
- OpenAI configuration is externalized.
- The adaptive router supports DIRECT, RETRIEVE, and CLARIFY.
- Retrieval is skipped for DIRECT and CLARIFY routes.
- RETRIEVE answers are grounded in retrieved context.
- Low-relevance retrieval does not produce fabricated document answers.
- The UI displays route decisions, sources, errors, and indexing status.
- The frontend is responsive.
- Backend tests pass.
- Frontend production build passes.
- Startup instructions are accurate.
- No API keys or local database files are committed.
- No placeholder modules or redundant snippets remain.

## 18. Final Report

After implementation, report:

1. Exact project location.
2. Final directory tree.
3. Files created.
4. Sample documents generated.
5. Python and Node.js versions detected.
6. Dependencies installed successfully or any blockers.
7. Backend test results.
8. Frontend build results.
9. Whether live OpenAI integration was verified.
10. Exact startup commands.
11. Local frontend and backend URLs.
12. Any remaining limitations.

Never report a test as passing unless it actually ran and passed.

Start by inspecting the workspace and logo, then build the complete application.