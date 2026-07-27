"""
llm_service.py

Purpose
-------
Load the trained Mini LLM and
generate text for the FastAPI backend.
"""

import os
import sys
import torch

# ---------------------------------------
# Add step1_llm folder to Python path
# ---------------------------------------

CURRENT_DIR = os.path.dirname(__file__)

STEP1_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "../llm")
)

if STEP1_DIR not in sys.path:
    sys.path.append(STEP1_DIR)

# ---------------------------------------
# Import Step-1 Files
# ---------------------------------------

from tokenizer import vocab, reverse_vocab
from model import MiniLLM

from config import (
    MODEL_PATH,
    EMBEDDING_DIM,
    MAX_GENERATED_WORDS,
    DEVICE
)

# ---------------------------------------
# Load Model Once
# ---------------------------------------

VOCAB_SIZE = len(vocab)

model = MiniLLM(
    vocab_size=VOCAB_SIZE,
    embedding_dim=EMBEDDING_DIM
)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=DEVICE)
)

model.eval()

# ---------------------------------------
# Prediction Function
# ---------------------------------------

def generate_text(text: str):

    text = text.lower()

    tokens = text.split()

    encoded = []

    for word in tokens:

        if word in vocab:

            encoded.append(vocab[word])

    if len(encoded) == 0:

        return "No known words found."

    with torch.no_grad():

        for _ in range(MAX_GENERATED_WORDS):

            x = torch.tensor([encoded])

            prediction = model(x)

            predicted_id = torch.argmax(
                prediction,
                dim=1
            ).item()

            encoded.append(predicted_id)

    generated_words = []

    for number in encoded:

        generated_words.append(
            reverse_vocab[number]
        )

    return " ".join(generated_words)