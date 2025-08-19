from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

class User(BaseModel):
    username: Annotated[str, Field(min_length=4)]
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, priority: Annotated[int, Body()]):
    return {"item_id":item_id, "item":item, "user":user, "priority": priority }

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Annotated[Item,Body(embed=True)]):
#     return {"item_id":item_id, "item":item  }