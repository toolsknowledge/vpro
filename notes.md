export OPENAI_API_KEY="your_api_key"

set OPENAI_API_KEY=your_api_key


from openai import OpenAI
client = OpenAI()
response = client.responses.create(
    model="gpt-5",
    input="Explain Python tuples in simple English"
)
print(response.output_text)


from openai import OpenAI

client = OpenAI()

prompt = """
Write Python code to find the largest number
in a list.
"""

response = client.responses.create(
    model="gpt-5",
    input=prompt
)

print(response.output_text)


prompt = """
Create a short educational video
showing a robot teaching Python programming
in a classroom.
"""

# Send prompt to a video generation model
# Model generates video
# Save the generated video




from openai import OpenAI

client = OpenAI()

speech = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input="Welcome to VPro Skills. Today we are learning Generative AI."
)

speech.write_to_file("welcome.mp3")



from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Explain Python lists in simple English"
)

print(response.output_text)


# 1hr (06.30AM) 
# FastAPI (3days)
# LLMS (Not) (3days)
# RAGS (8Types) (10 days)
# Agents - AWS,AZURE 
# Guardrails
# Evaluation
# VectorDB'S (Chroma,FAISS,Pinecone)

# Pendings
# genai (text,audio,video)
# LLMS
# ML - 10days
# DL - 10days
# NLP - 5days

# 8AM (Pending) 


