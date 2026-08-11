# FastAPI - used to develop api calls
from fastapi import FastAPI

# MongoClient - connect to mongodb database
from pymongo import MongoClient

# app used to develop GET,POST,PUT,DELETE.....
app = FastAPI()

# connect to mongodb
client = MongoClient("mongodb+srv://admin:admin@vpro.ti3kug7.mongodb.net/?appName=VPro")

# create database
db = client["cmp_db"]

# collection
employees = db["employees"]

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
    



   