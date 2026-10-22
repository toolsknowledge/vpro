
import os
import numpy as np
import faiss

from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

load_dotenv()

# connect to LLM (OPEN AI)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4.1-mini"


# STEP 1: Read text from TXT file and create chunkings also
def load_chunks():
    file_path = Path(__file__).resolve().parent / "sample.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return [p.strip() for p in text.split("\n\n") if p.strip()]


# STEP 2: Generate embeddings
def get_embeddings(texts):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return np.array(
        [item.embedding for item in response.data],
        dtype="float32"
    )


# STEP 3: Create FAISS index
def build_index(chunks):
    embeddings = get_embeddings(chunks)
    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


# STEP 4: Retrieve relevant chunks (similarity search)
def retrieve(query, chunks, index, top_k=3):
    query_embedding = get_embeddings([query])
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(
        query_embedding,
        min(top_k, index.ntotal)
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx != -1:
            results.append({
                "text": chunks[idx],
                "score": float(score)
            })

    return results


# STEP 5: Evaluate retrieval quality
def evaluate_retrieval(query, results):
    context = "\n\n".join(r["text"] for r in results)

    response = client.responses.create(
        model=LLM_MODEL,
        input=f"""
You are a retrieval quality evaluator.

Question: {query}

Retrieved documents:
{context}

Are the retrieved documents sufficient and relevant
to answer the question accurately?

Reply with only YES or NO.
"""
    )

    return response.output_text.strip().upper().startswith("YES")


# STEP 6: Rewrite query if retrieval is poor
def rewrite_query(query):
    response = client.responses.create(
        model=LLM_MODEL,
        input=f"""
Rewrite this question as a clear search query.
Preserve the original meaning.
Return only the rewritten query.

Question: {query}
"""
    )

    return response.output_text.strip()


# STEP 7: Generate final answer
def generate_answer(query, results):
    context = "\n\n".join(r["text"] for r in results)

    response = client.responses.create(
        model=LLM_MODEL,
        input=f"""
Answer using only the context below.
If the answer is unavailable, say:
"I don't have enough information to answer."

Context:
{context}

Question: {query}

Answer:
"""
    )

    return response.output_text.strip()


# STEP 8: Complete CRAG workflow
def answer_question(question, chunks, index):
    results = retrieve(question, chunks, index)

    relevant = evaluate_retrieval(question, results)
    corrected = False
    search_query = question

    if not relevant:
        corrected = True
        search_query = rewrite_query(question)
        results = retrieve(search_query, chunks, index)
        relevant = evaluate_retrieval(search_query, results)

    if relevant:
        answer = generate_answer(question, results)
    else:
        answer = "Retrieved information is insufficient."

    return {
        "question": question,
        "answer": answer,
        "results": results,
        "relevant": relevant,
        "corrected": corrected,
        "search_query": search_query
    }


# Terminal execution remains available
def main():
    chunks = load_chunks()
    index = build_index(chunks)

    question = input("Enter your question: ")
    result = answer_question(question, chunks, index)

    print("\nRetrieved chunks:")
    for item in result["results"]:
        print(f"\nScore: {item['score']:.3f}")
        print(item["text"])

    print("\nCorrection attempted:", result["corrected"])
    print("\nFINAL ANSWER:", result["answer"])


if __name__ == "__main__":
    main()
