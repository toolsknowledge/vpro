# FastAPI - predefined class
# FastAPI - develop GET,POST,PUT,DELETE
# HTTPException - used to handle the Exceptions
# Depends - used to verify tokens before execution
from fastapi import FastAPI,HTTPException,Depends
from pymongo.errors import DuplicateKeyError

# MongoClient - predefined class
# MongoClient - used to connect to MongoDB (Cloud)
from pymongo import MongoClient

# loads the .env file
import os

# parse the data
from dotenv import load_dotenv


# PasswordHash - hash the password
from pwdlib import PasswordHash

# used to generate token
import jwt

# timestamp in db
from datetime import datetime,timedelta,timezone

# security (tokens)
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from pydantic import BaseModel
from bson import ObjectId

load_dotenv()       # loads into memory
client = MongoClient("mongodb+srv://admin:admin@cluster0.uvbqm5r.mongodb.net/")

# create database
db = client["college_db"]
# create collection
collection = db["students"]
users = db["users"]
users.create_index("username",unique=True)

# Define Schema (BaseModel)
class Users(BaseModel):
    username: str
    password: str

class Students(BaseModel):
    name: str
    age: int
    course : str


# read _id from student (dict)
# convert to string
# add string to student again (id)
def format_student(student):
    student["id"] = str( student.pop("_id") )
    return student


# password_hash - function
# used to hash the passwords
# admin@123 - asbcsjkdgakjdgkagadkAGDKA (secuirity)
password_hash = PasswordHash.recommended()


# app object used create GET,POST,PUT and DELETE
# @app.get()            @app.put()
# @app.post()           @app.delete
app = FastAPI()



@app.post("/register")
def register(user:Users):
        # user.username
        # user.password
    hashed_password = password_hash.hash(user.password)
    try:
        users.insert_one({"username":user.username,"password":hashed_password})
    except DuplicateKeyError:
        raise HTTPException(status_code=409,detail="user name already existed")

    return {"message":"registration success !!!"}


@app.post("/login")
def login(user:Users):              # abc, abc@123
    try:
        # compare "username" with "db username"
        existed_user = users.find_one({"username":user.username})           # existed_user - db (_id, username & hash password)
        print(existed_user)
        if(existed_user is None or not password_hash.verify(user.password,existed_user["password"])):
            raise HTTPException(status_code=401,detail="username or password not matches !!!")

        # token
        # hello --- unreadable (secrete key) (exp) (algorithm)
        token = jwt.encode({"sub":existed_user["username"],
                    "exp":datetime.now(timezone.utc)+timedelta(minutes=30)},
                    "xxxxx",
                    algorithm="HS256")
        return {
            "message" : "login success !!!",
            "access_token" : token,
            "token_type" : "bearer"
        }
                   
    except:
        print("DB Operations Fail !!!")



# post
@app.post("/students",status_code=201)
def create_student(student:Students):
    try:
        res = collection.insert_one(student.model_dump()) 
        print(res) 
        return{
            "message" : "student registered successfully !!!",
            "id":str(res.inserted_id)
        }
    except:
        print("Invalid DB Operations")

# get request
@app.get("/students")
def get_students():
    records = collection.find()
    return [format_student(record) for record in records]


@app.get("/students/{student_id}")
def get_studentbyid(student_id:str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=404,detail="Invalid Object ID")
    record = collection.find_one({"_id":ObjectId(student_id)})
    if record is None:
        raise HTTPException(status_code=404,detail="Student Not Existed")
    return format_student(record)


# put request
@app.put("/students/{student_id}")
def update_student(student_id:str,student:Students):
    if not ObjectId.is_valid(student_id):
            raise HTTPException(status_code=404,detail="Invalid Object ID") 
    res = collection.update_one({"_id":ObjectId(student_id)},{"$set":student.model_dump()})   
    if res.matched_count == 0:
        raise HTTPException(status_code=404,detail="Student Not Existed")
    return {"message":"record updated successfully !!!"}


# delete record
@app.delete("/students/{student_id}")
def student_delete(student_id:str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=404,detail="Invalid Object ID") 
    res = collection.delete_one({"_id":ObjectId(student_id)})
    if res.deleted_count == 0:
            raise HTTPException(status_code=404,detail="Student Not Existed")
    
    return {"message":"record deleted successfully !!!"}



















