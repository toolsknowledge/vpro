import os
import re
import hashlib
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader

from openai import OpenAI
from sentence_transformers import SentenceTransformer, CrossEncoder


# ============================================================
# 1. CONFIGURATION
# ============================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

BASE_DIR = Path(__file__).resolve().parent

DATA_FOLDER = BASE_DIR / "data"
CHROMA_FOLDER = BASE_DIR / "chroma_db"

DATA_FOLDER.mkdir(exist_ok=True)
CHROMA_FOLDER.mkdir(exist_ok=True)


# ============================================================
# 2. LOAD MODELS
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Loading reranker...")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


# ============================================================
# 3. CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_FOLDER)
)

collection = chroma_client.get_or_create_collection(
    name="advanced_rag"
)


# ============================================================
# 4. FASTAPI
# ============================================================

app = FastAPI(
    title="Advanced RAG Application"
)


# ReactJS can call this API later
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# 5. REQUEST MODEL
# ============================================================

class Question(BaseModel):

    question: str


# ============================================================
# 6. READ PDF
# ============================================================

def read_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ============================================================
# 7. CHUNK DOCUMENT
# ============================================================

def create_chunks(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    chunk_size = 700
    overlap = 100

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start = end - overlap

    return chunks


# ============================================================
# 8. STORE DOCUMENT IN CHROMADB
# ============================================================

def store_document(file_path, file_name):

    print(f"Reading {file_name}...")

    text = read_pdf(file_path)

    if not text.strip():

        raise ValueError(
            "Could not extract text from the PDF."
        )

    print("Creating chunks...")

    chunks = create_chunks(text)

    print("Creating embeddings...")

    embeddings = embedding_model.encode(
        chunks,
        normalize_embeddings=True
    ).tolist()

    ids = []

    metadatas = []

    for index in range(len(chunks)):

        # Create a unique ID for each document chunk
        chunk_id = hashlib.md5(
            f"{file_name}-{index}".encode()
        ).hexdigest()

        ids.append(chunk_id)

        metadatas.append({
            "source": file_name,
            "chunk": index + 1
        })

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Stored {len(chunks)} chunks in ChromaDB"
    )

    return len(chunks)


# ============================================================
# 9. QUERY EXPANSION
# ============================================================

def expand_query(question):

    prompt = f"""
Generate 3 alternative search queries for the
following user question.

Keep the same meaning.

Return only the queries.
One query per line.

Question:
{question}
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )

    queries = response.output_text.strip().split("\n")

    queries = [
        query.strip("- ").strip()
        for query in queries
        if query.strip()
    ]

    # Keep the original question
    queries.insert(0, question)

    return queries[:4]


# ============================================================
# 10. VECTOR SEARCH
# ============================================================

def vector_search(query, top_k=5):

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas"
        ]
    )

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    results = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        results.append({
            "document": document,
            "metadata": metadata
        })

    return results


# ============================================================
# 11. KEYWORD SEARCH
# ============================================================

def keyword_search(question, top_k=5):

    # Extract words from the question
    words = re.findall(
        r"\b[a-zA-Z0-9]{3,}\b",
        question.lower()
    )

    data = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )

    documents = data["documents"]

    metadatas = data["metadatas"]

    results = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        score = 0

        document_lower = document.lower()

        for word in words:

            if word in document_lower:
                score += 1

        if score > 0:

            results.append({
                "document": document,
                "metadata": metadata,
                "keyword_score": score
            })

    # Highest keyword score first
    results.sort(
        key=lambda x: x["keyword_score"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# 12. HYBRID SEARCH
# ============================================================

def hybrid_search(question):

    # ----------------------------------------
    # Query Expansion
    # ----------------------------------------

    queries = expand_query(question)

    all_results = []

    # ----------------------------------------
    # Vector Search
    # ----------------------------------------

    for query in queries:

        results = vector_search(
            query,
            top_k=5
        )

        all_results.extend(results)

    # ----------------------------------------
    # Keyword Search
    # ----------------------------------------

    keyword_results = keyword_search(
        question,
        top_k=5
    )

    all_results.extend(keyword_results)

    # ----------------------------------------
    # Remove duplicate chunks
    # ----------------------------------------

    unique_documents = {}

    for result in all_results:

        document = result["document"]

        unique_documents[document] = result

    return list(
        unique_documents.values()
    )


# ============================================================
# 13. RERANKING
# ============================================================

def rerank(
    question,
    documents,
    top_k=3
):

    if not documents:
        return []

    pairs = []

    for item in documents:

        pairs.append([
            question,
            item["document"]
        ])

    # Cross-Encoder calculates relevance
    scores = reranker.predict(pairs)

    for item, score in zip(
        documents,
        scores
    ):

        item["rerank_score"] = float(score)

    # Highest relevance first
    documents.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return documents[:top_k]


# ============================================================
# 14. BUILD CONTEXT
# ============================================================

def build_context(documents):

    context = ""

    for item in documents:

        context += "\n"
        context += item["document"]
        context += "\n"

    return context


# ============================================================
# 15. GENERATE ANSWER
# ============================================================

def generate_answer(
    question,
    context
):

    prompt = f"""
You are a helpful RAG assistant.

Answer the question using ONLY the
information provided in the context.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not present in the context,
   say:
   "I could not find the answer in the documents."

Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )

    return response.output_text


# ============================================================
# 16. ADVANCED RAG PIPELINE
# ============================================================

def advanced_rag(question):

    # Step 1:
    # Query Expansion + Vector Search + Keyword Search
    documents = hybrid_search(question)

    # Step 2:
    # Reranking
    documents = rerank(
        question,
        documents,
        top_k=3
    )

    # Step 3:
    # Build Context
    context = build_context(documents)

    # Step 4:
    # Send Context + Question to LLM
    answer = generate_answer(
        question,
        context
    )

    # Step 5:
    # Return answer and sources
    return {
        "question": question,
        "answer": answer,
        "sources": [
            item["metadata"]
            for item in documents
        ]
    }


# ============================================================
# 17. UPLOAD API
# ============================================================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_path = DATA_FOLDER / file.filename

    content = await file.read()

    file_path.write_bytes(content)

    try:

        chunk_count = store_document(
            file_path,
            file.filename
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename,
        "chunks": chunk_count
    }

# ============================================================
# 18. ASK API
# ============================================================

@app.post("/ask")
def ask_question(request: Question):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Run Advanced RAG
    result = advanced_rag(
        request.question
    )

    return result


# ============================================================
# 19. START APPLICATION
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )