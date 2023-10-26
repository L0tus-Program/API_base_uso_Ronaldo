import requests

# Dados da solicitação POST
api_url = 'http://localhost:5000/query'  # Substitua pela URL da sua API
content_type = 'application/sql'  # Tipo de conteúdo apropriado para a sua API
sql_query = 'SELECT * FROM Clientes'  # Sua consulta SQL

# Cabeçalho da solicitação
headers = {
    'Content-Type': content_type,
}

# Corpo da solicitação
data = sql_query

# Enviando a solicitação POST
response = requests.post(api_url, headers=headers, data=data)

# Verificando a resposta
if response.status_code == 200:
    print('Solicitação POST bem-sucedida')
    print('Resposta da API:', response.json())
else:
    print('Falha na solicitação POST')
    print('Código de status:', response.status_code)
    print('Resposta da API:', response.text)
