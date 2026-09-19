import os
import json
import re
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is missing in .env"
    )

# connect to llm
client = OpenAI(
    api_key=OPENAI_API_KEY
)

# Use a cost-efficient model for evaluation.
LLM_MODEL = "gpt-5.6-luna"

EMBEDDING_MODEL = "text-embedding-3-small"

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"

DOCUMENT_DIR = DATA_DIR / "documents"

CHROMA_DIR = DATA_DIR / "chroma"

EVALUATION_FILE = DATA_DIR / "evaluation.json"

DOCUMENT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CHROMA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="RAG Evaluation Application",
    description=(
        "Evaluate RAG retrieval and generated answers"
    ),
    version="1.0"
)


# ============================================================
# CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

# name of the table is "evaluation_documents"
collection = chroma_client.get_or_create_collection(
    name="evaluation_documents"
)


# ============================================================
# MODELS
# ============================================================

class QuestionRequest(BaseModel):

    question: str


# ============================================================
# EMBEDDING
# ============================================================

def create_embedding(text):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


# ============================================================
# TEXT CHUNKING
# ============================================================

def chunk_text(
    text,
    chunk_size=500,
    overlap=50
):

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start = end - overlap

        if end >= len(text):
            break

    return chunks


# ============================================================
# INDEX DOCUMENTS
# ============================================================

def index_documents():

    # Avoid duplicate indexing
    if collection.count() > 0:
        return

    for file_path in DOCUMENT_DIR.iterdir():

        if file_path.suffix.lower() != ".txt":
            continue

        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):

            chunk_id = (
                f"{file_path.name}-{index}"
            )

            embedding = create_embedding(
                chunk
            )

            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                metadatas=[{
                    "filename": file_path.name,
                    "chunk_index": index
                }],
                embeddings=[embedding]
            )


# ============================================================
# RETRIEVE
# ============================================================

def retrieve(
    question,
    top_k=3
):

    question_embedding = create_embedding(
        question
    )

    result = collection.query(
        query_embeddings=[
            question_embedding
        ],
        n_results=top_k
    )

    documents = result.get(
        "documents",
        [[]]
    )[0]

    metadatas = result.get(
        "metadatas",
        [[]]
    )[0]

    distances = result.get(
        "distances",
        [[]]
    )[0]

    return (
        documents,
        metadatas,
        distances
    )


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(
    question,
    documents
):

    context = "\n\n".join(
        documents
    )

    instructions = """
You are a RAG assistant.

Answer the user's question using only
the provided context.

Do not invent information.

If the answer is not available in the
context, say that it is not available.

Give a short and simple answer.
"""

    prompt = f"""
Question:

{question}

Context:

{context}
"""

    response = client.responses.create(
        model=LLM_MODEL,
        instructions=instructions,
        input=prompt,
        store=False
    )

    return response.output_text.strip()


# ============================================================
# LLM EVALUATION
# ============================================================

def evaluate_with_llm(
    question,
    context,
    answer,
    expected_answer
):

    evaluation_prompt = f"""
Evaluate the following RAG response.

QUESTION:
{question}

RETRIEVED CONTEXT:
{context}

GENERATED ANSWER:
{answer}

EXPECTED ANSWER:
{expected_answer}

Evaluate these three things:

1. FAITHFULNESS

Is the generated answer supported by
the retrieved context?

2. RELEVANCE

Does the generated answer directly
answer the question?

3. CORRECTNESS

Is the generated answer consistent
with the expected answer?

Give each score from 0 to 1.

Return ONLY valid JSON:

{{
    "faithfulness": 0.0,
    "relevance": 0.0,
    "correctness": 0.0,
    "reason": "short explanation"
}}
"""

    response = client.responses.create(
        model=LLM_MODEL,
        input=evaluation_prompt,
        store=False
    )

    text = response.output_text.strip()

    # Remove markdown code fences if model returns them.
    text = re.sub(
        r"^```json\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    try:

        result = json.loads(text)

    except json.JSONDecodeError:

        return {
            "faithfulness": 0,
            "relevance": 0,
            "correctness": 0,
            "reason": (
                "Evaluator returned invalid JSON."
            )
        }

    return result


# ============================================================
# PRECISION
# ============================================================

def calculate_precision(
    retrieved_sources,
    expected_sources
):

    if not retrieved_sources:

        return 0

    relevant = 0

    for source in retrieved_sources:

        if source in expected_sources:

            relevant += 1

    return relevant / len(
        retrieved_sources
    )


# ============================================================
# RECALL
# ============================================================

def calculate_recall(
    retrieved_sources,
    expected_sources
):

    if not expected_sources:

        return 0

    relevant = 0

    for source in expected_sources:

        if source in retrieved_sources:

            relevant += 1

    return relevant / len(
        expected_sources
    )


# ============================================================
# RUN SINGLE EVALUATION
# ============================================================

def evaluate_question(
    question,
    expected_answer,
    expected_sources
):

    (
        documents,
        metadatas,
        distances
    ) = retrieve(
        question
    )

    retrieved_sources = []

    for metadata in metadatas:

        filename = metadata.get(
            "filename"
        )

        if filename not in retrieved_sources:

            retrieved_sources.append(
                filename
            )

    context = "\n\n".join(
        documents
    )

    answer = generate_answer(
        question,
        documents
    )

    precision = calculate_precision(
        retrieved_sources,
        expected_sources
    )

    recall = calculate_recall(
        retrieved_sources,
        expected_sources
    )

    llm_scores = evaluate_with_llm(
        question,
        context,
        answer,
        expected_answer
    )

    overall = (
        precision
        + recall
        + llm_scores["faithfulness"]
        + llm_scores["relevance"]
        + llm_scores["correctness"]
    ) / 5

    return {

        "question": question,

        "expected_answer": expected_answer,

        "generated_answer": answer,

        "retrieved_sources": retrieved_sources,

        "expected_sources": expected_sources,

        "precision": round(
            precision,
            2
        ),

        "recall": round(
            recall,
            2
        ),

        "faithfulness": round(
            float(
                llm_scores["faithfulness"]
            ),
            2
        ),

        "relevance": round(
            float(
                llm_scores["relevance"]
            ),
            2
        ),

        "correctness": round(
            float(
                llm_scores["correctness"]
            ),
            2
        ),

        "overall_score": round(
            overall,
            2
        ),

        "reason": llm_scores.get(
            "reason",
            ""
        )
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {

        "status": "running",

        "documents": collection.count(),

        "evaluation_dataset":
            EVALUATION_FILE.exists()

    }


# ============================================================
# INDEX
# ============================================================

@app.post("/index")
def index():

    index_documents()

    return {

        "message":
            "Documents indexed successfully.",

        "chunks":
            collection.count()

    }


# ============================================================
# ASK
# ============================================================

@app.post("/ask")
def ask(
    request: QuestionRequest
):

    documents, metadatas, distances = retrieve(
        request.question
    )

    if not documents:

        raise HTTPException(
            status_code=404,
            detail="No documents found."
        )

    answer = generate_answer(
        request.question,
        documents
    )

    sources = []

    for metadata in metadatas:

        filename = metadata.get(
            "filename"
        )

        if filename not in sources:

            sources.append(
                filename
            )

    return {

        "question":
            request.question,

        "answer":
            answer,

        "sources":
            sources,

        "retrieved_chunks":
            len(documents)

    }


# ============================================================
# EVALUATE ONE QUESTION
# ============================================================

@app.post("/evaluate")
def evaluate_single(
    request: QuestionRequest
):

    if not EVALUATION_FILE.exists():

        raise HTTPException(
            status_code=404,
            detail="evaluation.json not found."
        )

    dataset = json.loads(
        EVALUATION_FILE.read_text(
            encoding="utf-8"
        )
    )

    for item in dataset:

        if (
            item["question"].lower().strip()
            ==
            request.question.lower().strip()
        ):

            return evaluate_question(

                item["question"],

                item["expected_answer"],

                item["expected_sources"]

            )

    raise HTTPException(
        status_code=404,
        detail=(
            "Question not found in evaluation dataset."
        )
    )


# ============================================================
# EVALUATE COMPLETE DATASET
# ============================================================

@app.post("/evaluate-all")
def evaluate_all():

    if not EVALUATION_FILE.exists():

        raise HTTPException(
            status_code=404,
            detail="evaluation.json not found."
        )

    dataset = json.loads(
        EVALUATION_FILE.read_text(
            encoding="utf-8"
        )
    )

    results = []

    for item in dataset:

        result = evaluate_question(

            item["question"],

            item["expected_answer"],

            item["expected_sources"]

        )

        results.append(result)

    if not results:

        raise HTTPException(
            status_code=400,
            detail="Evaluation dataset is empty."
        )

    average_precision = sum(
        item["precision"]
        for item in results
    ) / len(results)

    average_recall = sum(
        item["recall"]
        for item in results
    ) / len(results)

    average_faithfulness = sum(
        item["faithfulness"]
        for item in results
    ) / len(results)

    average_relevance = sum(
        item["relevance"]
        for item in results
    ) / len(results)

    average_correctness = sum(
        item["correctness"]
        for item in results
    ) / len(results)

    overall = (
        average_precision
        + average_recall
        + average_faithfulness
        + average_relevance
        + average_correctness
    ) / 5

    return {

        "evaluation_summary": {

            "questions_evaluated":
                len(results),

            "precision":
                round(
                    average_precision,
                    2
                ),

            "recall":
                round(
                    average_recall,
                    2
                ),

            "faithfulness":
                round(
                    average_faithfulness,
                    2
                ),

            "relevance":
                round(
                    average_relevance,
                    2
                ),

            "correctness":
                round(
                    average_correctness,
                    2
                ),

            "overall_score":
                round(
                    overall,
                    2
                )
        },

        "results":
            results

    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "application":
            "RAG Evaluation Application",

        "docs":
            "/docs",

        "endpoints": [

            "/health",

            "/index",

            "/ask",

            "/evaluate",

            "/evaluate-all"

        ]

    }