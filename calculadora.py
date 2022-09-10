from calculadora_cotacao import calculadora_cotacao
from datamine import *
import re
import numpy as np
import pandas as pd

class calc():

    def run(self, valor_disponivel=None,rendimento_corte=None, divid_min=None, valor_min=None, valor_max=None):
        dataframe = pd.read_csv("./bi/2022-08-31_dataframe_cotacao.tsv", sep='\t')
        new_df = dataframe.copy()
        saida_json = self.igualdade(df_acoes=new_df, valor_disponivel=valor_disponivel, rendimento_corte=rendimento_corte,divid_min=divid_min, minimo=valor_min, maximo=valor_max)
        return saida_json

    def igualdade(self,df_acoes=None, valor_disponivel=None, rendimento_corte=None, divid_min=None,minimo=None, maximo=None):
        """
        valores das cotas <= ao valor para gastar no total
        numerode_cotas*dividendos
        para maximizar usaremos os valores das cotas como negativo
        """
        rendimento_mes = 0
        nome_acoes = re.compile("(APTO11)|(MXRF11)|(GAME11)|(RZAG11)|(BIME11)")
        rendimento_acao = rendimento_corte
        nome = []
        obj = []
        yid = []
        lado_rendimento = []
        tipo_negocio = []
        if divid_min == None:
            divid__min = 0
        for id, acao in df_acoes.iterrows():
            preco_divid = acao['Dividendo']
            preco_divid = preco_divid.replace('.', '')
            preco_divid = preco_divid.replace(',', '.').split()
            preco_divid = float(preco_divid[-1])
            divid_yid = acao['DividendYield']
            preco_acao = acao['Preço Atual']
            try:
                divid_yid = divid_yid.replace(',', '.').replace('%','').split()
                divid_yid = float(divid_yid[-1])
                preco_acao = preco_acao.replace('.', '').replace(',', '.').split()
                preco_acao = float(preco_acao[-1])
                if (preco_divid >= rendimento_acao and divid_yid >= divid_min) and (preco_acao >= minimo and preco_acao <= maximo):
                    try:
                        nome_acao = acao['Códigodo fundo']
                        preco_acao = acao['Preço Atual']
                        nome_negocio = acao['Setor']
                        preco_acao = preco_acao.replace('.','')
                        preco_acao = preco_acao.replace(',','.').split()
                        preco_acao = float(preco_acao[-1])

                        nome.append(nome_acao)
                        obj.append(preco_acao)
                        lado_rendimento.append(preco_divid)
                        yid.append(divid_yid)
                        tipo_negocio.append(nome_negocio)
                    except:
                        pass
            except:
                pass
        qte_cotas = []
        quanto_eu_tenho = valor_disponivel
        print(f'valor para investir = {quanto_eu_tenho}')
        rendimento = quanto_eu_tenho/len(nome)
        print(f'valor distribuido = {rendimento}')
        cotacoes_a_comprar = []
        valor_recebido_list = []
        for id, item in enumerate(obj):
            quantidade_cotas = rendimento/item
            qte_cotas.append(round(quantidade_cotas))
            compras = f'cota: {nome[id]}, qte: {round(quantidade_cotas)}'
            cotacoes_a_comprar.append(compras)
        for n, valor in enumerate(lado_rendimento):
            rendimento_acao = qte_cotas[n]*valor
            rendimento_mes += rendimento_acao
            valor_recebido = f'{nome[n]},o rendimento será de: {rendimento_acao}'
            valor_recebido_list.append(valor_recebido)


        saida_json = dict(zip(cotacoes_a_comprar,valor_recebido_list))
        return saida_json


if __name__ == "__main__":
    cl = calc()
    valor_disponivel = 1000
    rendimento_corte = 0.1
    divid_min = 1
    minimo = 8
    maximo = 12
    cl.run(valor_min=minimo, valor_max=maximo, rendimento_corte=rendimento_corte, valor_disponivel=valor_disponivel, divid_min=divid_min)
    # cl.otimizacao(1200)