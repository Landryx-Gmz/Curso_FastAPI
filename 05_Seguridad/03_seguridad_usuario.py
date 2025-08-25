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

@app.get("/items/")
async def get_items(tokken: Annotated[str,Depends(oauth2_scheme)]):
    return{"token": tokken}