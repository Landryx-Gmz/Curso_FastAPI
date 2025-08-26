#=============Json Web Token===============
# Estructura:
# xxxxx.yyyyy.zzzzz
# Contiene texto codificado para nuestra seguridad en nuestras aplicaciones para autenticacion
# Se instala con pip install PyJWT 
# Creamos con el comando| openssl rand -hex 32 | en powershell para generar una Key segura

import jwt
import datetime

#  Clave temporal para pruebas. No usar en producción.

SECRET_KEY = "openssl rand -hex 32"#clave generada con este comando 

payload: dict = {
    "username": "AndyGmz",
    "role": "admin",
    #Muy importante poner fecha de expiracion de token  con datetime:
    "exp" : datetime.datetime.now() + datetime.timedelta(hours=1)
}

# Crear token
token = jwt.encode(payload,SECRET_KEY,algorithm="HS256")
#print(token)


# Verificar / decodificar token

try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    # decoded = jwt.decode(token, "failedsecretkey", algorithms=["HS256"]) ejemplo de como capturar un error
    print(decoded)
except jwt.ExpiredSignatureError:
    print("jwt ha expirado")
except jwt.InvalidTokenError:
    print("Token invalido")