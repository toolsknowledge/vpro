# import chromadb
# print(chromadb.__version__)

import chromadb
client = chromadb.Client()

# in-memory (RAM)
collection = client.get_or_create_collection(name="employees")

collection.add(
    ids=["1"],
    documents=["Emp1"],
    metadatas=[{
        "city":"hyd",
        "exp":10
    }]
)
print("Record Inserted !!!")

data = collection.get()
print(data)