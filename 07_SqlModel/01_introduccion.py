#Instalamos sqlmodel (pip install sqlmodel)
from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

class Hero(SQLModel, table=True): # hacemos que con table=True la clase sea una tabla de base de datos
    id: int | None  = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None  = Field(default=None, index=True)
    secret_name : str

#Motor de base de datos con sqlite
sqlite_file_name="database.db"
sqlite_url=f"sqlite:///{sqlite_file_name}"
#importamos create_engine de sqlmodel
engine= create_engine(
    sqlite_url,
    connect_args={"check_same_tread":False}#esto permite que fastapi utilice la misma base de datos en diferentes hilos
)
#Creacion de BD
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Dependencia para secion

def get_session():
    with Session(engine) as session:
        yield session

SessionDep= Annotated[Session,Depends(get_session)]