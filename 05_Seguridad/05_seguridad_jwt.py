# Vamos a trabajar con pip install "passlib[bcrypt]" para el hasheo

from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

# Config(En un proyecto real esto iria a evironment variables/setting)
SECRET_KEY = "3430c03b489d375fd771b6f9a62c9ceb6283f32901abec80530333631b337220"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#HASSHEO PASSWORD
pwd_context = CryptContext(shcemes=["bcrypt"],deprecate="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password:str):
    return pwd_context.hash(password)