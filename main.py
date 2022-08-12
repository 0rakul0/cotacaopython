from fastapi import FastAPI
from datamine import *

app = FastAPI()
dt = datamine()

@app.get("/{name}")
async def root(name: str):
    return dt.inicio(name)
