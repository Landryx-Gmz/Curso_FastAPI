from fastapi import FastAPI
import time
import asyncio

app = FastAPI()


# El time.sleep lo bloquea o pausa
# El async def se procesa en el hilo principal(main thread)
# Entonces se ejecuta secuencialmente es decir espera que se termine de  ejecutar una request para empezar otra
# NO RECOMENDABLE
# Luego se procesa la request1 -> hola, adios -> request2-> hola, adios
@app.get("/async_sin_await")
async def async_sin_await():
    print("hola")
    time.sleep(5)
    print("adios")

#No se bloquea el main thread 
#Funcion se pausa para esperar el await 
# meintras espera se hace concurrente
# request1 hola, pausa -> request2 hola, pausa -> request1 adios, pausa -> request2 adios

@app.get("/async_con_await")
async def async_con_await():
    print("hola")
    await asyncio.sleep(5)
    print("adios")

# No ejecuta en el hilo principal(main thread) a no ser async def
# Por lo tanto son hilos diferente en paralelo

@app.get("/sync")
def sync():
    print("hola")
    time.sleep(5)
    print("adios")