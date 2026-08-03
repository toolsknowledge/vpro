# Example-1
# import pinecone
# print(pinecone.__version__)


# Example - 2
# from pinecone import Pinecone
# pc = Pinecone("")
# print("Connected Successfully!")


# Example-3
# from pinecone import Pinecone, ServerlessSpec
# pc = Pinecone("")
# pc.create_index(
#     name="rag-demo1",
#     dimension=4,
#     metric="cosine",
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     )
# )
# print("Index Created Successfully!")
# print(pc.list_indexes())

# Example-4
from pinecone import Pinecone
pc = Pinecone("")
index = pc.Index("rag-demo1")
index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": [0.12,0.45,0.67,0.89]
        }
    ]
)
print("Vector Inserted Successfully")


