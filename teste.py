import requests
import json


def inserir_dados():   
    # Dados da solicitação POST
    api_url = 'http://localhost:5000/novo_contato'  # Substitua pela URL da sua API
    content_type = 'application/json'  # Tipo de conteúdo apropriado para a sua API
    #sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL

    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
    }

    # Corpo da solicitação
    #data = sql_query


    id = input("Insira o ID : ")
    nome = input("Insira o nome : ")
    numero  = input("Insira o numero : ")
    codClient = input("Insira o codClient : ")
    ConfirmouWP = input("Insira o ConfirmouWP : ")
    ConfirmaEnvio = input("Insira o ConfirmaEnvio : ")
    envia = input("0 - False 1 - True : ")


    # Corpo da solicitação
    data = {
        "id": id,
        "nome": nome,
        "numero": numero,
        "codClient": codClient,
        "ConfirmouWP": ConfirmouWP,
        "ConfirmaEnvio": ConfirmaEnvio,
        "enviar" : int(envia)
    }

    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data)
    """
    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data_json)"""

    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)

def deletar():
     # Dados da solicitação POST
    api_url = 'http://localhost:5000/remove_registro'  # Substitua pela URL da sua API
    content_type = 'application/text'  # Tipo de conteúdo apropriado para a sua API
    #sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL

    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
    }
    data = input("Qual ID deseja deletar ? ")
    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, data=data)
    """
    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data_json)"""

    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)



def update():
    # Dados da solicitação POST
    api_url = 'http://localhost:5000/update'  # Substitua pela URL da sua API
    content_type = 'application/json'  # Tipo de conteúdo apropriado para a sua API
    #sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL

    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
    }

    # Corpo da solicitação
    #data = sql_query


    id = input("Insira o ID : ")
    nome = input("Insira o nome : ")
    numero  = input("Insira o numero : ")
    codClient = input("Insira o codClient : ")
    ConfirmouWP = input("Insira o ConfirmouWP : ")
    ConfirmaEnvio = input("Insira o ConfirmaEnvio : ")
    envia = input("0 - False 1 - True : ")


    # Corpo da solicitação
    data = {
        "id": id,
        "nome": nome,
        "numero": numero,
        "codClient": codClient,
        "ConfirmouWP": ConfirmouWP,
        "ConfirmaEnvio": ConfirmaEnvio,
        "envia" : envia
    }

    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data)
    """
    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data_json)"""

    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)

def contar():
    # Dados da solicitação POST
    api_url = 'http://localhost:5000/contar_clientes'  # Substitua pela URL da sua API
    content_type = 'application/data'  # Tipo de conteúdo apropriado para a sua API
    #sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL

    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
    }

    
    response = requests.get(api_url)
    """
    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data_json)"""

    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)

def criar_db():
     # Dados da solicitação POST
    api_url = 'http://localhost:5000/create_db'  # Substitua pela URL da sua API
    content_type = 'application/text'  # Tipo de conteúdo apropriado para a sua API
    #sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL

    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
    }

    # Enviando a solicitação POST
    response = requests.post(api_url)


    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)



while True:    
    menu = input("1 - Inserir dados\n2 - Deletar dados\n4 - Contar clientes\n5 - Criar DB\n0 - SAIR\n")
    match menu:
        case '1':
            inserir_dados()
        case '2':
            deletar()
        case '3':
            update()
        case '4':
            contar()
        case '5':
            criar_db()
        case '0':
            break
        case __:
            break
