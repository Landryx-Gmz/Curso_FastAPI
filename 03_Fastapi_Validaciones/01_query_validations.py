from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()
# ============Validaciones para Strings==================
# max_length
# min_length
# pattern

#==============Validaciones para Números==================
# gt (greater than)
# ge (greater than or equal)
# lt (less than)
#le (less than or equal)
def check_valid_id(id: str):
    if id % 2 != 0:
        raise ValueError("Necesita se par")
    return id

@app.get("/items/")
async def read_items(q: Annotated[int | None, Query(gt=3)] = None):
    results: dict = {"mensaje": "Acceso a get(read_items)"}
    if q:
        results.update({"q": q})
    return results