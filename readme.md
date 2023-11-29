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

/codigos_return (GET): Retorna a tabela codigos_return como JSON, possivelmente para análise de status de respostas.

- /query (POST): Recebe e executa uma consulta SQL personalizada.
- /all_log (GET): Envia todo o log registrado, provavelmente como um arquivo para download.
- /backup (GET): Envia um backup do banco de dados, presumivelmente para fins de recuperação ou análise.
- /all_db (GET): Retorna todos os dados do banco de dados, semelhante ao endpoint anterior.
- /create_db (POST): Cria o banco de dados e suas tabelas.
- /novo_contato (POST): Adiciona um novo cliente ao banco de dados.
- /consultar_cliente/int:cliente_id (GET): Consulta informações de um cliente pelo seu ID.
- /remove_registro (POST): Remove um registro de cliente pelo ID.
- /remove_telefone (POST): Remove um registro de cliente pelo número de telefone.
- /update (POST): Atualiza informações do cliente pelo ID.
- /confirma_envio (POST): Atualiza registros de clientes para indicar a confirmação de envio.
- /delete_clientes (POST): Deleta todos os registros de clientes.
- /contar_clientes (GET): Retorna a contagem total de clientes.
- /confirmaEqualNao (GET): Retorna o primeiro cliente com ConfirmaEnvio igual a "não".
- /enviar_false (GET) e /enviar_true (GET): Retornam clientes com o campo enviar configurado como 0 ou 1, respectivamente.
- /new_user (POST): Cria um novo usuário.
- /delete_user (POST): Remove um usuário pelo email.
- /update_password (POST): Atualiza a senha de um usuário pelo email.
- /update_token (POST): Atualiza o token de um usuário pelo email.
- /desabilita_cliente (POST) e /habilita_cliente (POST): Alteram o status de envio de um cliente para 0 ou 1.
- /status (GET): Verifica o status da API, indicando se está online.
- /verificar_numero (POST), /verificar_credenciais (POST), /verificar_credenciais_dash (POST): Validam as credenciais de clientes ou usuários, cada um para um propósito específico (número de telefone, usuários da API do WhatsApp, e painel de controle, respectivamente).
  
## Contribuindo

Sinta-se à vontade para contribuir para este projeto. Você pode abrir problemas, enviar solicitações de pull e melhorar a documentação.



## Possíveis implementações

- Flask-Login -> Para melhor gerenciamento de logins em seções -> https://flask-login.readthedocs.io/en/latest/
- Flask-RESTful -> Para melhor organização das requisições -> https://flask-restful.readthedocs.io/en/latest/
- Implementar função de backup do banco de dados por e-mail
- Criar tabela de dados para chave da API
- Configurar IP permitido para acessar a rota de log e backup
- Melhor utilização de before e after request



# A fazer

- Terminar de criar a tabela de lista de espera
- Try exception na evolution verificando sua disponibilidade
  - Em caso de erro, ficar verificando. Quando a API voltar enviar a mensagem de boas vindas para os clientes que estão em lista de espera
  - Após cada envio, remover o cliente da tabela