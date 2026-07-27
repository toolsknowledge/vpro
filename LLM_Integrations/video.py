from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

# Create video generation job
result = client.videos.create(
    model="sora-2",
    prompt="""
    Create a 5-second cinematic video of a futuristic city at night.
    The camera slowly moves forward through a neon-lit street as light
    rain falls, reflections shimmer on the road, and people with umbrellas
    walk in the background. Smooth motion, realistic lighting,
    high detail, 16:9.
    """
)

# raw code byte packets
video_id = result.id

print(f"Video ID: {video_id}")

# Wait until generation completes
while True:
    status = client.videos.retrieve(video_id)
    print("Current Status:", status.status)
    if status.status == "completed":
        print("Video generation completed.")
        break
    if status.status == "failed":
        print("Video generation failed.")
        exit()
    time.sleep(5)
# Download video AFTER completion
video = client.videos.download_content(video_id)
with open("output.mp4", "wb") as f:
    f.write(video.read())
print("Video downloaded successfully!")