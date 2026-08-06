from fastapi import FastAPI
from pydantic import BaseModel

from embeddings.embedding_model import get_embedding_model
from vector_store.vector_db import load_vector_db
from retriever.retriever import get_retriever
from llm.llm import get_llm
from prompts.rag_prompt import RAG_PROMPT


app = FastAPI(
    title="RAG Application API",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


print("Loading Embedding Model...")
embedding_model = get_embedding_model()

print("Loading Vector Database...")
vector_db = load_vector_db(embedding_model)

print("Creating Retriever...")
retriever = get_retriever(vector_db)

print("Loading LLM...")
llm = get_llm()

print("RAG API Ready...")


@app.get("/")
def home():
    return {
        "message": "Welcome to RAG API"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    docs = retriever.invoke(request.question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = RAG_PROMPT.format(
        context=context,
        question=request.question
    )

    response = llm.invoke(prompt)

    return {
        "question": request.question,
        "answer": response.content
    }