from loaders.pdf_loader import load_pdf
from splitter.text_spiltter import split_documents
from embeddings.embedding_model import get_embedding_model
print("Loading PDF...")
documents = load_pdf("data/python_sample_notes.pdf")
print(f"Pages Loaded : {len(documents)}")
print()
print("Splitting Documents...")
chunks = split_documents(documents)
print(f"Chunks Created : {len(chunks)}")
print()
print("Loading Embedding Model...")
embedding = get_embedding_model()
print(type(embedding))
print()
print("Part-1 Completed Successfully")