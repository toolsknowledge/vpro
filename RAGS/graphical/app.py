import os

import streamlit as st
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI

load_dotenv()

st.set_page_config(
    page_title="VPro Skills - Graph RAG",
    page_icon="🔗",
    layout="wide",
)

st.title("🔗 VPro Skills - Graph RAG")
st.write("Ask questions using information stored in Neo4j.")

# Read credentials
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


@st.cache_resource
def get_neo4j_driver(uri, username, password):
    driver = GraphDatabase.driver(
        uri,
        auth=(username, password),
    )
    driver.verify_connectivity()
    return driver


def retrieve_graph_facts(driver):
    """Retrieve facts stored as nodes and relationships."""

    query = """
    MATCH (a)-[r]->(b)
    RETURN a.name AS source,
           type(r) AS relationship,
           b.name AS target
    ORDER BY source
    LIMIT 200
    """

    with driver.session() as session:
        records = session.run(query)
        facts = [
            f"{record['source']} "
            f"-[{record['relationship']}]-> "
            f"{record['target']}"
            for record in records
        ]

    return facts


def generate_answer(question, facts, client):
    """Generate an answer using retrieved graph facts."""

    context = "\n".join(facts)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful Graph RAG assistant. "
                    "Answer using only the supplied graph facts. "
                    "Do not invent products, relationships, or sellers. "
                    "If the facts do not answer the question, "
                    "say that the graph does not contain enough information."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Graph facts:\n{context}\n\n"
                    f"Question: {question}\n\n"
                    "Give a clear, simple answer."
                ),
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content


# Validate configuration
required_values = {
    "NEO4J_URI": NEO4J_URI,
    "NEO4J_USERNAME": NEO4J_USERNAME,
    "NEO4J_PASSWORD": NEO4J_PASSWORD,
    "OPENAI_API_KEY": OPENAI_API_KEY,
}

missing = [
    name for name, value in required_values.items()
    if not value
]

if missing:
    st.error(
        "Missing configuration in .env: "
        + ", ".join(missing)
    )
    st.stop()


try:
    driver = get_neo4j_driver(
        NEO4J_URI,
        NEO4J_USERNAME,
        NEO4J_PASSWORD,
    )
    client = OpenAI(api_key=OPENAI_API_KEY)

    facts = retrieve_graph_facts(driver)

except Exception as error:
    st.error("Could not connect to a service.")
    st.info(
        "Check your Neo4j connection, credentials, "
        "internet access, and API configuration."
    )
    st.code(str(error))
    st.stop()


if not facts:
    st.warning(
        "No relationships found. Add graph data in Neo4j first."
    )
    st.stop()


with st.sidebar:
    st.subheader("Retrieved graph facts")
    st.caption(f"{len(facts)} relationships found")

    for fact in facts:
        st.write("• " + fact)


question = st.text_input(
    "Ask your question",
    placeholder="Who sells the phone case related to iPhone 16?",
)

if st.button("Get Answer", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Generating answer..."):
            try:
                answer = generate_answer(
                    question,
                    facts,
                    client,
                )

                st.subheader("Answer")
                st.write(answer)

                with st.expander("View graph context"):
                    for fact in facts:
                        st.write("• " + fact)

            except Exception as error:
                st.error("Could not generate the answer.")
                st.info(
                    "Check your OpenAI API key, model access, "
                    "API credits, and internet connection."
                )
                st.code(str(error))
