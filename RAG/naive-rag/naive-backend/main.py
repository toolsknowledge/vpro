# FastAPI - create rest apo's Ex.GET,POST,PUT,DELETE
# UploadFile - upload pdf files
# File - save the uploaded files
from fastapi import FastAPI, UploadFile, File
# CORSMiddleware - connect to frontend (Ex. React,Angular,VueJS,....)
from fastapi.middleware.cors import CORSMiddleware
# PdfReader - read content from pdf file
from pypdf import PdfReader
# SentenceTransformer - create embeddings
from sentence_transformers import SentenceTransformer
# OpenAI - llm
from openai import OpenAI
# load_dotenv - load .env file
from dotenv import load_dotenv
# install chromadb
import chromadb
# os - read data from ".env" file
import os


# Load environment variables
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# FastAPI
app = FastAPI()


# CORS for future ReactJS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="documents"
)

# --------------------------------------------------
# Create chunks
# --------------------------------------------------

def create_chunks(text, chunk_size=500):

    words = text.split()

    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    reader = PdfReader(file.file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    chunks = create_chunks(text)

    embeddings = embedding_model.encode(
        chunks
    ).tolist()

    ids = [
        f"{file.filename}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return {
        "message": "Document uploaded",
        "chunks": len(chunks)
    }


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

@app.post("/ask")
async def ask(question: str):

    question_embedding = embedding_model.encode(
        question
    ).tolist()


    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )


    # Get relevant chunks
    relevant_chunks = results["documents"][0] 


    # Create context
    context = "\n\n".join(
        relevant_chunks
    )


    # Send context + question to LLM
    prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{question}
"""


    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )


    return {
        "answer": response.output_text,
        "context": relevant_chunks
    }
