
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

load_dotenv()

# 1. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "python-learning"

# 3. Create index if it does not exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print("Index creation requested!")

# 4. Connect to the actual index
index = pc.Index(index_name)

print("Connected to Pinecone successfully!")

# 5. Sample documents
documents = [
    {
        "id": "doc1",
        "text": "Python is a programming language.",
        "category": "Python"
    },
    {
        "id": "doc2",
        "text": "Machine learning helps computers learn from data.",
        "category": "AI"
    },
    {
        "id": "doc3",
        "text": "React is used to build user interfaces.",
        "category": "Web Development"
    }
]

# 6. Generate embeddings and store vectors
vectors = []

for doc in documents:
    embedding = model.encode(doc["text"]).tolist()

    vectors.append({
        "id": doc["id"],
        "values": embedding,
        "metadata": {
            "text": doc["text"],
            "category": doc["category"]
        }
    })

# 7. Insert vectors
index.upsert(vectors=vectors)

print("Documents stored successfully!")

# 8. Check index statistics
print(index.describe_index_stats())

# 9. Search by meaning
question = input("Enter your question: ")

query_embedding = model.encode(question).tolist()

results = index.query(
    vector=query_embedding,
    top_k=1,
    include_metadata=True
)

# 10. Display results
print("\nMost relevant documents:")

for match in results.matches:
    print("ID:", match.id)
    print("Score:", round(match.score, 4))
    print("Text:", match.metadata["text"])
    print("Category:", match.metadata["category"])
    print("-" * 40)
