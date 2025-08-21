from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

app = FastAPI()

class Logger:
    def log(self, message: str) -> None:
        print(f"Logging message: {message}")

# @app.get("/products/{message}")
# def get_products(message: str):
#     logger = Logger()
#     logger.log(message)

# @app.get("/item/{message}")
# def get_item(message: str):
#     logger = Logger()
#     logger.log(message)

def get_logger():# Si este logger cambiase todos los endpoint lo harian tambien asi no se tiene de duplicar codigo
    return Logger()

logger_dependency = Annotated[Logger, Depends(get_logger)]#dependendia para inyectar en cualquier lado (buenas practicas)


@app.get("/item/{message}")
def get_item(message: str, logger: logger_dependency):
    logger.log(message)
    return message

@app.get("/products/{message}")
def get_products(message: str,logger: logger_dependency):
    logger.log(message)
    return message