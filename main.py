from fastapi import FastAPI
from datamine import *
from historico import *
from calculadora import *

app = FastAPI()
dt = datamine()
ht = historico()
cc = calc()

@app.get("/")
async def root():
    return {
        "msg":["use o nome da /fundos11/nome_cotação",
               "para ver o historico separadamente /hist/{name}",
               " a calculadora de acoes pode quebrar, pelo alto custo de processamento\n exemplo de uso \n",
               "para saber o calculo de qual cotação comprar com uma divisão necessaria\n",
               "min = start ou valor da cotação maxima\n",
               "max = close ou valor da cotação maxima\n",
               "rendimento_corte = referece ao valor de rentabilidade da cota\n",
               "valor_disponivel = referece ao valor total para comprar as acoes\n",
               "divid_min = referece ao valor em porcentagem de rentabilidade ou seja, quanto maior que 1 melhor\n",
               "/calculadora_cotacao/min=0&max=100&rendimento=0.9&rendimento_corte=rendimento_corte&valor_disponivel=valor_disponivel&divid_min=divid_min"
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

@app.get("/calculadora/min={minimo}&max={maximo}&rendimento={rendimento_corte}&valor_disponivel={valor_disponivel}&divid_min={divid_min}")
async def calculadora(minimo: float, maximo: float, rendimento_corte: float, valor_disponivel: float, divid_min:float):
    return cc.run(valor_min=minimo, valor_max=maximo, rendimento_corte=rendimento_corte, valor_disponivel=valor_disponivel, divid_min=divid_min)
