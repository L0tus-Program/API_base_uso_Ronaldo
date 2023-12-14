from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
CORS(app)


def authenticate():
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:

        return abort(401)
    else:

        return True


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


@app.route('/chorume',methods=['GET'])
def retorna_chorume():
    chorume ="junior"
    try:
        if chorume == 'junior':
            return jsonify({"Mensagem":"Junior fudido"}),200
        
    except Exception as e:
        return jsonify({"Erro":e}),400



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)