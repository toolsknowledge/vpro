import chromadb

# define the location
client = chromadb.PersistentClient(
    path="./test_db"
)

# create the database/collection
collection = client.get_or_create_collection(name="courses")

print("DataBase and Collection Created !!!")

# insert the records
collection.add(
    ids=["1","2","3","4","5"],
    documents=["Python is a programming language",            
             "Java is used for software development",
             "I love machine learning",
             "Deep learning uses neural networks",
             "Python is eazy to learn"]
)

print("5 documents are inserted !!!")

# fetch the data
results = collection.get()
print(results["ids"])
print(results["documents"])

# similarity search
result = collection.query(
    query_texts=["what is python"],
    n_results=2
)
print(result)

# update
collection.update(
    ids=["1"],
    documents = ["Python is widely used in machine laerning and AI"]
)
print("Document Updated !!!")
results = collection.get()
print(results["documents"])


collection.delete(ids=["2"])
print(collection.count())       # 4


collection.add(
    ids=["2"],
    documents=["Agentic AI"],
    metadatas=[{"VPro":"VPro","Batch-6":"Batch-6"}]
)
print(collection.count())

res1 = collection.get(
    where={"VPro":"VPro"}
)
print(res1)









