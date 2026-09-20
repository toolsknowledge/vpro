from openai import OpenAI
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Create OpenAI client
client = OpenAI()

# -----------------------------
# 1. Document
# -----------------------------
document = """
Python is a programming language.

Python supports functions.

Python supports object-oriented programming.

Python is widely used in Artificial Intelligence,
Machine Learning, Data Science and Web Development.

Python is easy to learn because its syntax is simple.
"""


# -----------------------------
# 2. Create chunks
# -----------------------------

# Guardrails

chunks = [
    chunk.strip()
    for chunk in document.split("\n\n")
    if chunk.strip()
]


# -----------------------------
# 3. Retrieve relevant chunks
# -----------------------------
def retrieve(question):

    question_words = question.lower().split()

    results = []

    for chunk in chunks:

        score = 0

        for word in question_words:

            if word in chunk.lower():
                score += 1

        if score > 0:
            results.append((score, chunk))

    results.sort(reverse=True)

    return [chunk for score, chunk in results[:3]]


# -----------------------------
# 4. Ask question
# -----------------------------
question = input("Ask your question: ")


# -----------------------------
# 5. Retrieve context
# -----------------------------
context = retrieve(question)

context_text = "\n\n".join(context)

print("\nRetrieved Context:")
print(context_text)


# -----------------------------
# 6. Send context to LLM
# -----------------------------
prompt = f"""
Answer the question using only the context below.

Context:
{context_text}

Question:
{question}

If the answer is not present in the context,
say "I don't know."
"""


response = client.responses.create(
    model="gpt-5",
    input=prompt
)


# -----------------------------
# 7. Display answer
# -----------------------------
print("\nAnswer:")
print(response.output_text)


# read text
# create chunks
# question
# retrive matched chunks based on user question
# prepare context
# llm
# generate the answer
