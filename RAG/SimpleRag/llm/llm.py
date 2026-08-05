import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
def get_llm():
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return llm