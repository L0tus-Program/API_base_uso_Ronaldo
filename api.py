from flask import Flask, request, jsonify, abort
import db
import sqlite3
"""
# Chave apenas temporaria
API_KEY = 'Messem@2023'"""

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
    """if api_key != API_KEY:
        return abort(401)"""
    print("Autenticado")
    return True

# Atualizar linha -> Fazer ainda
@app.route('/update_line', methods=['POST'])
def receber_json():
    if not authenticate():
        return abort(401)

    try:
        dados_json = request.get_json()
        print("Recebendo JSON \nInvocando DB")
        fine(dados_json)  # Invocando integração OPENAI
        return jsonify({"mensagem": "JSON recebido com sucesso", "dados": dados_json}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao processar JSON", "mensagem": str(e)}), 400
    


# Função enviar todo o banco de dados
@app.route('/all_db', methods=['GET'])
def enviar_db():
    """if not authenticate():
        return abort(401)"""

    try:
        # Conecte-se ao banco de dados SQLite 
        conn = sqlite3.connect('clientes.db')
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
    try:
        # Obtenha a consulta SQL do corpo da solicitação (POST)
        query = request.get_data(as_text=True)
        
        print(f'Query = {query}')
        
        # Conecte-se ao banco de dados SQLite 
        conn = sqlite3.connect('clientes.db')
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
        db.verifica()
        return jsonify({"mensagem": "Banco de dados Criado com Sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao processar banco de dados", "mensagem": str(e)}), 400






@app.route('/', methods=['GET'])
def enviar_status():
    try:
        return jsonify({"mensagem": "API online.", "GPT": "Status fine - OK"}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao acessar dados"}), 400







if __name__ == '__main__':
    app.run(debug=True)




