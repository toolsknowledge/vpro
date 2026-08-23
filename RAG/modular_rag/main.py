from knowledge import (
    documents,
    relationships
)

from query_processor import (
    process_query
)

from keyword_retriever import (
    keyword_search
)

from vector_retriever import (
    vector_search
)

from graph_retriever import (
    build_graph,
    graph_search
)

from reranker import (
    rerank
)

from context_builder import (
    build_context
)

from generator import (
    generate_answer
)


def modular_rag(question):

    print("\n" + "=" * 70)
    print("MODULAR RAG PIPELINE")
    print("=" * 70)

    # ----------------------------------------
    # 1. Query Processing
    # ----------------------------------------

    print("\n[1] Query Processing")

    question = process_query(
        question
    )

    print("Question:", question)


    # ----------------------------------------
    # 2. Build Graph
    # ----------------------------------------

    print("\n[2] Building Knowledge Graph")

    graph = build_graph(
        relationships
    )

    print(
        "Nodes:",
        graph.number_of_nodes()
    )

    print(
        "Edges:",
        graph.number_of_edges()
    )


    # ----------------------------------------
    # 3. Keyword Search
    # ----------------------------------------

    print("\n[3] Keyword Search")

    keyword_results = keyword_search(
        question,
        documents
    )

    for result in keyword_results:

        print(
            " ",
            result["text"]
        )


    # ----------------------------------------
    # 4. Vector Search
    # ----------------------------------------

    print("\n[4] Vector Search")

    vector_results = vector_search(
        question,
        documents
    )

    for result in vector_results:

        print(
            " ",
            result["text"],
            "Score:",
            round(
                result["score"],
                3
            )
        )


    # ----------------------------------------
    # 5. Graph Search
    # ----------------------------------------

    print("\n[5] Graph Search")

    graph_results = graph_search(
        question,
        graph,
        max_hops=2
    )

    for result in graph_results:

        print(
            " ",
            result["text"]
        )


    # ----------------------------------------
    # 6. Reranking
    # ----------------------------------------

    print("\n[6] Reranking")

    ranked_results = rerank(
        keyword_results,
        vector_results,
        graph_results
    )

    for result in ranked_results:

        print(
            " ",
            round(
                result["score"],
                3
            ),
            "→",
            result["text"]
        )


    # ----------------------------------------
    # 7. Context Builder
    # ----------------------------------------

    print("\n[7] Context Builder")

    context = build_context(
        ranked_results
    )

    print(context)


    # ----------------------------------------
    # 8. LLM
    # ----------------------------------------

    print("\n[8] LLM Generation")

    answer = generate_answer(
        question,
        context
    )


    # ----------------------------------------
    # 9. Final Answer
    # ----------------------------------------

    print("\n[9] FINAL ANSWER")

    print(answer)

    return answer


if __name__ == "__main__":

    while True:

        question = input(
            "\nAsk a question "
            "(type exit to stop): "
        )

        if question.lower().strip() == "exit":

            print("Goodbye!")

            break

        if not question.strip():

            print(
                "Please enter a question."
            )

            continue

        try:

            modular_rag(
                question
            )

        except Exception as e:

            print(
                "\nERROR:",
                str(e)
            )