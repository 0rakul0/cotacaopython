from datetime import datetime, date
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from joblib import Parallel, delayed
import re
from historico import *


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

        if result == None and site1.status_code == 500:
            print(f'site 1 off {site1}')
            result = self.so_site2(soup_fundo2)
        elif result == None and site2.status_code == 500:
            print(f'site 2 off {site2}')

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

        valor_mercado_pv = None
        valor_patrimonio_pv = None
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
            if segmento:
                segmento = segmento.find_next_sibling('span', {'class': 'description'}).text
                segmento = segmento.strip()
            else:
                segmento = 'N/A'
        except:
            segmento = soup_2.find('h3', text=re.compile('Segmento'))
            if segmento:
                segmento = segmento.find_next_sibling('strong', {'class': 'value'}).text
            else:
                segmento = 'N/A'

        # vinculos
        try:
            vinculos_list = []
            vinculos = soup_2.find('b', text=re.compile('FIIs relacionadas:'))
            vinculos = vinculos.find_next_sibling('div')
            vinculos = vinculos.find_all('a')
            for linha in vinculos:
                linha = linha.get('href')
                linha = linha.split('/')
                linha = linha[-1]
                vinculos_list.append(linha)
        except:
            vinculos_list = []
            vinculos = soup.find('div', {'id':'related-fiis-carousel'})
            vinculos = vinculos.find_all('div', {'class':'carousel-cell'})
            for vinc in vinculos:
                try:
                    nome_vinc = vinc.find('div', {'class':'item'})
                    nome_vinc = nome_vinc.find('span', {'class':'symbol'}).text
                    if nome_vinc != None:
                        vinculos_list.append(nome_vinc)
                except:
                    pass
        else:
            vinculos_list = []

        # ativos
        ativo = ''
        estado = ''
        try:
            ativo = soup.find('span', {'class':'fund-actives'}).text
            estado = soup.find('span', {'class':'fund-states'}).text
        except:
            ativo = len(vinculos_list)
            estado = ''

        ht = historico()
        hist_list = ht.historico_inicio(nome=self.nome_cotacao)

        # situação pag
        if hist_list != None:
            self.situacao_pg = 'REGULAR'
        else:
            self.situacao_pg = 'INREGULAR'


        dict_recurso = {'LIQUIDEZ_DIARIA':liquidez_d, 'NOME_COTA': self.nome_cotacao, 'VALOR_COTA': valor_cota,
                        'VALOR_PATRIMONIO': valor_patrimonio_pv, 'SEGMENTO': segmento,'VINCULOS':vinculos_list,
                        'ATIVOS':ativo, 'ESTADOS':estado,
                        'PORCENTAGEM_DIVIDENDOS': valor_porcentagem, 'PORCETAGEM_RENDIMENTO': situacao_porcentagem,
                        'RENDIMENTO': rendimento, 'P/PV': preco_por_acao, 'RENTABILIDADE_MÊS': rentabilidade,
                        'INFO': info, 'ULTIMO_PG': data, 'SITUACAO_PG': self.situacao_pg,
                        'VALOR_MERCADO':valor_mercado_pv, 'HISTORICO': hist_list}
        return dict_recurso

    def so_site2(self, soup_2):
        # Nome da cota
        try:
            nome_cota = soup_2.find('h2', {'class':'card-title'}).text
            nome_cota = nome_cota.split(' ')
            nome_cota = nome_cota[-1]
        except:
            nome_cota = self.nome_cotacao
        try:
            # Liquidez média diária
            liq_media_day = soup_2.find('span', text=re.compile('Liq\. méd\. diária'))
            liq_media_day = liq_media_day.find_parent('div').find('strong', {'class':'value'}).text
            liq_media_day = self.limpeza_real(liq_media_day)

            # valor da cota
            valor_cota = soup_2.find('h3', text=re.compile('Valor atual'))
            valor_cota = valor_cota.find_next_sibling('strong',{'class':'value'}).text
            valor_cota = self.limpeza_real(valor_cota)

            # porcentagem de dividendos
            porcentagem_divid = soup_2.find('small', text=re.compile('Rendimento'))
            porcentagem_divid = porcentagem_divid.find_next('b').text
            porcentagem_divid = self.limpeza_real(porcentagem_divid)

            # ultimo rendimento
            ultimo_rendimento = soup_2.find('span', text=re.compile('Último rendimento'))
            ultimo_rendimento = ultimo_rendimento.find_next('div', {'class':'info'}).find('strong', {'class':'value'}).text
            ultimo_rendimento = self.limpeza_real(ultimo_rendimento)

            # pvp
            valor_mercado_pv = None
            valor_patrimonio_pv = None
            valor_mercado_pv = soup_2.find('span', text=re.compile('Valor de mercado'))
            valor_mercado_pv = valor_mercado_pv.find_next_sibling('span', {'class': 'sub-value'}).text
            valor_mercado_pv = self.limpeza_real(valor_mercado_pv)
            valor_patrimonio_pv = soup_2.find('span', text=re.compile('Patrimônio'))
            valor_patrimonio_pv = valor_patrimonio_pv.find_next_sibling('span', {'class': 'sub-value'}).text
            valor_patrimonio_pv = self.limpeza_real(valor_patrimonio_pv)
            preco_por_acao = (valor_mercado_pv / valor_patrimonio_pv).real

            # setor
            segmento = soup_2.find('h3', text=re.compile('Segmento'))
            segmento = segmento.find_next_sibling('strong', {'class':'value'}).text

            # vinculos
            vinculos_list = []
            vinculos = soup_2.find('b', text=re.compile('FIIs relacionadas:'))
            vinculos = vinculos.find_next_sibling('div')
            vinculos = vinculos.find_all('a')
            for linha in vinculos:
                linha = linha.get('href')
                linha = linha.split('/')
                linha = linha[-1]
                vinculos_list.append(linha)

            ht = historico()
            hist_list = ht.historico_inicio(nome=nome_cota)

            dict_recurso = {'NOME_COTA':nome_cota,'SEGMENTO':segmento,'VINCULOS':vinculos_list,'LIQUIDEZ_MEDIA':liq_media_day,'VALOR_COTA':valor_cota,'PORCENMTAGEM_DIVIDENDOS':porcentagem_divid,'ULTIMO_RENDIMENTO':ultimo_rendimento,'P/VP': preco_por_acao, 'VALOR_MERCADO':valor_mercado_pv, 'VALOR_PATRIMONIO':valor_patrimonio_pv, 'HISTORICO':hist_list}
            return dict_recurso
        except:
            return None

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
    # ht = historico()
    # dt.inicio('rzag11')
    # dt.carteira_publica()

