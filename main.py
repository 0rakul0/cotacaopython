from fastapi import FastAPI
from datamine import *

app = FastAPI()
dt = datamine()

@app.get("/")
async def root():
    return {"msg":"use o nome da /cotacao/nome_cotação"}


@app.get("/cotacao/{name}")
async def cotacao(name: str):
    return dt.inicio(name)
