import pandas as pd
from datetime import datetime, timedelta
import sqlite3



def codigos_return():
    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS codigos_return (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    x_vezes INTEGER DEFAULT 0
)
    '''
 
    # Executar o comando SQL para criar a tabela
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()



def dash():
    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS painel (
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
        id INTEGER PRIMARY KEY,
        nome TEXT,
        numero TEXT,
        codClient TEXT,
        ConfirmaEnvio INTEGER CHECK (ConfirmaEnvio IN (0, 1)),
        enviar INTEGER CHECK (enviar IN (0, 1))
    )
    ''' 
    

    # Executar o comando SQL para criar a tabela
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

def popular_codigos_return():
    codigos = [
        (200, 0),
        (201, 0),
        (400, 0),
        (401, 0),
        (500, 0)
    ]

    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()

    # Inserir os códigos na tabela
    for codigo in codigos:
        cursor.execute("INSERT INTO codigos_return (codigo, x_vezes) VALUES (?, ?)", codigo)

    conn.commit()
    conn.close()

def popular_dash():
    email = 'felipe.gomes@messeminvestimentos.com.br'
    perfil = 'admin'
    senha = 'admin'  # Note que armazenar senhas em texto simples não é recomendado em produção
    token = '11111'  # Defina o token conforme necessário

    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()

    # Inserir o usuário na tabela
    cursor.execute("INSERT INTO painel (email, perfil, senha, token) VALUES (?, ?, ?, ?)", (email, perfil, senha, token))

    conn.commit()
    conn.close()

criar_db_sqlite()

criar_login()


codigos_return()

dash()

popular_dash()

popular_codigos_return()