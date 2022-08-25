import requests
from bs4 import BeautifulSoup as bs

class historico():
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
        if result == None and site1.status_code == 500:
            print(f'site 1 off {site1}')
            result = self.so_site2(soup_fundo2)
        elif result == None and site2.status_code == 500:
            print(f'site 2 off {site2}')
            result = self.so_site1(soup_fundo1)
        return result


    def hist(self, soup_1, soup_2):
        try:
            # grafico das cotações do funds
            hist_list = []
            cotacoes_historico = soup_1.find('section', {'id': 'quotations'})
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

        return hist_list

    def so_site1(self, soup_1):
        hist_list = []
        cotacoes_historico = soup_1.find('section', {'id': 'quotations'})
        historico = cotacoes_historico.get('data-chart')
        historico = historico.replace("\\", '')
        historico = eval(historico)
        historico = historico
        hist_list.append(historico)
        return hist_list

    def so_site2(self, soup_2):
        hist_list_site_2 = []
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
            hist_site_2 = {'DATA':data_pagamento, 'RENDIMENTO':rendimento_pg}
            hist_list_site_2.append(hist_site_2)
        return hist_list_site_2
if __name__=="__main__":
    ht = historico()
    ht.historico_inicio('mxrf11')