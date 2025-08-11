from enum import Enum
from fastapi import FastAPI

class CarDealer(Enum):
    HONDA = "honda"
    BMW = "bmw"
    FORD = "ford"

app = FastAPI()

@app.get("/models/{car_dealer}")
async def get_model(car_dealer: CarDealer):
    if car_dealer is CarDealer.HONDA:
        return {"car_dealer" : car_dealer, "message" : "Honda es Japones"}
    if car_dealer.value == "bmw":
        return {"car_dealer" : car_dealer, "message" : "Bmw es Aleman"}
    return {"car_dealer" : car_dealer, "message" : "Ford es USA"}