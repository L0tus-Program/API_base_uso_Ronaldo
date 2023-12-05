import requests

def download_backup():
    url = 'https://chat.conexaoia.digital/backup'  

    try:
        payload = {}
        headers = {
          'X-API-KEY': 'F14C7D7625414A3E5DA1811349667'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            with open('openaai.db', 'wb') as file:
                file.write(response.content)
            print('Arquivo salvo com sucesso!')
        else:
            print(f'Falha ao baixar o arquivo. Código de status: {response.status_code}')
    except requests.RequestException as e:
        print(f'Erro ao fazer o request: {e}')

download_backup()
