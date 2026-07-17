# FastAPI - used to build API Calls, Depends -- provide connection objects,HTTPException -- return exception
from fastapi import FastAPI, Depends, HTTPException, status

# Session - used to create Session for DB Interaction
from sqlalchemy.orm import Session

import models, schemas, auth
from database import engine, get_db

# Create tables in MySQL automatically (users)
models.Base.metadata.create_all(bind=engine)

# app object - used to build GET,POST,PUT,DELETE
app = FastAPI(title="Registration & Login API")

@app.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    # Check duplicates
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=auth.hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        return {"login": "fail"}

    token = auth.create_access_token(user.username)
    return {"login": "success", "access_token": token, "token_type": "bearer"}


@app.post("/employees", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(
    emp: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if db.query(models.Employee).filter(models.Employee.email == emp.email).first():
        raise HTTPException(status_code=400, detail="Employee email already exists")
    new_emp = models.Employee(**emp.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return db.query(models.Employee).all()

@app.get("/employees/{emp_id}", response_model=schemas.EmployeeResponse)
def get_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.put("/employees/{emp_id}", response_model=schemas.EmployeeResponse)
def update_employee(
    emp_id: int,
    emp_update: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in emp_update.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    db.commit()
    db.refresh(emp)
    return emp

@app.delete("/employees/{emp_id}")
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return {"message": "Employee deleted"}
