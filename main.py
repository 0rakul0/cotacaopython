from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup as bs
import re

app = FastAPI()

def limpeza(texto):
    texto = texto.replace('R$', '')
    texto = texto.replace(',', '.')
    texto = texto.strip()
    return texto

def inicio(nome):
    url = f"https://www.fundsexplorer.com.br/funds/{nome}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
    site = requests.get(url, headers=headers)
    soup = bs(site.content, 'html.parser')
    result = run(soup)
    return result

def run(soup):
    descricao_rentabilidade = soup.find('span', text=re.compile('Valor Patrimonial'))
    valor_cota = descricao_rentabilidade.find_next_sibling('span', {'class':'indicator-value'}).text
    valor_cota = limpeza(valor_cota)

    descricao_rendimento = soup.find('span', text=re.compile('Último Rendimento'))
    rendimento = descricao_rendimento.find_next_sibling('span', {'class': 'indicator-value'}).text
    rendimento = limpeza(rendimento)
    valor_rendimento = float(rendimento)

    #grafico das cotações
    cotacoes_historico = soup.find('section', {'id':'quotations'})
    historico = cotacoes_historico.get('data-chart')
    historico = historico.replace("\\",'')
    historico = eval(historico)
    historico = historico[-10:]
    dict_recurso = {'VALOR_COTA':valor_cota, 'RENDIMENTO':valor_rendimento, 'HISTORICO':historico}
    return dict_recurso

@app.get("/")
async def root():
    return {"msg":"use o nome da /cotacao/nome_cotação"}


@app.get("/cotacao/{name}")
async def cotacao(name: str):
    return inicio(name)
