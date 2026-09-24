import os
import time
import subprocess
from dotenv import load_dotenv
from google import genai
from google.genai import types
# -----------------------------------------
# 1. Load .env
# -----------------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found. "
        "Please add it to your .env file."
    )
# -----------------------------------------
# 2. Create Gemini client
# -----------------------------------------
client = genai.Client(
    api_key=api_key
)
# -----------------------------------------
# 3. Video prompt
# -----------------------------------------
prompt = """
Create a short educational video showing a friendly robot
teaching Python programming in a modern classroom.

The robot is standing in front of a digital classroom screen.

The screen displays:

print("Hello, World!")

Students are watching and learning.

The robot explains the Python code in a simple way.

Make the scene clean, professional, educational,
and suitable for beginner Python students.
"""


# -----------------------------------------
# 4. Start video generation
# -----------------------------------------
print("Starting video generation...")

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",

    source=types.GenerateVideosSource(
        prompt=prompt
    ),

    config=types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8
    )
)


print("Video generation started.")


# -----------------------------------------
# 5. Wait for completion
# -----------------------------------------

while not operation.done:

    print("Video is processing...")

    time.sleep(10)

    operation = client.operations.get(operation)


# -----------------------------------------
# 6. Check response
# -----------------------------------------

if operation.response is None:

    print("Video generation failed.")

    if operation.error:
        print("Error:", operation.error)

    exit()


# -----------------------------------------
# 7. Get generated video
# -----------------------------------------

generated_videos = operation.response.generated_videos

if not generated_videos:

    print("No video was generated.")
    exit()


video = generated_videos[0].video

print("Video generated successfully!")


# -----------------------------------------
# 8. Save video
# -----------------------------------------

output_file = "python_robot_class.mp4"

video.save(output_file)

print()
print("Video saved successfully:")
print(output_file)


# -----------------------------------------
# 9. Play video on Mac
# -----------------------------------------

print()
print("Opening video...")

subprocess.run(
    ["open", output_file]
)

print()
print("Done!")