from fastapi import FastAPI
app = FastAPI()



# http://localhost:8000/gym/101/9030001847
# path parameters
@app.get("/gym/{id}/{contact}")
def demo1(id:int,contact:int):
    return {"enrolled id" : id, "mobile" : contact}


# http://127.0.0.1:8000/search?sub=genai&page=1
# query
@app.get("/search")
def demo2(sub:str,page:int=10):
    return sub,page






# Path Parameter
@app.get("/users/{user_id}")
def path_para1(user_id:int):
    return user_id

# Query Parameter
@app.get("/search")
def query_para1(sub:str,page:int=1):
    return f"sub : {sub} and page {page}"






@app.get("/reg")
def demo_get():
    return "welcome to get req !!!"

@app.post("/reg1")
def demo_post():
    return "welcome to post req !!!"

@app.put("/reg2")
def demo_put():
    return "welcome to put req !!!"

@app.delete("/reg3")
def demo_delete():
    return "welcome to delete req !!!"

