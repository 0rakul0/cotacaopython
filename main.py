from fastapi import FastAPI
from datamine import *

app = FastAPI()
dt = datamine()


@app.get("/")
async def root():
    return {
        "msg":["use o nome da /fundos11/nome_cotação",
               "para ver o historico separadamente /hist/{name}"]
            }

@app.get("/fundos11/{name}")
async def fundos11(name: str):
    return dt.inicio(name)

@app.get("/historico/{name}")
async def historico(name: str):
    return dt.historico_inicio(name)

@app.get("/carteira")
async def carteira():
    return dt.carteira_publica()