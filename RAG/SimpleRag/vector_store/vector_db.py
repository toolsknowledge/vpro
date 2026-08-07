# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
PERSIST_DIRECTORY = "vector_store/chroma_db"
def create_vector_db(chunks, embedding_model):
    """
    Create and save Chroma Vector Database
    """
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=PERSIST_DIRECTORY
    )
    return vector_db


def load_vector_db(embedding_model):
    """
    Load existing Chroma Vector Database
    """
    vector_db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )
    return vector_db