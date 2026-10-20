import json
import os
import numpy as np
import chromadb
import faiss


class ChromaStore:
    """ChromaDB implementation of the vector-store interface."""

    def __init__(self, folder="chroma_data"):
        self.client = chromadb.PersistentClient(path=folder)
        self.collection = self.client.get_or_create_collection(
            name="document_chunks",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks, embeddings):
        ids = [f"chunk_{i}" for i in range(self.collection.count(),
                                            self.collection.count() + len(chunks))]
        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
        )

    def search(self, query_embedding, top_k=4):
        if self.collection.count() == 0:
            return []
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "distances"]
        )
        docs = result.get("documents", [[]])[0]
        distances = result.get("distances", [[]])[0]
        return [{"text": doc, "score": float(distance)} for doc, distance in zip(docs, distances)]


class FaissStore:
    """FAISS implementation with the same methods as ChromaStore."""

    def __init__(self, folder="faiss_data"):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)
        self.index_path = os.path.join(folder, "index.faiss")
        self.data_path = os.path.join(folder, "chunks.json")
        self.index = None
        self.chunks = []

        if os.path.exists(self.index_path) and os.path.exists(self.data_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

    def add_documents(self, chunks, embeddings):
        vectors = np.asarray(embeddings, dtype="float32")
        faiss.normalize_L2(vectors)

        if self.index is None:
            self.index = faiss.IndexFlatIP(vectors.shape[1])

        self.index.add(vectors)
        self.chunks.extend(chunks)
        faiss.write_index(self.index, self.index_path)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)

    def search(self, query_embedding, top_k=4):
        if self.index is None or not self.chunks:
            return []
        query = np.asarray([query_embedding], dtype="float32")
        faiss.normalize_L2(query)
        k = min(top_k, len(self.chunks))
        scores, positions = self.index.search(query, k)
        return [
            {"text": self.chunks[int(pos)], "score": float(score)}
            for score, pos in zip(scores[0], positions[0])
            if int(pos) >= 0
        ]


def create_vector_store():
    """Only this factory decides which vector database is used."""
    database = os.getenv("VECTOR_DB", "chroma").lower()

    if database == "chroma":
        return ChromaStore()
    if database == "faiss":
        return FaissStore()

    raise ValueError("VECTOR_DB must be 'chroma' or 'faiss'.")
