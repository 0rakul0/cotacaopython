from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re

class informes():

    def inicio(self, nome):
        ser = "./chromedriver105/chromedriver.exe"
        op = Options()
        self.nome_cotacao = nome
        op.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=ser, options=op)
        url_1 = f"https://www.fundsexplorer.com.br/funds/{nome}"
        driver.get(url_1)
        soup_fundo1 = bs(driver.page_source, 'html.parser')
        sleep(1)
        self.mineracao(soup_fundo1)

    def mineracao(self, dados):
        aviso_estruturado = dados.find('table', {'id':'DataTables_Table_0'})
        re_estruturado = aviso_estruturado.find('a', text=re.compile('Aviso aos Cotistas'))
        documento = re_estruturado.text
        link = re_estruturado.get('href')
        print(documento, link)

if __name__ =="__main__":
    inf = informes()
    inf.inicio("MXRF11")