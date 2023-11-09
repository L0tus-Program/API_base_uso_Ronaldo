# import pandas as pd
from datetime import datetime, timedelta
import sqlite3


def criar_login():
    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        perfil TEXT,
        senha TEXT,
        token TEXT
    )
    '''

    # Executar o comando SQL para criar a tabela
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


# Criar tabela manualmente


def criar_db_sqlite():
    print("Entrou criar")
    # Conectar ao banco de dados SQLite (ou criar um novo se não existir)
    conn = sqlite3.connect('openaai.db')

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
        ConfirmaEnvio TEXT,
        enviar INTEGER CHECK (enviar IN (0, 1))
    )
    '''

    # Executar o comando SQL para criar a tabela
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


# criar_db_sqlite()

# criar_login()
