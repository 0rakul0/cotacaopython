from datetime import datetime, date
import pandas as pd
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
        self.situacao_pg = None
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
            # Liquidez Diária
            liquidez_d = soup.find('span', text=re.compile('Liquidez Diária'))
            liquidez_d = liquidez_d.find_next_sibling('span', {'class': 'indicator-value'}).text
            liquidez_d = liquidez_d.strip()
            liquidez_d = liquidez_d.replace('.','')
            liquidez_d = int(liquidez_d)

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
            preco_por_acao = soup.find('span', text=re.compile('P/VP'))
            preco_por_acao = preco_por_acao.find_next_sibling('span', {'class': 'indicator-value'}).text
            preco_por_acao = preco_por_acao.replace(',', '.')
            preco_por_acao = preco_por_acao.strip()
            preco_por_acao = float(preco_por_acao)

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
            data = re.search(re.compile('na data .{5}'), info[0])
            data = data.group(0)
            data = data.split('/')
            data = f'ultimo pagamento - {data[0][-2:]}/{data[1]}/2022'
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

        hist_list = self.hist(soup, soup_2)

        dict_recurso = {'LIQUIDEZ_DIARIA':liquidez_d, 'NOME_COTA': self.nome_cotacao, 'VALOR_COTA': valor_cota,
                        'VALOR_PATRIMONIO': valor_patrimonio, 'SEGMENTO': segmento,
                        'PORCENTAGEM_DIVIDENDOS': valor_porcentagem, 'PORCETAGEM_RENDIMENTO': situacao_porcentagem,
                        'RENDIMENTO': rendimento, 'P/PV': preco_por_acao, 'RENTABILIDADE_MÊS': rentabilidade,
                        'INFO': info, 'ULTIMO_PG': data, 'SITUACAO_PG': self.situacao_pg, 'HISTORICO': hist_list}
        return dict_recurso

    def historico_inicio(self, nome):
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

        result = self.hist(soup_fundo1, soup_fundo2)

        return result

    def hist(self, soup, soup_2):
        try:
            # grafico das cotações do funds
            hist_list = []
            cotacoes_historico = soup.find('section', {'id': 'quotations'})
            historico = cotacoes_historico.get('data-chart')
            historico = historico.replace("\\", '')
            historico = eval(historico)
            historico = historico

            # result do status
            cotacoes_rendimentos = soup_2.find('input', {'id': 'results'})
            cotacoes_rendimentos = cotacoes_rendimentos.get('value')
            cotacoes_rendimentos = cotacoes_rendimentos.replace("[{", '').replace("}]", '')
            cotacoes_rendimentos = cotacoes_rendimentos.split("},{")
            for linha_cotaceos in cotacoes_rendimentos:
                list_linha_cotaceos = linha_cotaceos.split(',')
                data_pg = list_linha_cotaceos[5][6:]
                data_pg = data_pg[:-1]
                data_pagamento = data_pg.split('/')
                data_pagamento = f'{data_pagamento[2]}-{data_pagamento[1]}-{data_pagamento[0]}'
                rendimento_pg = list_linha_cotaceos[8][4:]
                rendimento_pg = rendimento_pg[:-1]
                rendimento_pg = float(rendimento_pg)
                for dado in historico:
                    if data_pagamento == dado['day']:
                        hist_item = {'DATA': data_pagamento, 'VALOR_COTA': dado['value'], 'RENDIMENTO': rendimento_pg}
                        hist_list.append(hist_item)
        except:
            hist_list = None

        # situação pag
        if hist_list != None:
            self.situacao_pg = 'REGULAR'
        else:
            self.situacao_pg = 'INREGULAR'

        return hist_list

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
        result = self.inicio(acao)
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

    def carteira_publica(self):
        carteira_df = pd.read_excel('./bi/minha_carteira.xlsx', header=0, sheet_name='Planilha1')
        carteira_dict = []
        for indice, linha in carteira_df.iterrows():
            cart_info = self.inicio(linha['acoes'])
            nome_acao = cart_info['NOME_COTA']
            liq_diaria = cart_info['LIQUIDEZ_DIARIA']
            valor_cota = cart_info['VALOR_COTA']
            rend = cart_info['RENDIMENTO']
            n_cotas = linha['numero_de_cotas']
            gastos = float(valor_cota * n_cotas)
            ganhos = float(rend * n_cotas)
            indice_lucro = float(100 * rend / valor_cota)

            dict_carteira = {'ID': indice,'LIQ_DIARIA':liq_diaria, 'ACOES': nome_acao, 'VALOR_UNI': valor_cota, 'RENDIMENTO': rend,
                                 'NUM_COTAS': n_cotas, 'GASTOS': gastos, 'GANHOS': ganhos, 'RANK_%': indice_lucro}
            carteira_dict.append(dict_carteira)
        return carteira_dict
if __name__ == "__main__":
    dt = datamine()
    # dt.inicio('xplg11')
    # dt.carteira_publica()
    dt.historico_inicio('mxrf11')
    # dt.abaixo_de(min=0, max=100, rendimento=0.9, limit_liquidez=30000, mes='08')
