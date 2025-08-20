from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, HTTPException
from typing import Annotated, Literal
from itertools import count

id_generator = count(start=1)
def obtener_nuevo_id() -> int:
    return next(id_generator)

class TareaBase(BaseModel):
    titulo : Annotated[str, Field(min_length=3)]
    estado: Literal["pendiente", "completado"] = "pendiente"

class TareaCreate(TareaBase):
    pass

class Tarea(TareaBase):
    id: Annotated[int, Field(gt=0)]

class FilterParams(BaseModel):
    limit: Annotated[int, Field(ge=1)] = 5
    offset: Annotated[int, Field(ge=0)] = 0
    estado: Literal["pendiente", "completado"] | None = None
    search: str | None = None
    

fake_db: list[Tarea] = [
    Tarea(id=1, titulo= "Estudiar Python", estado= "pendiente"),
    Tarea(id=2, titulo= "Lavar la ropa", estado= "completado"),
    Tarea(id=3, titulo= "Leer un libro", estado= "pendiente"),
    Tarea(id=4, titulo= "Ir al gimnasio", estado= "completado"),
    Tarea(id=5, titulo= "Comprar comida", estado= "pendiente"),
    Tarea(id=6, titulo= "Limpiar el cuarto", estado= "pendiente"),
    Tarea(id=7, titulo= "Pagar cuentas", estado= "completado"),
    Tarea(id=8, titulo= "Llamar a mamá", estado= "pendiente"),
    Tarea(id=9, titulo= "Revisar correo", estado= "pendiente"),
    Tarea(id=10, titulo= "Lavar carro", estado= "pendiente"),
]

app = FastAPI()

@app.get("/tareas/", response_model=list[Tarea])
def obtener_listafake(filtros: Annotated[FilterParams, Query()]):
    # if filtros.estado:
    #     tareas_filtradas = [tarea for tarea in fake_db if tarea.estado == filtros.estado]
    # else:
    #     tareas_filtradas = fake_db
    # return tareas_filtradas


    #==========Filtrar tareas======
    #   TAREA POR ESTADO 
    tareas_filtradas =(
        [tarea for tarea in fake_db if tarea.estado == filtros.estado]if filtros.estado else fake_db
    )
    #   TAREA POR TITULO SI SE PRPORCIONA
    if filtros.search:
        tareas_filtradas=[
        t for t in tareas_filtradas if filtros.search.lower() in t.titulo.lower()
        ]

    # Aplicar paginacion
    return tareas_filtradas[filtros.offset: filtros.offset + filtros.limit]

@app.get("/tareas/{id}", response_model=Tarea)
def get_tarea(id: int):
    for tarea in fake_db:
        if tarea.id == id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

#=========metodo Post==========

@app.post("/tarea/", response_model=Tarea)
def crear_tarea(tarea: TareaCreate):
    nuevo_id: int