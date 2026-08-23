import networkx as nx
def build_graph(relationships):
    graph = nx.DiGraph()
    for source, relationship, target in relationships:
        graph.add_edge(
            source,
            target,
            relationship=relationship
        )
    return graph

def graph_search(
    question,
    graph,
    max_hops=2
):

    question_lower = question.lower()
    relevant_entities = []
    for entity in graph.nodes:
        if entity.lower() in question_lower:
            relevant_entities.append(entity)

    results = []
    for entity in relevant_entities:
        visited = {entity}
        current_nodes = {entity}

        for _ in range(max_hops):

            next_nodes = set()

            for current in current_nodes:

                for target in graph.successors(current):

                    relationship = graph[
                        current
                    ][target]["relationship"]

                    results.append({
                        "text": (
                            f"{current} "
                            f"--[{relationship}]--> "
                            f"{target}"
                        ),
                        "score": 1.0,
                        "source": "graph"
                    })

                    if target not in visited:

                        next_nodes.add(target)
                        visited.add(target)

            current_nodes = next_nodes

    return results