
import os
from io import BytesIO

import faiss
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from pypdf import PdfReader


# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL",
    "text-embedding-3-small"
)

app = FastAPI(title="Naive RAG Application")

# Allow a future React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stored in memory while the backend is running
chunks = []
vector_index = None


# STEP 3: Split text into chunks
def split_into_chunks(text, chunk_size=800, overlap=150):
    text = " ".join(text.split())       
    result = []

    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            result.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return result


# STEP 4: Convert text into embeddings
def create_embeddings(text_list):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text_list
    )

    vectors = [item.embedding for item in response.data]

    return np.array(vectors, dtype="float32")


# STEP 1 and STEP 2: Upload and read PDF
@app.post("/upload-pdf")        # React
async def upload_pdf(file: UploadFile = File(...)):
    global chunks, vector_index

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    try:
        pdf_bytes = await file.read()
        reader = PdfReader(BytesIO(pdf_bytes))

        # Extract text from every PDF page
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF."
            )

        # STEP 3: Chunking
        new_chunks = split_into_chunks(text)

        # STEP 4: Create embeddings
        embeddings = create_embeddings(new_chunks)

        # Normalize vectors for cosine similarity search
        faiss.normalize_L2(embeddings)

        # STEP 5: Store vectors in FAISS
        new_index = faiss.IndexFlatIP(embeddings.shape[1])
        new_index.add(embeddings)

        # Replace the previous document's index
        chunks = new_chunks
        vector_index = new_index

        return {
            "message": "PDF uploaded and indexed successfully",
            "filename": file.filename,
            "total_pages": len(reader.pages),
            "total_chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(e)}"
        )


# STEP 6, 7 and 8: Ask a question
class Question(BaseModel):
    question: str


@app.post("/ask")               # ReactJS
def ask_question(data: Question):
    if vector_index is None or not chunks:
        raise HTTPException(
            status_code=400,
            detail="Upload a PDF before asking questions."
        )

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    try:
        # Convert the question into an embedding
        query_embedding = create_embeddings([data.question])
        faiss.normalize_L2(query_embedding)

        # STEP 7: Find the 3 most relevant chunks
        k = min(3, len(chunks))

        scores, indices = vector_index.search(query_embedding, k)

        retrieved_chunks = [
            chunks[i]
            for i in indices[0]
            if i >= 0
        ]

        context = "\n\n".join(retrieved_chunks)

        # STEP 8: Generate an answer using OpenAI
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer using only the provided document context. "
                        "If the answer is not available in the context, "
                        "say: 'The answer was not found in the uploaded "
                        "document.' Do not invent facts."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Document context:\n{context}\n\n"
                        f"Question: {data.question}"
                    )
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        return {
            "question": data.question,
            "answer": answer,
            "retrieved_chunks": retrieved_chunks
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(e)}"
        )


# Health check
@app.get("/")
def home():
    return {
        "message": "Naive RAG API is running",
        "pdf_uploaded": vector_index is not None
    }

