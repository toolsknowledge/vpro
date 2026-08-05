from langchain_core.prompts import PromptTemplate

template = """
You are a helpful AI Assistant.
Answer ONLY using the provided Context.
If the answer is not available in the context,
reply:
"I don't know based on the provided document."
Context:
{context}
Question:
{question}
Answer:
"""

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)