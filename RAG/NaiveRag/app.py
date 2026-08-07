from loaders.pdf_loader import load_pdf
from splitter.text_spiltter import split_documents
from embeddings.embedding_model import get_embedding_model
from vector_store.vector_db import load_vector_db
from retriever.retriever import get_retriever
from llm.llm import get_llm
from prompts.rag_prompt import RAG_PROMPT
def main():
    print("=" * 60)
    print("          RAG QUESTION ANSWERING SYSTEM")
    print("=" * 60)
    
    # Load Embedding Model
    print("\nLoading Embedding Model...")
    embedding_model = get_embedding_model()
    
    # Load Existing Vector Database
    print("Loading Chroma Vector Database...")
    vector_db = load_vector_db(embedding_model)

    # Create Retriever
    # retrurn top 3 matches based on question
    retriever = get_retriever(vector_db)

    # Load LLM
    llm = get_llm()

    print("\nSystem Ready!")
    print("\nType 'exit' to quit.\n")
    while True:
        question = input("Ask Question : ")
        if question.lower() == "exit":
            print("\nThank You!")
            break
        # Retrieve Documents
        # docs - top 3 matches
        docs = retriever.invoke(question)
        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        # Build Prompt
        prompt = RAG_PROMPT.format(
            context=context,
            question=question

        )
        # Call LLM
        response = llm.invoke(prompt)
        print("\nAnswer\n")
        print(response.content)
        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()