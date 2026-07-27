"""
config.py

Purpose
-------
Store all configurable settings
used in the Mini LLM API.

Advantages
----------
1. Easy to maintain
2. Easy to update
3. Avoid duplicate values
4. Professional project structure
"""

# -------------------------------------
# Model Configuration
# -------------------------------------

MODEL_PATH = "../llm/model.pth" 

EMBEDDING_DIM = 16

MAX_GENERATED_WORDS = 20

# -------------------------------------
# API Configuration
# -------------------------------------

API_TITLE = "Mini LLM API"

API_VERSION = "1.0.0"

API_DESCRIPTION = "Backend API for Mini Language Model"

# -------------------------------------
# Device
# -------------------------------------

DEVICE = "cpu"