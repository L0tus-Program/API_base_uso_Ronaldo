# Documentação da API

## Introdução

Este projeto consiste em uma API criada com o Flask que permite gerenciar dados de clientes em um banco de dados SQLite. A API oferece várias funcionalidades, como adicionar novos clientes, consultar dados do banco de dados, atualizar informações de clientes e muito mais.

## Requisitos

- Python 3.x
- Flask
- Outras bibliotecas (listadas em requirements.txt)

## Instalação

1. Clone o repositório:

   git clone https://github.com/seurepositorio/seuprojeto.git

2. Navegue até o diretório do projeto:

   cd seuprojeto

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

A API estará disponível em http://localhost:5000.

# Endpoints

- /all_db (GET): Retorna todos os dados do banco de dados.
- /query (POST): Envie uma consulta SQL personalizada e receba os resultados.
- /create_db (POST): Crie o banco de dados e tabelas.
- /novo_contato (POST): Adicione um novo cliente ao banco de dados.
- /remove_registro (POST): Remova um cliente pelo ID.
- /update (POST): Atualize informações do cliente pelo ID.
- /confirma_envio (POST): Atualize todos os registros com ConfirmaEnvio "sim" para "não".
- /delete_clientes (POST): Exclua todos os registros de clientes.
- /contar_clientes (GET): Contagem total de registros de clientes.
- /confirmaEqualNao (GET): Retorne o primeiro cliente com ConfirmaEnvio "não".

## Contribuindo

Sinta-se à vontade para contribuir para este projeto. Você pode abrir problemas, enviar solicitações de pull e melhorar a documentação.
