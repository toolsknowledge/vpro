"""Generate the four sample documents into sample_files/.

These are small, original demo files created by this script (they are not
copies of any other files).  Run:  python scripts/make_sample_files.py
"""
from pathlib import Path

from docx import Document
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

OUT = Path(__file__).resolve().parent.parent / "sample_files"
OUT.mkdir(exist_ok=True)


def make_pdf():
    st = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(OUT / "sample_rag_architecture_notes.pdf"), pagesize=A4)
    page1 = [
        ("Title", "RAG Architecture Notes"),
        ("Heading2", "1. What is Retrieval-Augmented Generation?"),
        ("BodyText", "RAG retrieves relevant documents and supplies them as context to a language model. "
                     "The model answers from that context instead of relying only on what it memorised during training."),
        ("Heading2", "2. The indexing pipeline"),
        ("BodyText", "The indexing pipeline runs once per document: Upload, Extract, Clean, Chunk, Embed, and Store in ChromaDB. "
                     "Extraction turns files into text. Cleaning normalises whitespace. Chunking splits text into pieces of about "
                     "800 tokens with 120 tokens of overlap. Embedding converts every chunk into a numerical vector. "
                     "The vectors, the chunk text and the source metadata are stored in a persistent ChromaDB collection."),
        ("Heading2", "3. Chunking versus embeddings"),
        ("BodyText", "Chunking splits long text into smaller passages so that each passage fits the model's context window and "
                     "focuses on one topic. Embeddings are different: an embedding is a list of numbers that represents the meaning of "
                     "a chunk, so that chunks with similar meaning can be found by comparing vectors."),
    ]
    page2 = [
        ("Heading2", "4. The question-answering pipeline"),
        ("BodyText", "When a user asks a question, the same embedding model converts the question into a query vector. "
                     "ChromaDB returns the top K chunks whose vectors are closest to the query vector. These chunks are placed in a prompt "
                     "together with the question, and the chat model writes an answer with citations to the source pages."),
        ("Heading2", "5. Why overlap matters"),
        ("BodyText", "Overlap repeats a small amount of text at the end of one chunk at the start of the next, so a sentence that "
                     "falls on a boundary is still fully visible in at least one chunk."),
    ]
    story = []
    for sty, txt in page1:
        story += [Paragraph(txt, st[sty]), Spacer(1, 10)]
    story.append(PageBreak())
    for sty, txt in page2:
        story += [Paragraph(txt, st[sty]), Spacer(1, 10)]
    doc.build(story)


def make_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "Course Catalog"
    ws.append(["Course", "Duration", "Fee", "Mode", "Level"])
    rows = [
        ("Python Full Stack", "16 weeks", 30000, "Online", "Beginner"),
        ("Data Science with Python", "20 weeks", 40000, "Hybrid", "Intermediate"),
        ("Generative AI and RAG", "10 weeks", 35000, "Online", "Intermediate"),
        ("Java Full Stack", "18 weeks", 32000, "Classroom", "Beginner"),
        ("DevOps on AWS", "12 weeks", 28000, "Online", "Intermediate"),
    ]
    for r in rows:
        ws.append(r)
    ws2 = wb.create_sheet("Batches")
    ws2.append(["Course", "Start Date", "Trainer", "Seats"])
    ws2.append(["Python Full Stack", "2026-01-12", "Anita Rao", 25])
    ws2.append(["Generative AI and RAG", "2026-02-02", "Kiran Kumar", 20])
    ws2.append(["DevOps on AWS", "2026-02-16", None, 15])  # missing trainer on purpose
    wb.save(OUT / "sample_course_catalog.xlsx")


def make_docx():
    d = Document()
    d.add_heading("Training Policy", 0)
    d.add_heading("Attendance", 1)
    d.add_paragraph("Learners must attend at least 80 percent of live sessions to be eligible for a course certificate.")
    d.add_heading("Project assessment", 1)
    d.add_paragraph("Every course ends with a capstone project. Projects are assessed on correctness, code quality, "
                    "documentation and a final presentation. A project score of at least 60 percent is required to pass.")
    d.add_heading("Refund policy", 1)
    d.add_paragraph("Fees are refundable in full within 7 days of the batch start date. After 7 days no refund is available.")
    t = d.add_table(rows=3, cols=2)
    t.style = "Table Grid"
    for i, (a, b) in enumerate([("Assessment component", "Weight"), ("Capstone project", "50%"), ("Weekly quizzes", "20%")]):
        t.cell(i, 0).text, t.cell(i, 1).text = a, b
    d.save(OUT / "sample_training_policy.docx")


def make_txt():
    (OUT / "sample_course_overview.txt").write_text(
        "VPro Skills EduTech Course Overview\n\n"
        "About the Generative AI and RAG course:\n"
        "This 10-week course teaches learners to build document question answering applications with Python, "
        "OpenAI models and ChromaDB.\n\n"
        "Course modules:\n"
        "Module 1 covers embeddings and vector search. Module 2 covers chunking strategies and metadata. "
        "Module 3 covers prompt design and grounded answers with citations. Module 4 covers evaluation and deployment.\n\n"
        "Prerequisites:\n"
        "Learners should know basic Python and be comfortable using the command line.\n",
        encoding="utf-8")


if __name__ == "__main__":
    make_pdf(); make_xlsx(); make_docx(); make_txt()
    print("Created:", *sorted(p.name for p in OUT.iterdir()), sep="\n  ")
