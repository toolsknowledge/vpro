def build_context(results):

    context_parts = []

    for result in results:

        context_parts.append(
            f"- {result['text']}"
        )

    return "\n".join(
        context_parts
    )