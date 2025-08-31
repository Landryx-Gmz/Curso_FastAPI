#intalamos httpx (pip install httpx)
#Instalamos pytest(pip install pytest)
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "Hello World"}


client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

#para hacer el testing si no tenemos ningun archivo con el nombre test
#tenemos que en la terminal escribir:  pytest (nombre del archivo)