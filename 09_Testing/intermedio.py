from fastapi import FastAPI, HTTPException, Header
from typing import Annotated
from pydantic import BaseModel

fake_secret_token = "misupertoken"

class User(BaseModel):
    id: str 
    username: str
    email: str

fake_user_db: dict[str,User] = {
    "1": User(id="1", username="Andy", email="andy@mail.com"),
    "2": User(id="2", username="Rougsh", email="Rougsh@mail.com"),
    "3": User(id="3", username="Anni", email="Anni@mail.com")
} 

app = FastAPI()

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id:str, x_token:Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    if user_id not in fake_user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_user_db[user_id]

@app.post("/users/", response_model=User)
async def create_user(user: User, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    if user.id in fake_user_db:
        raise HTTPException(status_code=409, detail="User already exist")
    fake_user_db[user.id] = user
    return user