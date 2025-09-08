from fastapi import FastAPI, HTTPException, Depends
import asyncio

app = FastAPI()

class MockDatabase: