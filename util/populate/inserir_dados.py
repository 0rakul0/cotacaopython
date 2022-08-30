import psycopg2
from util.conn.conexao import *


class inserir_dados():
    def __init__(self):
        self.conexao, self.cursor = conectando()
        self.nome_schema = schema_e_tabela()
        self.vinculo_id = None
        self.historico_id = None
        self.info_id = None


    def inserir_vinculo(self, texto_vinculo=None, nome_cota=None):
        try:
            self.conexao.commit()
            result = self.cursor.execute(f"""
            select *
            from {self.nome_schema}.vinculo
            insert into vinculo (idvinculos, vinculos, nome_cota)
            values ({texto_vinculo}, {nome_cota});
            """)
            self.vinculo_id = result
        except:
            vinculo_id = None
        return self.vinculo_id

    def inserir_historico(self, data=None, valor_cota=None, rendimento=None, nome_cota=None):
        try:
            self.conexao.commit()
            result = self.cursor.execute(f"""
            select *
            from {self.nome_schema}.historico
            insert into historico (id, data, valor_cota, rendimento, nome_cota )
            values ({data}, {valor_cota}, {rendimento}, {nome_cota});
            """)
            self.historico_id = result
        except:
            self.historico_id = None
        return self.historico_id

    def inserir_info(self,texto_info=None, nome_cota=None):
        try:
            self.conexao.commit()
            result = self.cursor.execute(f"""
            select *
            from {self.nome_schema}.info
            insert into info (id, texto, nome_cota)
            values ({texto_info}, {nome_cota});
            """)
            self.info_id = result
        except:
            self.info_id = None

        return self.info_id

    def inserir_acoes(self, tabela, name, segmento, liq_media_day, valor_cota, rendimento, valor_porcentagem, porcentagem_divid, liquidez_d, valor_patrimonio_pv, valor_mercado_pv, rentabilidade, preco_por_acao, ultimo_pg):
        try:
            self.conexao.commit()
            result = self.cursor.execute(f"""
            select *
            from {self.nome_schema}.{tabela};
            insert into {tabela} (idacao, name, segmento, vinculo_id, historico_id, liq_media_day, valor_cota, rendimento,
                       valor_porcentagem, info_id, porcentagem_divid, liquidez_d, valor_patrimonio_pv, valor_mercado_pv,
                       rentabilidade, preco_por_acao, ultimo_pg)
            values ({name}, {segmento}, {self.inserir_vinculo}, {self.inserir_historico}, {liq_media_day}, {valor_cota},{rendimento},
                       {valor_porcentagem}, {self.inserir_info}, {porcentagem_divid}, {liquidez_d}, {valor_patrimonio_pv}, {valor_mercado_pv},
                       {rentabilidade}, {preco_por_acao}, {ultimo_pg});""")
            print("dados inseridos")
            return result
        except Exception as e:
            print(f"erro ao inserir dado {e}")