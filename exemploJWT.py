from flask import Flask, request, jsonify, abort
import jwt
import datetime
import secrets

app = Flask(__name)

# Sua chave secreta para assinar tokens JWT
SECRET_KEY = secrets.token_urlsafe(32)

# Função para gerar um token JWT
def create_token(data):
    # Defina os dados que você deseja incluir no token
    payload = {
        'data': data,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Defina o tempo de expiração do token
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Função para verificar um token JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expirado. Faça login novamente."
    except jwt.InvalidTokenError:
        return "Token inválido. Faça login novamente."

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    # Autentique o usuário (verifique o nome de usuário e senha) e gere um token JWT se a autenticação for bem-sucedida
    # Substitua isso com a lógica de autenticação real
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'usuario' and password == 'senha':
        token = create_token({'username': username})
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Falha na autenticação'}), 401

# Rota protegida que requer autenticação por token JWT
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token de autenticação ausente'}), 401

    token = token.replace('Bearer ', '')  # Remova o prefixo 'Bearer ' do cabeçalho de autorização

    payload = verify_token(token)
    if isinstance(payload, str):
        return jsonify({'message': payload}), 401

    return jsonify({'message': 'Rota protegida', 'user': payload['data']['username']}), 200

if __name__ == '__main__':
    app.run(debug=True)
