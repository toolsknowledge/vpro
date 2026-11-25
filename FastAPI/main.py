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


# read _id from dict
# convert to string
# update string in dict
def format_student(student):
    student["id"] = str( student.pop("_id") )
    return student

# it is used to hash the passwords
password_hash = PasswordHash.recommended()



app = FastAPI()
# app object used to develop API Calls
# get, post,put,delete,head,trace, patch....
# @app.get()
# @app.post()
# @app.put()

# create post request
@app.post("/register")
def register(user:Users):
    hashed_password = password_hash.hash( user.password )
    try:
        users.insert_one({"username":user.username,"password":hashed_password})
    except DuplicateKeyError:
        raise HTTPException(status_code=409,detail="user name already existed")
    return {"message":"Registration Successful !!!"}


# create post request
@app.post("/login")
def login(user:Users):          # user - data coming from frontend user.username, user.password
    try:
        existed_user = users.find_one({"username":user.username})
        # existed_user (db record) # username = existed_user["username"], existed_user["password"]
        if(existed_user is None or not password_hash.verify(user.password,existed_user["password"])):
            return HTTPException(status_code = 401, detail="username or password not matches")
        
        # readable (Vikas) (Samba) user.username  - unreadable (secrete key)
        
        token = jwt.encode({
            "sub":existed_user["username"],
            "exp":datetime.now(timezone.utc) + timedelta(minutes=30)},
            "7d018e57b6c0b6f61ea8728e66c6ae59ea16bc5d1065e2ea5902f8bc6812734d",
            algorithm="HS256")
        return {
            "message" : "login successful !!!",
            "access_token" : token,
            "token_type" : "bearer"
        }
        
    except:
        print("Error !!!")


    