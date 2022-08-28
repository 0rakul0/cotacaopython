from util.conn.settings import *
from util.conn.conexao import *

conexao, cursor = conectando()
nome_schema = schema_e_tabela()

def create(query):
    # criação de tabela
    try:
        cursor.execute(query=query)
        conexao.commit()
        print("Tabela Criada")
    except:
        print("A tabela já existe")

def find_all():
    """
    :return: retorna todos os itens
    """
    cursor.execute("SELECT*FROM acao;")
    return cursor.fetchall()


def find_one(id, tabela):
    """
    :param id: do produto
    :return:
    """
    cursor.execute(f"SELECT * FROM {nome_schema}.{tabela} WHERE id=%s ;", (id,))
    return cursor.fetchall()


def update_user(id, name, tabela):
    cursor.execute(f"UPDATE {nome_schema}.{tabela} SET name = %s WHERE id=%s;", (name, id))


def delete_user(id, tabela):
    cursor.execute(f"DELETE FROM {nome_schema}.{tabela} WHERE id=%s ;", (id))


if __name__ == "__main__":
    from util.conn.conexao import *
    cursor = conexao.cursor()

    with open("./create_table.sql") as arq:
        query = arq.read()
        query = query.replace('\n', ' ').replace('   ', ' ')
        create(query)

    # create_produto(name="laranja", valor=5.4, quantidade=7)
    # print(find_all())
    cursor.close()
    conexao.close()
