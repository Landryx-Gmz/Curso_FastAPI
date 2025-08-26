from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid auth credentials")
    return user

async def get_current_active_user(current_user: Annotated[UserInDB,Depends(get_current_user)]):
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrec username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Retornar "token falso" (username)
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user:Annotated[User,Depends(get_current_active_user)]):
    return current_user

#======Flujo del login=======
# 1.- Login ->(formdata(usernam,password) -> FastAPI(POST -> "/token"))

#==============Lo que no vemos:====================
# 2.- Explorador recibe el "token" si es correcto retorna el "token" a FastApi y el explorador lo guarda
# 3.- Cuando vamos a ruta get("/users/me") esta enviando el (token dentro de header de autorizacion): "Bearer token"