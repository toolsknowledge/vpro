# used to encrypt the password / compare the passwords
import bcrypt

# used to generate tokens (jwt) 
import jwt

# set exp date to tokens
from datetime import datetime,timedelta,timezone

# used to convert readable data to unreadable format
SECRET_KEY = "d244bab78d771f55ae8aa86a2b2767fd1a94534b15659c2783dac5cff86e3242"
ALGORITHM = "HS256"

# Expire time to token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Generate Hashed Password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()


# Compare the passwords
def verify_password(plain:str,hashed:str)->bool:
    return bcrypt.checkpw(plain.encode(),hashed.encode())

# create token
def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)




