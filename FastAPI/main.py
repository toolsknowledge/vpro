# FastAPI - predefined class
# FastAPI - develop GET,POST,PUT,DELETE
# HTTPException - used to handle the Exceptions
# Depends - used to verify tokens before execution
from fastapi import FastAPI,HTTPException,Depends

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
from fastapi.security import HTTPBearer,HttpAuthorizationCredentials

from pydantic import BaseModel


load_dotenv()       # loads into memory
client = MongoClient(os.getenv("MONGO_URL"))

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

