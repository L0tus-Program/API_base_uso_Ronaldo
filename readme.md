# Documentação da API

## Ultimas implementações

- Criptografia dos dados enviados no JSOn de resposta, utilizando JWT
- Criptografia da chave JWT com base em Cifra de Cesar

## Introdução

Este projeto consiste em uma API criada com o Flask que permite gerenciar dados de clientes em um banco de dados SQLite. A API oferece várias funcionalidades, como adicionar novos clientes, consultar dados do banco de dados, atualizar informações de clientes e muito mais.

## Primeira execução

Para primeira execução, não esqueça de utilizar o endpoint /create_db para criar o banco de dados SQLITE.
Também não esqueça de configurar uma chave para a sua API no src.json

## Requisitos

- Python 3.x
- Flask
- Flask-cors
- SQLITE 3
- JWT
  

Todas as bibliotecas externas serão acrescentadas também ao requirements.txt

## Instalação

1. Clone o repositório:

   git clone https://github.com/L0tus-Program/API_base_uso_Ronaldo

2. Navegue até o diretório do projeto:

   cd API_base_uso_Ronaldo

3. Crie um ambiente virtual (opcional, mas recomendado):

   python -m venv venv

4. Ative o ambiente virtual (Linux/macOS):

   source venv/bin/activate

   Ou no Windows:

   venv\Scripts\activate

5. Instale as dependências:

   pip install -r requirements.txt

Uso

# Iniciar o servidor

Para iniciar o servidor da API, execute o seguinte comando:

python api.py

A API estará disponível em http://localhost:5000. OU outro ip/porta que você definir.

# Endpoints

- /codigos_return (GET): Retorna a tabela codigos_return como JSON.
- /query (POST): Recebe e executa consultas SQL personalizadas.
- /all_log (GET): Retorna todo o log armazenado no arquivo log.txt.
- /all_db (GET): Retorna todos os dados do banco de dados.
- /create_db (POST): Cria o banco de dados e tabelas.
- /novo_contato (POST): Adiciona um novo cliente ao banco de dados.
- /consultar_cliente/<cliente_id> (GET): Consulta um cliente pelo ID.
- /remove_registro (POST): Remove um cliente pelo ID.
- /remove_telefone (POST): Remove um cliente pelo telefone.
- /update (POST): Atualiza informações do cliente pelo ID.
- /update_password (POST): Atualiza a senha de um usuário pelo email.
- /update_token (POST): Atualiza o token de um usuário pelo email.
- /new_user (POST): Cria um novo usuário.
- /delete_user (POST): Remove um usuário pelo email.
- /confirma_envio (POST): Atualiza todos os registros com ConfirmaEnvio "sim" para "não".
- /delete_clientes (POST): Exclui todos os registros de clientes.
- /contar_clientes (GET): Contagem total de registros de clientes.
- /confirmaEqualNao (GET): Retorna o primeiro cliente com ConfirmaEnvio "não".
- /enviar_false (GET): Retorna todos os clientes com enviar igual a 1.
- /desabilita_cliente (POST): Altera o valor de enviar para 0 de um cliente.
  
## Contribuindo

Sinta-se à vontade para contribuir para este projeto. Você pode abrir problemas, enviar solicitações de pull e melhorar a documentação.


## Possíveis implementações

- Flask-Login -> Para melhor gerenciamento de logins em seções -> https://flask-login.readthedocs.io/en/latest/
- Flask-RESTful -> Para melhor organização das requisições -> https://flask-restful.readthedocs.io/en/latest/
- Implementar função de backup do banco de dados por e-mail
- Criar tabela de dados para chave da API
