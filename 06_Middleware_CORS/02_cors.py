# CORS es un mecanismo de seguridad del navegador que restringe las solicitudes HTTP de origen cruzado;
#  el middleware en FastAPI lo maneja añadiendo los encabezados necesarios 
# para permitir de manera segura que otros dominios accedan a tu API


# Header CORS Comunes:
#---------------------
# Acces-Control-Allow-Origin: Specifies allowed origins
# Acces-Control-Allow-Methods: Specifies alllowed HTTP methos
# Acces-Control-Allow-Header: Specifies allowed headers
# Acces-Control-Allow-Credentials: Indicates if credentials are allowed
# Acces-Control-Expose-Headers: Specifies header exposed to browser
# Acces-Control-Max-Age: Speciefies how long preflight results can be cached


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app=FastAPI()

origins =[
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
    
)

@app.get("/")
async def root():
    return {"messege": "Hello World"}

