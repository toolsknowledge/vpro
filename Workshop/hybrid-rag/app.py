import os
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic

from rank_bm25 import BM25Okapi

from dotenv import load_dotenv

load_dotenv()


# -----------------------------
# 1. Load Documents
# -----------------------------

def load_documents(folder_path):

    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            file_path = os.path.join(folder_path, file)

            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

    return documents


# -----------------------------
# 2. Split Documents
# -----------------------------

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(documents)


# -----------------------------
# 3. Create Vector Database
# -----------------------------

def create_vector_db(documents):

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

    vector_db = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory="./chroma_db"
    )

    return vector_db


# -----------------------------
# 4. Keyword Search - BM25
# -----------------------------

def keyword_search(query, documents, top_k=3):

    texts = [doc.page_content for doc in documents]

    tokenized_documents = [
        text.lower().split()
        for text in texts
    ]

    bm25 = BM25Okapi(tokenized_documents)

    query_tokens = query.lower().split()

    scores = bm25.get_scores(query_tokens)

    top_indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    return [documents[i] for i in top_indexes]


# -----------------------------
# 5. Hybrid Search
# -----------------------------

def hybrid_search(query, vector_db, documents):

    # Vector search
    vector_results = vector_db.similarity_search(
        query,
        k=3
    )

    # Keyword search
    keyword_results = keyword_search(
        query,
        documents,
        top_k=3
    )

    # Combine results
    combined = vector_results + keyword_results

    # Remove duplicate chunks
    unique_documents = []

    seen = set()

    for doc in combined:

        content = doc.page_content

        if content not in seen:

            seen.add(content)
            unique_documents.append(doc)

    return unique_documents


# -----------------------------
# 6. Generate Answer
# -----------------------------

# def generate_answer(query, documents):

#     context = "\n\n".join(
#         doc.page_content
#         for doc in documents
#     )

#     llm = ChatAnthropic(
#         model="claude-sonnet-4-20250514",
#         temperature=0
#     )

#     prompt = f"""
# Answer the question using only the context below.

# Context:
# {context}

# Question:
# {query}

# If the answer is not available in the context,
# say "I don't know based on the provided documents."
# """

#     response = llm.invoke(prompt)

#     return response.content

def generate_answer(query, documents):

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    temperature=0
)

    prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{query}

If the answer is not available in the context,
say "I don't know based on the provided documents."
"""

    response = llm.invoke(prompt)

    return response.content


# -----------------------------
# 7. Streamlit Application
# -----------------------------

st.title("Hybrid RAG Application")

st.write(
    "Vector Search + Keyword Search + Claude"
)


# Load documents
documents = load_documents("./data/documents")


if documents:

    # Split documents
    chunks = split_documents(documents)

    # Create vector database
    vector_db = create_vector_db(chunks)

    st.success(
        f"Loaded {len(documents)} documents"
    )

    question = st.text_input(
        "Ask a question"
    )

    if question:

        # Hybrid retrieval
        results = hybrid_search(
            question,
            vector_db,
            chunks
        )

        # Generate answer
        answer = generate_answer(
            question,
            results
        )

        st.subheader("Answer")

        st.write(answer)

        st.subheader("Retrieved Documents")

        for i, doc in enumerate(results):

            st.write(
                f"**Document {i + 1}**"
            )

            st.write(
                doc.page_content
            )

else:

    st.warning(
        "Please add PDF files inside data/documents/"
    )