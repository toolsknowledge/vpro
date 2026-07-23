"""
train.py

Purpose
-------
Train the Mini LLM.

Steps

1. Load Dataset
2. Create Model
3. Define Loss Function
4. Define Optimizer
5. Train
6. Save Model
"""

import torch
import torch.nn as nn
import torch.optim as optim

from tokenizer import vocab
from dataset import inputs, outputs
from model import MiniLLM

# ---------------------------------
# Hyper Parameters
# ---------------------------------

VOCAB_SIZE = len(vocab)

EMBEDDING_DIM = 16

EPOCHS = 1000

LEARNING_RATE = 0.01

# ---------------------------------
# Create Model
# ---------------------------------

model = MiniLLM(
    vocab_size=VOCAB_SIZE,
    embedding_dim=EMBEDDING_DIM
)

# ---------------------------------
# Loss Function
# ---------------------------------

criterion = nn.CrossEntropyLoss()

# ---------------------------------
# Optimizer
# ---------------------------------

optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)

# ---------------------------------
# Training Loop
# ---------------------------------

for epoch in range(EPOCHS):

    total_loss = 0

    for x, y in zip(inputs, outputs):

        x = torch.tensor([x])

        y = torch.tensor([y])

        prediction = model(x)

        loss = criterion(prediction, y)

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(
        f"Epoch {epoch+1}/{EPOCHS}  Loss = {total_loss:.4f}"
    )

# ---------------------------------
# Save Model
# ---------------------------------

torch.save(
    model.state_dict(),
    "model.pth"
)

print("\nTraining Completed.")

print("Model Saved Successfully.")