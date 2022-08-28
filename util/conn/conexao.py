import psycopg2
from util.conn.settings import *
# configurações

def conectando():
    host, user, password, database, port = conect('docker')
    cursor = None
    conexao = None
    try:
        conn_str = f'host={host} user={user} dbname={database} password={password} port={port}'
        conexao = psycopg2.connect(conn_str)
        print("conectado")
        cursor = conexao.cursor()
    except:
        print("falha ao conectar")

    return conexao, cursor