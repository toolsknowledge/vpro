import faiss

index = faiss.read_index("documents.index")
print("Vectors loaded:", index.ntotal)

