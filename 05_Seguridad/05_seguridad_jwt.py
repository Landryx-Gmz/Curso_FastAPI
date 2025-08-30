# Vamos a trabajar con pip install "passlib[bcrypt]" para el hasheo

from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings


# Config(En un proyecto real esto iria a evironment variables/setting)
# export SECRET_KEY="------" ponemos nuestar configuraciones en nuestras variables de entorno o .env

# Opciones para trabajar en nuestras variables de entorno:
# Opcion 1: dotenv  (pip install dotenv) y lo importamos(from dotenv import load_dotenv) u tambien importamos(import os)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY") or "valor por defecto"
ALGORITHM = os.getenv("ALGORITHM") or "valor por defecto"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 30)#casteamos a int ya que es un numero


# # Opcion 2: con pydantic(pip install pydantic_settings)importamos(from pydantic_settings import BaseSettings)
# class Setting(BaseSettings):
#     SECRET_KEY: str
#     ALGORITHM : str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int

#     class Config:
#         env_file = ".env"

# settings = Setting
# settings.SCRET_KEY



#HASSHEO PASSWORD
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password:str):
    return pwd_context.hash(password)

# Fake DB

fake_users_db: dict = {
    "johndoe": {
        "username": "johndoe",
        "email" : "jonhndoe@xample.com",
        "full_name" : "Jonh Doe",
        "disable" : False,
        "hashed_password" : get_password_hash("secret")
    },
    "alice": {
        "username": "alice",
        "email" : "alice@xample.com",
        "full_name" : "Alice Smith",
        "disable" : True,
        "hashed_password" : get_password_hash("secret2")
    }
}

#MODELS
#modelo/clases de token:
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: str |None = None

#modelo/clases de usuarios:
class User(BaseModel):
    username:str
    email:str |None = None
    full_name:str |None = None
    disable:bool |None = None

#usuarios bd con password hasheado
class UserInDb(User):
    hashed_password: str



#AUTENTICACION/HELPERS

def get_user(db:dict, username:str):
    if username in db:
        user_dict= db[username]
        return UserInDb(**user_dict)

#autenticacion de usuario
def authenticate_user(fake_db:dict, username:str,password:str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# crear access token
def create_access_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# FASTAPI

app = FastAPI()

#Sistema de seguridad
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str,Depends(oauth2_scheme)]):#Inyeccion de dependencias
    #casos de credenciales
    credential_exeption = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Can validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM] )
        username= payload.get("sub")
        if username is None:
            raise credential_exeption
        token_data = TokenData(username=username)
    except InvalidTokenError:
            raise credential_exeption
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credential_exeption
    return user

#funcion para saber si el usuario esta activo
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):#Inyeccion de dependencias
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

#ENDPOINTS

@app.post("/token", response_model = Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username},expires_delta=access_token_expires)
    return Token(access_token=access_token,token_type="bearer")


@app.get("/users/me")
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user   