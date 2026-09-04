import os
from pathlib import Path
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from anthropic import Anthropic
from dotenv import load_dotenv

# ============================================================
# 1. LOAD ENVIRONMENT
# ============================================================
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY is missing. "
        "Create a .env file and add your Anthropic API key."
    )
client = Anthropic(api_key=API_KEY)

# ============================================================
# 2. LOAD PDF
# ============================================================
def load_pdf(pdf_path):
    """
    Read text from a PDF file.
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    reader = PdfReader(pdf_path)

    text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            text += f"\n[Page {page_number}]\n"
            text += page_text

    if not text.strip():
        raise ValueError(
            "No readable text found in the PDF."
        )

    return text


# ============================================================
# 3. CREATE CHUNKS
# ============================================================
def create_chunks(text, chunk_size=1000, overlap=200):
    """
    Split document into smaller pieces.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ============================================================
# 4. CREATE RETRIEVAL INDEX
# ============================================================
def create_index(chunks):
    """
    Convert chunks into TF-IDF vectors.
    """

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(chunks)

    return vectorizer, vectors


# ============================================================
# 5. RETRIEVE DOCUMENTS
# ============================================================
def retrieve_documents(
    question,
    chunks,
    vectorizer,
    vectors,
    top_k=5
):
    """
    Find the most relevant chunks.
    """

    question_vector = vectorizer.transform([question])

    scores = cosine_similarity(
        question_vector,
        vectors
    )[0]

    ranked_indexes = scores.argsort()[::-1]

    results = []

    for index in ranked_indexes[:top_k]:

        results.append({
            "chunk": chunks[index],
            "score": float(scores[index])
        })

    return results


# ============================================================
# 6. ASK CLAUDE
# ============================================================
def ask_claude(prompt):
    """
    Send a prompt to Claude.
    """

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text.strip()

# ============================================================
# 7. SHOULD I RETRIEVE?
# ============================================================
def should_retrieve(question):
    """
    Self-RAG decides whether external documents
    are necessary.
    """

    prompt = f"""
You are a retrieval decision system.

Question:
{question}

Decide whether a document retrieval step is necessary.

Return ONLY one word:

YES
or
NO

Use YES when the question requires information
that should come from the provided PDF.

Use NO when the question is general knowledge,
simple conversation, or can be answered without
the PDF.
"""

    result = ask_claude(prompt)

    result = result.upper()

    return "YES" in result


# ============================================================
# 8. CHECK DOCUMENT RELEVANCE
# ============================================================
def check_relevance(question, documents):
    """
    Check whether retrieved documents are relevant
    to the question.
    """

    context = "\n\n".join(
        [
            f"DOCUMENT {i + 1}:\n{doc['chunk']}"
            for i, doc in enumerate(documents)
        ]
    )

    prompt = f"""
You are a document relevance evaluator.

QUESTION:
{question}

RETRIEVED DOCUMENTS:
{context}

Are these documents relevant to answering
the question?

Return ONLY:

YES
or
NO
"""

    result = ask_claude(prompt)

    return "YES" in result.upper()


# ============================================================
# 9. GENERATE ANSWER
# ============================================================
def generate_answer(question, documents):
    """
    Generate an answer using retrieved documents.
    """

    context = "\n\n".join(
        [
            f"DOCUMENT {i + 1}:\n{doc['chunk']}"
            for i, doc in enumerate(documents)
        ]
    )

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the
information present in the documents.

QUESTION:
{question}

DOCUMENTS:
{context}

Rules:

1. Do not invent information.
2. If the documents do not contain the answer,
   say that the answer is not available in the document.
3. Give a clear student-friendly explanation.
4. Keep the answer concise.
5. Mention the page number when it is available.

ANSWER:
"""

    return ask_claude(prompt)


# ============================================================
# 10. CHECK WHETHER ANSWER IS SUPPORTED
# ============================================================
def check_support(question, answer, documents):
    """
    Check whether the generated answer is supported
    by retrieved documents.
    """

    context = "\n\n".join(
        [
            doc["chunk"]
            for doc in documents
        ]
    )

    prompt = f"""
You are a factuality evaluator.

QUESTION:
{question}

ANSWER:
{answer}

DOCUMENTS:
{context}

Determine whether every important claim in the
answer is supported by the documents.

Return ONLY:

YES
or
NO
"""

    result = ask_claude(prompt)

    return "YES" in result.upper()


# ============================================================
# 11. CHECK ANSWER QUALITY
# ============================================================
def check_answer_quality(question, answer):
    """
    Evaluate answer quality.
    """

    prompt = f"""
You are an answer quality evaluator.

QUESTION:
{question}

ANSWER:
{answer}

Check whether the answer is:

- Correct
- Relevant
- Clear
- Complete
- Easy for a student to understand

Return ONLY:

YES
or
NO
"""

    result = ask_claude(prompt)

    return "YES" in result.upper()


# ============================================================
# 12. REFINE QUESTION
# ============================================================
def refine_question(question):
    """
    Improve the question when retrieval is poor.
    """

    prompt = f"""
Rewrite the following question to make it
better for document retrieval.

Original question:
{question}

Return ONLY the improved question.
"""

    return ask_claude(prompt)


# ============================================================
# 13. SELF-RAG PIPELINE
# ============================================================
def self_rag(question, chunks, vectorizer, vectors):
    """
    Complete Self-RAG workflow.
    """

    print("\n" + "=" * 70)
    print("SELF-RAG")
    print("=" * 70)

    print("\nQUESTION:")
    print(question)

    # --------------------------------------------------------
    # STEP 1: SHOULD I RETRIEVE?
    # --------------------------------------------------------

    print("\n[1] Should I retrieve?")

    retrieve = should_retrieve(question)

    if not retrieve:

        print("Decision: NO")
        print("Generating answer without document retrieval...")

        answer = ask_claude(
            f"""
Answer the following question clearly
for a student.

Question:
{question}
"""
        )

        print("\nFINAL ANSWER:")
        print(answer)

        return answer

    print("Decision: YES")

    # --------------------------------------------------------
    # STEP 2: RETRIEVE DOCUMENTS
    # --------------------------------------------------------

    for attempt in range(1, 4):

        print(
            f"\n[2] Retrieve documents - Attempt {attempt}"
        )

        documents = retrieve_documents(
            question,
            chunks,
            vectorizer,
            vectors,
            top_k=5
        )

        print(
            f"Retrieved {len(documents)} documents."
        )

        # ----------------------------------------------------
        # STEP 3: CHECK RELEVANCE
        # ----------------------------------------------------

        print("\n[3] Are documents relevant?")

        relevant = check_relevance(
            question,
            documents
        )

        if relevant:

            print("Relevance: YES")

            break

        print("Relevance: NO")

        if attempt == 3:

            return (
                "I could not find sufficiently relevant "
                "information in the PDF."
            )

        print("Refining question...")

        question = refine_question(question)

        print(
            "Refined question:",
            question
        )

    # --------------------------------------------------------
    # STEP 4: GENERATE ANSWER
    # --------------------------------------------------------

    print("\n[4] Generate answer")

    answer = generate_answer(
        question,
        documents
    )

    print("Answer generated.")

    # --------------------------------------------------------
    # STEP 5: CHECK SUPPORT
    # --------------------------------------------------------

    print("\n[5] Is answer supported?")

    supported = check_support(
        question,
        answer,
        documents
    )

    if not supported:

        print("Support: NO")

        print("Answer is not sufficiently supported.")

        if attempt < 3:

            print("Retrieving again...")

            refined_question = refine_question(
                question
            )

            documents = retrieve_documents(
                refined_question,
                chunks,
                vectorizer,
                vectors,
                top_k=5
            )

            answer = generate_answer(
                refined_question,
                documents
            )

            supported = check_support(
                refined_question,
                answer,
                documents
            )

    else:

        print("Support: YES")

    # --------------------------------------------------------
    # STEP 6: CHECK ANSWER QUALITY
    # --------------------------------------------------------

    print("\n[6] Is answer good?")

    good = check_answer_quality(
        question,
        answer
    )

    if good:

        print("Quality: YES")

        print("\n" + "=" * 70)
        print("FINAL ANSWER")
        print("=" * 70)

        print(answer)

        return answer

    # --------------------------------------------------------
    # STEP 7: RETRIEVE AGAIN
    # --------------------------------------------------------

    print("Quality: NO")

    print("\nRetrieving again...")

    refined_question = refine_question(
        question
    )

    documents = retrieve_documents(
        refined_question,
        chunks,
        vectorizer,
        vectors,
        top_k=5
    )

    answer = generate_answer(
        refined_question,
        documents
    )

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(answer)

    return answer


# ============================================================
# 14. MAIN APPLICATION
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("SELF-RAG PDF QUESTION ANSWERING SYSTEM")
    print("=" * 70)

    # --------------------------------------------------------
    # PDF FILE
    # --------------------------------------------------------

    pdf_path = input(
        "\nEnter PDF path: "
    ).strip()

    # --------------------------------------------------------
    # LOAD PDF
    # --------------------------------------------------------

    print("\nLoading PDF...")

    text = load_pdf(pdf_path)

    print(
        f"PDF loaded successfully."
    )

    print(
        f"Total characters: {len(text)}"
    )

    # --------------------------------------------------------
    # CREATE CHUNKS
    # --------------------------------------------------------

    print("\nCreating chunks...")

    chunks = create_chunks(text)

    print(
        f"Created {len(chunks)} chunks."
    )

    # --------------------------------------------------------
    # CREATE INDEX
    # --------------------------------------------------------

    print("\nCreating retrieval index...")

    vectorizer, vectors = create_index(
        chunks
    )

    print("Retrieval index created.")

    # --------------------------------------------------------
    # QUESTION LOOP
    # --------------------------------------------------------

    while True:

        print("\n" + "-" * 70)

        question = input(
            "Ask a question (type 'exit' to stop): "
        ).strip()

        if question.lower() == "exit":

            print("\nGoodbye!")

            break

        if not question:

            print("Please enter a question.")

            continue

        try:

            self_rag(
                question,
                chunks,
                vectorizer,
                vectors
            )

        except Exception as e:

            print("\nERROR:")
            print(e)


# ============================================================
# 15. START APPLICATION
# ============================================================

if __name__ == "__main__":
    main()
