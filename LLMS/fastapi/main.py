"""
main.py

Purpose
-------
FastAPI Entry Point

Responsibilities

1. Create FastAPI Application
2. Create API Endpoints
3. Receive Requests
4. Call Mini LLM
5. Return Responses
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION
)

from schemas import (
    PredictionRequest,
    PredictionResponse
)

from llm_service import generate_text

# ---------------------------------------
# Create FastAPI Application
# ---------------------------------------

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# ------------------------------------
# Enable CORS
# ------------------------------------

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# Home API
# ---------------------------------------

@app.get("/")
def home():

    return {
        "message": "Mini LLM API is Running Successfully"
    }


# ---------------------------------------
# Health API
# ---------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ---------------------------------------
# Prediction API
# ---------------------------------------

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: PredictionRequest):

    generated_text = generate_text(request.text)

    return PredictionResponse(
        generated_text=generated_text
    )