import requests
from bs4 import BeautifulSoup as bs
from joblib import Parallel, delayed
import re
from datamine import *

class calculadora_cotacao():

    def abaixo_de(self, min=None, max=None, rendimento=None, limit_liquidez=None, mes=None):
        url = "https://www.fundsexplorer.com.br/funds"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
        site1 = requests.get(url, headers=headers)
        soup_fundo1 = bs(site1.content, 'html.parser')

        resultado = []
        result = self.fund_cotas(soup_fundo1, valor_min=min, valor_max=max, rendimento=rendimento, limit_liquidez=limit_liquidez, mes=mes)
        for x in result:
            if x != None:
                resultado.append(x)
        result = resultado
        return result

    def executor(self, acao, valor_min=None, valor_max=None, rendimento=None, limit_liquidez=None, mes=None):
        dt = datamine()
        result = dt.inicio(acao)
        if result != None:
            valor_acao = result['VALOR_COTA']
            if valor_acao != 'N/A':
                if valor_acao > valor_min.real and valor_acao < valor_max.real:
                    data = result['ULTIMO_PG']
                    if data != None:
                        mes_corte = data.split(' - ')
                        mes_corte = mes_corte[-1]
                        mes_corte = mes_corte.split('/')
                        mes_corte = mes_corte[1]
                        corte = result['RENDIMENTO']
                        liquedez = result['LIQUIDEZ_DIARIA']
                        if corte > rendimento and liquedez > limit_liquidez and mes_corte == mes:
                            try:
                                if result['P/PV'] >= 1:
                                    pvp = 'caro'
                                else:
                                    pvp = 'com desconto'
                            except:
                                pvp = None
                            cota = result['LIQUIDEZ_DIARIA'], acao, result['VALOR_COTA'], corte, result['SEGMENTO'], data, result['P/PV'], pvp
                            print(f'fundos entre R${valor_min} e R${valor_max}, {cota}')
                            return {cota}

    def fund_cotas(self, soup, valor_min=None, valor_max=None, rendimento=None, limit_liquidez=None, mes=None):
        # lista de cotações
        lista_cotas = []
        # nome da cota
        fundos = soup.find('section', {'id': 'fiis-list'})
        fundos = fundos.find('div', {'class': 'row'})
        fundos = fundos.find_all('span', {'class', 'symbol'})
        for nome_fundos in fundos:
            nome_fundos = nome_fundos.text
            lista_cotas.append(nome_fundos)

        execucao = Parallel(n_jobs=-1)(
            delayed(self.executor)(acao=acao, valor_min=valor_min, valor_max=valor_max, rendimento=rendimento, limit_liquidez=limit_liquidez, mes=mes) for acao
            in lista_cotas)
        return execucao

if __name__ == "__main__":
    cc = calculadora_cotacao()
    cc.abaixo_de(min=0, max=100, rendimento=0.9, limit_liquidez=30000, mes='08')