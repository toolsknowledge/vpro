import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)
from pydantic import BaseModel
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from sentence_transformers import CrossEncoder
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is not set. "
        "Please add it to your .env file."
    )

app = FastAPI(
    title="Advanced RAG with Claude",
    description=(
        "Advanced RAG using Claude, "
        "ChromaDB, HuggingFace and FastAPI"
    ),
    version="1.0.0"
)

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    temperature=0,
    max_tokens=2000,
    api_key=ANTHROPIC_API_KEY
)

embeddings = HuggingFaceEmbeddings(
    model_name=(
        "sentence-transformers/"
        "all-MiniLM-L6-v2"
    )
)

vector_store = Chroma(
    collection_name="advanced_rag",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(
    exist_ok=True
)

class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Advanced RAG with Claude is running",
        "docs": "/docs",
        "upload_endpoint": "/upload",
        "question_endpoint": "/ask"
    }



def load_text_file(file_path: Path) -> List[Document]:
    text = file_path.read_text(encoding="utf-8")
    document = Document(
        page_content=text,
        metadata={
            "source": file_path.name
        }
    )
    return [document]



def load_document(file_path: Path) -> List[Document]:
    extension = file_path.suffix.lower()
    if extension == ".pdf":
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()
        return documents

    elif extension == ".txt":
        return load_text_file(file_path)

    else:
        raise ValueError("Only PDF and TXT files are supported.")


def ingest_document(file_path: Path):
    documents = load_document(file_path)
    for document in documents:
        document.metadata["source"] = file_path.name

    chunks = (text_splitter.split_documents(documents))
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    vector_store.add_documents(documents=chunks)
    return {
        "file": file_path.name,
        "documents": len(documents),
        "chunks": len(chunks)
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):        # file : rag_notes.pdf

    allowed_extensions = {".pdf",".txt"}

    extension = Path(file.filename).suffix.lower()      # rag_notes.pdf

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF and TXT files are supported."
            )
        )

    file_path = (DATA_DIR / file.filename)      # data / rag_notes.pdf

    content = await file.read()
    file_path.write_bytes(content)

    try:
        result = ingest_document(file_path)
        return {
            "message": (
                "Document indexed successfully"
            ),
            **result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# 17. QUERY EXPANSION USING CLAUDE
# ============================================================

def expand_query(
    question: str
) -> List[str]:

    """
    Convert one question into multiple
    search-friendly queries.

    Example:

        What is Advanced RAG?

    Claude may generate:

        What is Advanced RAG?
        Advanced Retrieval Augmented Generation
        Advanced RAG architecture
        Advanced RAG retrieval techniques
    """


    # --------------------------------------------------------
    # PROMPT FOR CLAUDE
    # --------------------------------------------------------

    prompt = f"""
You are a search query optimization expert.

Generate exactly 3 alternative search queries
for the user's question.

Rules:

1. Preserve the original meaning.
2. Use different terminology.
3. Make each query useful for semantic search.
4. Return ONLY the queries.
5. Return one query per line.
6. Do not number the queries.
7. Do not explain anything.

User Question:

{question}
"""


    # --------------------------------------------------------
    # SEND PROMPT TO CLAUDE
    # --------------------------------------------------------

    response = llm.invoke(
        prompt
    )


    # --------------------------------------------------------
    # GET CLAUDE RESPONSE
    # --------------------------------------------------------

    text = response.content.strip()


    # --------------------------------------------------------
    # CONVERT RESPONSE INTO LIST
    # --------------------------------------------------------

    queries = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


    # --------------------------------------------------------
    # ADD ORIGINAL QUESTION
    # --------------------------------------------------------

    queries.insert(
        0,
        question
    )


    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    unique_queries = []

    for query in queries:

        if query not in unique_queries:

            unique_queries.append(
                query
            )


    # Return maximum four queries.
    return unique_queries[:4]


# ============================================================
# 18. MULTI-QUERY RETRIEVAL
# ============================================================

def retrieve_candidates(
    queries: List[str],
    k: int = 5
):

    """
    Search ChromaDB using multiple queries.

    Example:

        Query 1 → ChromaDB
        Query 2 → ChromaDB
        Query 3 → ChromaDB
        Query 4 → ChromaDB

                    ↓

             Combine Results

                    ↓

             Remove Duplicates
    """


    all_documents = []


    # --------------------------------------------------------
    # SEARCH FOR EVERY QUERY
    # --------------------------------------------------------

    for query in queries:

        documents = (
            vector_store.similarity_search(
                query,
                k=k
            )
        )


        all_documents.extend(
            documents
        )


    # --------------------------------------------------------
    # REMOVE DUPLICATE DOCUMENTS
    # --------------------------------------------------------

    unique_documents = {}


    for document in all_documents:

        source = document.metadata.get(
            "source",
            "unknown"
        )


        chunk_id = document.metadata.get(
            "chunk_id",
            ""
        )


        # Create unique key.
        key = (
            f"{source}_{chunk_id}"
        )


        unique_documents[key] = (
            document
        )


    # Return unique documents.
    return list(
        unique_documents.values()
    )


# ============================================================
# 19. CROSS-ENCODER RE-RANKING
# ============================================================

def rerank_documents(
    question: str,
    documents: list,
    top_n: int = 5
):

    """
    Re-rank candidate documents.

    Vector search:
        Finds possible documents.

    Cross Encoder:
        Finds the most relevant documents.
    """


    # If no documents exist.
    if not documents:

        return []


    # --------------------------------------------------------
    # CREATE QUESTION + DOCUMENT PAIRS
    # --------------------------------------------------------

    pairs = []


    for document in documents:

        pairs.append(
            (
                question,
                document.page_content
            )
        )


    # --------------------------------------------------------
    # CALCULATE RELEVANCE SCORES
    # --------------------------------------------------------

    scores = reranker.predict(
        pairs
    )


    # --------------------------------------------------------
    # COMBINE DOCUMENTS + SCORES
    # --------------------------------------------------------

    ranked = list(
        zip(
            documents,
            scores
        )
    )


    # --------------------------------------------------------
    # SORT BY SCORE
    # --------------------------------------------------------

    ranked.sort(
        key=lambda item: float(
            item[1]
        ),
        reverse=True
    )


    # --------------------------------------------------------
    # RETURN TOP DOCUMENTS
    # --------------------------------------------------------

    return ranked[:top_n]


# ============================================================
# 20. BUILD CONTEXT
# ============================================================

def build_context(
    ranked_documents
):

    """
    Convert the best retrieved documents
    into context that will be sent to Claude.
    """


    context_parts = []

    sources = []


    # --------------------------------------------------------
    # PROCESS EACH DOCUMENT
    # --------------------------------------------------------

    for index, (
        document,
        score
    ) in enumerate(
        ranked_documents,
        start=1
    ):


        # Get source name.
        source = document.metadata.get(
            "source",
            "unknown"
        )


        # PDF pages are zero-indexed.
        page = document.metadata.get(
            "page"
        )


        if page is not None:

            source_name = (
                f"{source}, page {page + 1}"
            )

        else:

            source_name = source


        # ----------------------------------------------------
        # ADD CONTENT TO CONTEXT
        # ----------------------------------------------------

        context_parts.append(
            f"""
[Context {index}]

Source:
{source_name}

Content:
{document.page_content}
"""
        )


        # ----------------------------------------------------
        # SAVE SOURCE INFORMATION
        # ----------------------------------------------------

        sources.append(
            {
                "source": source_name,
                "score": round(
                    float(score),
                    4
                )
            }
        )


    # Combine all contexts.
    context = "\n\n".join(
        context_parts
    )


    return context, sources


# ============================================================
# 21. GENERATE FINAL ANSWER USING CLAUDE
# ============================================================

def generate_answer(
    question: str,
    context: str
):

    """
    Claude receives:

        User Question
              +
        Retrieved Context

    and generates a grounded answer.
    """


    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are a professional AI teaching assistant.

Answer the user's question using ONLY
the provided context.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not available in
   the provided context, say:

   "The information is not available
    in the provided documents."

4. Explain the answer clearly.
5. Use examples when the context supports them.
6. Keep the answer educational.
7. Do not mention internal retrieval processes.

==================================================
CONTEXT
==================================================

{context}

==================================================
QUESTION
==================================================

{question}

==================================================
ANSWER
==================================================
"""


    # --------------------------------------------------------
    # SEND TO CLAUDE
    # --------------------------------------------------------

    response = llm.invoke(
        prompt
    )


    # Return Claude's answer.
    return response.content


# ============================================================
# 22. ASK QUESTION API
# ============================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    """
    Complete Advanced RAG query pipeline:

        Question
           ↓
        Query Expansion
           ↓
        Multi Query Retrieval
           ↓
        Deduplication
           ↓
        Re-Ranking
           ↓
        Context
           ↓
        Claude
           ↓
        Answer
    """


    # --------------------------------------------------------
    # STEP 1: GET USER QUESTION
    # --------------------------------------------------------

    question = (request.question.strip())


    # Check empty question.
    if not question:

        raise HTTPException(
            status_code=400,
            detail=(
                "Question cannot be empty."
            )
        )


    # ========================================================
    # STEP 2: QUERY EXPANSION
    # ========================================================

    queries = expand_query(question)


    # ========================================================
    # STEP 3: MULTI-QUERY RETRIEVAL
    # ========================================================
    candidates = (
        retrieve_candidates(
            queries,
            k=5
        )
    )


    # If nothing was retrieved.
    if not candidates:

        return {
            "question": question,
            "answer": (
                "No relevant documents found."
            ),
            "generated_queries": queries,
            "candidate_documents": 0,
            "selected_documents": 0,
            "sources": []
        }


    # ========================================================
    # STEP 4: RE-RANKING
    # ========================================================

    ranked_documents = (
        rerank_documents(
            question,
            candidates,
            top_n=5
        )
    )


    # ========================================================
    # STEP 5: BUILD CONTEXT
    # ========================================================

    context, sources = (
        build_context(
            ranked_documents
        )
    )


    # ========================================================
    # STEP 6: GENERATE ANSWER USING CLAUDE
    # ========================================================

    answer = generate_answer(
        question,
        context
    )


    # ========================================================
    # STEP 7: RETURN RESPONSE
    # ========================================================

    return {
        "question": question,

        "answer": answer,

        "generated_queries": queries,

        "candidate_documents": len(
            candidates
        ),

        "selected_documents": len(
            ranked_documents
        ),

        "sources": sources
    }


# ============================================================
# 23. START FASTAPI SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn


    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )