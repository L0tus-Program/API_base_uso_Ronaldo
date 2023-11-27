import datetime
import smtplib
from email.mime.text import MIMEText
import requests 
import json
import time
import sqlite3


def send_whats(nome,numero):
    time.sleep(15)
    try:

        url = "https://api.conexaoia.digital/message/sendText/ronaldo"
        
        message = f'Olá {nome}, eu sou Ronaldo'


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
    except Exception as e:
        pass 
    # Como contornar o problema caso a evolution cair ?




# Função pra criação de log
def log_request(request, response):
    try:
        with open("log.txt", "a") as log_file:
            current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            ip_address = request.remote_addr
            request_content = request.data.decode('utf-8')
            response_content = response.get_data(as_text=True)
            log_entry = f"{current_time} - IP: {ip_address}\nRequest Content:\n{request_content}\nResponse Content:\n{response_content}\n\n"
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
    msg = MIMEText(conteudo, 'plain', 'utf-8') # é necessário codificar o objeto para utf-8 para poder enviar acentos
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



# Retorna o ultimo cliente cadastrado
def last_client():
    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()

    cursor.execute("SELECT nome, numero FROM clientes ORDER BY id DESC LIMIT 1")
    last_client = cursor.fetchone()

    conn.close()

    return last_client if last_client else None
