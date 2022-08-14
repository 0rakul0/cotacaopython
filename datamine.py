import requests
from bs4 import BeautifulSoup as bs
import re

class datamine():
    def __init__(self):
        self.nome_cotacao = ''
        self.valor_cota = None
        self.valor_rendimento = None
        self.historico = []

    def limpeza_real(self, texto):
        texto = texto.replace('R$', '')
        texto = texto.replace('.', '')
        texto = texto.replace(',', '.')
        texto = texto.strip()
        texto = float(texto)
        return texto

    def inicio(self, nome):
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
        # valor da cota
        valor_cota = soup.find('div', {'id':'stock-price'})
        valor_cota = valor_cota.find('span', {'class':'price'}).text
        valor_cota = self.limpeza_real(valor_cota)

        #porcentagem de dividendos
        porcentagem = soup.find('span', text=re.compile('Dividend Yield'))
        valor_porcentagem = porcentagem.find_next_sibling('span', {'class':'indicator-value'}).text
        valor_porcentagem = valor_porcentagem.replace(',', '.').replace('%','')
        valor_porcentagem = valor_porcentagem.strip()
        valor_porcentagem = float(valor_porcentagem)
        situacao = 1-valor_porcentagem
        if situacao < 0:
            situacao_porcentagem = f'acima de 1% - vale investir - {valor_porcentagem}%'
        else:
            situacao_porcentagem = f'abaixo de 1% - segurar ou vender - {valor_porcentagem}%'

        descricao_rentabilidade = soup.find('span', text=re.compile('Valor Patrimonial'))
        valor_patrimonio = descricao_rentabilidade.find_next_sibling('span', {'class':'indicator-value'}).text
        valor_patrimonio = self.limpeza_real(valor_patrimonio)
        self.valor_cota = valor_patrimonio

        descricao_rendimento = soup.find('span', text=re.compile('Último Rendimento'))
        rendimento = descricao_rendimento.find_next_sibling('span', {'class': 'indicator-value'}).text
        rendimento = self.limpeza_real(rendimento)
        self.valor_rendimento = rendimento

        """
        P/VP = Valor de mercado na bolsa de valores / Valor patrimonial da empresa
        P/PV se tiver abaixo de 1 é pq tem desconto, logo significa que a empresa vale em bolsa menos do que o seu patrimônio líquido. Isso pode ser uma boa oportunidade para o investidor.
        """
        valor_mercado_pv = soup_2.find('span', text=re.compile('Valor de mercado'))
        valor_mercado_pv = valor_mercado_pv.find_next_sibling('span', {'class':'sub-value'}).text
        valor_mercado_pv = self.limpeza_real(valor_mercado_pv)
        valor_patrimonio_pv = soup_2.find('span', text=re.compile('Patrimônio'))
        valor_patrimonio_pv = valor_patrimonio_pv.find_next_sibling('span', {'class':'sub-value'}).text
        valor_patrimonio_pv = self.limpeza_real(valor_patrimonio_pv)
        preco_por_acao = (valor_mercado_pv/valor_patrimonio_pv).real

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
        info = soup.find('div', {'class':'text-dynamic-dividends'})
        info = info.find_all('p')
        for p in info:
            texto = p.text
            texto = texto.replace('\n', '').replace('  ', '')
            texto = texto.strip()
            p_list.append(texto)
        info = p_list


        #grafico das cotações
        cotacoes_historico = soup.find('section', {'id':'quotations'})
        historico = cotacoes_historico.get('data-chart')
        historico = historico.replace("\\",'')
        historico = eval(historico)
        self.historico = historico
        historico = historico[-15:]


        dict_recurso = {'VALOR_COTA':valor_cota, 'VALOR_PATRIMONIO':valor_patrimonio, 'PORCENTAGEM_DIVIDENDOS':valor_porcentagem, 'PORCETAGEM_RENDIMENTO':situacao_porcentagem, 'RENDIMENTO':rendimento,'P/PV':preco_por_acao, 'RENTABILIDADE_MÊS':rentabilidade, 'INFO':info ,'HISTORICO':historico}
        return dict_recurso

if __name__ == "__main__":
    dt = datamine()
    dt.inicio("mxrf11")