# python -c "import secrets;print(secrets.token_hex(32))"
# FastAPI - predefined class
# used to develop api calls Ex. GET,POST,PUT,DELETE

# HTTPException - predefined class
# used to handle Exceptions
from fastapi import FastAPI,HTTPException,Depends

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

# PasswordHash - used to encrypt the passwords
from pwdlib import PasswordHash

# import err
from pymongo.errors import DuplicateKeyError

# we are importing add time stamp to token
from datetime import datetime,timedelta,timezone
# used to generate token
import jwt
# handle exceptions (tokens)
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

# Step 1. load .env file
load_dotenv()

# Step 2: connect to mongodb
client = MongoClient(os.getenv("MONGO_URL"))

# Step 3: connect to database
db = client["college_db"]

# Step 4. connect to  collection
collection  = db["students"]

# users collection will create automatically
users = db["users"]
users.create_index("username",unique=True)

# Step 5. Define Schema
class Student(BaseModel):
    name: str
    age: int
    course : str

class Users(BaseModel):
    username: str
    password: str



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

password_hash = PasswordHash.recommended()

#post
@app.post("/register")
def register(user:Users):
    haseded_password = password_hash.hash( user.password )
    try:
        users.insert_one({"username":user.username,"password":haseded_password})
    except DuplicateKeyError:
        raise HTTPException(status_code=409,detail="User name already existed !!!")
    return {"message":"Registration Successful !!!"}


#post
@app.post("/login")
def login(user:Users):
    existed_user = users.find_one({"username":user.username})
    if(existed_user is None or not password_hash.verify(user.password,existed_user["password"])):
        raise HTTPException(status_code=401,detail="Invalid username or password")
    
    token = jwt.encode({"sub":existed_user["username"],
                        "exp":datetime.now(timezone.utc)+timedelta(minutes=30)},
                        os.getenv("SECRET_KEY"),
                        algorithm="HS256")
    return {
        "message":"login successful !!!",
        "access_token" : token,
        "token_type" : "bearer"
    }


# Authentication
security = HTTPBearer()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"]
        )

        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: username missing"
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired. Please login again."
        )

    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )

    user = users.find_one({"username": username})

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user



# protect
#post
@app.post("/students")
def create_student(student:Student,current_user:dict=Depends(get_current_user)):
    res = collection.insert_one(student.model_dump())
    return {
        "message" : "Student Added Successfullly !!!",
        "id":str(res.inserted_id)
    }


@app.get("/students")
def get_students(current_user:dict=Depends(get_current_user)):
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



























