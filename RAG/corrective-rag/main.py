import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_chroma import Chroma

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from langgraph.graph import StateGraph, START, END

from typing import TypedDict


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set in .env file")


# ============================================================
# 2. CREATE LLM
# ============================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ============================================================
# 3. CREATE DOCUMENTS
# ============================================================

documents = [

    Document(
        page_content="""
        Python is a high-level programming language.
        Python is easy to learn and supports object-oriented programming.
        Python is commonly used for web development, data science,
        machine learning and artificial intelligence.
        """,
        metadata={"source": "python.txt"}
    ),

    Document(
        page_content="""
        FastAPI is a modern Python web framework.
        FastAPI is commonly used to build REST APIs.
        It provides automatic API documentation and supports
        asynchronous programming.
        """,
        metadata={"source": "fastapi.txt"}
    ),

    Document(
        page_content="""
        MongoDB is a NoSQL database.
        MongoDB stores data in documents using a JSON-like structure.
        MongoDB is commonly used with modern web applications.
        """,
        metadata={"source": "mongodb.txt"}
    ),

    Document(
        page_content="""
        React is a JavaScript library used for building user interfaces.
        React applications are created using components.
        React supports reusable UI components.
        """,
        metadata={"source": "react.txt"}
    )
]


# ============================================================
# 4. CREATE VECTOR DATABASE
# ============================================================

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="corrective_rag_demo"
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)


# ============================================================
# 5. DEFINE GRAPH STATE
# ============================================================

class RAGState(TypedDict):
    question: str
    documents: list
    relevance: str
    final_answer: str


# ============================================================
# 6. RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(state: RAGState):

    print("\n==============================")
    print("STEP 1: RETRIEVING DOCUMENTS")
    print("==============================")

    question = state["question"]

    docs = retriever.invoke(question)

    print(f"\nQuestion: {question}")

    print("\nRetrieved Documents:")

    for i, doc in enumerate(docs, start=1):

        print(f"\nDocument {i}:")
        print(doc.page_content.strip())

    return {
        "documents": docs
    }


# ============================================================
# 7. EVALUATE RETRIEVED DOCUMENTS
# ============================================================

def evaluate_documents(state: RAGState):

    print("\n==============================")
    print("STEP 2: EVALUATING DOCUMENTS")
    print("==============================")

    question = state["question"]

    documents = state["documents"]

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are a document relevance evaluator.

        Question:
        {question}

        Retrieved Documents:
        {context}

        Decide whether the retrieved documents contain
        useful information for answering the question.

        Return ONLY one word:

        RELEVANT

        or

        NOT_RELEVANT
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "context": context
        }
    )

    result = response.content.strip().upper()

    print("\nEvaluator Result:", result)

    if "RELEVANT" in result and "NOT_RELEVANT" not in result:
        relevance = "relevant"
    else:
        relevance = "not_relevant"

    return {
        "relevance": relevance
    }


# ============================================================
# 8. CORRECT RETRIEVAL
# ============================================================

def correct_retrieval(state: RAGState):

    print("\n==============================")
    print("STEP 3: CORRECTING RETRIEVAL")
    print("==============================")

    question = state["question"]

    print("\nOriginal question:")
    print(question)

    # --------------------------------------------------------
    # Simple classroom correction:
    # Ask the LLM to rewrite the query into better search terms.
    # --------------------------------------------------------

    prompt = ChatPromptTemplate.from_template(
        """
        Improve the following search query.

        Original Question:
        {question}

        Return only a better search query.
        Do not explain anything.
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": question
        }
    )

    improved_query = response.content.strip()

    print("\nImproved Query:")
    print(improved_query)

    # --------------------------------------------------------
    # Search again using the improved query
    # --------------------------------------------------------

    new_docs = retriever.invoke(improved_query)

    print("\nCorrected Retrieval Results:")

    for i, doc in enumerate(new_docs, start=1):

        print(f"\nDocument {i}:")
        print(doc.page_content.strip())

    return {
        "documents": new_docs
    }


# ============================================================
# 9. GENERATE FINAL ANSWER
# ============================================================

def generate_answer(state: RAGState):

    print("\n==============================")
    print("STEP 4: GENERATING ANSWER")
    print("==============================")

    question = state["question"]

    documents = state["documents"]

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful teacher.

        Answer the question using ONLY the provided context.

        If the answer is not available in the context,
        say that the information is not available.

        Explain the answer in simple English.

        Question:
        {question}

        Context:
        {context}

        Answer:
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "context": context
        }
    )

    answer = response.content

    print("\nFINAL ANSWER:")
    print(answer)

    return {
        "final_answer": answer
    }


# ============================================================
# 10. ROUTER
# ============================================================

def check_relevance(state: RAGState):

    if state["relevance"] == "relevant":

        print("\nDocuments are useful.")
        print("Going directly to answer generation.")

        return "generate"

    else:

        print("\nDocuments are NOT useful.")
        print("Going to corrective retrieval.")

        return "correct"


# ============================================================
# 11. BUILD LANGGRAPH
# ============================================================

graph = StateGraph(RAGState)


# Add nodes

graph.add_node(
    "retrieve",
    retrieve_documents
)

graph.add_node(
    "evaluate",
    evaluate_documents
)

graph.add_node(
    "correct",
    correct_retrieval
)

graph.add_node(
    "generate",
    generate_answer
)


# Start

graph.add_edge(
    START,
    "retrieve"
)


# Retrieve → Evaluate

graph.add_edge(
    "retrieve",
    "evaluate"
)


# Evaluate → Relevant / Not Relevant

graph.add_conditional_edges(
    "evaluate",
    check_relevance,
    {
        "generate": "generate",
        "correct": "correct"
    }
)


# Correct → Generate

graph.add_edge(
    "correct",
    "generate"
)


# Generate → End

graph.add_edge(
    "generate",
    END
)


# Compile graph

app = graph.compile()


# ============================================================
# 12. USER INPUT
# ============================================================

print("\n======================================")
print("       CORRECTIVE RAG DEMO")
print("======================================")

question = input(
    "\nAsk your question: "
)


# ============================================================
# 13. RUN GRAPH
# ============================================================

result = app.invoke(
    {
        "question": question,
        "documents": [],
        "relevance": "",
        "final_answer": ""
    }
)


# ============================================================
# 14. FINAL OUTPUT
# ============================================================

print("\n======================================")
print("             FINAL RESULT")
print("======================================")

print(result["final_answer"])