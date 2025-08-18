from typing import Annotated
from fastapi import FastAPI,Path,Query

app = FastAPI

@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(ge=1, title="ID OF ITEM")],#Aqui ponemos las validaciones
    q: Annotated[str | None, Query(alias="item-query")] = None
    ):
    ...