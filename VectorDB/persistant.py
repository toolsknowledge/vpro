import chromadb

###################### connect to database ######################
client = chromadb.PersistentClient(
    path="./chroma_db"
) 
# print("Database connected Successfully !!!")
###################### connect to database ended ######################



###################### create  the table (collection) ######################
collection = client.get_or_create_collection(
    name="employees"
)
# print(collection._embedding_function)
# print(client.list_collections())  # all-MiniLM-L6-V2
###################### create  the table (collection) ended ######################


###################### insert single record table (collection) ######################
collection.add(
    ids=["1"],
    documents=["Ravi is Python Developer"],
    metadatas=[{"city":"hyderabad","experience":10}]
)
# print(collection.get())
# print(collection.get()["documents"])
# print(collection.get(include=["embeddings","documents","metadatas"]))
###################### insert single record table (collection) ended ######################


###################### insert multiple record table (collection) ######################
collection.add(
    ids=["2","3","4"],
    documents=["Priya is Java Developer",
               "Rahul is AI Engineer",
               "Sneha is Data Scientist"],
    metadatas=[{"city":"bangalore"},
               {"city":"chennai"},
                {"city":"pune"}]
)
# print(collection.get()["documents"])
# print(collection.get(ids=["2"])["documents"])
###################### insert multiple record table (collection) ended######################


###################### update single record table (collection) ######################
collection.update(
    ids=["1"],
    documents=["Ravi is Senior Python Developer"],
    metadatas=[{
        "city":"hyderabad",
        "experience":11
    }]
)
# print(collection.get(ids=["1"])["documents"])
# print(collection.get()["documents"])
###################### update single record table (collection) ended ######################


###################### delete single record table (collection) ######################
collection.delete(
    ids=["3"]
)
print(collection.get()["ids"])
###################### delete single record table (collection) ended ######################


###################### similarity search ######################

# results = collection.query(
#     query_texts=["Python Engineer"],
#     n_results=3
# )
# print(results["documents"])
###################### similarity search ended ######################
