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

@app.get("/fundos/min={min}&max={max}")
async  def fundos(min: float, max: float):
    return dt.abaixo_de(min=min, max=max, rendimento=0.1)

@app.get("/fundos11/{name}")
async def fundos11(name: str):
    return dt.inicio(name)

@app.get("/hist/{name}")
async def hist(name: str):
    return dt.hist(name)

@app.get("/carteira")
async def carteira():
    return dt.carteira_publica()