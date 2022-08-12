import requests
from bs4 import BeautifulSoup as bs
import re


class datamine():
    def __init__(self):
        self.nome_cotacao = ''
        self.valor_cota = None
        self.valor_rendimento = None
        self.historico = []

    def limpeza(self, texto):
        texto = texto.replace('R$', '')
        texto = texto.replace(',', '.')
        texto = texto.strip()
        return texto

    def inicio(self, nome):
        url = f"https://www.fundsexplorer.com.br/funds/{nome}"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
        site = requests.get(url, headers=headers)
        soup = bs(site.content, 'html.parser')
        result = self.run(soup)
        self.nome_cotacao = nome
        return result

    def run(self, soup):
        descricao_rentabilidade = soup.find('span', text=re.compile('Valor Patrimonial'))
        valor_cota = descricao_rentabilidade.find_next_sibling('span', {'class':'indicator-value'}).text
        valor_cota = self.limpeza(valor_cota)
        self.valor_cota = float(valor_cota)

        descricao_rendimento = soup.find('span', text=re.compile('Último Rendimento'))
        rendimento = descricao_rendimento.find_next_sibling('span', {'class': 'indicator-value'}).text
        rendimento = self.limpeza(rendimento)
        self.valor_rendimento = float(rendimento)

        #grafico das cotações
        cotacoes_historico = soup.find('section', {'id':'quotations'})
        historico = cotacoes_historico.get('data-chart')
        historico = historico.replace("\\",'')
        historico = eval(historico)
        self.historico = historico
        historico = historico[-10:]

        dict_recurso = {'VALOR_COTA':valor_cota, 'RENDIMENTO':rendimento, 'HISTORICO':historico}

        return dict_recurso

if __name__ == "__main__":
    dt = datamine()
    dt.inicio("mxrf11")