# FastAPI - used to develop api calls
from fastapi import FastAPI,HTTPException

# MongoClient - connect to mongodb database
from pymongo import MongoClient

import bcrypt

import jwt
from datetime import datetime,timedelta


# app used to develop GET,POST,PUT,DELETE.....
app = FastAPI()

# connect to mongodb
client = MongoClient("mongodb+srv://admin:admin@vpro.ti3kug7.mongodb.net/?appName=VPro")

# create database
db = client["cmp_db"]

# collection
employees = db["employees"]


SECRETE_KEY = "my-vpro-secret-key-123"
ALGORITHM = "HS256"


@app.post("/register")
def register(username: str, password: str):
    existed_user = employees.find_one({"username": username})

    if existed_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists!"
        )

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    employees.insert_one({
        "username": username,
        "password": hashed_password.decode("utf-8")
    })

    return {
        "message": "employee registered successfully !!!"
    }


# login
@app.post("/login")
def login(username: str, password: str):
    user = employees.find_one({"username": username})

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid User Name"
        )

    # password = plain text entered by user
    # user["password"] = bcrypt hashed password from MongoDB
    password_match = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    )

    if not password_match:
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = jwt.encode(
        {
            "username": username,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
        SECRETE_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "login success !!!",
        "token": token
    }
    

    


# post
@app.post("/employees")
def create_emp(name:str,dept:str,salary:float):
    new_emp = {
        "name" : name,
        "dept" : dept,
        "salary" : salary
    }
    res = employees.insert_one(new_emp)
    return {
        "message" : "employee inserted successfully !!!",
        "id":str(res.inserted_id)
    }


# get
@app.get("/employees")
def read_employees():
    emps = employees.find()

    result = []
    for emp in emps:
        emp["_id"]=str(emp["_id"])
        result.append(emp)

    return result


@app.get("/employees/{name}")
def read_emp(name:str):
    emp = employees.find_one({"name":name})

    if emp:
        emp["_id"] = str(emp["_id"])
        return emp

    return {"msg":"employee not found !!!"}
    
@app.put("/employees/{name}/{new_name}/{updated_salary}")
def update_employee(name:str,new_name:str,updated_salary:float):
    res = employees.update_one({"name":name},{"$set":{"name":new_name,"salary":updated_salary}})    
    return {"message":"record updated successfully",
            "modifies":res.modified_count}

@app.delete("/employees/{name}")
def delete_employee(name:str):
    res = employees.delete_one({"name":name})
    return {
        "message" : "record deleted successfully !!!",
        "count" : res.deleted_count
    }


# insert_one()
# find()
# find_one()
# update_one()
# delete_one()


   