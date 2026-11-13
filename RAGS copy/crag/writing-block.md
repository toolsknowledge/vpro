# MASTER PROMPT: BUILD A COMPLETE CORRECTIVE RAG APPLICATION

## 1. PROJECT ROLE

Act as a Senior AI Engineer, Python Backend Developer, React Frontend Developer, UI/UX Designer, and Software Architect.

Build a complete, production-style educational Corrective RAG application for **VPro Skills EduTech**.

The application must be beginner-friendly, responsive, visually professional, maintainable, and easy to demonstrate to students.

This is a real working application, not a static UI demo.

Follow all requirements carefully. Do not add unnecessary code, unnecessary libraries, unnecessary abstractions, or unrelated features.

## 2. PROJECT NAME

VPro Skills – Corrective RAG Student Assistant

Application tagline:

"Learn Smarter with AI-Powered Knowledge Retrieval"

## 3. TECHNOLOGY STACK

Use ONLY the following primary technology stack:

### Frontend
- React.js
- Vite
- JavaScript
- HTML5
- CSS3
- Axios
- React Router only if multiple routes are genuinely required

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic
- Python-dotenv

### AI and RAG
- OpenAI LLM
- OpenAI Embeddings
- ChromaDB
- PDF document loader
- Text splitting and chunking
- Retrieval and relevance evaluation
- Query transformation
- Corrective retrieval

### Database
- ChromaDB persistent vector database

### Knowledge Source
- PDF document

IMPORTANT:
Generate a sample educational PDF document yourself and use it as the initial knowledge source.

Do not depend on me to upload a PDF to get the initial application running.

## 4. COMPANY BRANDING

Company name: VPro Skills EduTech

Website: https://www.vproskills.com/

Use the company logo provided in the project input.

The uploaded logo is named logo(2).jpeg.

Copy the supplied logo into:

frontend/public/logo.jpeg

Use this exact logo in the application header.

Requirements:
- Do not recreate the logo.
- Do not modify the logo.
- Do not replace it with a text-based logo.
- Maintain its original proportions.
- Display it with appropriate dimensions.
- Ensure it looks good on desktop and mobile devices.

Use a professional branding theme based on:
- Orange
- Black
- White
- Light grey

Use orange as the primary brand accent.

## 5. APPLICATION OBJECTIVE

Build an AI-powered student assistant that answers questions using information available in PDF knowledge documents.

The application must implement Corrective RAG.

The system should not blindly trust the first set of retrieved documents.

It must evaluate retrieved information, identify irrelevant or insufficient context, correct the retrieval process, and generate answers only when sufficient supporting information is available.

The primary objective is to teach students how Corrective RAG works through an actual working application.

## 6. CORRECTIVE RAG WORKFLOW

Implement the following workflow.

### Step 1: Student Question

The student enters a question in the React chat interface.

Example:

"What is Python?"

### Step 2: Query Processing

- Receive the question through FastAPI.
- Validate the question.
- Prepare the query for retrieval.
- Generate query embeddings using OpenAI embeddings.

### Step 3: Initial Retrieval

- Search relevant documents from ChromaDB.
- Retrieve the top 5 relevant chunks.
- Include similarity or relevance information.
- Collect the source document and page metadata.

### Step 4: Document Relevance Evaluation

Use the OpenAI LLM to evaluate retrieved chunks.

Classify retrieved information as:

- Relevant
- Partially Relevant
- Irrelevant

The evaluator must determine whether the retrieved content actually answers the student's question.

Do not assume that a retrieved chunk is relevant simply because it was returned by ChromaDB.

### Step 5: Corrective Mechanism

If the retrieved information is irrelevant or insufficient:

1. Identify the reason for retrieval failure.
2. Rewrite or improve the student's query.
3. Perform another retrieval against ChromaDB.
4. Evaluate the newly retrieved documents.
5. Compare the quality of the initial and corrected retrieval.
6. Continue only for a limited number of attempts.

Use a maximum of 2 corrective retrieval attempts.

IMPORTANT:

The knowledge source for this project is PDF documents only.

Do not introduce external web search or unrelated knowledge sources.

The correction mechanism must work through query transformation and repeated retrieval from the available PDF knowledge base.

### Step 6: Final Answer Generation

When sufficient relevant context is available:

- Generate a clear answer using the OpenAI LLM.
- Use simple English.
- Explain concepts in student-friendly language.
- Include examples wherever useful.
- Avoid unnecessary technical terminology.
- Include source document names and page references.

If sufficient context is not available after correction:

Return a friendly message:

"I could not find sufficient information in the available learning materials to answer this question accurately. Please try rephrasing your question or consult your trainer."

Never generate unsupported answers.

### Step 7: Display Results

Display the following information in the frontend:

- Student question
- AI-generated answer
- Retrieved documents
- Relevance status
- Whether corrective retrieval was triggered
- Number of correction attempts
- Final retrieval status
- Source PDF and page numbers

## 7. SAMPLE PDF GENERATION

Create a professional sample educational PDF.

File name:

knowledge_base/python_learning_guide.pdf

Document title:

"Python Programming – Student Learning Guide"

Include approximately 10–15 pages of educational content.

Topics:

1. Introduction to Python
2. Features of Python
3. Python Installation
4. Python Variables
5. Python Data Types
6. Strings
7. Lists
8. Tuples
9. Dictionaries
10. Sets
11. Conditional Statements
12. Loops
13. Functions
14. Object-Oriented Programming
15. Exception Handling

Requirements:

- Use clear educational explanations.
- Include Python code examples.
- Include practical examples.
- Use headings and subheadings.
- Add page numbers.
- Use professional PDF formatting.
- Make the document readable for beginners.

Use ReportLab to generate the PDF.

The generated PDF must be used by the application during its initial setup.

## 8. PDF PROCESSING PIPELINE

Implement PDF ingestion.

Requirements:

1. Read the PDF document.
2. Extract text page by page.
3. Clean unnecessary whitespace.
4. Split content into chunks.
5. Use chunk size around 800 characters.
6. Use chunk overlap around 150 characters.
7. Generate embeddings using OpenAI.
8. Store embeddings in ChromaDB.
9. Store document metadata.

Metadata should include:

- document_name
- page_number
- chunk_id
- source

Avoid inserting duplicate chunks when the application restarts.

Implement a simple ingestion endpoint.

Example:

POST /api/documents/ingest

Also provide an endpoint to list available documents.

## 9. CHROMADB CONFIGURATION

Use persistent ChromaDB storage.

Database directory:

backend/chroma_db/

Collection name:

vpro_corrective_rag

Requirements:

- Use persistent storage.
- Create the collection automatically if missing.
- Use OpenAI embeddings consistently for indexing and retrieval.
- Avoid unnecessary re-indexing.
- Handle empty collections gracefully.
- Handle embedding errors.
- Handle database connection and persistence errors.

## 10. OPENAI CONFIGURATION

Use environment variables.

Create:

backend/.env.example

Include:

OPENAI_API_KEY=your_openai_api_key
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

Never hardcode API keys.

Never expose the API key to React.

Use the configured OpenAI chat model and embedding model.

Implement appropriate error handling for:
- Invalid API keys
- API rate limits
- Network failures
- API timeouts
- Invalid model configuration

## 11. FASTAPI BACKEND STRUCTURE

Create a clean and simple backend architecture.

Suggested structure:

backend/
    app/
        main.py
        config.py
        schemas.py
        services/
            pdf_service.py
            embedding_service.py
            retrieval_service.py
            relevance_service.py
            corrective_rag_service.py
        api/
            routes.py
    knowledge_base/
        python_learning_guide.pdf
    chroma_db/
    requirements.txt
    .env
    .env.example

Keep the architecture simple.

Do not create unnecessary files or classes.

Implement the following APIs:

### API 1: Health Check

GET /api/health

Return backend status.

### API 2: Chat

POST /api/chat

Request:

{
  "question": "What is Python?"
}

Response should contain:

{
  "question": "What is Python?",
  "answer": "Python is...",
  "retrieval_status": "relevant",
  "corrective_retrieval_used": false,
  "correction_attempts": 0,
  "sources": [],
  "retrieved_documents": []
}

Use proper Pydantic response models.

### API 3: Ingest PDF

POST /api/documents/ingest

Process the available PDF and save embeddings in ChromaDB.

### API 4: List Documents

GET /api/documents

Return available PDF documents.

### API 5: Retrieval Details

Return retrieval information through the chat response itself or a dedicated API if genuinely required.

Do not build duplicate APIs unnecessarily.

Configure CORS correctly for the React development server.

Use proper HTTP status codes and meaningful error messages.

## 12. REACT FRONTEND REQUIREMENTS

Build a complete student-friendly chat application.

Use React with Vite.

Create a professional responsive interface.

### Header

Include:

- VPro Skills logo
- Application name: Corrective RAG Assistant
- Subtitle: AI-Powered Learning Assistant
- Backend connection status indicator

### Main Layout

Desktop:

- Professional header.
- Main chat section.
- Optional right-side retrieval information panel.
- Clean spacing and alignment.

Mobile:

- Responsive header.
- Chat occupies available width.
- Retrieval information should collapse into an expandable section.
- Input area must remain easy to access.
- Avoid horizontal scrolling.

### Welcome Screen

Display:

"Welcome to VPro Skills AI Learning Assistant"

Subtitle:

"Ask questions about your Python learning materials. I will find relevant information and explain it in simple words."

Include sample question cards:

1. What is Python?
2. Explain Python data types.
3. What is the difference between List and Tuple?
4. Explain Python functions.
5. What is OOPS in Python?

When a student clicks a sample question, automatically populate and submit it.

### Chat Interface

Include:

- Student message bubble.
- AI assistant message bubble.
- Loading animation.
- Typing indicator.
- Auto-scroll to the latest message.
- Chat input field.
- Send button.
- Enter key submission.
- Disabled send button when input is empty.
- Error messages.
- Clear conversation option.

### Rich CSS Styling

Create a polished interface.

Use:

- Modern card layouts.
- Soft shadows.
- Rounded corners.
- Professional typography.
- Smooth transitions.
- Subtle hover effects.
- Responsive grids.
- Attractive buttons.
- Consistent spacing.
- Professional loading indicators.
- Clean icons.
- Beautiful chat bubbles.
- Proper empty states.

Use CSS variables for theme colors.

Avoid excessive animations.

Do not use unnecessary UI libraries.

The interface must look like a professional commercial AI learning application.

## 13. CORRECTIVE RAG VISUALIZATION

This is an important feature.

Students should understand what happens internally when they ask a question.

Provide an expandable panel titled:

"How Corrective RAG Works"

Show the following stages:

1. Question Received
2. Query Processing
3. Initial Document Retrieval
4. Relevance Evaluation
5. Corrective Retrieval (when required)
6. Final Answer Generation

For each stage display:

- Stage name
- Status
- Short explanation
- Relevant retrieval information

Use visual statuses:

- Completed
- In Progress
- Corrected
- Failed

If corrective retrieval is not triggered, clearly display:

"Initial retrieval was relevant. No correction was required."

If corrective retrieval is triggered, visually highlight the correction stage.

Make the workflow easy for students to understand.

## 14. SOURCE DOCUMENT DISPLAY

Below every AI response, provide a Sources section.

Display:

- PDF document name
- Page number
- Relevant extracted text snippet

Allow students to expand and collapse source information.

Do not display fabricated citations.

Every source must correspond to an actual retrieved chunk.

## 15. SECURITY AND VALIDATION

Implement essential security practices.

- Validate incoming questions.
- Limit question length.
- Never expose API keys.
- Use environment variables.
- Validate PDF file types if uploads are supported.
- Restrict file size.
- Handle malformed PDFs.
- Prevent arbitrary filesystem access.
- Add request timeouts where appropriate.
- Avoid logging secrets.
- Handle unexpected exceptions gracefully.

Do not add authentication or role management in this initial version.

## 16. ERROR-HANDLING REQUIREMENTS

This project must be designed to minimize errors.

Handle:

- Backend unavailable.
- React unable to connect to FastAPI.
- Missing environment variables.
- Invalid OpenAI API key.
- Empty ChromaDB collection.
- Missing PDF.
- Invalid PDF.
- Empty PDF content.
- Embedding generation failure.
- Retrieval failure.
- OpenAI response failure.
- Invalid API responses.

Show understandable error messages to students.

Do not expose internal stack traces in the UI.

Keep technical details in backend logs.

## 17. TESTING REQUIREMENTS

Test the complete application.

Backend tests should cover:

1. Health check.
2. PDF extraction.
3. PDF chunking.
4. Document ingestion.
5. ChromaDB storage.
6. Relevant retrieval.
7. Irrelevant retrieval.
8. Query correction.
9. Final answer generation.
10. Missing configuration handling.

Use mocked OpenAI responses for unit tests where appropriate.

Do not require paid OpenAI API calls for every automated test.

Frontend tests should cover basic chat rendering, question submission, loading states, and error handling.

## 18. DOCUMENTATION

Create a detailed README.md.

Include:

- Project overview.
- Architecture.
- Technology stack.
- Folder structure.
- Prerequisites.
- Installation.
- Environment configuration.
- Backend startup.
- Frontend startup.
- PDF ingestion.
- Testing.
- Common errors and solutions.

Provide exact commands for Windows and macOS.

## 19. APPLICATION EXECUTION

Backend:

cd backend

Create virtual environment.

Windows:

python -m venv venv
venv\Scripts\activate

macOS:

python3 -m venv venv
source venv/bin/activate

Install:

pip install -r requirements.txt

Run:

uvicorn app.main:app --reload

Frontend:

cd frontend

npm install

npm run dev

The frontend should run using Vite.

Use a configurable API base URL.

## 20. DEVELOPMENT RULES – VERY IMPORTANT

Follow these rules throughout development:

1. Write only necessary code.
2. Avoid unnecessary packages.
3. Avoid unnecessary abstractions.
4. Do not duplicate code.
5. Do not create unused files.
6. Do not generate fake API responses.
7. Do not use static answers as a substitute for actual RAG.
8. Do not hardcode API keys.
9. Do not expose backend secrets.
10. Do not skip error handling.
11. Do not ignore failed API calls.
12. Do not generate unsupported answers.
13. Use meaningful variable and function names.
14. Follow consistent coding standards.
15. Ensure all frontend APIs match backend response schemas.
16. Verify imports and dependencies.
17. Verify that all application features work together.
18. Keep the application easy for students to understand.
19. Do not add features outside the requested scope.
20. Do not claim successful execution unless you have actually tested it.

## 21. DEVELOPMENT APPROACH

Do not generate the entire application in one huge response.

Develop the application in the following milestones.

### Milestone 1: Project Setup

- Create project folders.
- Create React application.
- Create FastAPI application.
- Configure dependencies.
- Configure environment variables.
- Copy the provided company logo.
- Generate the sample PDF.

Verify both frontend and backend startup.

### Milestone 2: PDF and ChromaDB

- Implement PDF extraction.
- Implement chunking.
- Implement embeddings.
- Implement ChromaDB persistence.
- Implement document ingestion.
- Verify document storage.

### Milestone 3: Basic RAG

- Implement student question API.
- Implement retrieval.
- Implement context preparation.
- Implement OpenAI answer generation.
- Implement source citations.

Test basic RAG before proceeding.

### Milestone 4: Corrective RAG

- Implement relevance evaluator.
- Implement query transformation.
- Implement corrective retrieval.
- Implement retrieval retry limits.
- Implement final relevance validation.
- Implement insufficient-context response.

Test relevant and irrelevant questions.

### Milestone 5: React Frontend

- Build header.
- Add company logo.
- Build welcome screen.
- Build chat interface.
- Add sample questions.
- Connect FastAPI.
- Display responses.
- Display source documents.
- Display corrective RAG workflow.

### Milestone 6: Professional UI

- Apply complete CSS styling.
- Make the application responsive.
- Optimize desktop layout.
- Optimize mobile layout.
- Add loading and error states.
- Verify logo display.

### Milestone 7: Final Testing

- Test complete application.
- Fix errors.
- Check API integration.
- Check document ingestion.
- Check corrective retrieval.
- Check responsive UI.
- Update README.

## 22. FINAL ACCEPTANCE CRITERIA

The project is complete only when:

- React frontend works.
- FastAPI backend works.
- Company logo appears correctly.
- Sample PDF is generated.
- PDF text is extracted.
- Embeddings are generated.
- ChromaDB stores document vectors.
- Student can ask questions.
- Relevant answers are generated.
- Irrelevant retrieval is detected.
- Query correction works.
- Corrective retrieval is demonstrated.
- Sources and page numbers are displayed.
- Insufficient-context questions are handled safely.
- The application works on desktop and mobile.
- Installation documentation is complete.
- Essential tests pass.

## 23. FIRST ACTION

Start with Milestone 1 only.

Before writing code:

1. Inspect the project directory.
2. Locate the provided logo image.
3. Confirm the available Python and Node.js versions.
4. Present the proposed folder structure.
5. Identify the required dependencies.

Then implement Milestone 1.

After completing Milestone 1:

- Run the backend.
- Run the frontend.
- Verify the logo.
- Verify the generated PDF.
- Report the files created and tests performed.

STOP after Milestone 1.

Wait for my instruction:

"Start Milestone 2"

Do not automatically proceed to the next milestone.

Remember: Build a clean, reliable, student-friendly Corrective RAG application for VPro Skills EduTech. Prioritize accuracy, simplicity, maintainability, professional UI, and working functionality.