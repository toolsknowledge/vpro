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
# @app.get()        @app.post()     @app.patch()        @app.delete()



#post
@app.post("/students")
def create_student(student:Student):
    res = collection.insert_one(student.model_dump())
    return {
        "message" : "Student Added Successfullly !!!",
        "id":str(res.inserted_id)
    }



















