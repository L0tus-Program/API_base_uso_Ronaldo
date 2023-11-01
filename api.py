from flask import Flask, request, jsonify, abort
import db
import sqlite3
import json 

# Abra o arquivo JSON
with open('src.json', 'r') as file:
    src = json.load(file)


# key API
API_KEY = str(src['key'])

# Outras configurações do aplicativo
DEBUG = True
ENV = 'development'
HOST = 'localhost'
PORT = 5000

# Criando aplicação
app = Flask(__name__)

# Autenticação
def authenticate():
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:
        return abort(401)
    print("Autenticado")
    return True




# Função enviar todo o banco de dados
@app.route('/all_db', methods=['GET'])
def enviar_db():
    if not authenticate():
        return abort(401)

    try:
        # Conecte-se ao banco de dados SQLite 
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Execute uma consulta para obter os dados do banco de dados (substitua com sua própria consulta)
        cursor.execute("SELECT * FROM Clientes")
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

        # Envie os dados como resposta em formato JSON
        return jsonify({"mensagem": "Dados do banco de dados", "dados": dados_json}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao processar dados do banco de dados", "mensagem": str(e)}), 400

# Passar query
@app.route('/query', methods=['POST'])
def recebe_query():
    if not authenticate():
        return abort(401)
    try:
        # Obtenha a consulta SQL do corpo da solicitação (POST)
        query = request.get_data(as_text=True)
        
        print(f'Query = {query}')
        
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
        return jsonify(results), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao processar a consulta", "mensagem": str(e)}), 400



# Função criar 
@app.route('/create_db',methods=['POST'] )
def criar_db():
    if not authenticate():
        return abort(401)
    try:
        db.criar_db_sqlite()
        db.criar_login()
        return jsonify({"mensagem": "Banco de dados Criado com Sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao processar banco de dados", "mensagem": str(e)}), 400




# Cadastrar novo contato
@app.route('/novo_contato', methods=['POST'])
def novo_contato():
    if not authenticate():
        return abort(401)
    try:
        # Recebe os dados JSON da solicitação POST
        dados = request.get_json()
        print(f"Dados = {dados}")

        # Extrai os campos necessários do JSON
        id = dados['id']
        nome = dados['nome']
        numero = dados['numero']
        codClient = dados['codClient']
        ConfirmouWP = dados['ConfirmouWP']
        ConfirmaEnvio = dados['ConfirmaEnvio']
        enviar = dados['enviar']

        # Conecta-se ao banco de dados
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Executa a query SQL para inserir um novo cliente na tabela
        query = "INSERT INTO clientes (id, nome, numero, codClient, ConfirmouWP, ConfirmaEnvio, enviar) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (id, nome, numero, codClient, ConfirmouWP, ConfirmaEnvio, enviar))

        # Comita a transação e fecha a conexão com o banco de dados
        conn.commit()
        conn.close()

        # Retorna uma resposta de sucesso
        return jsonify({'message': 'Cliente adicionado com sucesso'}), 201

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400




# Remover pelo ID
@app.route('/remove_registro', methods=['POST'])
def remove_registro():
    if not authenticate():
        return abort(401)
    try:
        dados = request.get_data(as_text=True)
       # print(f'Remover = {dados}\nTipo de dado = {type(dados)}')
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = f"DELETE FROM clientes WHERE id = {dados}"
        # Execute a consulta SQL
        cursor.execute(query)
        conn.commit()
        conn.close()
        
        # Retorna uma resposta de sucesso
        return jsonify({'message': 'Cliente removido com sucesso'}), 201
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400




# Update pelo ID

@app.route('/update', methods = ['POST'])
def update_id():
    if not authenticate():
        return abort(401)
    try:
        dados = request.get_data(as_text=True)
        print(f'Remover = {dados}\nTipo de dado = {type(dados)}')
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = "UPDATE clientes SET nome = ?, numero = ?, ConfirmouWP = ?, ConfirmaEnvio = ? WHERE id = ?"
        # Execute a consulta SQL
        cursor.execute(query,(dados['nome'], dados['numero'], dados['ConfirmouWP'], dados['ConfirmaEnvio'], dados['id']))
        conn.commit()
        conn.close()
        
        # Retorna uma resposta de sucesso
        return jsonify({'message': 'Cliente atualizado com sucesso'}), 201
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400






# Update confirma envio = Nao
@app.route('/confirma_envio', methods = ['POST'])
def confirma_envio():
    if not authenticate():
        return abort(401)
    try:
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = "UPDATE Clientes SET ConfirmaEnvio = 'nao' WHERE ConfirmaEnvio = 'sim'"
        # Execute a consulta SQL
        cursor.execute(query)
        conn.commit()
        conn.close()
        
        # Retorna uma resposta de sucesso
        return jsonify({'message': 'Clientes atualizados com sucesso'}), 201
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400







# Deleta TODOS os clientes
@app.route('/delete_clientes', methods = ['POST'])
def delete_clientes():
    if not authenticate():
        return abort(401)
    try:
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()
        query = "DELETE FROM Clientes"
        # Execute a consulta SQL
        cursor.execute(query)
        conn.commit()
        conn.close()
        
        # Retorna uma resposta de sucesso
        return jsonify({'message': 'Clientes deletados com sucesso'}), 201
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400




# Contar todos os clientes
@app.route('/contar_clientes', methods = ['GET'])
def contar_clientes():
    if not authenticate():
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

        # Envie os dados como resposta em formato JSON
        return jsonify({"mensagem": "Contagem de registros", "contador": contador}), 200


    except Exception as e:
        return jsonify({"erro": "Erro ao contar clientes", "mensagem": str(e)}), 400



# Retornar primeiro cliente com ConfirmaEnvio = não
@app.route('/confirmaEqualNao', methods = ['GET'])
def confirmaEqualNao():
    if not authenticate():
        return abort(401)
    try:
        # Conecte-se ao banco de dados SQLite 
        conn = sqlite3.connect('openaai.db')
        cursor = conn.cursor()

        # Execute uma consulta para obter os dados do banco de dados (substitua com sua própria consulta)
        cursor.execute("SELECT * FROM Clientes WHERE ConfirmaEnvio = 'nao' ORDER BY id DESC LIMIT 1")
        # Recupere o valor do contador
        registro = cursor.fetchone()

        # Feche a conexão com o banco de dados
        conn.close()

        # Envie os dados como resposta em formato JSON
        if registro is None:
            return jsonify({"mensagem": "Nenhum cliente encontrado!", "registro": registro}), 200

        return jsonify({"mensagem": "Contagem de registros", "registro": registro}), 200


    except Exception as e:
        return jsonify({"erro": "Erro ao contar clientes", "mensagem": str(e)}), 400




#Cria um novo user

@app.route('/new_user', methods = ['POST'])
def new_user():
    if not authenticate():
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
        cursor.execute(query, (email, perfil,senha, token))

        # Comita a transação e fecha a conexão com o banco de dados
        conn.commit()
        conn.close()

        # Retorna uma resposta de sucesso
        return jsonify({'message': 'User adicionado com sucesso'}), 201

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400



# Remover usuário pelo email
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if not authenticate():
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
        
        # Retorna uma resposta de sucesso
        return jsonify({'message': 'User removido com sucesso'}), 201
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Alterar senha do usuário pelo email
@app.route('/update_password', methods=['POST'])
def update_password():
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

        # Retorna uma resposta de sucesso
        return jsonify({'message': 'Senha atualizada com sucesso'}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400


# Alterar token do usuário
@app.route('/update_token', methods=['POST'])
def update_token():
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

        # Retorna uma resposta de sucesso
        return jsonify({'message': 'Token atualizado com sucesso'}), 200

    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({'error': str(e)}), 400








# Conferir API online

@app.route('/', methods=['GET'])
def enviar_status():
    if not authenticate():
        return abort(401)
    try:
        return jsonify({"mensagem": "API online.", "GPT": "Status - OK"}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao acessar dados"}), 400







if __name__ == '__main__':
    app.run(debug=True)



