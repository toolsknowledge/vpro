import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

embedding_function = OpenAIEmbeddingFunction(
    api_key="",
    model_name="text-embedding-3-small"
)

client = chromadb.PersistentClient(
    path="./chroma_db1"
)

collection = client.get_or_create_collection(
    name="students",
    embedding_function=embedding_function
)

print(client.list_collections())
print(collection._embedding_function)

collection.add(
    ids=["1"],
    documents=["Hello"],
    metadatas=[{"test":"abc"}]
)