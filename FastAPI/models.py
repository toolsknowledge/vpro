from database import Base
from sqlalchemy import Column,Integer,String,Float

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,index=True,nullable=False)
    email = Column(String(100),unique=True,index=True,nullable=False)
    hashed_password = Column(String(256),nullable=False)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    department = Column(String(50), nullable=False)
    salary = Column(Float, nullable=False)



