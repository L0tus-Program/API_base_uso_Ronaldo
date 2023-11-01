import requests
import json


def inserir_dados():   
    # Dados da solicitação POST
    api_url = 'http://localhost:5000/novo_contato'  # Substitua pela URL da sua API
    content_type = 'application/json'  # Tipo de conteúdo apropriado para a sua API
    #sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
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
    
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
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
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
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
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
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
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
    }

    # Enviando a solicitação POST
    response = requests.post(api_url,headers= headers)


    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)

def inserir_user():
    # Dados da solicitação POST
    api_url = 'http://localhost:5000/new_user'  # Substitua pela URL da sua API
    content_type = 'application/json'  # Tipo de conteúdo apropriado para a sua API
    #sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
    }

    # Corpo da solicitação
    #data = sql_query


    email = input('Email = ')
    perfil = input ('perfil = ')
    senha = input ('senha = ')
    token = input ('token = ')
    


    # Corpo da solicitação
    data = {
        "email": email,
        "perfil": perfil,
        "senha": senha,
        "token": token
       
    }

    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data)


    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)



def delete_user():
     # Dados da solicitação POST
    api_url = 'http://localhost:5000/delete_user'  # Substitua pela URL da sua API
    content_type = 'application/text'  # Tipo de conteúdo apropriado para a sua API
    
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
    }
    data = input("Qual email user deseja deletar ? ")
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



def altera_senha():
    # Dados da solicitação POST
    api_url = 'http://localhost:5000/update_password'  # Substitua pela URL da sua API
    content_type = 'application/json'  # Tipo de conteúdo apropriado para a sua API
    #sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
    }

    # Corpo da solicitação
    #data = sql_query


    email = input("Insira o email : ")
    new_password = input("Insira a nova senha : ")
   


    # Corpo da solicitação
    data = {
        "email": email,
        "new_password": new_password
        
    }

    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data)
  

    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)
    

def altera_token():
    # Dados da solicitação POST
    api_url = 'http://localhost:5000/update_token'  # Substitua pela URL da sua API
    content_type = 'application/json'  # Tipo de conteúdo apropriado para a sua API
    api_key = "F14C7D7625414A3E5DA1811349667"
    
    # Cabeçalho da solicitação
    headers = {
        'Content-Type': content_type,
        'X-API-KEY': str(api_key)
    }

    # Corpo da solicitação
    

    email = input("Insira o email : ")
    new_token = input("Insira o novo token : ")
   


    # Corpo da solicitação
    data = {
        "email": email,
        "new_token": new_token
        
    }

    # Enviando a solicitação POST
    response = requests.post(api_url, headers=headers, json=data)
  

    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação POST bem-sucedida')
        print('Resposta da API:', response.json())
    else:
        print('Falha na solicitação POST')
        print('Código de status:', response.status_code)
        print('Resposta da API:', response.text)
    


while True:    
    menu = input("1 - Inserir dados\n2 - Deletar dados\n4 - Contar clientes\n5 - Criar DB\n6 - Inserir USER\n7 - Delete user\n8 - Altera senha USER\n9 - Update token\n0 - SAIR\n")
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
        case '6':
            inserir_user()
        case '7':
            delete_user()
        case '8':
            altera_senha()
        case '9':
            altera_token()
        case '0':
            break
        case __:
            break
