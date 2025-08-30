from fastapi import FastAPI, Request, Response
import time
from typing import Callable

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    strart_time = time.perf_counter()    
    response = await call_next(request)
    process_time = time.perf_counter() - strart_time
    print(process_time)
    response.headers["X-Process_Time"] = str(process_time)
    return response





@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/slow")
async def slow_root():
    time.sleep(1)
    return {"message": "Hello sloooow"}