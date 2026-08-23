def keyword_search(question, documents, top_k=5):
    question_words = set(
        question.lower().split()
    )
    results = []
    for document in documents:
        document_words = set(
            document["text"].lower().split()
        )
        matching_words = (
            question_words &
            document_words
        )
        score = len(matching_words)
        if score > 0:
            results.append({
                "id": document["id"],
                "text": document["text"],
                "score": score,
                "source": "keyword"
            })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]