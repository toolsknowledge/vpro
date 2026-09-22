# Oracle,MySQL - RDBMS
# Chroma, FAISS, Pinecone - VectorDB
# (Open Source / Doucments(Hello) / POC)
# FAISS (Searching - Speed) (META) (facebook ai similarity search)
# Pinecone (Speed - Semantic Searched) "Hello" ---> "Hi", reset my pass, forgot pass
# (Cloud DB)



from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# Hello ---> embeddings

# pc - connection object
pc = Pinecone(api_key="pcsk_39KrRS_MLRgPVtuhD8G8yKVW7nJPvnfzBYsRYScyAQG96QrpQSyWPfxZ8Hp9ApWFgH82gj")
print("Pinecone Connected Successfully !!!")
# Create only if it doesn't already exist
if not pc.has_index("student-index-ex"):
    pc.create_index(
        name="student-index-ex",
        dimension=384,                        # embedding models (sentensce-transformers)                     
        metric="cosine",                    # comparing the embeddings
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print("Index Created Successfully !!!")
else:
    print("Index already exists !!!")

# Connect to the index
index = pc.Index("student-index-ex")
print("Index connected successfully !!!")

text = "Hello"
embedding = model.encode(text)

index.upsert(
    vectors=[
        {
            "id":"student1",
            "values":embedding.tolist(),  # Hello
            "metadata":{"name":"vpro","course":"python"}
        }
    ]
)
print("Record Inserted Successfully !!!")

result = index.fetch(ids=["student1"])
print(result)

index.update(
    id="student1",
    set_metadata={
        "course":"python with pinecone"
    }
)
print("Record Updated Successfully !!!")

result1 = index.fetch(ids=["student1"])
print(result1)

index.delete(ids=["student1"])
print("Record Deleted !!!")

