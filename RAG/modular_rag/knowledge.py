documents = [
    {
        "id": 1,
        "text": "VPro Skills provides Python training."
    },
    {
        "id": 2,
        "text": "VPro Skills provides Java training."
    },
    {
        "id": 3,
        "text": "VPro Skills provides Data Structures training."
    },
    {
        "id": 4,
        "text": "VPro Skills provides Generative AI training."
    },
    {
        "id": 5,
        "text": "VPro Skills provides Agentic AI training."
    },
    {
        "id": 6,
        "text": "Python training includes NumPy and Pandas."
    },
    {
        "id": 7,
        "text": "Generative AI training includes RAG and Large Language Models."
    },
    {
        "id": 8,
        "text": "Agentic AI training includes LangChain and LangGraph."
    },
    {
        "id": 9,
        "text": "RAG combines retrieval with Large Language Models."
    },
    {
        "id": 10,
        "text": "LangGraph is used to build stateful AI workflows."
    }
]


# Knowledge graph data
relationships = [
    ("VPro Skills", "provides", "Python Training"),
    ("VPro Skills", "provides", "Java Training"),
    ("VPro Skills", "provides", "Data Structures Training"),
    ("VPro Skills", "provides", "Generative AI Training"),
    ("VPro Skills", "provides", "Agentic AI Training"),

    ("Python Training", "includes", "NumPy"),
    ("Python Training", "includes", "Pandas"),

    ("Generative AI Training", "includes", "RAG"),
    ("Generative AI Training", "includes", "Large Language Models"),

    ("Agentic AI Training", "includes", "LangChain"),
    ("Agentic AI Training", "includes", "LangGraph"),

    ("RAG", "uses", "Large Language Models"),
    ("LangGraph", "builds", "AI Workflows")
]