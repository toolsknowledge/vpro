import chromadb
# client = chromadb.Client()    # RAM
# client = chromadb.PersistentClient(path="./chroma_db") # Persistant
client = chromadb.HttpClient(host="localhost",port=8000)    # Http Connection   #chroma run --path ./chroma_db
print("--Connected--")
#collection = client.create_collection(name="courses")
collection = client.get_or_create_collection(name="courses")
print("courses table created !!!")
collection.add(
    documents=["Python is a programming language",
               "Java is used for enterprise application development",
               "React is used to build user interfaces"],
    ids=[
        "course1",
        "course2",
        "course3"
    ]
)
print("documents added to courses table")
result = collection.get()
print(result)
result1 = collection.get(
    ids=["course1"]
)
print(result1)
result2 = collection.query(
    query_texts = ["what is used to create UI ?"],
    n_results = 2
)
print(result2)

collection.add(
    documents = ["Python is a programming language",
                 "React is used to build user interfaces"],
    ids=["course4","course5"],
    metadatas=[
        {"category":"Programming"},
        {"category":"Frontend"}
    ]
)


collection.update(
    ids=["course4"],
    documents=["Python is a popular programming language"]
)

collection.delete(
    ids=["course4"]
)

total = collection.get()
print(total)


count = collection.count()
print(count)

client.delete_collection(
    name="courses"
)




