from datetime import datetime, date
import requests
from bs4 import BeautifulSoup as bs
from joblib import Parallel, delayed
import re


class datamine():
    def __init__(self):
        self.nome_cotacao = ''
        self.valor_cota = None
        self.valor_rendimento = None
        self.historico = []
        self.acoes_valores_rendimentos = []

    def limpeza_real(self, texto):
        texto = texto.replace('R$', '')
        texto = texto.replace('.', '')
        texto = texto.replace(',', '.')
        texto = texto.strip()
        try:
            texto = float(texto)
        except:
            texto = texto
        return texto

    def inicio(self, nome):
        self.nome_cotacao = nome
        url_2 = f'https://statusinvest.com.br/fundos-imobiliarios/{nome}'
        url_1 = f"https://www.fundsexplorer.com.br/funds/{nome}"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
        site1 = requests.get(url_1, headers=headers)
        soup_fundo1 = bs(site1.content, 'html.parser')

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
        site2 = requests.get(url_2, headers=headers)
        soup_fundo2 = bs(site2.content, 'html.parser')

        result = self.run(soup_fundo1, soup_fundo2)

        self.nome_cotacao = nome
        return result

    def run(self, soup, soup_2):
        try:
            # valor da cota
            valor_cota = soup.find('div', {'id': 'stock-price'})
            valor_cota = valor_cota.find('span', {'class': 'price'}).text
            valor_cota = self.limpeza_real(valor_cota)

            # porcentagem de dividendos
            porcentagem = soup.find('span', text=re.compile('Dividend Yield'))
            valor_porcentagem = porcentagem.find_next_sibling('span', {'class': 'indicator-value'}).text
            valor_porcentagem = valor_porcentagem.replace(',', '.').replace('%', '')
            valor_porcentagem = valor_porcentagem.strip()
            valor_porcentagem = float(valor_porcentagem)
            situacao = 1 - valor_porcentagem
            if situacao < 0:
                situacao_porcentagem = f'acima de 1% - vale investir - {valor_porcentagem}%'
            else:
                situacao_porcentagem = f'abaixo de 1% - segurar ou vender - {valor_porcentagem}%'

            descricao_rentabilidade = soup.find('span', text=re.compile('Valor Patrimonial'))
            valor_patrimonio = descricao_rentabilidade.find_next_sibling('span', {'class': 'indicator-value'}).text
            valor_patrimonio = self.limpeza_real(valor_patrimonio)
            self.valor_cota = valor_patrimonio

            descricao_rendimento = soup.find('span', text=re.compile('Último Rendimento'))
            rendimento = descricao_rendimento.find_next_sibling('span', {'class': 'indicator-value'}).text
            rendimento = self.limpeza_real(rendimento)
            self.valor_rendimento = rendimento
        except:
            return None

        try:
            """
            P/VP = Valor de mercado na bolsa de valores / Valor patrimonial da empresa
            P/PV se tiver abaixo de 1 é pq tem desconto, logo significa que a empresa vale em bolsa menos do que o seu patrimônio líquido. Isso pode ser uma boa oportunidade para o investidor.
            """
            valor_mercado_pv = soup_2.find('span', text=re.compile('Valor de mercado'))
            valor_mercado_pv = valor_mercado_pv.find_next_sibling('span', {'class': 'sub-value'}).text
            valor_mercado_pv = self.limpeza_real(valor_mercado_pv)
            valor_patrimonio_pv = soup_2.find('span', text=re.compile('Patrimônio'))
            valor_patrimonio_pv = valor_patrimonio_pv.find_next_sibling('span', {'class': 'sub-value'}).text
            valor_patrimonio_pv = self.limpeza_real(valor_patrimonio_pv)
            preco_por_acao = (valor_mercado_pv / valor_patrimonio_pv).real
        except:
            preco_por_acao = None

        """
        Rentabilidade Mês / para renda variavel
        Rentabilidade = (preço atual / preço anterior) x 100 – 100
        """
        rentabilidade = soup.find('span', text=re.compile('Rentab\. no mês'))
        rentabilidade = rentabilidade.find_next_sibling('span', {'class': 'indicator-value'}).text
        rentabilidade = rentabilidade.replace(',', '.').replace('%', '')
        rentabilidade = rentabilidade.strip()
        rentabilidade = float(rentabilidade)

        """
        info de dividendos
        """
        p_list = []
        info = soup.find('div', {'class': 'text-dynamic-dividends'})
        info = info.find_all('p')
        for p in info:
            texto = p.text
            texto = texto.replace('\n', '').replace('  ', '')
            texto = texto.strip()
            p_list.append(texto)
        info = p_list

        try:
            data = info[0][-7:]
            data = data.replace(').', '')
            data = data.split('/')
            data = f'data pagemento - {data[0]}/{data[1]}/2022'
        except:
            data = None
        """
        segmento
        """
        try:
            segmento = soup.find('span', text=re.compile('Segmento'))
            segmento = segmento.find_next_sibling('span', {'class': 'description'}).text
            segmento = segmento.strip()
        except:
            segmento = None

        # grafico das cotações
        cotacoes_historico = soup.find('section', {'id': 'quotations'})
        historico = cotacoes_historico.get('data-chart')
        historico = historico.replace("\\", '')
        historico = eval(historico)
        self.historico = historico
        historico = historico[-15:]

        dict_recurso = {'NOME_COTA':self.nome_cotacao, 'VALOR_COTA': valor_cota, 'VALOR_PATRIMONIO': valor_patrimonio, 'SEGMENTO': segmento,
                        'PORCENTAGEM_DIVIDENDOS': valor_porcentagem, 'PORCETAGEM_RENDIMENTO': situacao_porcentagem,
                        'RENDIMENTO': rendimento, 'P/PV': preco_por_acao, 'RENTABILIDADE_MÊS': rentabilidade,
                        'INFO': info, 'QUANDO_PAGA':data, 'HISTORICO': historico}
        return dict_recurso

    def abaixo_de(self, min=None, max=None):
        url = "https://www.fundsexplorer.com.br/funds"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
        site1 = requests.get(url, headers=headers)
        soup_fundo1 = bs(site1.content, 'html.parser')

        resultado = []
        result = self.fund_cotas(soup_fundo1, valor_min=min, valor_max=max)
        for x in result:
            if x != None:
                resultado.append(x)
        print(resultado)
        result = resultado
        return result

    def executor(self, acao, valor_min=None, valor_max=None):
        result = self.inicio(acao)
        if result != None:
            valor_acao = result['VALOR_COTA']
            if valor_acao != 'N/A':
                if valor_acao > valor_min.real and valor_acao < valor_max.real:
                    data = result['QUANDO_PAGA']
                    if data != None:
                        cota = acao,result['VALOR_COTA'],result['RENDIMENTO'],result['SEGMENTO'], data
                        print(f'fundos entre R${valor_min} e R${valor_max}, {cota}')
                        return cota

    def fund_cotas(self, soup, valor_min=None, valor_max=None):
        #lista de cotações
        lista_cotas = []
        # nome da cota
        fundos = soup.find('section', {'id':'fiis-list'})
        fundos = fundos.find('div', {'class':'row'})
        fundos = fundos.find_all('span', {'class', 'symbol'})
        for nome_fundos in fundos:
            nome_fundos = nome_fundos.text
            lista_cotas.append(nome_fundos)

        execucao = Parallel(n_jobs=-1)(delayed(self.executor)(acao=acao, valor_min=valor_min, valor_max=valor_max) for acao in lista_cotas)
        return execucao

if __name__ == "__main__":
    dt = datamine()
    dt.abaixo_de(min=10, max=40)