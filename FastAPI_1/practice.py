from fastapi import FastAPI
from pymongo import MongoClient
app = FastAPI() # @app.get(). @app.post().  @app.put().  @app.delete()
client = MongoClient("mongodb+srv://admin:admin@vpro.ti3kug7.mongodb.net/?appName=VPro")
practice_db = client["practice_db"]
students = practice_db["students"]

@app.post("/students")
def create_students(name:str,marks:float,age:int):
    res = students.insert_one({"name":name,"marks":marks,"age":age})
    return {
        "message":"record inserted successfully !!!",
        "id":str(res.inserted_id)
    }

@app.get("/students")
def read_students():
    data = students.find()
    result = []
    for student in data:
        student["_id"] = str(student["_id"])
        result.append(student)

    return result


@app.get("/students/{name}")
def student_name(name:str):
    record = students.find_one({"name":name})
    if record:
        record["_id"] = str(record["_id"])
        return record
    return {
        "message" : "student not available"
    }

@app.put("/students/{name}")
def update_student(name:str,marks:float):
    res = students.update_one({"name":name},{"$set":{"marks":marks}})
    return {
        "message" : "record updated successfully !!!",
        "id":str(res.modified_count)
    }

@app.delete("/students/{name}")
def delete_student(name:str):
    res = students.delete_one({"name":name})
    return {
        "message" : "record deleted successfully !!!",
        "id" :res.deleted_count
    }





