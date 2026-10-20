import os
from dotenv import load_dotenv
from getpass import getpass
from openai import OpenAI
from document_loader import load_docx, split_text
from vector_store import create_vector_store


DOCX_PATH = "sample_guide.docx"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = getpass("Enter your OpenAI API key: ").strip()
    if not api_key:
        print("OpenAI API key is required.")
        return

    client = OpenAI(api_key=api_key)

    if not os.path.exists(DOCX_PATH):
        print(f"Cannot find {DOCX_PATH}. Put the DOCX file in this folder.")
        return

    text = load_docx(DOCX_PATH)
    chunks = split_text(text)

    if not chunks:
        print("No text found in the DOCX file.")
        return

    store = create_vector_store()

    # Index the document only if the selected database is empty.
    # For a fresh re-index, delete chroma_data/ or faiss_data/ first.
    if os.getenv("VECTOR_DB", "chroma").lower() == "chroma":
        is_empty = store.collection.count() == 0
    else:
        is_empty = store.index is None

    if is_empty:
        print(f"Creating embeddings for {len(chunks)} text chunks...")
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=chunks)
        embeddings = [item.embedding for item in response.data]
        store.add_documents(chunks, embeddings)
        print(f"Indexed {len(chunks)} chunks using {os.getenv('VECTOR_DB', 'chroma').upper()}.")
    else:
        print(f"Using existing {os.getenv('VECTOR_DB', 'chroma').upper()} index.")

    print("\nAsk questions about sample_guide.docx. Type 'exit' to stop.")

    while True:
        question = input("\nYour question: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        query_response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[question]
        )
        query_embedding = query_response.data[0].embedding
        results = store.search(query_embedding, top_k=4)

        if not results:
            print("No indexed content found. Please index the DOCX first.")
            continue

        context = "\n\n".join(item["text"] for item in results)
        prompt = f"""
Answer the user's question using only the context below.
If the answer is not in the context, say: "I cannot find that information in the document."
Do not guess or add outside facts. Keep the answer clear and simple.

Context:
{context}

Question: {question}
"""
        answer = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You answer questions accurately from supplied document context only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        print("\nAnswer:", answer.choices[0].message.content.strip())


if __name__ == "__main__":
    main()
