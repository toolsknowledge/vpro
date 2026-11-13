# implement keyword search and vector search
from collections import defaultdict
import re
from rank_bm25 import BM25Okapi

def tokenize(text: str):
    # Preserve underscores and hyphens in identifiers like JWT_SECRET_KEY.
    return re.findall(r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*", text.lower())

class HybridRetriever:
    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k
        self.ids, self.documents, self.metadatas, self.bm25 = [], [], [], None

    def rebuild_from_chroma(self, collection):
        data = collection.get(include=["documents", "metadatas"])
        self.ids = data.get("ids", [])
        self.documents = data.get("documents", []) or []
        self.metadatas = data.get("metadatas", []) or []
        tokenized = [tokenize(doc) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized) if tokenized and any(tokenized) else None

    def search(self, query, embedding_model, collection, top_k=5):
        if not self.documents or not query.strip():
            return []
        candidate_count = min(max(top_k * 3, 10), len(self.documents))
        vector = embedding_model.encode([query], normalize_embeddings=True).tolist()[0]
        found = collection.query(
            query_embeddings=[vector], n_results=candidate_count,
            include=["documents", "metadatas", "distances"]
        )
        semantic_ranks, payloads = {}, {}
        ids = found.get("ids", [[]])[0]
        docs = found.get("documents", [[]])[0]
        metas = found.get("metadatas", [[]])[0]
        for rank, (doc_id, doc, meta) in enumerate(zip(ids, docs, metas), 1):
            semantic_ranks[doc_id] = rank
            payloads[doc_id] = {"text": doc, "metadata": meta or {}}

        bm25_ranks = {}
        if self.bm25:
            scores = self.bm25.get_scores(tokenize(query))
            order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            for rank, idx in enumerate(order[:candidate_count], 1):
                if scores[idx] <= 0:
                    continue
                doc_id = self.ids[idx]
                bm25_ranks[doc_id] = rank
                payloads.setdefault(doc_id, {
                    "text": self.documents[idx],
                    "metadata": self.metadatas[idx] if idx < len(self.metadatas) else {}
                })

        fused = defaultdict(float)
        for doc_id, rank in semantic_ranks.items():
            fused[doc_id] += 1 / (self.rrf_k + rank)
        for doc_id, rank in bm25_ranks.items():
            fused[doc_id] += 1 / (self.rrf_k + rank)

        results = []
        for doc_id in sorted(fused, key=fused.get, reverse=True)[:top_k]:
            item = payloads[doc_id]
            meta = item["metadata"]
            results.append({
                "id": doc_id, "text": item["text"],
                "source": meta.get("source", "Unknown source"),
                "chunk": meta.get("chunk", "?"),
                "rrf_score": fused[doc_id],
                "semantic_rank": semantic_ranks.get(doc_id, "—"),
                "bm25_rank": bm25_ranks.get(doc_id, "—")
            })
        return results