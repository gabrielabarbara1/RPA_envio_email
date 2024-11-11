import smtplib
import email.message
import mysql.connector
from datetime import datetime

# Configurar as informações de conexão com o banco de dados
config = {
    'user': 'usuario',
    'password': 'senha',
    'host': 'host',
    'database': 'database'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

query = """
SELECT c.email, c.razao, cc.data_ativacao, cc.id_filial 
from cliente_contrato cc 
left join cliente c on c.id = cc.id_cliente
WHERE cc.id_filial = 17
"""

# Executar a consulta SQL
cursor.execute(query)
result = cursor.fetchall()

data = datetime.now().strftime("%d-%m-%Y")

try:
    with open(f"/home/Log_email/envio_email_bbg_{data}.log", "a") as arquivo:
        for row in result:
            cliente_nome = row[1]

            with open("texto_email.html", "r") as f:
                corpo_email = f.read().replace("{cliente_nome}", cliente_nome)

            msg = email.message.EmailMessage()
            msg['Subject'] = "Assunto"
            msg['From'] = "Nome que é pra mostrar aqui <no-reply@teste.com.br>"
            msg['To'] = row[0]
            password = 'senha'
            msg.set_content(corpo_email, subtype='html')

            # Conectando ao servidor de e-mail via SMTP SSL
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                # Login Credentials for sending the mail
                s.login('no-reply@teste.com.br', password)
                s.send_message(msg)

            print(f'Email enviado: {row[0]}')
            arquivo.write(f"E-mail enviado para {row[0]}\n")
except Exception as e:
    print("Erro ao abrir arquivo")
    print(e)

cursor.close()
conn.close()