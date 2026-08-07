import os
import shutil

from loaders.pdf_loader import load_pdf
from splitter.text_spiltter import split_documents
from embeddings.embedding_model import get_embedding_model
from vector_store.vector_db import create_vector_db


DATA_FOLDER = "data"
VECTOR_DB_FOLDER = "vector_store/chroma_db"


def ingest():

    print("=" * 60)
    print("        RAG DOCUMENT INGESTION")
    print("=" * 60)

    # ---------------------------------------------------
    # Delete old vector database (optional)
    # ---------------------------------------------------

    if os.path.exists(VECTOR_DB_FOLDER):

        print("\nDeleting old Vector Database...")

        shutil.rmtree(VECTOR_DB_FOLDER)

    # ---------------------------------------------------
    # Load Embedding Model
    # ---------------------------------------------------

    print("\nLoading Embedding Model...")

    embedding_model = get_embedding_model()

    # ---------------------------------------------------
    # Read all PDFs
    # ---------------------------------------------------

    all_documents = []

    pdf_files = [
        file
        for file in os.listdir(DATA_FOLDER)
        if file.endswith(".pdf")
    ]

    if len(pdf_files) == 0:

        print("No PDF files found inside data folder.")

        return

    for pdf in pdf_files:

        pdf_path = os.path.join(DATA_FOLDER, pdf)

        print(f"\nLoading : {pdf}")

        docs = load_pdf(pdf_path)

        all_documents.extend(docs)

    print(f"\nTotal Pages Loaded : {len(all_documents)}")

    # ---------------------------------------------------
    # Split Documents
    # ---------------------------------------------------

    print("\nSplitting Documents...")

    chunks = split_documents(all_documents)

    print(f"Total Chunks Created : {len(chunks)}")

    # ---------------------------------------------------
    # Create Vector Database
    # ---------------------------------------------------

    print("\nCreating Chroma Vector Database...")

    create_vector_db(chunks, embedding_model)

    print("\nVector Database Created Successfully!")

    print("\nLocation : vector_store/chroma_db")

    print("\nIngestion Completed Successfully.")

    print("=" * 60)


if __name__ == "__main__":

    ingest()