from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme : OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str |None = None
    full_name: str |None = None
    disable: bool |None = None

class UserInDB(User):
    hashed_password: str

fake_users_db: dict = {
    "johndoe": {
        "username": "johndoe",
        "email" : "jonhndoe@xample.com",
        "full_name" : "Jonh Doe",
        "disable" : False,
        "hashed_password" : "fakehashedsecret"
    },
    "alice": {
        "username": "alice",
        "email" : "alice@xample.com",
        "full_name" : "Alice Smith",
        "disable" : True,
        "hashed_password" : "fakehashedsecret2"
    }
}

def fake_hash_password(password:str)-> str:
    return "fakehashed" + password

def get_user(db:dict,username:str)-> UserInDB |None:
    if username in db:
        return UserInDB(**db[username])
    return None

def fake_decode_token(token: str) -> UserInDB | None:
    return get_user(fake_users_db, token)

async def get_current_user(token: Annotated[str,Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user:Annotated[User,Depends(get_current_user)]):
    return current_user