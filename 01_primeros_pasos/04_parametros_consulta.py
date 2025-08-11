from fastapi import FastAPI


app = FastAPI()

cars_list: list[dict] = [
    {"car_name": "Elantra"},
    {"car_name": "Civic"},
    {"car_name": "Sentra"},
    {"car_name": "Corolla"},
]

@app.get("/cars/")
async def get_cars(skip: int = 0,limit:int= 10, optional: bool | None = None):
    if optional:
        return{
            "list": cars_list[skip : skip + limit],
            "optional" : optional
        }
    return cars_list[skip : skip + limit]