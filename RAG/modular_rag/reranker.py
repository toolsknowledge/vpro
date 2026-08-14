def rerank(
    keyword_results,
    vector_results,
    graph_results,
    top_k=8
):

    combined = {}

    # Keyword results
    for result in keyword_results:

        key = result["text"]

        combined[key] = {
            "text": result["text"],
            "score": 0,
            "sources": []
        }

        combined[key]["score"] += (
            result["score"] * 1.0
        )

        combined[key]["sources"].append(
            "keyword"
        )

    # Vector results
    for result in vector_results:

        key = result["text"]

        if key not in combined:

            combined[key] = {
                "text": result["text"],
                "score": 0,
                "sources": []
            }

        combined[key]["score"] += (
            result["score"] * 2.0
        )

        combined[key]["sources"].append(
            "vector"
        )

    # Graph results
    for result in graph_results:

        key = result["text"]

        if key not in combined:

            combined[key] = {
                "text": result["text"],
                "score": 0,
                "sources": []
            }

        combined[key]["score"] += (
            result["score"] * 1.5
        )

        combined[key]["sources"].append(
            "graph"
        )

    results = list(
        combined.values()
    )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]