"""
predict.py

Purpose
-------
Load the trained Mini LLM and
generate continuous text.

Flow

User Input
    ↓
Encode
    ↓
Predict Next Word
    ↓
Append Prediction
    ↓
Predict Again
    ↓
Repeat
"""

import torch

from tokenizer import vocab, reverse_vocab
from model import MiniLLM

# -----------------------------------
# Hyper Parameters
# -----------------------------------

VOCAB_SIZE = len(vocab)

EMBEDDING_DIM = 16

MAX_WORDS = 20

# -----------------------------------
# Create Model
# -----------------------------------

model = MiniLLM(
    vocab_size=VOCAB_SIZE,
    embedding_dim=EMBEDDING_DIM
)

# -----------------------------------
# Load Trained Model
# -----------------------------------

model.load_state_dict(
    torch.load("model.pth")
)

# -----------------------------------
# Prediction Mode
# -----------------------------------

model.eval()

# -----------------------------------
# User Input
# -----------------------------------

sentence = input("Enter text : ")

sentence = sentence.lower()

tokens = sentence.split()

# -----------------------------------
# Convert Words to IDs
# -----------------------------------

encoded = []

for word in tokens:

    if word in vocab:

        encoded.append(vocab[word])

# -----------------------------------
# Check Unknown Words
# -----------------------------------

if len(encoded) == 0:

    print("\nNo known words found in vocabulary.")

    exit()

# -----------------------------------
# Generate Text
# -----------------------------------

with torch.no_grad():

    for _ in range(MAX_WORDS):

        x = torch.tensor([encoded])

        prediction = model(x)

        predicted_id = torch.argmax(
            prediction,
            dim=1
        ).item()

        encoded.append(predicted_id)

# -----------------------------------
# Decode IDs into Words
# -----------------------------------

generated_words = []

for number in encoded:

    generated_words.append(
        reverse_vocab[number]
    )

# -----------------------------------
# Display Result
# -----------------------------------

print()

print("=" * 50)
print("Generated Text")
print("=" * 50)

print(" ".join(generated_words))


