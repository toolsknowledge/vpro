# from openai import OpenAI
# client = OpenAI()
# speech = client.audio.speech.create(
#     model="gpt-4o-mini-tts",
#     voice="alloy",
#     input="Welcome to VPro Skills. Today we are learning Generative AI."
# )
# speech.write_to_file("welcome.mp3")



# Example-2 (Code)
# from openai import OpenAI
# client = OpenAI()
# prompt = """
# Write Java code to find the largest number
# in a list.
# """
# response = client.responses.create(
#     model="gpt-5",
#     input=prompt
# )
# print(response.output_text)



# Example-1 (Text)
# from openai import OpenAI
# client = OpenAI()
# response = client.responses.create(
#     model="gpt-5",
#     input="Explain Python tuples in simple English"
# )
# print(response.output_text)

