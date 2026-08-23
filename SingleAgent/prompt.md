# Build a Single-Agent Code Review Application — Complete Development Instructions

You are a senior AI application architect and full-stack developer.

Help me build a **complete, end-to-end Single-Agent Code Review Application**.

The application must be **student-friendly**, **easy to understand**, **production-style in architecture**, but the code must remain **straightforward and minimal**.

Do not add unnecessary abstractions, unnecessary design patterns, unnecessary microservices, or extra code that does not directly support the application requirements.

---

# 1. IMPORTANT DEVELOPMENT RULES

Follow these rules throughout the entire project.

## Rule 1: Develop Phase by Phase

Develop the application in clear phases.

For every phase:

1. Explain the purpose of the phase.
2. Show the folder structure relevant to that phase.
3. Show installation commands.
4. Create the required files.
5. Provide complete code for each file.
6. Explain the code in simple student-level language.
7. Do not skip implementation details.

However:

**Do NOT test every phase individually.**

Complete the implementation phase by phase first.

After all phases are completed, perform:

- Backend testing
- Config Server testing
- MCP integration testing
- RAG testing
- LangGraph workflow testing
- File upload testing
- React frontend testing
- End-to-end application testing

---

# 2. DO NOT ASSUME ANYTHING

Do not assume:

- Python version
- Node.js version
- Operating system
- Existing folders
- Existing API keys
- Existing databases
- Existing packages
- Existing environment variables

Before starting, ask me only the **essential questions required to make implementation decisions**.

Do not ask unnecessary questions.

If a decision can safely use a standard default, clearly mention the default and ask for confirmation only if necessary.

---

# 3. APPLICATION NAME

Use the temporary project name:

**AI Code Review Agent**

Keep the project name easy to change later.

---

# 4. MAIN APPLICATION GOAL

Build a web application where a user can:

1. Upload source code files.
2. Upload multiple code files.
3. View uploaded files.
4. Select one or more files for review.
5. Send the code to an AI Code Review Agent.
6. Receive a structured code review.
7. Ask follow-up questions about the review.
8. Retrieve relevant coding knowledge using RAG.
9. Allow the agent to use MCP tools when external tools or structured operations are required.
10. Show the complete review in a React frontend.

The system should support common source files such as:

- `.py`
- `.js`
- `.ts`
- `.jsx`
- `.tsx`
- `.java`
- `.cpp`
- `.c`
- `.cs`
- `.go`

Do not attempt to support every programming language initially.

Keep the architecture extensible.

---

# 5. REQUIRED TECHNOLOGY STACK

Use the following stack.

## Backend

- Python
- FastAPI
- Uvicorn

## AI Frameworks

- LangChain
- LangGraph

## LLM

The LLM provider must be configurable.

Initially implement one primary provider based on the configuration.

The architecture should allow future providers without rewriting the application.

For example:

- OpenAI
- Anthropic
- Other future LLM providers

Do not implement unnecessary provider integrations immediately.

Implement only what is required for the selected primary provider.

---

## RAG

Use:

- LangChain
- ChromaDB

The RAG system should store coding knowledge and retrieve relevant information during code review.

Example knowledge:

- Python best practices
- JavaScript best practices
- Security guidelines
- Clean code principles
- Common code smells
- Error handling recommendations

Initially use a small set of local knowledge documents.

Do not create a complicated ingestion pipeline.

Keep ingestion simple and understandable.

---

## Agent Orchestration

Use:

- LangGraph

Even though this is a **single-agent application**, use LangGraph to manage the workflow.

The graph should be simple.

Suggested workflow:

```text
START
  |
  v
Receive User Request
  |
  v
Validate Uploaded Code
  |
  v
Retrieve Relevant Knowledge from RAG
  |
  v
Decide Whether MCP Tool Is Required
  |
  v
Code Review Agent
  |
  v
Generate Structured Review
  |
  v
END
```

Do not create multiple agents.

There should be only **one main Code Review Agent**.

Use LangGraph for workflow orchestration, not for unnecessary complexity.

---

# 6. MCP REQUIREMENT

Include MCP:

**Model Context Protocol**

Create a simple MCP Server for the application.

The MCP server should expose only useful tools.

Initially create simple tools such as:

### Tool 1: Code Metadata Tool

Input:

- file name
- file extension
- code content

Output:

- language
- number of lines
- number of characters

### Tool 2: Basic Code Analysis Tool

Perform simple deterministic analysis such as:

- Detect empty files
- Detect extremely large files
- Count functions if practical
- Count classes if practical

Do not duplicate the LLM's job.

The MCP tools should demonstrate:

```text
Code Review Agent
       |
       v
   MCP Client
       |
       v
   MCP Server
       |
       v
      Tools
```

The LangGraph workflow should allow the Code Review Agent to call MCP tools when required.

Show exactly:

1. MCP Server implementation
2. MCP Tool definitions
3. MCP Client implementation
4. How the FastAPI backend communicates with the MCP client
5. How the LangGraph agent uses MCP results

Keep MCP implementation minimal and educational.

---

# 7. CONFIG SERVER REQUIREMENT

Create a separate **Config Server**.

The Config Server must be an independent FastAPI application.

It should manage application configuration such as:

- LLM provider
- LLM model name
- API key references or configuration values
- Temperature
- Maximum tokens
- RAG configuration
- ChromaDB configuration
- MCP server URL or connection configuration

Architecture:

```text
                    +-------------------+
                    |   Config Server   |
                    |                   |
                    | LLM Configuration |
                    | Model Configuration|
                    | RAG Configuration |
                    | MCP Configuration |
                    +---------+---------+
                              |
                              |
                              v
+--------------------------------------------------+
|              Code Review Backend                 |
|                                                  |
|  FastAPI                                         |
|     |                                            |
|     v                                            |
| Configuration Client -----------------------------+
|     |
|     v
| LangGraph
|     |
|     +----------+
|     |          |
|     v          v
|    RAG        MCP
|     |          |
|     v          v
| ChromaDB    MCP Server
|
v
LLM
+--------------------------------------------------+
```

---

# 8. CONFIG SERVER SECURITY

Do not hardcode API keys in source code.

Use environment variables.

Example:

```text
OPENAI_API_KEY=your_key
```

The Config Server should demonstrate how configuration is centrally provided to the main application.

However, do not expose secrets in API responses unnecessarily.

Design a simple student-friendly approach.

Clearly explain:

### Local Development Flow

```text
.env
  |
  v
Config Server
  |
  v
Code Review Backend
  |
  v
LLM Client
```

Also explain what would change in a real production environment.

For example:

```text
Secret Manager
      |
      v
Config Service
      |
      v
Application
```

Do not implement AWS Secrets Manager, Vault, or other cloud services unless explicitly requested later.

Only explain them as future production options.

---

# 9. EXACT REAL-TIME CONFIGURATION USAGE

Show the exact runtime flow.

For example:

```text
User clicks "Review Code"
        |
        v
React sends request
        |
        v
FastAPI Code Review Backend
        |
        v
Configuration Client requests configuration
        |
        v
Config Server returns active configuration
        |
        v
Backend initializes or obtains configured LLM
        |
        +-------------------+
        |                   |
        v                   v
      RAG                MCP Client
        |                   |
        v                   v
Retrieve Knowledge      Execute Tool
        |                   |
        +---------+---------+
                  |
                  v
           LangGraph Workflow
                  |
                  v
           Code Review Agent
                  |
                  v
             Review Result
                  |
                  v
                React
```

Clearly identify where configuration is used in the actual code.

Do not just explain theoretically.

Show the actual files and methods responsible for:

- Fetching configuration
- Creating the LLM
- Creating the RAG components
- Connecting to MCP
- Executing the LangGraph workflow

---

# 10. CODE REVIEW AGENT RESPONSIBILITIES

The single Code Review Agent should review:

## A. Code Quality

Check:

- Readability
- Naming
- Code duplication
- Code structure
- Unnecessary complexity

## B. Bugs

Identify potential:

- Logical errors
- Null or None problems
- Incorrect conditions
- Edge cases

## C. Security

Identify common issues such as:

- Hardcoded secrets
- Unsafe input handling
- Dangerous operations

Do not claim a complete security audit.

Clearly present these as AI-assisted findings.

## D. Performance

Identify obvious issues such as:

- Unnecessary loops
- Repeated calculations
- Inefficient data handling

## E. Best Practices

Use RAG-retrieved knowledge where relevant.

---

# 11. STRUCTURED CODE REVIEW RESPONSE

The backend should return a clean JSON response.

Example:

```json
{
  "review_id": "generated-id",
  "summary": "Overall summary of the code.",
  "score": 82,
  "issues": [
    {
      "severity": "high",
      "category": "bug",
      "file": "example.py",
      "line": 10,
      "message": "Possible division by zero.",
      "suggestion": "Check the denominator before division."
    }
  ],
  "improvements": [
    "Use meaningful variable names.",
    "Add exception handling."
  ],
  "rag_context_used": true,
  "mcp_tools_used": [
    "code_metadata"
  ]
}
```

Use Pydantic models.

Keep the models simple.

Do not create unnecessary nested schemas.

---

# 12. FILE UPLOAD REQUIREMENT

The FastAPI backend must allow users to upload code files.

Support:

```text
.py
.js
.ts
.jsx
.tsx
.java
.c
.cpp
.cs
.go
```

Validate:

- Allowed extension
- File size
- Empty file

Do not implement antivirus scanning.

Clearly mention that production systems may require additional security controls.

Initially:

- Store uploaded files locally.
- Use a simple upload directory.
- Generate a unique review or upload ID.

Do not introduce S3, cloud storage, or databases initially.

Keep it simple.

Suggested structure:

```text
uploads/
    upload_id/
        file1.py
        file2.js
```

---

# 13. RAG IMPLEMENTATION

Create a simple RAG pipeline.

Suggested structure:

```text
rag/
├── documents/
│   ├── python_best_practices.md
│   ├── javascript_best_practices.md
│   ├── security_guidelines.md
│   └── clean_code.md
│
├── ingest.py
├── vector_store.py
└── retriever.py
```

The flow should be:

```text
Knowledge Documents
        |
        v
Document Loader
        |
        v
Text Splitter
        |
        v
Embeddings
        |
        v
ChromaDB
        |
        v
Retriever
        |
        v
Code Review Agent
```

Keep the RAG pipeline straightforward.

Do not add:

- Query rewriting
- Reranking
- Self-RAG
- Corrective RAG
- Agentic RAG

This project uses basic RAG because the main goal is student-level understanding.

---

# 14. LANGCHAIN USAGE

Use LangChain only where it provides value.

Use it for:

- LLM integration
- Prompt templates
- Document loading
- Text splitting
- Embeddings
- Vector store
- Retrieval

Do not create unnecessary chains.

The application should remain easy to trace.

---

# 15. LANGGRAPH IMPLEMENTATION

Create one simple LangGraph workflow.

Suggested nodes:

```text
1. validate_code
2. retrieve_context
3. run_mcp_tools
4. review_code
5. format_response
```

State should contain only necessary data.

Example:

```python
class CodeReviewState(TypedDict):
    files: list
    rag_context: str
    mcp_results: dict
    review_result: dict
```

Do not put unnecessary objects into the state.

Clearly explain:

- State
- Nodes
- Edges
- Conditional logic, if any

---

# 16. FASTAPI BACKEND

Create a clean FastAPI application.

Suggested API structure:

```text
POST /api/files/upload

GET /api/files/{upload_id}

POST /api/review

GET /api/review/{review_id}
```

Initially, keep only APIs that are actually needed.

Do not add:

- Authentication
- User management
- Payment systems
- Admin panels
- Database persistence

unless explicitly requested later.

Focus on the Code Review Agent.

---

# 17. REACT FRONTEND

Use:

- React
- Vite

Keep the frontend simple.

Suggested pages:

```text
Home
Code Review
Review Result
```

However, if a single-page interface is simpler, that is acceptable.

The UI should include:

### Section 1: Upload Code

- Upload one or multiple files
- Show selected files
- Remove files

### Section 2: Review Options

Initially keep options minimal.

For example:

- Review focus: General / Bugs / Security / Performance

Do not add unnecessary settings.

### Section 3: Review Button

```text
Review My Code
```

### Section 4: Review Result

Display:

- Overall score
- Summary
- Issues
- Severity
- File
- Line number
- Suggestion
- Improvements
- RAG usage
- MCP tools used

Use simple CSS.

Do not introduce a large UI component library unless required.

Student-friendly and clean design is more important than complex UI.

---

# 18. SUGGESTED PROJECT STRUCTURE

Use a structure similar to this:

```text
ai-code-review-agent/
│
├── config-server/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   └── schemas.py
│   │
│   ├── .env
│   └── requirements.txt
│
├── mcp-server/
│   ├── server.py
│   └── requirements.txt
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── files.py
│   │   │   └── review.py
│   │   │
│   │   ├── agent/
│   │   │   ├── graph.py
│   │   │   ├── state.py
│   │   │   └── reviewer.py
│   │   │
│   │   ├── rag/
│   │   │   ├── ingest.py
│   │   │   ├── retriever.py
│   │   │   └── documents/
│   │   │
│   │   ├── mcp/
│   │   │   └── client.py
│   │   │
│   │   ├── config/
│   │   │   └── client.py
│   │   │
│   │   ├── services/
│   │   │   ├── file_service.py
│   │   │   └── review_service.py
│   │   │
│   │   └── models/
│   │       └── review.py
│   │
│   ├── uploads/
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   └── App.jsx
    │
    └── package.json
```

You may simplify this structure if some folders contain only one unnecessary file.

Do not create empty architectural layers just for appearance.

---

# 19. DEVELOPMENT PHASES

Develop the application in exactly these logical phases.

## Phase 1 — Architecture and Prerequisites

Before coding:

- Confirm essential choices.
- Show final architecture.
- Explain component responsibilities.
- Show complete request flow.
- Show required software.
- Show installation commands.

---

## Phase 2 — Project Setup

Create:

```text
ai-code-review-agent
```

Create:

- Config Server
- MCP Server
- Backend
- Frontend

Create virtual environments where required.

Install required dependencies.

Explain every dependency briefly.

Do not install unnecessary packages.

---

## Phase 3 — Config Server

Implement:

- FastAPI Config Server
- Environment variable loading
- LLM configuration
- Model configuration
- RAG configuration
- MCP configuration

Create an endpoint such as:

```text
GET /config/application
```

Ensure secrets are not unnecessarily returned.

Show exactly how the backend consumes this configuration.

---

## Phase 4 — MCP Server

Implement:

- MCP Server
- Code metadata tool
- Basic deterministic code analysis tool

Keep the implementation small.

Explain the MCP request flow.

---

## Phase 5 — RAG

Implement:

- Knowledge documents
- Document ingestion
- Text splitting
- Embeddings
- ChromaDB
- Retriever

Do not test yet.

Just build correctly.

---

## Phase 6 — LangChain LLM Layer

Implement:

- Configuration-driven LLM creation
- Prompt template
- Structured output handling where appropriate

Do not hardcode the model configuration.

---

## Phase 7 — LangGraph Single-Agent Workflow

Implement:

```text
validate_code
        |
        v
retrieve_context
        |
        v
run_mcp_tools
        |
        v
review_code
        |
        v
format_response
```

Only one main AI agent should perform the review.

Clearly identify which code represents the actual agent.

---

## Phase 8 — FastAPI Backend

Implement:

- File upload API
- File retrieval API
- Review API
- Review result API

Connect:

- Config Server
- RAG
- MCP
- LangGraph
- LLM

---

## Phase 9 — React Frontend

Implement:

- File upload
- Selected files display
- Review type selection
- API communication
- Loading state
- Error handling
- Review result display

Keep CSS simple.

---

## Phase 10 — Complete Integration

Connect all components.

Final architecture:

```text
                    React Frontend
                          |
                          | HTTP
                          v
                FastAPI Code Review API
                          |
            +-------------+-------------+
            |             |             |
            v             v             v
       Config Client     LangGraph      File Storage
            |               |
            v               |
       Config Server         |
                            |
                    +-------+-------+
                    |               |
                    v               v
                   RAG         MCP Client
                    |               |
                    v               v
                ChromaDB       MCP Server
                    |
                    v
                   LLM
```

Correct the architecture if necessary to reflect the actual runtime dependency flow.

Do not force an incorrect diagram.

---

# 20. FINAL TESTING ONLY

After completing all phases, test the entire application.

Perform testing only after the full implementation is complete.

Test:

## Config Server

Verify:

- Configuration endpoint works.
- Environment values are correctly loaded.
- Secrets are not exposed.

## MCP Server

Verify:

- Metadata tool works.
- Basic analysis tool works.

## RAG

Verify:

- Documents are ingested.
- Relevant context is retrieved.

## Backend

Verify:

- File upload.
- Multiple file upload.
- File validation.
- Review API.

## LangGraph

Verify the complete workflow:

```text
validate_code
→ retrieve_context
→ run_mcp_tools
→ review_code
→ format_response
```

## Frontend

Verify:

- File selection.
- File upload.
- Review request.
- Result rendering.
- Error handling.

## End-to-End

Use at least one simple sample source file.

Demonstrate:

```text
Upload
   ↓
Backend
   ↓
Config Server
   ↓
LangGraph
   ↓
RAG
   ↓
MCP
   ↓
LLM
   ↓
Structured Review
   ↓
React UI
```

---

# 21. CODE STYLE REQUIREMENTS

All code must follow these rules.

## Keep Code Straightforward

Prefer:

```python
def get_review():
    ...
```

over unnecessary abstractions.

Avoid:

- Complex factory patterns
- Excessive inheritance
- Unnecessary dependency injection frameworks
- Generic abstractions that students cannot understand

unless technically required.

---

## Add Comments Only When Useful

Do not add comments to every line.

Use comments only for:

- Important logic
- LangGraph workflow behavior
- MCP communication
- RAG retrieval
- Configuration flow

---

## Naming

Use meaningful names.

Examples:

```python
review_code()
retrieve_context()
get_application_config()
upload_files()
```

Avoid vague names such as:

```python
process()
handle()
run()
do_task()
```

unless their purpose is obvious from context.

---

# 22. EXPLANATION STYLE

Explain everything at a student level.

For every important component, explain:

### What is it?

### Why do we need it?

### Where is it used?

### How does data flow through it?

Example:

```text
LangChain
    ↓
Used to communicate with the LLM and build the RAG components.

LangGraph
    ↓
Used to control the step-by-step workflow of the Code Review Agent.

MCP
    ↓
Used to allow the agent/application to access structured external tools.

RAG
    ↓
Used to retrieve relevant coding knowledge before the LLM performs the review.
```

---

# 23. REAL-TIME REQUEST FLOW

At the end, provide a detailed walkthrough of what happens when the user clicks:

```text
Review My Code
```

Explain step by step.

Example:

```text
1. User selects files in React.

2. React uploads files to FastAPI.

3. FastAPI validates the files.

4. React sends the review request.

5. Backend requests active configuration.

6. Config Server provides non-secret runtime configuration.

7. LangGraph starts.

8. validate_code node checks input.

9. retrieve_context node queries ChromaDB.

10. run_mcp_tools node calls MCP tools.

11. review_code node combines:

    - Uploaded code
    - User review focus
    - RAG context
    - MCP analysis
    - LLM configuration

12. LLM generates the review.

13. format_response creates structured JSON.

14. FastAPI returns the response.

15. React displays the result.
```

Ensure this flow matches the actual implementation.

---

# 24. README

At the end, create a complete README.

Include:

- Project overview
- Architecture
- Technologies
- Prerequisites
- Installation
- Environment variables
- Starting Config Server
- Starting MCP Server
- Running RAG ingestion
- Starting Backend
- Starting React Frontend
- Complete execution order
- API endpoints
- End-to-end usage
- Troubleshooting

Use exact commands based on the implementation.

Do not provide placeholder commands that do not match the code.

---

# 25. IMPORTANT: DO NOT ADD THESE UNLESS I ASK

Do not add:

- Authentication
- JWT
- Login
- Registration
- User database
- Redis
- Celery
- Kafka
- Kubernetes
- Docker
- CI/CD
- Cloud deployment
- Payment
- Admin panel
- Multi-agent architecture
- Agent memory
- Complex observability platforms
- Advanced RAG
- Reranking
- Evaluation pipelines

This project is specifically for learning the core integration of:

```text
Single AI Agent
+
LangGraph
+
LangChain
+
LLM
+
RAG
+
ChromaDB
+
MCP
+
Config Server
+
FastAPI
+
React
+
Code File Upload
```

---

# 26. OUTPUT FORMAT FOR EACH PHASE

For each phase, use this format:

```text
PHASE X — NAME

1. Objective

2. What We Are Building

3. Folder Structure

4. Installation Commands

5. Implementation

6. Code Explanation

7. How This Connects to the Next Phase
```

Do not perform testing after each phase.

Continue building until the entire application is implemented.

Only after all phases are complete:

```text
FINAL TESTING
```

Then perform complete testing and fix any integration issues.

---

# 27. START NOW

Before writing code:

1. Analyze the architecture carefully.
2. Identify only essential technical decisions that require my input.
3. Ask those questions first.
4. Once answered, create the complete application phase by phase.
5. Do not skip files.
6. Do not provide pseudo-code where real code is required.
7. Do not add unnecessary code.
8. Keep everything student-friendly.
9. Keep the architecture realistic but simple.
10. At the end, perform complete integration testing.

The final result must be a working, understandable, end-to-end **Single-Agent AI Code Review Application**.