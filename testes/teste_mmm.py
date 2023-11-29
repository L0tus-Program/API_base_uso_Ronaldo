import smtplib
from email.mime.text import MIMEText



def mail():
    try:
        print("Entrando na função mail")
            # Dados de autenticação
        username = "felipe@ladodefora.site"
        password = "Flg@1999"
        emailDestino = "felipe.gomes@messeminvestimentos.com.br"
        conteudo = "Erro com a APi"
        # Criação do objeto MIMEText
        msg = MIMEText(conteudo, 'plain', 'utf-8') # é necessário codificar o objeto para utf-8 para poder enviar acentos
        msg['To'] = emailDestino
        msg['From'] = username
        msg['Subject'] = "Erro com a API"

        # Adicionando cabeçalhos de conteúdo
        msg.add_header('Content-Type', 'text/plain; charset=UTF-8')

        """# Enviando o e-mail
        with smtplib.SMTP("email-ssl.com.br", 587) as server: #587 465
            print("Entrou no servidor")
            server.starttls()
            server.login(username, password)
            server.sendmail(username, emailDestino, msg.as_string())"""
        
        # Enviando o e-mail usando SMTP_SSL
        with smtplib.SMTP_SSL("email-ssl.com.br", 465) as server:
            server.login(username, password)
            server.sendmail(username, emailDestino, msg.as_string())

        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")



mail()