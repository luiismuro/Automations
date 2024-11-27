import threading

def tarefa(nome):
    print(f"Iniciando a tarefa {nome}")
    for i in range(5):
        print(f"Tarefa {nome}: {i}")

# Criando threads
thread1 = threading.Thread(target=tarefa, args=("A",))
thread2 = threading.Thread(target=tarefa, args=("B",))

# Iniciando as threads
thread1.start()
thread2.start()

# Aguardando as threads terminarem
thread1.join()
thread2.join()
print("Tarefas concluídas!")
