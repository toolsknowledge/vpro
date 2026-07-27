from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi import FastAPI

# wants to connect other appln - React,Angular,VueJS, Java(8080), dotnet,........
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/")
def home():
    return {"message":"welcome to FastAPI"}

@app.get("/ask")
def ask_ai(question : str):
    response = client.responses.create(
        model = "gpt-5",
        input = question
    )
    return {"answer":response.output_text}