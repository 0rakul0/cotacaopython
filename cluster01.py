import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import datetime


class cluster():

    def dataframe(self):
        url_1 = f"https://www.fundsexplorer.com.br/ranking"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
        site1 = requests.get(url_1, headers=headers)
        soup_fundo1 = bs(site1.content, 'html.parser')

        data = self.extrat(soup_fundo1)
        self.tratamento(data)

    def extrat(self, soup):
        # procura a tabela
        tabela = soup.find('table', {'id':'table-ranking'})
        # joga a tabela para uma string
        tabela_str = str(tabela)
        # transforma a tabela em um dataframe
        df = pd.read_html(tabela_str)[0]
        
        return df

    def tratamento(self, dados):
        #tratando valores vazios
        dados.rename(columns={'Códigodo fundo':'Codigo_do_fundo','Preço Atual':'Preco_Atual','Liquidez Diária':'Liquidez_Diaria','DY (3M)Acumulado':'DY_(3M)Acumulado','DY (6M)Acumulado':'DY_(6M)Acumulado','DY (12M)Acumulado':'DY_(12M)Acumulado','DY (3M)Média':'DY_(3M)Média','DY (6M)Média':'DY_(6M)Média','DY (12M)Média':'DY_(12M)Média','DY Ano':'DY_Ano','Variação Preço':'Variacao_Preco','Rentab. Período':'Rentab.Periodo','Patrimônio Líq.':'PatrimonioLiq','P/VPA':'P_VPA','VariaçãoPatrimonial':'Variacao_Patrimonial','Rentab. Patr.no Período':'Rentab._Patr.no_Periodo','Rentab. Patr.Acumulada':'Rentab._Patr.Acumulada','VacânciaFísica':'Vacancia_Fisica','VacânciaFinanceira':'VacanciaFinanceira'}
                     , inplace=True)
        #pega os dados para tratar
        dados_tratados = dados
        data = datetime.date.today()

        dados_tratados.to_csv(f'./bi/{data}_dataframe_cotacao.csv', encoding='utf8', sep=';')
        dados_tratados.to_csv(f'./bi/{data}_dataframe_cotacao.tsv', encoding='utf8', sep='\t')


if __name__=="__main__":
    cl = cluster()
    cl.dataframe()