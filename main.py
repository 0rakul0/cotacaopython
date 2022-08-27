from fastapi import FastAPI
from datamine import *
from historico import *
from calculadora_cotacao import *

app = FastAPI()
dt = datamine()
ht = historico()
cc = calculadora_cotacao()

@app.get("/")
async def root():
    return {
        "msg":["use o nome da /fundos11/nome_cotação",
               "para ver o historico separadamente /hist/{name}",
               " a calculadora de acoes pode quebrar, pelo alto custo de processamento\n exemplo de uso \n",
               "/calculadora_cotacao/min=0&max=100&rendimento=0.9&limit_liquidez=30000&mes='08'"
               ]
            }

@app.get("/fundos11/{name}")
async def fundos11(name: str):
    return dt.inicio(name)

@app.get("/historico/{name}")
async def historico(name: str):
    return ht.historico_inicio(name)

@app.get("/carteira")
async def carteira():
    return dt.carteira_publica()

@app.get("/calculadora_cotacao/min={minimo}&max={maximo}&rendimento={rendimento}&limit_liquidez={limit_liquidez}&mes={mes}")
async def calculadora_cotacao(minimo: float, maximo: float, rendimento: float, limit_liquidez: int, mes: str):
    return cc.abaixo_de(min=minimo, max=maximo, rendimento=rendimento, limit_liquidez=limit_liquidez, mes=mes)