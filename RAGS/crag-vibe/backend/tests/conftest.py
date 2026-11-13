"""Shared test fixtures. No test calls the real OpenAI API or touches backend/chroma_db."""

import hashlib
import math
import re

import pytest
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app import config
from app.services import openai_service, retrieval_service

SAMPLE_PAGES = [
    "Python Variables. A variable is a name that stores a value in memory. "
    "You create a variable by assigning a value with the equals sign, for example age = 20.",
    "Python Lists. A list is an ordered, mutable collection written inside square brackets. "
    "Lists can grow and shrink, and items can be changed with list methods like append and remove.",
    "Exception Handling. An exception is an error that happens while a program runs. "
    "Use try and except blocks to handle errors such as ZeroDivisionError gracefully.",
]


def fake_embed_texts(texts: list[str]) -> list[list[float]]:
    """Deterministic bag-of-words embedding: texts that share words get similar vectors."""
    vectors = []
    for text in texts:
        vector = [0.0] * 256
        for word in re.findall(r"[a-z]+", text.lower()):
            vector[int(hashlib.md5(word.encode()).hexdigest(), 16) % 256] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        vectors.append([value / norm for value in vector])
    return vectors


def write_pdf(path, pages: list[str], header: str = "VPro Skills Test Guide") -> None:
    pdf = canvas.Canvas(str(path), pagesize=A4)
    for number, text in enumerate(pages, start=1):
        pdf.drawString(50, 800, header)
        text_object = pdf.beginText(50, 760)
        for start in range(0, len(text), 90):
            text_object.textLine(text[start:start + 90])
        pdf.drawText(text_object)
        pdf.drawString(280, 30, f"Page {number}")
        pdf.showPage()
    pdf.save()


@pytest.fixture(autouse=True)
def isolated_environment(tmp_path, monkeypatch):
    """Every test gets its own knowledge base folder, ChromaDB folder and fake OpenAI embeddings."""
    knowledge_base = tmp_path / "knowledge_base"
    knowledge_base.mkdir()
    monkeypatch.setattr(config, "KNOWLEDGE_BASE_DIR", knowledge_base)
    monkeypatch.setattr(config, "CHROMA_DB_DIR", tmp_path / "chroma_db")
    monkeypatch.setattr(retrieval_service, "embed_texts", fake_embed_texts)
    cached_functions = (retrieval_service._get_client, openai_service.get_client)  # saved before tests patch them
    for function in cached_functions:
        function.cache_clear()
    yield knowledge_base
    for function in cached_functions:
        function.cache_clear()


@pytest.fixture
def sample_pdf(isolated_environment):
    path = isolated_environment / "sample_guide.pdf"
    write_pdf(path, SAMPLE_PAGES)
    return path
