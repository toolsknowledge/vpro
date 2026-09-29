# FastAPI - predefined class
# used to develop api calls Ex. GET,POST,PUT,DELETE

# HTTPException - predefined class
# used to handle Exceptions
from fastapi import FastAPI,HTTPException

# MongoClient - predefined class
# used to connect mongpdb 
from pymongo import MongoClient

# os library, used to read data from .env file
import os

# BaseModel - used to define Schema
# Ex. name - str, age - int, course - str, branch - str
# pydantic - inbuilt library (no need to download)
from pydantic import BaseModel

# ObjectId - used to handle the _id
from bson import ObjectId

# load_dotenv - predefined method
# used to load .env file
from dotenv import load_dotenv


# Step 1. load .env file
load_dotenv()


# Step 2: connect to mongodb
client = MongoClient(os.getenv("MONGO_URL"))

# Step 3: connect to database
db = client["college_db"]

# Step 4. connect to  collection
collection  = db["students"]


# Step 5. Define Schema
class Student(BaseModel):
    name: str
    age: int
    course : str


# create app
app = FastAPI()
# app - GET,POST,PUT,DELETE,.....
# @app.get()        @app.post()     @app.put()        @app.delete()


# remove _id
# convert to str
# add string to id
# add id to student again
def format_student(student):
    student["id"] = str(student.pop("_id"))
    return student



#post
@app.post("/students")
def create_student(student:Student):
    res = collection.insert_one(student.model_dump())
    return {
        "message" : "Student Added Successfullly !!!",
        "id":str(res.inserted_id)
    }


@app.get("/students")
def get_students():
    records = collection.find() 
    return [format_student(record) for record in records] 


@app.get("/students/{student_id}")  
def get_studentbyid(student_id:str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400,detail="Invalid Object ID")
    student = collection.find_one({"_id":ObjectId(student_id)})  
    if student is None:
        raise HTTPException(status_code=404,detail="Student Not Found !!!")

    return format_student(student)


@app.put("/students/{student_id}")
def update_student(student_id:str,student:Student):     # student - new data

    
    
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400,detail="Invalid Student ID")

    result = collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": student.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404,detail="Student Not Found !!!")
    return {"message":"record updated successfully !!!"}


@app.delete("/students/{student_id}")
def student_delete(student_id:str):
    if not ObjectId.is_valid(student_id):
            raise HTTPException(status_code=400,detail="Invalid Student ID") 

    result = collection.delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Student Not Deleted !!!")
    return {"message":"student record deleted successfully !!!"}


# insert_one() # insert document(record) into collection (table)
# find() - used to fetch all documents
# find_one() - retrive single document
# update_one() - update single document
# delete_one() - delete single document

# format_student() - converts _id to id
# ObjectId() - converts str to object id

# 2hours  <1min llm


# account --  admin network
# day after tomarrow -- questions

# LLMS (3days)



























