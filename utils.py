import datetime
import smtplib
from email.mime.text import MIMEText
import requests
import json
# import time
import sqlite3
import csv
import threading #Devo fazer a nova tentativa da evolution em outra thread ?
import jwt


def send_whats(nome, numero, codClient):
    # time.sleep(15)
    try:

        url = "https://api.conexaoia.digital/message/sendText/ronaldo"

        message = f'Olá {nome}. Sou o Ronaldo e trabalho como especialista em renda variável. Estou aqui para oferecer sugestões e orientações sobre investimentos nessa área.'

        payload = json.dumps({
            "number": numero,
            "options": {
                "delay": 1200,
                "presence": "composing",
                "linkPreview": False
            },
            "textMessage": {
                "text": message
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'apikey': 'B6D711FCDE4D4FD5936544120E713976'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        print(response.status_code)
        if response.status_code != 201:
            try:
                conn = sqlite3.connect('openaai.db')
                cursor = conn.cursor()
                # Executa a query SQL para inserir um novo cliente na tabela
                query = "INSERT INTO lista_espera ( nome, numero, codClient) VALUES ( ?, ?, ?)"
                cursor.execute(query, (nome, numero, codClient,
                                    ))

                # Comita a transação e fecha a conexão com o banco de dados
                conn.commit()
                conn.close()

                return 'Erro'
            except Exception as e:
                pass
            finally:
                try:
                    # Dados da solicitação POST
                    api_url = 'http://192.168.0.249:5000/novo_contato'  # Substitua pela URL da sua API
                    content_type = 'application/json'  # Tipo de conteúdo apropriado para a sua API
                    # sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL
                    api_key = "F14C7D7625414A3E5DA1811349667"

                    # Cabeçalho da solicitação
                    headers = {
                        'Content-Type': content_type,
                        'X-API-KEY': str(api_key)
                    }

                   


                    # Enviando a solicitação POST
                    response = requests.post(api_url, headers=headers)
                    print("Response")
                    print(response)
                    segredo = response.json()
                    data = segredo.get("token")
                    print(data)

                    segredo = segredo.get("key")
                    print(segredo)
                    # segredo = cifra(segredo)
                    # Descriptografe o token usando a mesma chave secreta
                    dados = jwt.decode(data, segredo, algorithms=['HS256'])
                    print(dados)
                    """
                    # Enviando a solicitação POST
                    response = requests.post(api_url, headers=headers, json=data_json)"""

                    # Verificando a resposta
                    if response.status_code == 200:
                        dados_json = dados.get('data')
                        print('Solicitação POST bem-sucedida')
                        print('Resposta da API:', dados_json)
                    else:
                        print('Falha na solicitação POST')
                        print('Código de status:', dados.status_code)
                        print('Resposta da API:', dados.text)
                except Exception as e:
                    print(f"Erro: {e}")

            
        
        # Após o envio bem-sucedido, exclua o cliente da tabela
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Comando para excluir o cliente da tabela lista_espera
        query_delete = "DELETE FROM lista_espera WHERE codClient = ?"
        cursor.execute(query_delete, (codClient,))
        conn.commit()
        conn.close()
    except Exception as e:
        pass
    # Como contornar o problema caso a evolution cair ?


def invoca_lista():
    try:
        # Dados da solicitação POST
        api_url = 'http://192.168.0.249:5000/lista_espera'  # Substitua pela URL da sua API
        content_type = 'application/json'  # Tipo de conteúdo apropriado para a sua API
        # sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL
        api_key = "F14C7D7625414A3E5DA1811349667"

        # Cabeçalho da solicitação
        headers = {
            'Content-Type': content_type,
            'X-API-KEY': str(api_key)
        }

       
        # Enviando a solicitação POST
        response = requests.post(api_url, headers=headers)
        print(response)
    except Exception as e:
        pass
        



# Função pra criação de log
def log_request(request, response):
    try:
        with open("log.txt", "a") as log_file:
            current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            ip_address = request.remote_addr
            rota = request.path
            request_content = request.data.decode('utf-8')
            response_content = response.get_data(as_text=True)
            log_entry = f"{current_time} - IP: {ip_address}\nRoute:{rota}\nRequest Content:\n{request_content}\nResponse Content:\n{response_content}\n\n"
            log_file.write(log_entry)
    except Exception as e:
        # Em caso de erro ao registrar o log, você pode optar por fazer algum tratamento específico ou simplesmente ignorá-lo.
        pass


def mail():
    print("Entrando na função mail")
    # Dados de autenticação
    username = "openaai@conexaoia.digital"
    password = "Messem@2023"
    emailDestino = "felipe.gomes@messeminvestimentos.com.br"
    conteudo = "Erro com a APi"
    # Criação do objeto MIMEText
    # é necessário codificar o objeto para utf-8 para poder enviar acentos
    msg = MIMEText(conteudo, 'plain', 'utf-8')
    msg['To'] = emailDestino
    msg['From'] = username
    msg['Subject'] = "Erro com a API"

    # Adicionando cabeçalhos de conteúdo
    msg.add_header('Content-Type', 'text/plain; charset=UTF-8')

    # Enviando o e-mail
    with smtplib.SMTP("smtp.hostinger.com", 465) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, emailDestino, msg.as_string())

    print("E-mail enviado com sucesso!")


# Retorna o ultimo cliente cadastrado -> Deixou de ser usada, pode ser removida pro deploy final
def last_client():
    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nome, numero FROM clientes ORDER BY id DESC LIMIT 1")
    last_client = cursor.fetchone()

    conn.close()

    return last_client if last_client else None


def export_to_csv():
    try:
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Sua consulta SQL
        query = "SELECT * FROM clientes WHERE enviar = '1'"

        cursor.execute(query)
        rows = cursor.fetchall()

        # Nome do arquivo CSV de saída
        csv_file = 'relatorio.csv'

        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            # Escreve os cabeçalhos das colunas
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(rows)  # Escreve os dados das linhas

        print(f"Os dados foram exportados para {csv_file} com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro ao exportar para CSV: {e}")

    finally:
        if conn:
            conn.close()



def message_from_front(numero,message,instancia):
    try:

        url = f'https://api.conexaoia.digital/message/sendText/{instancia}'

        #message = f'Olá {nome}. Sou o Ronaldo e trabalho como especialista em renda variável. Estou aqui para oferecer sugestões e orientações sobre investimentos nessa área.'

        payload = json.dumps({
            "number": numero,
            "options": {
                "delay": 1200,
                "presence": "composing",
                "linkPreview": False
            },
            "textMessage": {
                "text": message
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'apikey': 'B6D711FCDE4D4FD5936544120E713976'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        print(response.status_code)




    except Exception as e:
        pass



def deslogar_evolution(instancia):
    try:
        url = f'https://api.conexaoia.digital/instance/logout/{instancia}'
    
        payload = {}
        headers = {
        'apikey': 'B6D711FCDE4D4FD5936544120E713976'
        }
        
        response = requests.request("DELETE", url, headers=headers, data=payload)
        
        print(response.text)
        
    except Exception as e:
        return "erro deslogar"



def deletar_instancia(instancia):
    try:

        
        url = f'https://api.conexaoia.digital/instance/delete/{instancia}'
        
        payload = {}
        headers = {
        'apikey': 'B6D711FCDE4D4FD5936544120E713976'
        }
        
        response = requests.request("DELETE", url, headers=headers, data=payload)
        
        print(response.text)

    except Exception as e:
        return "erro deletar"



def criar_instancia(instancia):
    try:

        
        url = "https://api.conexaoia.digital/instance/create"
 
        payload = json.dumps({
        "instanceName": instancia,
        "token": "B6D711FCsDE4D4FD5936544120Es713976",
        "qrcode": True
        })
        headers = {
        'Content-Type': 'application/json',
        'apikey': 'B6D711FCDE4D4FD5936544120E713976'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)

    except Exception as e:
        return "erro criar"