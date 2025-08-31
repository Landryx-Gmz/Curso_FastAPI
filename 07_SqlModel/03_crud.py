#Instalamos sqlmodel (pip install sqlmodel)

from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Annotated
from fastapi import Depends, FastAPI,Query, HTTPException
from contextlib import asynccontextmanager


#Modelo Base
class HeroBase(SQLModel):
    name: str = Field(index = True)
    age: int |None = Field(default=None, index=True)

#Modelo para BD
class Hero(HeroBase, table=True):
    id: int |None = Field(default=None, primary_key=True)
    secret_name: str

#Modelo Publico(Respuestas API)
class HeroPublic(HeroBase):
    id: int

#Modelo para crear
class HeroCreate(HeroBase):
    secret_name: str

#Modelo para Updates
class HeroUpdate(SQLModel):
    name: str |None = None
    age: int |None = None
    secret_name: str |None = None

#Motor de base de datos con sqlite
sqlite_file_name="database.db"#nombre de la base de datos
sqlite_url=f"sqlite:///{sqlite_file_name}"#tipo de base de datos

#importamos create_engine de sqlmodel para el motor de base de datos
engine= create_engine(
    sqlite_url,
    connect_args={"check_same_thread":False}#esto permite que fastapi utilice la misma base de datos en diferentes hilos
)
#Creacion de BD
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Dependencia para secion

def get_session():
    with Session(engine) as session:
        yield session

SessionDep= Annotated[Session,Depends(get_session)]

# Lifespan Events (codigo que se ejecuta antes de que la app inicie una reques o antes de que cierre la app)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #codigo que se ejecutara antes
    create_db_and_tables()
    yield
    #codigo que se ejecutara despues

app = FastAPI(lifespan=lifespan)

# CRUD
# Get (Leer todo los Heroes)
@app.get("/heroes/", response_model=list[HeroPublic])
def get_heroes(
    session:SessionDep,
    offset: int = 0,
    limit: Annotated[int,Query(le=100)] = 100
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit).all())
    return heroes

# Get (Leer heroe por ID)
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def get_hero_id(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Post (Crear heroe)
@app.post("/heroes/", response_model=HeroPublic)
def create_heroe(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

#Patch (actualizar heroe por id)
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_heroe(hero_id: int,hero: HeroUpdate, session : SessionDep):
    hero_db = session.get(hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

#Delete (eliminar Heroe por id)
@app.delete("/heroes/{hero_id}")
def delete_heroe(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
