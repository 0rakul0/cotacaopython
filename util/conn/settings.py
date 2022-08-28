def conect(numb):
    """
    configuraçãoes do docker
    """
    host = ''
    user = ''
    password = ''
    database = ''
    port = ''

    if numb == 'localhost':
        host = 'localhost'
        user = 'postgres'
        password='00110011aa'
        database = 'acoes_e_cotacoes'
        port = '5432'

    elif numb == 'docker':
        host = 'host.docker.internal'
        user = 'postgres'
        password = 'postgrespw'
        database = 'acoes_e_cotacoes'
        port = '49153'

    return host, user, password, database, port

def schema_e_tabela():
    nome_schema = 'acoes_ecotacoes'
    return nome_schema