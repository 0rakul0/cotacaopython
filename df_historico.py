import pandas as pd
from historico import historico


class gerador_csv():
    def chamada_hist(self, dados):
        hist = historico()
        dataframe = pd.read_csv(dados, sep=';')
        nomes = dataframe['Códigodo_fundo']
        for x in nomes:
            days = []
            values = []
            rendimentos = []
            data_hist = hist.historico_inicio(x)
            for y in data_hist:
                day = y.get('day')
                value = y.get('value')
                days.append(day)
                values.append(value)
                try:
                    rendimento = y.get('rendimento')
                    rendimentos.append(rendimento)
                except:
                    rendimento = 'None'
                    rendimentos.append(rendimento)

            dict_base = {'days':days, 'values':values, 'redimentos':rendimentos}
            dict_base = pd.DataFrame(dict_base)
            dict_base.to_csv(f'./hist/{x}.csv', sep=';')

if __name__ == "__main__":
    gc = gerador_csv()
    nome_csv = './bi/2022-09-14_dataframe_cotacao.csv'
    gc.chamada_hist(dados=nome_csv)