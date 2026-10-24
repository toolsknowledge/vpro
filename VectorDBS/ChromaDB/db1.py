# import chromadb
import chromadb

# import SentenceTransformer
from sentence_transformers import SentenceTransformer

# import model
# this model used to create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# define the db location
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# table & database - programming
collection = client.get_or_create_collection(name="programming")

print("DataBase and Collection Created !!!")


documents=["Python is a programming language",            
             "Java is used for software development",
             "I love machine learning",
             "Deep learning uses neural networks",
             "Python is eazy to learn"]

ids=["1","2","3","4","5"]

embeddings = model.encode(documents).tolist()

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings
)
print(collection.count())

query = "what is python ?"
query_embedding = model.encode(query).tolist()

res = collection.query(
    query_embeddings = [query_embedding],
    n_results = 3
)
print(res)
















