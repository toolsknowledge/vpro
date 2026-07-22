"""
dataset.py

Purpose
-------
Create training examples for the Mini LLM.

Example

Sentence

python is easy

Training Data

Input      Output

python  -> is

python is -> easy
"""

# Import tokenizer

from tokenizer import encoded_tokens

# -------------------------
# Create Dataset
# -------------------------

inputs = []

outputs = []

# Loop through tokens

for i in range(len(encoded_tokens) - 1):

    input_sequence = encoded_tokens[:i + 1]

    target = encoded_tokens[i + 1]

    inputs.append(input_sequence)

    outputs.append(target)

# -------------------------
# Print Dataset
# -------------------------

print("=" * 50)

print("INPUTS")

print("=" * 50)

for item in inputs:
    print(item)

print()

print("=" * 50)

print("OUTPUTS")

print("=" * 50)

for item in outputs:
    print(item)