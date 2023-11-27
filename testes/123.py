import smtplib
from email.mime.text import MIMEText


print("Entrando na função mail")
    # Dados de autenticação
username = "openaai@conexaoia.digital"
password = "Messem@2023"
emailDestino = "felipe.gomes@messeminvestimentos.com.br"
conteudo = "Erro com a APi"
# Criação do objeto MIMEText
msg = MIMEText(conteudo, 'plain', 'utf-8') # é necessário codificar o objeto para utf-8 para poder enviar acentos
msg['To'] = emailDestino
msg['From'] = username
msg['Subject'] = "Erro com a API"

# Adicionando cabeçalhos de conteúdo
msg.add_header('Content-Type', 'text/plain; charset=UTF-8')

# Enviando o e-mail
with smtplib.SMTP("smtp.hostinger.com", 465) as server:
    server.starttls()
    server.login(username, password)
    server.sendmail(username, emailDestino, msg.as_string())

print("E-mail enviado com sucesso!")