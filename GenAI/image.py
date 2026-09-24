import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
prompt = """
Create a professional educational illustration of a friendly robot
teaching Python programming in a modern classroom.
The robot is standing in front of a large digital screen.
The screen displays:
print("Hello, World!")
Several students are sitting in the classroom and learning.
Clean, modern, colorful educational style.
Suitable for beginner Python students.
"""
result = client.images.generate(
    model="gpt-image-2",
    prompt=prompt,
    size="1536x1024",
    quality="medium",
    output_format="png"
)
image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)
output_file = "python_robot_class.png"
with open(output_file, "wb") as f:
    f.write(image_bytes)
print("Image generated successfully!")
print("Saved as:", output_file)