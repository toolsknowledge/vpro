# OpenAI - used to connect to ChatGPT
from openai import OpenAI

# load_dotenv() - used to load environmental file
from dotenv import load_dotenv

# import os module
import os

# loading environmental file
load_dotenv()

# connect to chatgpt
client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))

question = input("Enter your Question :")

response = client.responses.create(
    model = "gpt-4",
    input = question
)

print(response.output_text)
