from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def vector_search(question, documents, top_k=5):
    texts = [
        document["text"]
        for document in documents
    ]
    vectorizer = TfidfVectorizer()
    document_vectors = vectorizer.fit_transform(
        texts
    )
    question_vector = vectorizer.transform(
        [question]
    )
    similarities = cosine_similarity(
        question_vector,
        document_vectors
    )[0]
    results = []
    for index, score in enumerate(similarities):
        if score > 0:
            results.append({
                "id": documents[index]["id"],
                "text": documents[index]["text"],
                "score": float(score),
                "source": "vector"
            })
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    return results[:top_k]