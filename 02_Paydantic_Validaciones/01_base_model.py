from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    id : int
    nombre : str
    email : str
    edad : int | None = None
    activo : bool

app = FastAPI()

@app.get("/users/")
def get_users():
    ...

@app.post("/users/")
def create_users(user: User):
    return{
        "mensaje" : f"Usuario {user.nombre.capitalize()} creado exitosamente",
        "datos" : user
    }

