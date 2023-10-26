import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import os # Verificar se o BD existe na pasta de arquivos


"""def bd(df_BaseTest):
    print("Entrando na função bd")
    df_BaseTest = df_BaseTest
    print("Criando banco de dados")
    # Conexão com o sqlite
    conn = sqlite3.connect('clientes.db')
    #transforma o dataframe em tabela SQL
    df_BaseTest.to_sql('Clientes', conn, if_exists='replace',index = True )
    conn.commit()
    conn.close()




def verifica():
    # Nome do arquivo do banco de dados SQLite
    db_file = "clientes.db"
    print(f"Verificando se o arquivo {db_file} existe")
    # Verifica se o arquivo do banco de dados existe
    if os.path.isfile(db_file):
        print(f"O banco de dados {db_file} existe.")
    else:
        print(f"O banco de dados {db_file} não existe.")
        try:
            print("Carregando dataframes")
            df_BaseTest = pd.read_excel('BaseTest.xlsx')
            
            bd(df_BaseTest)
           # assessores()
        except:
            print("Sem planilhas para carregar")

"""

#verifica()







# Criar tabela manualmente


def criar_db_sqlite():
    print("Entrou criar")
    # Conectar ao banco de dados SQLite (ou criar um novo se não existir)
    conn = sqlite3.connect('clientes.db')

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    # Definir o comando SQL para criar a tabela
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS clientes (
        id TEXT,
        nome TEXT,
        numero TEXT,
        codClient TEXT,
        ConfirmouWP TEXT,
        ConfirmaEnvio TEXT
    )
    '''

    # Executar o comando SQL para criar a tabela
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


criar_db_sqlite()



"""
def update():
    print("Carregando dataframes")
    df_conexao = pd.read_excel('clientes_conexao.xlsx')
    df_produtos = pd.read_excel('clientes_conexao_produtos.xlsx')
    df_assessores = pd.read_excel('assessores.xlsx')
    df_atendimentos = pd.read_excel('atendimentosDados.xlsx')
    bd(df_conexao,df_produtos,df_assessores,df_atendimentos)
    """




