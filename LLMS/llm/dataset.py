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
# print(len([18, 11, 5, 18, 11, 16, 2, 9, 11, 1, 14, 12, 11, 7, 4, 12, 11, 16, 18, 17, 11, 10, 8, 13, 
# 18, 23, 13, 0, 22, 13, 14, 12, 21, 6, 3, 20, 19, 15)]
print(len(encoded_tokens))

for i in range(len(encoded_tokens) - 1):
    input_sequence = encoded_tokens[:i + 1] # [0:1]
    print("Hello.....",i,input_sequence)
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