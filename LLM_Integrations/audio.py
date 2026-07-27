from openai import OpenAI

from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="ash",
    input="Hello !, welcome to audio generation with LLM !!!"
) as response:
    response.stream_to_file("output.mp3")
    print("Audio Generated !!!")

