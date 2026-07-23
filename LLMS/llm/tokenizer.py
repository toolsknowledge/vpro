"""
tokenizer.py

Purpose:
--------
This file prepares text for our Mini LLM.
It performs:
1. Read text file
2. Convert to lowercase
3. Split text into words (Tokenization)
4. Build Vocabulary (Word -> ID)
5. Build Reverse Vocabulary (ID -> Word)
6. Encode text into numbers
7. Decode numbers back into text
"""

# -----------------------------
# STEP 1 : Read the dataset
# -----------------------------

import os
CURRENT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(CURRENT_DIR, "data.txt")
with open(DATA_PATH, "r") as file:
    text = file.read()
# -----------------------------
# STEP 2 : Convert to lowercase
# -----------------------------
text = text.lower()
# -----------------------------
# STEP 3 : Tokenization
# -----------------------------
tokens = text.split()  # List
# -----------------------------
# STEP 4 : Create Vocabulary
# -----------------------------
unique_words = sorted(set(tokens)) # List
print("----------------------Unique-----------")
print(unique_words)
vocab = {} # {"ai":0,......,"python":18,"is":11,"eazy":5}
for index, word in enumerate(unique_words):
    vocab[word] = index
# {"VPro":3}. 
# -----------------------------
# STEP 5 : Reverse Vocabulary # {3:"VPro"}
# -----------------------------
reverse_vocab = {} # {"0":"ai",........}
for word, index in vocab.items():
    reverse_vocab[index] = word
# -----------------------------
# STEP 6 : Encode Text
# -----------------------------
encoded_tokens = [] # [18,11,5,0,........]
for word in tokens:
    encoded_tokens.append(vocab[word])
# -----------------------------
# STEP 7 : Decode Text
# -----------------------------
decoded_tokens = [] # ["python","is","eazy",......]

for number in encoded_tokens:
    decoded_tokens.append(reverse_vocab[number])
# -----------------------------
# STEP 8 : Display Everything
# -----------------------------
print("=" * 50)
print("Original Text")
print("=" * 50)
print(text)
print("\n")
print("=" * 50)
print("Tokens")
print("=" * 50)
print(tokens)
print("\n")
print("=" * 50)
print("Vocabulary")
print("=" * 50)
print(vocab)
print("\n")
print("=" * 50)
print("Reverse Vocabulary")
print("=" * 50)
print(reverse_vocab)
print("\n")
print("=" * 50)
print("Encoded Tokens")
print("=" * 50)
print(encoded_tokens)

print("\n")

print("=" * 50)
print("Decoded Tokens")
print("=" * 50)
print(decoded_tokens)