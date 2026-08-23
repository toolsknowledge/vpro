import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv(
    "OPENAI_API_KEY"
)

if not api_key:

    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Check your .env file."
    )


client = OpenAI(
    api_key=api_key
)


def generate_answer(
    question,
    context
):

    prompt = f"""
You are a helpful RAG assistant.

Answer the question using ONLY
the provided context.

Context:
{context}

Question:
{question}

If the answer is not present
in the context, say:

"I don't have enough information."

Give a short and clear answer.
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    return response.output_text