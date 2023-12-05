import schedule
import time



def backup():
    print("executando backup")

def finetuning():
    print("Executando finetuning")

def email():
    print("Enviando email")




def tarefa():
    # Aqui você coloca a função que quer automatizar
    print("Executando tarefa...")

# Agendando a tarefa para rodar a cada minuto
schedule.every().minute.do(tarefa)
schedule.every().second.do(backup)
schedule.every().second.do(finetuning)
schedule.every().second.do(email)



# Loop para que o agendador execute as tarefas
while True:
    schedule.run_pending()
    time.sleep(1)  # Verifica a cada segundo se há tarefas agendadas para rodar
