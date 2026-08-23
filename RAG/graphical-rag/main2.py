import os
import json
import networkx as nx
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. LOAD ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is missing. Add it to your .env file."
    )

client = OpenAI(api_key=api_key)

MODEL = "gpt-4o-mini"


# ============================================================
# 2. KNOWLEDGE BASE
# ============================================================

knowledge_base = """
VPro Skills is a technology training institute.

Sambasiva Rao is a Technical Architect at VPro Skills.
Sambasiva Rao has 17 years of experience.

VPro Skills provides Python training.
VPro Skills provides Java training.
VPro Skills provides Data Structures training.
VPro Skills provides Generative AI training.
VPro Skills provides Agentic AI training.

Python training includes NumPy and Pandas.

Generative AI training includes RAG and Large Language Models.

Agentic AI training includes LangChain and LangGraph.

LangChain is a framework used for building applications
with Large Language Models.

LangGraph is a framework used for building stateful
and multi-step AI agent workflows.

RAG stands for Retrieval-Augmented Generation.

RAG combines information retrieval with Large Language Models.
"""


# ============================================================
# 3. CREATE KNOWLEDGE GRAPH
# ============================================================

graph = nx.DiGraph()


# ============================================================
# 4. EXTRACT ENTITIES AND RELATIONSHIPS
# ============================================================

def extract_graph_data(text):

    prompt = f"""
Extract entities and relationships from the text below.

Return ONLY JSON with this exact structure:

{{
    "entities": [
        "entity1",
        "entity2"
    ],
    "relationships": [
        {{
            "source": "entity1",
            "relationship": "relationship",
            "target": "entity2"
        }}
    ]
}}

Rules:
1. Every source and target must appear in entities.
2. Keep entity names short and meaningful.
3. Keep relationship names short.
4. Do not add information that is not present in the text.

Text:

{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are a Knowledge Graph extraction system.
Always return valid JSON.
Do not return markdown.
Do not return explanations.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "LLM returned an empty response while creating the graph."
        )

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print("\nInvalid JSON returned by LLM:")
        print(content)
        raise ValueError("Could not parse graph JSON.") from e


# ============================================================
# 5. BUILD KNOWLEDGE GRAPH
# ============================================================

def build_graph():

    print("\n" + "=" * 60)
    print("BUILDING KNOWLEDGE GRAPH")
    print("=" * 60)

    data = extract_graph_data(knowledge_base)

    graph.clear()

    for entity in data.get("entities", []):

        entity = entity.strip()

        if entity:
            graph.add_node(entity)

    for relation in data.get("relationships", []):

        source = relation.get("source", "").strip()
        relationship = relation.get("relationship", "").strip()
        target = relation.get("target", "").strip()

        if not source or not target:
            continue

        graph.add_node(source)
        graph.add_node(target)

        graph.add_edge(
            source,
            target,
            relationship=relationship
        )

    print(f"\nEntities created : {graph.number_of_nodes()}")
    print(f"Relationships    : {graph.number_of_edges()}")


# ============================================================
# 6. DISPLAY GRAPH IN TERMINAL
# ============================================================

def display_graph():

    print("\n" + "=" * 60)
    print("KNOWLEDGE GRAPH")
    print("=" * 60)

    for source, target, data in graph.edges(data=True):

        print(
            f"{source} "
            f"--[{data['relationship']}]--> "
            f"{target}"
        )


# ============================================================
# 7. VISUALIZE KNOWLEDGE GRAPH
# ============================================================

def visualize_graph(
    highlighted_nodes=None,
    highlighted_edges=None,
    title="Graph RAG - Knowledge Graph"
):

    highlighted_nodes = set(
        highlighted_nodes or []
    )

    highlighted_edges = set(
        highlighted_edges or []
    )

    plt.figure(figsize=(16, 10))

    pos = nx.spring_layout(
        graph,
        seed=42,
        k=2.2
    )

    normal_nodes = [
        node
        for node in graph.nodes
        if node not in highlighted_nodes
    ]

    special_nodes = [
        node
        for node in graph.nodes
        if node in highlighted_nodes
    ]

    normal_edges = [
        edge
        for edge in graph.edges
        if edge not in highlighted_edges
    ]

    special_edges = [
        edge
        for edge in graph.edges
        if edge in highlighted_edges
    ]

    # Normal nodes
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=normal_nodes,
        node_size=2800
    )

    # Highlighted nodes
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=special_nodes,
        node_size=3400,
        node_shape="o"
    )

    # Normal edges
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=normal_edges,
        arrows=True,
        arrowsize=22,
        width=2
    )

    # Highlighted edges
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=special_edges,
        arrows=True,
        arrowsize=28,
        width=4
    )

    # Node labels
    nx.draw_networkx_labels(
        graph,
        pos,
        font_size=10,
        font_weight="bold"
    )

    # Relationship labels
    edge_labels = nx.get_edge_attributes(
        graph,
        "relationship"
    )

    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=edge_labels,
        font_size=9
    )

    plt.title(
        title,
        fontsize=18,
        fontweight="bold"
    )

    plt.axis("off")
    plt.tight_layout()
    plt.show()


# ============================================================
# 8. FIND RELEVANT ENTITIES
# ============================================================

def find_relevant_entities(question):

    entities = list(graph.nodes)

    prompt = f"""
You are selecting entities from a knowledge graph.

Available entities:

{json.dumps(entities, indent=2)}

User question:

{question}

Select ONLY entities from the available list
that are directly relevant to the question.

Return JSON:

{{
    "entities": ["entity1", "entity2"]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are a Knowledge Graph entity selection system.

Return only valid JSON.
Never invent entities.
Only select entities from the supplied list.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    if not content:
        return []

    try:
        data = json.loads(content)
    except json.JSONDecodeError:

        print("\nWarning: Could not parse entity response.")
        print("LLM response:", content)

        return []

    selected_entities = data.get("entities", [])

    valid_entities = []

    for entity in selected_entities:

        if entity in graph:
            valid_entities.append(entity)

    return valid_entities


# ============================================================
# 9. GRAPH RETRIEVAL WITH MULTI-HOP TRAVERSAL
# ============================================================

def retrieve_from_graph(
    question,
    max_hops=2
):

    relevant_entities = find_relevant_entities(question)

    print("\nRelevant entities:")

    if not relevant_entities:

        print("No relevant entities found.")
        return [], [], []

    for entity in relevant_entities:
        print(f"- {entity}")

    retrieved_relationships = set()
    retrieved_edges = set()
    retrieved_nodes = set(relevant_entities)

    # --------------------------------------------------------
    # Traverse outgoing relationships
    # --------------------------------------------------------

    for entity in relevant_entities:

        current_nodes = {entity}
        visited = {entity}

        for _ in range(max_hops):

            next_nodes = set()

            for current in current_nodes:

                for target in graph.successors(current):

                    relationship = graph[
                        current
                    ][target]["relationship"]

                    retrieved_relationships.add(
                        f"{current} "
                        f"--[{relationship}]--> "
                        f"{target}"
                    )

                    retrieved_edges.add(
                        (current, target)
                    )

                    retrieved_nodes.add(target)

                    if target not in visited:

                        next_nodes.add(target)
                        visited.add(target)

            current_nodes = next_nodes

            if not current_nodes:
                break

    # --------------------------------------------------------
    # Include incoming relationships
    # --------------------------------------------------------

    for entity in relevant_entities:

        for source in graph.predecessors(entity):

            relationship = graph[
                source
            ][entity]["relationship"]

            retrieved_relationships.add(
                f"{source} "
                f"--[{relationship}]--> "
                f"{entity}"
            )

            retrieved_edges.add(
                (source, entity)
            )

            retrieved_nodes.add(source)

    return (
        list(retrieved_relationships),
        list(retrieved_nodes),
        list(retrieved_edges)
    )


# ============================================================
# 10. GENERATE ANSWER
# ============================================================

def generate_answer(
    question,
    graph_context
):

    context = "\n".join(graph_context)

    prompt = f"""
You are a Graph RAG assistant.

Answer the question using ONLY the
knowledge graph relationships provided below.

Knowledge Graph Context:

{context}

Question:

{question}

Rules:

1. Do not use outside knowledge.
2. Do not invent relationships.
3. If the graph does not contain enough information,
   say:

   "I don't have enough information in the knowledge graph."

Answer clearly and concisely.
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
You answer questions using graph-retrieved knowledge.
Always stay grounded in the supplied graph context.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ============================================================
# 11. GRAPH RAG PIPELINE
# ============================================================

def graph_rag(question):

    print("\n" + "=" * 60)
    print("GRAPH RAG PIPELINE")
    print("=" * 60)

    print("\nQuestion:")
    print(question)

    # --------------------------------------------------------
    # STEP 1: Find relevant entities
    # --------------------------------------------------------

    print("\n[1] Finding relevant entities...")

    (
        graph_context,
        retrieved_nodes,
        retrieved_edges
    ) = retrieve_from_graph(
        question,
        max_hops=2
    )

    # --------------------------------------------------------
    # STEP 2: Graph retrieval
    # --------------------------------------------------------

    print("\n[2] Graph retrieval...")

    if not graph_context:

        print("No graph context found.")

        return (
            "I don't have enough information "
            "in the knowledge graph."
        )

    for item in graph_context:
        print("   ", item)

    # --------------------------------------------------------
    # STEP 3: Visualize retrieved graph
    # --------------------------------------------------------

    print(
        "\n[3] Opening graph visualization..."
    )

    visualize_graph(
        highlighted_nodes=retrieved_nodes,
        highlighted_edges=retrieved_edges,
        title="Graph RAG - Retrieved Knowledge"
    )

    # --------------------------------------------------------
    # STEP 4: Generate answer
    # --------------------------------------------------------

    print(
        "\n[4] Generating answer using graph context..."
    )

    answer = generate_answer(
        question,
        graph_context
    )

    return answer


# ============================================================
# 12. MAIN
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("              GRAPH RAG DEMO")
    print("=" * 60)

    # --------------------------------------------------------
    # Build graph
    # --------------------------------------------------------

    build_graph()

    # --------------------------------------------------------
    # Display graph in terminal
    # --------------------------------------------------------

    display_graph()

    # --------------------------------------------------------
    # Display complete graph
    # --------------------------------------------------------

    print(
        "\nOpening complete Knowledge Graph..."
    )

    visualize_graph(
        title="Graph RAG - Complete Knowledge Graph"
    )

    # --------------------------------------------------------
    # Ask questions
    # --------------------------------------------------------

    while True:

        question = input(
            "\nAsk a question "
            "(type 'exit' to stop): "
        )

        if question.lower().strip() == "exit":

            print("\nGoodbye!")
            break

        if not question.strip():

            print("Please enter a question.")
            continue

        try:

            answer = graph_rag(question)

            print("\n" + "=" * 60)
            print("FINAL ANSWER")
            print("=" * 60)

            print(answer)

        except Exception as e:

            print("\nError:", str(e))