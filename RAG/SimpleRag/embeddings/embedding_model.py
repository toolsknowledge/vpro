# embeddings/embedding_model.py
from langchain_huggingface import HuggingFaceEmbeddings
def get_embedding_model():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embedding_model