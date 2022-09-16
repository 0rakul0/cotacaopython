import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, ttest_ind
from historico import *


class regres_hist():
    def run(self, nome, dados=None):
        x, y, z = self.extrat_hist(nome, dados)
        self.blpl(x,y,z)

    def blpl(self, x=None, y=None,z=None):
        """
        :param x: data
        :param y: valor
        :param z: renda
        :return:
        """
        plt.subplot(211)
        plt.plot(x,y,'-k')
        ax = plt.subplot(212)
        ax.boxplot([y], showfliers=False)
        ax.set_xticklabels(['y'])
        plt.show()
        print(ttest_ind(y,z))


    def extrat_hist(self, nome_acao, dados=None):
        hist = historico()
        valores = hist.historico_inicio(nome_acao)
        dados_valor_cota = []
        dados_valor_rendimento = []
        dados_data = []
        for x in valores:
            nome_cota = x.get('NOME_COTA')
            data_cota = x.get('DATA')
            valor_cota = x.get('VALOR_COTA')
            rendimento_cota = x.get('RENDIMENTO')
            if valor_cota < 80:
                dados_valor_cota.append(valor_cota)
                dados_valor_rendimento.append(rendimento_cota)
                dados_data.append(data_cota)

        dados_valor_cota = np.array(dados_valor_cota)
        dados_valor_rendimento = np.array(dados_valor_rendimento)
        dados_data = np.array(dados_data)

        if dados:
            return dados_data, dados_valor_cota, dados_valor_rendimento

        plt.scatter(dados_data, dados_valor_rendimento, label='data(rendimento)')
        plt.xlabel = 'datas'
        plt.ylabel = 'valor da cota'
        plt.legend()
        plt.show()

        plt.scatter(x=dados_data, y=dados_valor_cota, label='data(valor_cota)')
        plt.xlabel='datas'
        plt.ylabel='valor da cota'
        plt.legend()
        plt.show()
        
        beta, beta0, _,_, std_err = linregress(dados_valor_cota, dados_valor_rendimento)
        print(f'beta = {beta}')
        print(f'beta0 = {beta0}')
        print(f'desvio_padrão = {std_err}')
        yLin = beta * dados_valor_cota + beta0

        plt.plot(dados_valor_cota, yLin, '-k', dados_valor_cota, dados_valor_rendimento, 'ok', label='reta')
        plt.xlabel ='valor_cota'
        plt.ylabel ='rendimento'
        plt.legend()
        plt.show()


if __name__ == "__main__":
    rgh = regres_hist()
    rgh.run("mxrf11", dados=None)