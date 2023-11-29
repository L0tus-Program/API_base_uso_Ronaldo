import requests 
import json


def send_whats(nome,numero):
    #time.sleep(15)
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

        if response.status_code == '201':
            print("Tudo certo")
        else:
            print("Deu ruim não envia nada")
        
        print(response.text)
        print(response.status_code)
    except Exception as e:
        pass 
    # Como contornar o problema caso a evolution cair ?





#send_whats("Crackudinho do php","5551997572169")

send_whats("O brabo","5551992090470")

#send_whats("hum","0101")