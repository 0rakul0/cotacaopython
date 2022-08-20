from datamine import *
import re
class calc():
    def igualdade(self, acoes, valor_disponivel):
        """
        valores das cotas <= ao valor para gastar no total
        numerode_cotas*dividendos
        para maximizar usaremos os valores das cotas como negativo
        """

        rendimento_mes = 0
        nome_acoes = re.compile("(APTO11)|(MXRF11)|(GAME11)|(RZAG11)|(TORD11)|(VGHF11)")
        # nome_acoes = re.compile("(BNFS11)|(FAED11)|(FOFT11)|(IRIM11)|(JPPA11)|(PRSV11)|(TGAR11)")
        # obj = [9.25, 9.99, 9.7, 10.23]
        # lado_rendimento =[0.12, 0.12, 0.13, 0.14]
        nome = []
        obj = []
        lado_rendimento = []
        for acao in acoes:
            if nome_acoes.search(acao[0]):
                nome.append(acao[0])
                obj.append(acao[1])
                lado_rendimento.append(acao[2])

        qte_cotas = []

        quanto_eu_tenho = valor_disponivel

        print(f'valor para investir = {quanto_eu_tenho}')
        rendimento = quanto_eu_tenho/len(nome)
        print(f'valor distribuido = {rendimento}')
        for id, item in enumerate(obj):
            quantidade_cotas = rendimento/item
            qte_cotas.append(round(quantidade_cotas))
            print(f'cota: {nome[id]}, qte: {round(quantidade_cotas)}')
        for n, valor in enumerate(lado_rendimento):
            rendimento_acao = qte_cotas[n]*valor
            rendimento_mes += rendimento_acao
            print(f'valor recebido por acao da {nome[n]}, será de: {rendimento_acao}')
        print({rendimento_mes})
        return rendimento_mes

if __name__ == "__main__":
    cl = calc()
    dt = datamine()
    acoes = dt.abaixo_de(min=0, max=16, rendimento=0.1)
    valor_disponivel = 1000
    cl.igualdade(acoes, valor_disponivel)