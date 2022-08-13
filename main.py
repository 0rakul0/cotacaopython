from fastapi import FastAPI
from datamine import *

app = FastAPI()
dt = datamine()


@app.get("/")
async def root():
    return {"msg":"use o nome da /fundos11/nome_cotação"}


@app.get("/fundos11/{name}")
async def fundos11(name: str):
    return dt.inicio(name)
