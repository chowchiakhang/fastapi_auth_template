from datetime import datetime, timedelta, timezone
import os

import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext


load_dotenv()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

secret_key = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def decode(token: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=[ALGORITHM])

def create_access_token(data: dict, minutes: int | None = None):
    if minutes is None:
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt
