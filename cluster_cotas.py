import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


class cluster():

    def dataframe(self):
        url_1 = f"https://www.fundsexplorer.com.br/ranking"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
        site1 = requests.get(url_1, headers=headers)
        soup_fundo1 = bs(site1.content, 'html.parser')

        self.extrat(soup_fundo1)


    def extrat(self, soup):
        # procura a tabela
        tabela = soup.find('table', {'id':'table-ranking'})

        # joga a tabela para uma string
        tabela_str = str(tabela)

        # transforma a tabela em um dataframe
        df = pd.read_html(tabela_str)[0]

        #sava a tabeal em um csv
        df.to_csv('./bi/dataframe_cotacao.csv', index=True, sep=';')
        df.to_csv('./bi/dataframe_cotacao.tsv', sep='\t')
        return df

if __name__=="__main__":
    cl = cluster()
    cl.dataframe()