from flask import Flask, request, jsonify, abort, render_template, send_from_directory, send_file,after_this_request
from flask_cors import CORS
import db
import sqlite3
import json
import datetime
import secrets
import jwt
import sys
import os
from utils import log_request,send_whats,last_client
import threading
#from utils import teste



# Abra o arquivo JSON
with open('src.json', 'r') as file:
    src = json.load(file)


# key API
API_KEY = str(src['key'])

# Sua chave secreta para assinar tokens JWT
SECRET_KEY = secrets.token_urlsafe(32)


# Outras configurações do aplicativo
DEBUG = True
ENV = 'development'
HOST = 'localhost'
PORT = 5000

# Criando aplicação
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Quando subir pra VPS, configurar domínios que podem acessar

# Autenticação

def authenticate():
    print("Mensagem de autenticacao", file=sys.stdout)
    api_key = request.headers.get('X-API-KEY')
    print(api_key)
    if api_key != API_KEY:

        return abort(401)
    else:
        
        return True
        

def validar_cliente(codClient):
    try:
        print("Entrou validar cliente")
        print("Entrou validar cliente", file=sys.stderr)
        # Conecta-se ao banco de dados
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Executa a consulta para verificar se o cliente existe
        cursor.execute("SELECT EXISTS(SELECT 1 FROM clientes WHERE codClient = ?)", (codClient,))
        exists = cursor.fetchone()[0]

        # Fecha a conexão com o banco de dados
        conn.close()

        return True if exists == 1 else False
    except Exception as e:
        print(f"Erro ao verificar cliente: {str(e)}")
        return False



# Registrar códigos return
def log_responses(response):
    status_code = response.status_code
    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE codigos_return SET x_vezes = x_vezes + 1 WHERE codigo = ?', (status_code,))
    conn.commit()
    conn.close()
    return response


@app.before_request
def before():
    print("teste before")


@app.after_request
def after_request(response):
    if request.path == '/novo_contato':
        last = last_client()
        if last:
            nome, numero = last
            # Iniciar a função em uma thread
            t = threading.Thread(target=send_whats(nome,numero))
            t.start()
          
            # Ações específicas para a rota '/novo_contato' aqui
            
    return log_responses(response)

# Rota para retornar a tabela codigos_return como JSON
@app.route('/codigos_return', methods=['GET'])
def get_codigos_return():
    conn = sqlite3.connect('openaai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM codigos_return')
    rows = cursor.fetchall()
    conn.close()

    # Criar um dicionário com os resultados
    data = [{'codigo': row[1], 'x_vezes': row[2]} for row in rows]
    return jsonify(data)



# Passar query
 
@app.route('/query', methods=['POST'])
def recebe_query():
    print("Mensagem de debug", file=sys.stdout)
    print("Mensagem de erro", file=sys.stderr)
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Obtenha a consulta SQL do corpo da solicitação (POST)
        query = request.get_data(as_text=True)
       
        print(f'Query = {query}',file=sys.stderr)
      
        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor() 
       
        # Execute a consulta SQL
        cursor.execute(query)
       
        # Se a consulta for uma consulta SELECT, você pode buscar os resultados
        if query.strip().lower().startswith("select"):
            data = cursor.fetchall()
            # Converta os resultados em uma lista de dicionários (caso necessário)
            results = [dict(zip([column[0] for column in cursor.description], row)) for row in data]
        else:
            results = None
       
        conn.commit()
        conn.close()
 
        # Envie os dados como resposta em formato JSON
        print(results)
        log_request(request, jsonify(
            {'message': results}))
        return jsonify(results), 200
 
    except Exception as e:
        return jsonify({"erro": "Erro ao processar a consulta", "mensagem": str(e)}), 400
 
 
# Função enviar todo o log
@app.route('/all_log', methods=['GET'])
def enviar_log():
    try:
        if not authenticate():
            log_request(request, jsonify({'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
            return abort(401)

        # Envia o arquivo log.txt para download
        return send_file('log.txt', as_attachment=True)

    except Exception as e:
        return jsonify({"erro": "Erro ao processar dados do log", "mensagem": str(e)}), 400




# Função enviar todo o banco de dados
@app.route('/backup', methods=['GET'])
def backup():
    try:
        if not authenticate():
            log_request(request, jsonify({'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
            return abort(401)

        # Envia o arquivo log.txt para download
        return send_file('openaai.db', as_attachment=True)

    except Exception as e:
        return jsonify({"erro": "Erro ao processar dados do banco de dados", "mensagem": str(e)}), 400




# Função enviar todo o banco de dados
@app.route('/all_db', methods=['GET'])
def enviar_db():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)

    try:
        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Execute uma consulta para obter os dados do banco de dados (substitua com sua própria consulta)
        cursor.execute("SELECT * FROM clientes")
        data = cursor.fetchall()

        # Converta os dados em uma lista de dicionários
        dados_json = []
        for row in data:
            dados_json.append({
                "index": row[0],
                "nome": row[1],
                "numero": row[2],
                "codClient": row[3],
                "ConfirmouWP": row[4],
                "ConfirmaEnvio": row[5],

                # Adicione mais colunas conforme necessário
            })

        # Feche a conexão com o banco de dados
        conn.close()
        payload = {
            'data': dados_json,
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # return jsonify({"mensagem": "Contagem de registros", "contador": contador}), 200

        return jsonify({"mensagem": "Dados do banco de dados", "key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao processar dados do banco de dados", "mensagem": str(e)}), 400


# Função criar
@app.route('/create_db', methods=['POST'])
def criar_db():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        db.criar_db_sqlite()
        db.criar_login()
        log_request(request, jsonify(
            {'message': 'Banco de dados Criado com Sucesso'}))
        payload = {
            'data': "Banco de dados criado com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        

        log_request(request, jsonify({'Payload': payload}))
        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao processar banco de dados", "mensagem": str(e)}), 400


# Cadastrar novo contato
@app.route('/novo_contato', methods=['POST'])
def novo_contato():
    global SECRET_KEY
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        
        # Recebe os dados JSON da solicitação POST
        dados = request.get_json()
        print(f"Dados = {dados}")

        # Extrai os campos necessários do JSON
        
        nome = dados['nome']
        numero = dados['numero']
        codClient = dados['codClient']
        ConfirmaEnvio = 1
        enviar = 1

        # Conecta-se ao banco de dados
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Executa a query SQL para inserir um novo cliente na tabela
        query = "INSERT INTO clientes ( nome, numero, codClient,  ConfirmaEnvio, enviar) VALUES ( ?, ?, ?, ?, ?)"
        cursor.execute(query, (nome, numero, codClient,
                        ConfirmaEnvio, enviar))

        # Comita a transação e fecha a conexão com o banco de dados
        conn.commit()
        conn.close()

        payload = {
            'data': "Cliente adicionado com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
       
        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Consulta pelo codClient
@app.route('/consultar_cliente/<int:cliente_id>', methods=['GET'])
def consulta(cliente_id):
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        # Corrigindo a consulta SQL para selecionar o cliente com base no ID
        query = "SELECT * FROM clientes WHERE codClient = ?"

        # Execute a consulta SQL
        cursor.execute(query, (cliente_id,))

        # Obtenha os resultados da consulta
        cliente = cursor.fetchone()

        conn.close()

        if cliente is None:
            return jsonify({'message': 'Cliente não encontrado'}), 404

        payload = {
            'data': "Cliente consultado com sucesso",
            'resultado': cliente,
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        log_request(request, jsonify({'Payload': payload}))
        return jsonify({"key": SECRET_KEY, "token": token, "cliente": cliente}), 200
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Remover pelo codigo xp
@app.route('/remove_registro', methods=['POST'])
def remove_registro():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        dados = request.get_data(as_text=True)
       # print(f'Remover = {dados}\nTipo de dado = {type(dados)}')
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = f"DELETE FROM clientes WHERE codClient = {dados}"
        # Execute a consulta SQL
        cursor.execute(query)
        conn.commit()
        conn.close()
        payload = {
            'data': "Cliente removido com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # return jsonify({"mensagem": "Contagem de registros", "contador": contador}), 200

        log_request(request, jsonify({'Payload': payload}))
        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400



# Remover pelo telefone
@app.route('/remove_telefone', methods=['POST'])
def remove_telefone():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        
        dados = request.get_data(as_text=True)
       # print(f'Remover = {dados}\nTipo de dado = {type(dados)}')
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = f"DELETE FROM clientes WHERE numero = {dados}"
        # Execute a consulta SQL
        cursor.execute(query)
        conn.commit()
        conn.close()
        payload = {
            'data': "Cliente removido com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # return jsonify({"mensagem": "Contagem de registros", "contador": contador}), 200

        log_request(request, jsonify({'Payload': payload}))
        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400



# Update pelo ID
@app.route('/update', methods=['POST'])
def update_id():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        dados = request.get_data(as_text=True)
        print(f'Remover = {dados}\nTipo de dado = {type(dados)}')
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = "UPDATE clientes SET nome = ?, numero = ?, ConfirmaEnvio = ? WHERE codClient = ?"
        # Execute a consulta SQL
        cursor.execute(query, (dados['nome'], dados['numero'],
                        dados['ConfirmaEnvio']))
        conn.commit()
        conn.close()
        payload = {
            'data': "Cliente atualizado com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        log_request(request, jsonify({'Payload': payload}))
        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Update confirma envio = Nao
@app.route('/confirma_envio', methods=['POST'])
def confirma_envio():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = "UPDATE Clientes SET ConfirmaEnvio = 'nao' WHERE ConfirmaEnvio = 'sim'"
        # Execute a consulta SQL
        cursor.execute(query)
        conn.commit()
        conn.close()
        payload = {
            'data': "Clientes adicionados com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        log_request(request, jsonify({'Payload': payload}))
        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Deleta TODOS os clientes
@app.route('/delete_clientes', methods=['POST'])
def delete_clientes():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = "DELETE FROM Clientes"
        # Execute a consulta SQL
        cursor.execute(query)
        conn.commit()
        conn.close()
        payload = {
            'data': "Clientes deletados com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Contar todos os clientes
@app.route('/contar_clientes', methods=['GET'])
def contar_clientes():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))

        return abort(401)
    try:
        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Execute uma consulta para obter os dados do banco de dados (substitua com sua própria consulta)
        cursor.execute("SELECT COUNT(*) FROM Clientes")
        # Recupere o valor do contador
        contador = cursor.fetchone()[0]

        # Feche a conexão com o banco de dados
        conn.close()
        payload = {
            'data': contador,
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify(contador), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao contar clientes", "mensagem": str(e)}), 400


# Retornar primeiro cliente com ConfirmaEnvio = não
@app.route('/confirmaEqualNao', methods=['GET'])
def confirmaEqualNao():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Execute uma consulta para obter os dados do banco de dados (substitua com sua própria consulta)
        cursor.execute(
            "SELECT * FROM Clientes WHERE ConfirmaEnvio = 'nao' ORDER BY id DESC LIMIT 1")
        # Recupere o valor do contador
        registro = cursor.fetchone()

        # Feche a conexão com o banco de dados
        conn.close()

        # Envie os dados como resposta em formato JSON
        if registro is None:
            payload = {
                'data': "Nenhum cliente encontrado",
                # tempo de expiração do token
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            log_request(request, jsonify({'Payload': payload}))

            return jsonify({"key": SECRET_KEY, "token": token}), 200

        payload = {
            'data': registro,
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ", "mensagem": str(e)}), 400

# Retronar todos os clientes com ENVIAR igual a 0
@app.route('/enviar_false', methods=['GET'])
def enviar_false():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Execute uma consulta para obter os dados do banco de dados (substitua com sua própria consulta)
        cursor.execute(
            "SELECT * FROM clientes WHERE enviar = 0")
        # Recupere o valor do contador
        registro = cursor.fetchall()

        # Feche a conexão com o banco de dados
        conn.close()

        # Envie os dados como resposta em formato JSON
        if registro is None:
            payload = {
                'data': "Nenhum cliente encontrado",
                # tempo de expiração do token
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            log_request(request, jsonify({'Payload': payload}))

            return jsonify({"key": SECRET_KEY, "token": token}), 200

        payload = {
            'data': registro,
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        return jsonify({"erro": "Erro", "mensagem": str(e)}), 400


# Retronar todos os clientes com ENVIAR igual a 1
@app.route('/enviar_true', methods=['GET'])
def enviar_true():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Execute uma consulta para obter os dados do banco de dados 
        cursor.execute(
            "SELECT * FROM clientes WHERE enviar = '1'")
        # Recupere o valor do contador
        registro = cursor.fetchall()

        # Feche a conexão com o banco de dados
        conn.close()

        # Envie os dados como resposta em formato JSON
        if registro is None:
            payload = {
                'data': "Nenhum cliente encontrado",
                # tempo de expiração do token
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            log_request(request, jsonify({'Payload': payload}))

            return jsonify({"key": SECRET_KEY, "token": token}), 200

        payload = {
            'data': registro,
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        return jsonify({"erro": "Erro", "mensagem": str(e)}), 400


# Cria um novo user

@app.route('/new_user', methods=['POST'])
def new_user():

    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Recebe os dados JSON da solicitação POST
        dados = request.get_json()
        print(f"Dados = {dados}")

        # Extrai os campos necessários do JSON

        email = dados['email']
        perfil = dados['perfil']
        senha = dados['senha']
        token = dados['token']

        # Conecta-se ao banco de dados
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Executa a query SQL para inserir um novo usuário na tabela
        query = "INSERT INTO users (email, perfil,senha, token) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (email, perfil, senha, token))

        # Comita a transação e fecha a conexão com o banco de dados
        conn.commit()
        conn.close()
        payload = {
            'data': "User adicionado com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Remover usuário pelo email
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        dados = request.get_data(as_text=True)
       # print(f'Remover = {dados}\nTipo de dado = {type(dados)}')
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = f"DELETE FROM users WHERE email = '{dados}'"
        print(query)
        # Execute a consulta SQL
        cursor.execute(query)
        conn.commit()
        conn.close()
        payload = {
            'data': "User removido com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Alterar senha do usuário pelo email
@app.route('/update_password', methods=['POST'])
def update_password():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Recebe o email e a nova senha do usuário a ser atualizada no corpo da solicitação POST
        data = request.get_json()
        email = data['email']
        new_password = data['new_password']

        # Conecta-se ao banco de dados
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Executa a query SQL para atualizar a senha do usuário com base no email
        query = "UPDATE users SET senha = ? WHERE email = ?"
        cursor.execute(query, (new_password, email))

        # Comita a transação e fecha a conexão com o banco de dados
        conn.commit()
        conn.close()
        payload = {
            'data': "Senha atualizada com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400



# Alterar enviar para 0 
@app.route('/desabilita_cliente',methods = ['POST'])
def desabilita():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Recebe o email e a nova senha do usuário a ser atualizada no corpo da solicitação POST
        data = request.get_json()
        codClient = data['codClient']
        # Verifique se o cliente existe
        if not validar_cliente(codClient):
            payload = {
            'data': "Cliente nao encontrado",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
             }
            log_request(request, jsonify({'Payload': payload}))
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({"key": SECRET_KEY, "token": token,}), 200
           

        # Conecta-se ao banco de dados
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Executa a query SQL 
        query = f"UPDATE clientes SET enviar = 0 WHERE codClient = '{codClient}'"

        #cursor.execute(query, (codClient))
        cursor.execute(query)
        print(f'Executando query = {query}' )
        # Comita a transação e fecha a conexão com o banco de dados
        conn.commit()
        conn.close()
        payload = {
            'data': "Cliente desabilitado com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token,}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Alterar enviar para 1
@app.route('/habilita_cliente',methods = ['POST'])
def habilita():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Recebe o email e a nova senha do usuário a ser atualizada no corpo da solicitação POST
        data = request.get_json()
        codClient = data['codClient']
        # Verifique se o cliente existe
        if not validar_cliente(codClient):
            payload = {
            'data': "Cliente nao encontrado",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
             }
            log_request(request, jsonify({'Payload': payload}))
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({"key": SECRET_KEY, "token": token,}), 200
           

        # Conecta-se ao banco de dados
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Executa a query SQL 
        query = f"UPDATE clientes SET enviar = 1 WHERE codClient = '{codClient}'"

        #cursor.execute(query, (codClient))
        cursor.execute(query)
        print(f'Executando query = {query}' )
        # Comita a transação e fecha a conexão com o banco de dados
        conn.commit()
        conn.close()
        payload = {
            'data': "Cliente habilitado com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token,}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400




# Alterar token do usuário
@app.route('/update_token', methods=['POST'])
def update_token():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        # Recebe o email e o novo token do usuário a ser atualizado no corpo da solicitação POST
        data = request.get_json()
        email = data['email']
        new_token = data['new_token']

        # Conecta-se ao banco de dados
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Executa a query SQL para atualizar o token do usuário com base no email
        query = "UPDATE users SET token = ? WHERE email = ?"
        cursor.execute(query, (new_token, email))

        # Comita a transação e fecha a conexão com o banco de dados
        conn.commit()
        conn.close()
        payload = {
            'data': "Token atualizado com sucesso",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400





@app.route('/')
def index():
    return render_template('index.html')

# Rota para servir os arquivos estáticos do React


@app.route('/static/js/<path:filename>')
def serve_static_js(filename):
    return send_from_directory('static/js', filename)

# Rota para servir os arquivos CSS


@app.route('/static/css/<path:filename>')
def serve_static_css(filename):
    return send_from_directory('static/css', filename)



# Conferir API online

@app.route('/status', methods=['GET'])
def enviar_status():
    if not authenticate():
        log_request(request, jsonify(
            {'message': 'REQUISIÇÃO NÃO AUTENTICADA!'}))
        return abort(401)
    try:
        payload = {
            'data': "API online.", "GPT": "Status - OK",
            # tempo de expiração do token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        log_request(request, jsonify({'Payload': payload}))
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"key": SECRET_KEY, "token": token}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao acessar dados", "Error": str(e)}), 400

# Rota para verificar as credenciais


@app.route("/verificar_numero", methods=["POST"])
def verificar_numero():
    if not authenticate():
        return abort(401)
    try:
        # Obter os dados JSON enviados na solicitação
        data = request.get_json()
        numero = data.get("numero")
    

        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect("openaai.db")
        cursor = conn.cursor()

        # Execute uma consulta para verificar as credenciais (substitua com sua própria consulta)
        cursor.execute(
            f'SELECT * FROM clientes WHERE numero = {numero}'
        )
        usuario = cursor.fetchone()   
    
        # Feche a conexão com o banco de dados
        conn.close()

        if usuario:
            # Credenciais corretas, gera um token JWT
            payload = {
                # Assume que o primeiro campo é o ID do usuário
                "usuario": usuario[0],
                "numero": numero,
                "token": usuario[4],
                # tempo de expiração do token
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            log_request(request, jsonify({'Payload': payload}))

            return jsonify(payload), 200
        else:
            log_request(request, jsonify({'Payload': payload}))
            return jsonify(payload), 401

    except Exception as e:
        return (
            jsonify(
                {"erro": "Erro ao verificar as credenciais", "mensagem": str(e)}),
            500,
        )



# Verificar credenciais de users para api whats
@app.route("/verificar_credenciais", methods=["POST"])
def verificar_credenciais():
    if not authenticate():
        return abort(401)
    try:
        # Obter os dados JSON enviados na solicitação
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")

        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect("openaai.db")
        cursor = conn.cursor()

        # Execute uma consulta para verificar as credenciais (substitua com sua própria consulta)
        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND senha = ? ", (email, senha)
        )
        usuario = cursor.fetchone()
    
        # Feche a conexão com o banco de dados
        conn.close()

        if usuario:
            # Credenciais corretas, gera um token JWT
            payload = {
                # Assume que o primeiro campo é o ID do usuário
                "usuario": usuario[0],
                "email": email,
                "token": usuario[4],
                # tempo de expiração do token
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            log_request(request, jsonify({'Payload': payload}))

            return jsonify({"key": SECRET_KEY, "mensagem": "Credenciais corretas", "token": token}), 200
        else:
            log_request(request, jsonify({'Payload': payload}))
            return jsonify({"mensagem": "Credenciais incorretas"}), 401

    except Exception as e:
        return (
            jsonify(
                {"erro": "Erro ao verificar as credenciais", "mensagem": str(e)}),
            500,
        )

# Verificar credenciais dashboard API
@app.route("/verificar_credenciais_dash", methods=["POST"])
def verificar_credenciais_dash():
    if not authenticate():
        return abort(401)
    try:
        print("Entrou try dash", file=sys.stderr)
        # Obter os dados JSON enviados na solicitação
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")

        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect("openaai.db")
        cursor = conn.cursor()

        # Execute uma consulta para verificar as credenciais (substitua com sua própria consulta)
        cursor.execute(
            "SELECT * FROM painel WHERE email = ? AND senha = ? ", (email, senha)
        )
        usuario = cursor.fetchone()
       
    
        # Feche a conexão com o banco de dados
        conn.close()

        if usuario:
            # Credenciais corretas, gera um token JWT 
            payload = {
                # Assume que o primeiro campo é o ID do usuário
                "usuario": usuario[0],
                "email": email,
                "token": usuario[4],
                # tempo de expiração do token
                #"exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            
            log_request(request, jsonify({'Payload': payload}))
            
            return jsonify({"key": SECRET_KEY, "mensagem": "Credenciais corretas", "token": token}), 200
        else:
            log_request(request, jsonify({'Payload': payload}))
            return jsonify({"mensagem": "Credenciais incorretas"}), 401

    except Exception as e:
        return (
            jsonify(
                {"erro": "Erro ao verificar as credenciais", "mensagem": str(e)}),
            500,
        )

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
