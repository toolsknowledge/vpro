"""
schemas.py

Purpose
-------
Define Request and Response models
for our Mini LLM API.
"""

from pydantic import BaseModel


# --------------------------------------
# Request Model
# --------------------------------------

class PredictionRequest(BaseModel):

    text: str


# --------------------------------------
# Response Model
# --------------------------------------

class PredictionResponse(BaseModel):

    generated_text: str