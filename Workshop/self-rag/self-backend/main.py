import os
import shutil

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pypdf import PdfReader


# --------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHAT_MODEL = os.getenv(
    "OPENAI_CHAT_MODEL",
    "gpt-4o-mini"
)

EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL",
    "text-embedding-3-small"
)


# --------------------------------------------------
# 2. OPENAI CLIENT
# --------------------------------------------------

client = OpenAI(api_key=OPENAI_API_KEY)


# --------------------------------------------------
# 3. FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Self-RAG Demo",
    description="Simple Self-RAG application"
)


# --------------------------------------------------
# 4. CORS
# --------------------------------------------------
# This allows future HTML/CSS/JavaScript or React
# applications to call this FastAPI backend.
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 5. CHROMA DB
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)


# --------------------------------------------------
# 6. UPLOAD DIRECTORY
# --------------------------------------------------

os.makedirs("uploads", exist_ok=True)


# ==================================================
# HELPER FUNCTIONS
# ==================================================


# --------------------------------------------------
# Create embedding
# --------------------------------------------------

def create_embedding(text):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


# --------------------------------------------------
# Ask LLM
# --------------------------------------------------

def ask_llm(prompt):

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


# --------------------------------------------------
# Split text into simple chunks
# --------------------------------------------------

def split_text(text, chunk_size=800):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


# --------------------------------------------------
# Read uploaded file
# --------------------------------------------------

def read_file(file_path):

    if file_path.lower().endswith(".pdf"):

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    else:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()


# ==================================================
# SELF-RAG FUNCTIONS
# ==================================================


# --------------------------------------------------
# STEP 1
# RETRIEVE DECISION
# --------------------------------------------------

def should_retrieve(question):

    prompt = f"""
You are the retrieval decision component of a Self-RAG system.

The application has a private knowledge base containing
company information, courses, trainers, services, technologies,
projects and other organization-specific information.

User question:
{question}

Decide whether the answer should come from the private
knowledge base.

Return ONLY one word:

YES
or
NO

Rules:

1. If the question asks about the company, organization,
   courses, trainers, services, products, technologies,
   projects, contact information, or any information that
   may exist in the private knowledge base, return YES.

2. If the question is general knowledge that does not require
   the private knowledge base, return NO.

3. When uncertain, return YES.

Examples:

Question: What is the company name?
Answer: YES

Question: What courses does the company provide?
Answer: YES

Question: Who is the trainer?
Answer: YES

Question: What technologies do you provide training on?
Answer: YES

Question: What is the capital of India?
Answer: NO

Question: What is Python?
Answer: NO

Question: Explain machine learning.
Answer: NO

Now classify the user question.

Return ONLY:
YES
or
NO
"""

    result = ask_llm(prompt)

    result = result.strip().upper()

    return result == "YES"

# --------------------------------------------------
# STEP 2
# RETRIEVE DOCUMENTS
# --------------------------------------------------

def retrieve_documents(question, top_k=3):

    question_embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]

    return documents


# --------------------------------------------------
# STEP 3
# ISREL CHECK
# --------------------------------------------------

def check_relevance(question, documents):

    if not documents:
        return False

    context = "\n\n".join(documents)

    prompt = f"""
You are a Self-RAG relevance evaluator.

Question:
{question}

Retrieved information:
{context}

Is the retrieved information relevant to
answering the question?

Return ONLY:

YES

or

NO
"""

    result = ask_llm(prompt)

    return result.upper().startswith("YES")


# --------------------------------------------------
# STEP 4
# GENERATE ANSWER
# --------------------------------------------------

def generate_answer(question, documents=None):

    if documents:

        context = "\n\n".join(documents)

        prompt = f"""
Answer the user's question using the provided
knowledge base information.

Knowledge base:
{context}

Question:
{question}

Rules:

1. Use the knowledge base when relevant.
2. Do not invent facts.
3. If the information is not available,
   clearly say that it is not available.
4. Give a simple and useful answer.
"""

    else:

        prompt = f"""
Answer the following question using your
general knowledge.

Question:
{question}

Give a clear and useful answer.
"""

    return ask_llm(prompt)


# --------------------------------------------------
# STEP 5
# ISSUP CHECK
# --------------------------------------------------

def check_support(question, answer, documents):

    context = "\n\n".join(documents)

    prompt = f"""
You are a Self-RAG answer evaluator.

Question:
{question}

Retrieved information:
{context}

Generated answer:
{answer}

Is the generated answer supported by the
retrieved information?

Return ONLY:

YES

or

NO
"""

    result = ask_llm(prompt)

    return result.upper().startswith("YES")


# --------------------------------------------------
# STEP 6
# ISUSE CHECK
# --------------------------------------------------

def check_usefulness(question, answer):

    prompt = f"""
You are a Self-RAG usefulness evaluator.

Question:
{question}

Answer:
{answer}

Is this answer useful, clear and does it
actually resolve the user's question?

Return ONLY:

YES

or

NO
"""

    result = ask_llm(prompt)

    return result.upper().startswith("YES")


# --------------------------------------------------
# STEP 7
# IMPROVE ANSWER
# --------------------------------------------------

def improve_answer(question, answer, documents):

    context = "\n\n".join(documents)

    prompt = f"""
You are improving an answer in a Self-RAG system.

Question:
{question}

Knowledge base:
{context}

Previous answer:
{answer}

Create a better answer.

Rules:

1. Use only information supported by the
   knowledge base.
2. Do not invent information.
3. Correct unsupported statements.
4. Make the answer clear and useful.
"""

    return ask_llm(prompt)


# ==================================================
# API ENDPOINTS
# ==================================================


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Self-RAG API is running"
    }


# --------------------------------------------------
# UPLOAD DOCUMENT
# --------------------------------------------------

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    text = read_file(file_path)

    chunks = split_text(text)

    if not chunks:

        return {
            "message": "No text found in file"
        }

    # Store chunks in ChromaDB

    for index, chunk in enumerate(chunks):

        embedding = create_embedding(chunk)

        collection.add(
            ids=[
                f"{file.filename}-{index}"
            ],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": file.filename
                }
            ]
        )

    return {
        "message": "Document uploaded successfully",
        "file": file.filename,
        "chunks": len(chunks)
    }


# --------------------------------------------------
# ASK QUESTION
# --------------------------------------------------

@app.post("/ask")
async def ask_question(question: str):

    # ==============================================
    # 1. SELF-RAG DECISION
    # ==============================================

    retrieve = should_retrieve(question)


    # ==============================================
    # 2. NO RETRIEVAL
    # ==============================================

    if not retrieve:

        answer = generate_answer(question)

        return {
            "question": question,
            "retrieve": False,
            "answer": answer
        }


    # ==============================================
    # 3. RETRIEVE
    # ==============================================

    documents = retrieve_documents(question)


    # ==============================================
    # 4. ISREL CHECK
    # ==============================================

    relevant = check_relevance(
        question,
        documents
    )

    if not relevant:

        return {
            "question": question,
            "retrieve": True,
            "relevant": False,
            "answer": "I could not find relevant information in the knowledge base."
        }


    # ==============================================
    # 5. GENERATE
    # ==============================================

    answer = generate_answer(
        question,
        documents
    )


    # ==============================================
    # 6. ISSUP CHECK
    # ==============================================

    supported = check_support(
        question,
        answer,
        documents
    )


    # ==============================================
    # 7. IMPROVE IF NOT SUPPORTED
    # ==============================================

    if not supported:

        answer = improve_answer(
            question,
            answer,
            documents
        )


    # ==============================================
    # 8. ISUSE CHECK
    # ==============================================

    useful = check_usefulness(
        question,
        answer
    )


    # ==============================================
    # 9. FINAL IMPROVEMENT
    # ==============================================

    if not useful:

        answer = improve_answer(
            question,
            answer,
            documents
        )


    # ==============================================
    # 10. FINAL ANSWER
    # ==============================================

    return {

        "question": question,

        "self_rag": {

            "retrieve": retrieve,

            "relevant": relevant,

            "supported": supported,

            "useful": useful
        },

        "answer": answer
    }