from pydantic import BaseModel,EmailStr

class UserRegister(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    login: str
    access_token: str | None = None
    token_type : str | None = None

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float

class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    department: str | None = None
    salary: float | None = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    salary: float

    class Config:
        from_attributes = True
