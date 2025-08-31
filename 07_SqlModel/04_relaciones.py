#Instalamos sqlmodel (pip install sqlmodel)

from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship
from typing import Annotated
from fastapi import Depends, FastAPI,Query, HTTPException
from contextlib import asynccontextmanager

#==============MODELOS Y RELACIONES==================

#Modelo Base
class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class HeroBase(SQLModel):
    name: str = Field(index = True)
    age: int |None = Field(default=None, index=True)

#Modelo para BD
class Team(TeamBase, table=True):
    id: int |None = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(HeroBase, table=True):
    id: int |None = Field(default=None, primary_key=True)
    secret_name: str
    team_id: int |None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")

#Modelo Publico(Respuestas API)
class TeamPublic(TeamBase):
    id: int

class HeroPublic(HeroBase):
    id: int
    team_id: int |None = None

#Modelo para crear
class TeamCreate(TeamBase):
    pass

class HeroCreate(HeroBase):
    team_id: int | None = None
    secret_name: str

#Modelo para Updates
class TeamUpdates(SQLModel):
    name: str | None = None
    headquarters: str |None = None


class HeroUpdate(SQLModel):
    name: str |None = None
    age: int |None = None
    secret_name: str |None = None
    team_id: int |None = None


#=====================SQLITE======================

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

#========================LIFESPAN EVENT==========================
# Lifespan Events (codigo que se ejecuta antes de que la app inicie una reques o antes de que cierre la app)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #codigo que se ejecutara antes
    create_db_and_tables()
    yield
    #codigo que se ejecutara despues

app = FastAPI(lifespan=lifespan)


#=================ENDPOINTS=====================


# ==================CRUD====================
# Get (Leer todo los Heroes)
@app.get("/heroes/", response_model=list[HeroPublic])
def get_heroes(
    session:SessionDep,
    offset: int = 0,
    limit: Annotated[int,Query(le=100)] = 100
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
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
    hero_db = session.get(Hero,hero_id)
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



# =======================TEAMS==========================

#Crear team
@app.post("/teams/", response_model=TeamPublic)
def create_team(team: TeamCreate, session: SessionDep):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

#Obtener team por ID
@app.get("/teams/{team_id}", response_model=TeamPublic)
def get_team(team_id: int, session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

#Eliminar team
@app.delete("/teams/{team_id}")
def delete_team(team_id: int, session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    #opcion 1 team_id = None en todods los heroes
    for hero in team.heroes:
        hero.team_id = None
        hero.team = None
    #opcion 2 Borrar todos los heroes del equipo
    # for hero in team.heroes:
    #     session.delete(hero)
    session.delete(team)
    session.commit()
    return{"messege": f"Team{team.name} delete!"}

