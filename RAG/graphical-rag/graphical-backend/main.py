import os
import json
import networkx as nx

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. LOAD ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Add it to your .env file."
    )

client = OpenAI(api_key=api_key)


# ============================================================
# 2. MODEL
# ============================================================

MODEL = "gpt-4o-mini"


# ============================================================
# 3. KNOWLEDGE BASE
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
# 4. CREATE KNOWLEDGE GRAPH
# ============================================================

graph = nx.DiGraph()


# ============================================================
# 5. EXTRACT GRAPH DATA
# ============================================================

def extract_graph_data(text):
            # VPro Skills Provides AgenticAI
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
        response_format={
            "type": "json_object"
        },
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
            "LLM returned an empty response "
            "while creating the graph."
        )

    try:
        data = json.loads(content)

    except json.JSONDecodeError as e:

        print("\nInvalid JSON returned by LLM:")
        print(content)

        raise ValueError(
            "Could not parse graph JSON."
        ) from e

    return data


# ============================================================
# 6. BUILD KNOWLEDGE GRAPH
# ============================================================

def build_graph():

    print("\n" + "=" * 60)
    print("BUILDING KNOWLEDGE GRAPH")
    print("=" * 60)

    data = extract_graph_data(
        knowledge_base
    )

    # --------------------------------------------------------
    # Add entities
    # --------------------------------------------------------

    for entity in data.get("entities", []):

        entity = entity.strip()

        if entity:
            graph.add_node(entity)

    # --------------------------------------------------------
    # Add relationships
    # --------------------------------------------------------

    for relation in data.get(
        "relationships",
        []
    ):

        source = relation.get(
            "source",
            ""
        ).strip()

        relationship = relation.get(
            "relationship",
            ""
        ).strip()

        target = relation.get(
            "target",
            ""
        ).strip()

        if not source or not target:
            continue

        graph.add_node(source)
        graph.add_node(target)

        graph.add_edge(
            source,
            target,
            relationship=relationship
        )

    print(
        f"\nEntities created : "
        f"{graph.number_of_nodes()}"
    )

    print(
        f"Relationships     : "
        f"{graph.number_of_edges()}"
    )


# ============================================================
# 7. DISPLAY KNOWLEDGE GRAPH
# ============================================================

def display_graph():

    print("\n" + "=" * 60)
    print("KNOWLEDGE GRAPH")
    print("=" * 60)

    for source, target, data in graph.edges(
        data=True
    ):

        print(
            f"{source} "
            f"--[{data['relationship']}]--> "
            f"{target}"
        )


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
        response_format={
            "type": "json_object"
        },
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

        print(
            "\nWarning: Could not parse entity response."
        )

        print(
            "LLM response:",
            content
        )

        return []

    selected_entities = data.get(
        "entities",
        []
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Only keep entities that actually exist in graph.
    # --------------------------------------------------------

    valid_entities = []

    for entity in selected_entities:

        if entity in graph:

            valid_entities.append(entity)

    return valid_entities


# ============================================================
# 9. GRAPH RETRIEVAL
# ============================================================

def retrieve_from_graph(
    question,
    max_hops=2
):

    relevant_entities = find_relevant_entities(
        question
    )

    print(
        "\nRelevant entities:"
    )

    if not relevant_entities:

        print(
            "No relevant entities found."
        )

        return []

    for entity in relevant_entities:

        print(
            f"- {entity}"
        )

    retrieved_relationships = set()

    # --------------------------------------------------------
    # Traverse graph
    # --------------------------------------------------------

    for entity in relevant_entities:

        if entity not in graph:
            continue

        # ----------------------------------------------------
        # Outgoing relationships
        # ----------------------------------------------------

        current_nodes = {
            entity
        }

        visited = {
            entity
        }

        for _ in range(max_hops):

            next_nodes = set()

            for current in current_nodes:

                for target in graph.successors(
                    current
                ):

                    relationship = graph[
                        current
                    ][target][
                        "relationship"
                    ]

                    retrieved_relationships.add(
                        f"{current} "
                        f"--[{relationship}]--> "
                        f"{target}"
                    )

                    if target not in visited:

                        next_nodes.add(
                            target
                        )

                        visited.add(
                            target
                        )

            current_nodes = next_nodes

            if not current_nodes:
                break

        # ----------------------------------------------------
        # Incoming relationships
        # ----------------------------------------------------

        for source in graph.predecessors(
            entity
        ):

            relationship = graph[
                source
            ][entity][
                "relationship"
            ]

            retrieved_relationships.add(
                f"{source} "
                f"--[{relationship}]--> "
                f"{entity}"
            )

    return list(
        retrieved_relationships
    )


# ============================================================
# 10. GENERATE ANSWER
# ============================================================

def generate_answer(
    question,
    graph_context
):

    context = "\n".join(
        graph_context
    )

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

   "I don't have enough information
    in the knowledge graph."

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

    return response.choices[
        0
    ].message.content


# ============================================================
# 11. GRAPH RAG PIPELINE
# ============================================================

def graph_rag(question):

    print("\n" + "=" * 60)
    print("GRAPH RAG PIPELINE")
    print("=" * 60)

    print(
        "\nQuestion:"
    )

    print(
        question
    )

    # ========================================================
    # STEP 1
    # ========================================================

    print(
        "\n[1] Finding relevant entities..."
    )

    graph_context = retrieve_from_graph(
        question,
        max_hops=2
    )

    # ========================================================
    # STEP 2
    # ========================================================

    print(
        "\n[2] Graph retrieval..."
    )

    if not graph_context:

        return (
            "I don't have enough information "
            "in the knowledge graph."
        )

    for item in graph_context:

        print(
            "   ",
            item
        )

    # ========================================================
    # STEP 3
    # ========================================================

    print(
        "\n[3] Generating answer using graph context..."
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
    print("             GRAPH RAG DEMO")
    print("=" * 60)

    # --------------------------------------------------------
    # Build graph
    # --------------------------------------------------------

    build_graph()

    # --------------------------------------------------------
    # Display graph
    # --------------------------------------------------------

    display_graph()

    # --------------------------------------------------------
    # Ask questions
    # --------------------------------------------------------

    while True:

        question = input(
            "\nAsk a question "
            "(type 'exit' to stop): "
        )

        if question.lower().strip() == "exit":

            print(
                "\nGoodbye!"
            )

            break

        if not question.strip():

            print(
                "Please enter a question."
            )

            continue

        try:

            answer = graph_rag(
                question
            )

            print(
                "\n" + "=" * 60
            )

            print(
                "FINAL ANSWER"
            )

            print(
                "=" * 60
            )

            print(
                answer
            )

        except Exception as e:

            print(
                "\nError:",
                str(e)
            )