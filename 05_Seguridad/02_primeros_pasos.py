#=========Protocolos de seguridad=======
# OAuth 2 (La que se utiliza ahora y la que vamos a utilizar con FastAPI)
# OAtuh 1 (ya no se utiliza)
# OpenID Connect(Capa construida encima de OAuth2)
# OpenID (No tiene relacios con OAuth2)
# OpenAPI(describe las estructuras de las API)


#========OAuth 2 con flujo de pasword + Bearer token
# Frontend(username+password) -> retorna token -> Backend(valida token) -> Acceso a cierta data


from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme : OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def get_items(tokken: Annotated[str,Depends(oauth2_scheme)]):
    return{"token": tokken}