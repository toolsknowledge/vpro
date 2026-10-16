# MASTER PROMPT: Build a Complete Advanced RAG Application Using FastAPI, Streamlit, ChromaDB, and Claude

## 1. Your Role

Act as an experienced Python developer and AI application engineer.

Build a complete, working Advanced RAG application from scratch. Create the actual project files in the available workspace using ChatGPT Work.

The application must be simple, student-friendly, easy to understand, and suitable for demonstrating Advanced RAG concepts to students.

**Important:** Do not only provide code snippets or instructions. Create the files, install dependencies where possible, run the application, test it, and fix errors.

## 2. Application Requirements

Build an Advanced RAG application that indexes a website and answers user questions using the website's content.

Default website:

https://www.vproskills.com/

The user must also be able to enter another website URL dynamically.

The application must use:

- Python
- FastAPI for the backend
- Streamlit for the frontend
- ChromaDB for persistent vector storage
- Sentence Transformers for embeddings
- scikit-learn for TF-IDF keyword search
- Claude API for query expansion and final answer generation
- BeautifulSoup for extracting website text
- Requests for HTTP communication
- python-dotenv for loading `.env` configuration

Do not replace these technologies with alternatives.

## 3. Required Project Structure

Create this project structure:

advanced-rag/
- main.py
- requirements.txt
- .env
- advanced-frontend/
  - app.py
  - requirements.txt

- chroma_db/ — created automatically when the application runs.

Keep the backend logic in a single Python file named `main.py`.

Keep the Streamlit interface in `advanced-frontend/app.py`.

Create separate `requirements.txt` files for the backend and frontend.

Create a `.env` template containing configuration variables. Never insert a real or fabricated API key.

## 4. Website Indexing

Implement a function:

`read_website(url)`

Requirements:
- Download the supplied webpage.
- Extract readable text using BeautifulSoup.
- Handle HTTP errors, timeouts, invalid URLs, and empty page content.
- Use reasonable request timeouts and response-size limits.
- Do not crawl the entire website. Index only the supplied webpage.
- Validate URLs and prevent requests to localhost, private IP addresses, and other non-public destinations.
- Do not bypass website access restrictions.

Implement a function:

`create_chunks(text)`

Requirements:
- Split the extracted text into smaller chunks.
- Use a default chunk size of 120 words.
- Use a default overlap of 25 words.
- Make chunk size and overlap easy to configure.
- Ensure the chunks are meaningful and non-empty.
- Explain the chunking logic through comments.

Implement a function:

`index_website(url)`

Requirements:
1. Read the website.
2. Create text chunks.
3. Generate embeddings using Sentence Transformers.
4. Create TF-IDF representations using scikit-learn.
5. Replace the previous indexed website's records in ChromaDB.
6. Store chunk IDs, text, embeddings, source URLs, and chunk numbers.
7. Update the in-memory variables required for retrieval.
8. Return a clear success response containing the URL and number of chunks.
9. Handle errors without leaving the application in a misleading state.

Use a persistent ChromaDB collection named `vpro_website_chunks` and a configurable local database directory.

Use the embedding model `sentence-transformers/all-MiniLM-L6-v2`.

Normalize embeddings and ensure that the vector-search distance calculation is consistent with the chosen similarity scoring.

The application must support one active website index at a time.

## 5. Advanced RAG Retrieval

Implement a hybrid retrieval process.

### A. Query Expansion

Create a function that uses Claude to generate alternative search queries for the user's question.

Example:

Original question:
"What AI courses are available?"

Possible expanded queries:
- What artificial intelligence courses does the website offer?
- Which AI training programs are available?
- What topics are covered in the AI courses?

Use the original question if query expansion fails.

Avoid unnecessary LLM calls.

### B. Vector Search

Use ChromaDB to retrieve relevant chunks based on embedding similarity.

### C. Keyword Search

Use scikit-learn's `TfidfVectorizer` and cosine similarity to retrieve relevant chunks based on keywords.

### D. Hybrid Search

Combine the vector-search and keyword-search scores using these initial weights:

- Vector similarity: 65%
- Keyword similarity: 35%

Keep the weights configurable.

Normalize or transform scores appropriately so that the two scoring methods are comparable.

Remove duplicate chunks and avoid returning irrelevant results.

### E. Result Selection

- Rank the retrieved chunks by the combined score.
- Select the most relevant chunks.
- Make the number of retrieved chunks configurable.
- Keep the source URL and chunk number available for debugging.
- Do not claim that a separate reranker model is implemented unless an actual reranker is included.

### F. Context Preparation

Combine the selected chunks into a clear context string.

Avoid exceeding the configured context budget.

Preserve the source information so the answer can be traced to the indexed content.

## 6. Claude Integration

Use the Anthropic Python SDK and Claude API.

Read the API key and model ID from `.env`.

Example configuration:

ANTHROPIC_API_KEY=your_actual_key_here
CLAUDE_MODEL=your_accessible_claude_model_id
CHROMA_PATH=./chroma_db

The model ID must be valid and accessible to the user's Anthropic account. Do not assume a model is available without checking its configuration or current documentation.

Implement a reusable function:

`claude_text(prompt, max_tokens=400)`

Requirements:
- Send the prompt to Claude.
- Return the generated text.
- Handle API errors and missing configuration.
- Make the output token limit configurable.
- Do not expose the API key in responses or logs.

Use Claude for query expansion and final answer generation.

### Final Answer Rules

The final prompt sent to Claude must instruct it to:

- Answer using the retrieved website context.
- Use simple English.
- Give clear, direct answers.
- Avoid inventing facts, fees, dates, schedules, or policies.
- Clearly state when the indexed content does not contain the answer.
- Distinguish website facts from information that is unavailable.
- Avoid claiming that the application guarantees factual correctness.

## 7. FastAPI Endpoints

Implement these endpoints:

### GET `/`

Return a simple application status message.

### POST `/index`

Accept JSON:

{
  "url": "https://www.vproskills.com/"
}

Call the website-indexing function.

Return the indexing status, URL, and total chunk count.

### GET `/status`

Return the current indexing status, indexed URL, and number of indexed chunks.

If the application has not indexed a website, return an appropriate status.

### POST `/ask`

Accept JSON:

{
  "question": "What AI topics does VPro Skills teach?"
}

Process the question through query expansion, hybrid retrieval, context preparation, and Claude answer generation.

Return the answer and useful retrieval details, such as the source URL and selected chunk information.

Validate all request inputs and return meaningful HTTP error responses.

## 8. Streamlit Frontend

Create `advanced-frontend/app.py`.

Use a clean, professional, student-friendly interface with the title:

VPro Skills — Advanced RAG

The interface must include:

1. A website URL input field.
2. Default URL: `https://www.vproskills.com/`.
3. An **Index Website** button.
4. An indexing progress indicator.
5. A success or error message after indexing.
6. A **Check Index Status** button.
7. A chat input for asking questions.
8. A chat interface displaying user questions and AI answers.
9. A **Clear Chat** button.
10. An expandable section showing retrieval details for debugging.

Use Streamlit's chat components and session state.

Connect the UI to FastAPI through HTTP requests.

Use this default backend URL:

`http://127.0.0.1:8000`

Make the backend URL configurable through an environment variable if practical.

The UI must handle connection failures, HTTP errors, timeouts, and unexpected JSON responses gracefully.

Keep the frontend code simple and avoid unnecessary packages.

## 9. Requirements Files

Create the backend `requirements.txt` containing the dependencies actually imported by `main.py`.

Create `advanced-frontend/requirements.txt` containing the dependencies actually imported by `app.py`.

Pin compatible versions where appropriate.

Do not include unused libraries.

Ensure that the application uses a consistent set of package versions.

## 10. Configuration and Security

- Load configuration using `python-dotenv`.
- Keep secrets in `.env`.
- Provide `.env.example` if useful.
- Add `.env`, `chroma_db/`, virtual environments, and Python cache files to `.gitignore`.
- Never hardcode a real API key.
- Do not return secrets in API responses.
- Validate website URLs.
- Use request timeouts and response-size limits.
- Avoid executing downloaded website content.
- Handle external API errors without crashing the server.

## 11. Persistence and Error Handling

ChromaDB must use persistent local storage.

Do not delete the database directory whenever the application starts.

Ensure that the application can determine whether an index exists after a restart.

Because TF-IDF data and other retrieval state may be held in memory, implement a simple and reliable strategy to restore or rebuild the required retrieval state after restarting the backend.

Do not report a successful index if indexing failed.

If re-indexing fails, avoid leaving the application with mismatched ChromaDB records and in-memory retrieval data. Explain any limitations clearly.

## 12. Code Quality

- Keep backend logic in `main.py`.
- Keep frontend logic in `advanced-frontend/app.py`.
- Use descriptive variable and function names.
- Add comments where they help beginners understand the code.
- Keep the code concise and easy to teach.
- Avoid unnecessary classes, abstractions, and complicated design patterns.
- Do not add authentication, user management, database systems other than ChromaDB, or unrelated features.
- Do not create features that are not requested.
- Do not leave placeholder functions or incomplete implementations.

## 13. Testing and Verification

After creating the files, perform the following checks wherever the environment permits:

1. Verify Python syntax.
2. Verify that imports work.
3. Check that requirements files include the necessary packages.
4. Check that `.env` configuration is loaded correctly.
5. Start the FastAPI application.
6. Test the `/` endpoint.
7. Test the `/status` endpoint before indexing.
8. Test `/index` with the default VPro Skills URL.
9. Test `/status` after successful indexing.
10. Test `/ask` with a question whose answer appears in the indexed content.
11. Test a question whose answer is absent from the indexed content.
12. Test invalid URL handling.
13. Test API connection failures.
14. Check that the Streamlit UI can communicate with FastAPI.
15. Check whether the index and retrieval state remain usable after restarting the backend.

Do not claim that a test passed unless it was actually executed successfully.

If internet access, API credentials, package installation, or other environmental restrictions prevent a test, clearly identify the untested part and provide the exact command needed to test it.

Fix errors discovered during testing before declaring the project ready.

## 14. Run Instructions

Provide clear commands for setting up and running the application.

Backend:

`pip install -r requirements.txt`

`uvicorn main:app --reload`

Frontend, from the `advanced-frontend` directory:

`pip install -r requirements.txt`

`streamlit run app.py`

Explain that FastAPI and Streamlit must run in separate terminals.

Provide the local URLs for the Streamlit interface and FastAPI Swagger documentation.

## 15. Final Deliverables

Create all required files in the workspace.

At the end, provide:

1. The project folder structure.
2. A list of files created.
3. The purpose of each file in simple English.
4. The contents and location of the `.env` template.
5. Installation and execution commands.
6. A list of tests actually performed and their results.
7. Any remaining limitations or required manual steps.

If possible, package the completed project into a ZIP file.

## Final Instruction

Build the application according to these requirements without adding unrelated features or inventing missing requirements.

Prioritize correctness, simplicity, reliable execution, and ease of understanding.

Create the actual files, run the available tests, fix errors, and report honestly what has and has not been verified.