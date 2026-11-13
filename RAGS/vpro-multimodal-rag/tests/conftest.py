import hashlib
import sys
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.document_registry import DocumentRegistry  # noqa: E402
from backend.vector_store import VectorStore  # noqa: E402
from config.settings import Settings  # noqa: E402


class FakeEmbedder:
    """Deterministic, offline stand-in for OpenAIEmbedder (bag-of-words hashing, 64 dims)."""
    model = "fake-embed"
    retries = 0
    retry_log: list = []

    def _vec(self, text):
        v = [0.0] * 64
        for w in text.lower().split():
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % 64] += 1.0
        if not any(v):
            v[0] = 1.0
        return v

    def embed_texts(self, texts, progress=None):
        out = [self._vec(t) for t in texts]
        if progress:
            progress(len(out), len(out))
        return out

    def embed_query(self, text):
        if not text.strip():
            raise ValueError("empty")
        return self._vec(text)


class FakeChatClient:
    def __init__(self, reply="Answer [1]"):
        self.reply, self.calls = reply, []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kw):
        self.calls.append(kw)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=self.reply))])


@pytest.fixture
def settings(tmp_path):
    return Settings(openai_api_key="sk-test", chroma_dir=tmp_path / "chroma", data_dir=tmp_path / "data")


@pytest.fixture
def registry(settings):
    return DocumentRegistry(settings.registry_path, settings.processed_dir, settings.uploads_dir)


@pytest.fixture
def store(settings):
    return VectorStore(settings.chroma_dir, "test_collection", "fake-embed")


@pytest.fixture
def embedder():
    return FakeEmbedder()


# ---- sample file builders ----
@pytest.fixture
def make_docx():
    def _make(paragraphs=(("Heading 1", "Policy"), ("Normal", "Be kind.")), table=None):
        from docx import Document
        d = Document()
        for style, text in paragraphs:
            if style.startswith("Heading"):
                d.add_heading(text, int(style.split()[-1]))
            else:
                d.add_paragraph(text)
        if table:
            t = d.add_table(rows=len(table), cols=len(table[0]))
            for i, row in enumerate(table):
                for j, v in enumerate(row):
                    t.cell(i, j).text = v
        b = BytesIO(); d.save(b); return b.getvalue()
    return _make


@pytest.fixture
def make_xlsx():
    def _make(sheets):
        from openpyxl import Workbook
        wb = Workbook(); wb.remove(wb.active)
        for name, rows in sheets.items():
            ws = wb.create_sheet(name)
            for r in rows:
                ws.append(r)
        b = BytesIO(); wb.save(b); return b.getvalue()
    return _make


@pytest.fixture
def make_pdf():
    def _make(pages):
        from reportlab.pdfgen import canvas
        b = BytesIO(); c = canvas.Canvas(b)
        for text in pages:
            if text:
                c.drawString(72, 750, text)
            c.showPage()
        c.save(); return b.getvalue()
    return _make
