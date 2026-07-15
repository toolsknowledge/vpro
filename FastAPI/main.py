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
