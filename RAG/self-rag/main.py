import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# ============================================================
# 1. LOAD ENVIRONMENT
# ============================================================

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing in .env")


# ============================================================
# 2. LLM
# ============================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ============================================================
# 3. SAMPLE KNOWLEDGE BASE
# ============================================================

knowledge = """
VPro Skills is a technology training institute.

VPro Skills provides training in Python, Java, Data Structures,
Generative AI, Agentic AI, Machine Learning, Deep Learning,
NLP, RAG, LangChain and LangGraph.

The institute provides practical training for students,
working professionals and faculty.

Python training covers Python basics, OOP concepts,
NumPy, Pandas and data visualization.

Generative AI training covers LLMs, embeddings,
vector databases, RAG, LangChain and Agentic AI.

Students are encouraged to work on practical projects
and coding exercises.

VPro Skills focuses on industry-ready skills and
interview preparation.
"""


# ============================================================
# 4. CREATE DOCUMENT
# ============================================================

documents = [
    Document(
        page_content=knowledge,
        metadata={"source": "vpro_skills.txt"}
    )
]


# ============================================================
# 5. SPLIT DOCUMENT INTO CHUNKS
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)


# ============================================================
# 6. CREATE EMBEDDINGS
# ============================================================

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# ============================================================
# 7. CREATE VECTOR DATABASE
# ============================================================

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="self_rag_demo"
)


# ============================================================
# 8. RETRIEVER
# ============================================================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# ============================================================
# 9. SELF-RAG - CHECK DOCUMENT RELEVANCE
# ============================================================

def check_relevance(question, retrieved_documents):

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_documents
    )

    prompt = f"""
You are a document relevance evaluator.

Question:
{question}

Retrieved documents:
{context}

Determine whether the retrieved documents contain
information useful for answering the question.

Return ONLY:

YES

or

NO
"""

    response = llm.invoke(prompt)

    result = response.content.strip().upper()

    return result.startswith("YES")


# ============================================================
# 10. SELF-RAG - GENERATE ANSWER
# ============================================================

def generate_answer(question, retrieved_documents):

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_documents
    )

    prompt = f"""
You are a helpful RAG assistant.

Answer the user's question using ONLY the information
provided in the context.

If the context does not contain the answer,
say:

"I don't have enough information in the knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content


# ============================================================
# 11. SELF-RAG - CHECK ANSWER
# ============================================================

def check_answer(question, answer, retrieved_documents):

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_documents
    )

    prompt = f"""
You are an answer evaluator.

Question:
{question}

Context:
{context}

Generated Answer:
{answer}

Check whether the generated answer is fully supported
by the provided context.

Return ONLY:

YES

if the answer is supported.

Return:

NO

if the answer contains unsupported information.
"""

    response = llm.invoke(prompt)

    result = response.content.strip().upper()

    return result.startswith("YES")


# ============================================================
# 12. SELF-RAG PIPELINE
# ============================================================

def self_rag(question):

    print("\n" + "=" * 60)
    print("USER QUESTION")
    print("=" * 60)

    print(question)

    # --------------------------------------------------------
    # STEP 1: RETRIEVE
    # --------------------------------------------------------

    print("\n[1] Retrieving documents...")

    retrieved_documents = retriever.invoke(question)

    print(
        f"Retrieved {len(retrieved_documents)} documents"
    )

    # --------------------------------------------------------
    # STEP 2: CHECK RELEVANCE
    # --------------------------------------------------------

    print("\n[2] Checking document relevance...")

    relevant = check_relevance(
        question,
        retrieved_documents
    )

    if not relevant:

        print("Documents are NOT relevant.")

        return (
            "I could not find relevant information "
            "in the knowledge base."
        )

    print("Documents are relevant.")

    # --------------------------------------------------------
    # STEP 3: GENERATE ANSWER
    # --------------------------------------------------------

    print("\n[3] Generating answer...")

    answer = generate_answer(
        question,
        retrieved_documents
    )

    print("Generated answer:")
    print(answer)

    # --------------------------------------------------------
    # STEP 4: SELF-CHECK
    # --------------------------------------------------------

    print("\n[4] Checking generated answer...")

    supported = check_answer(
        question,
        answer,
        retrieved_documents
    )

    # --------------------------------------------------------
    # STEP 5: SELF-CORRECTION
    # --------------------------------------------------------

    if supported:

        print("Answer is supported.")

        return answer

    print("Answer is NOT fully supported.")
    print("Regenerating answer...")

    corrected_answer = generate_answer(
        question,
        retrieved_documents
    )

    return corrected_answer


# ============================================================
# 13. MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n======================================")
    print("       SELF-RAG DEMO APPLICATION")
    print("======================================")

    while True:

        question = input(
            "\nAsk a question (type 'exit' to stop): "
        )

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = self_rag(question)

        print("\n" + "=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)

        print(answer)