import json
import os

TAREFAS = "tarefas.json"


def carregar_tarefas():
    if not os.path.exists(TAREFAS):
        with open(TAREFAS, "w") as arquivo:
            json.dump([], arquivo)

    with open(TAREFAS, "r") as arquivo:
        try:
            return json.load(arquivo)
        except:
            return []


def salvar_tarefas(tarefas):
    with open(TAREFAS, "w") as arquivo:
        json.dump(tarefas, arquivo, indent=4)


def adicionar_tarefa(usuario):
    tarefas = carregar_tarefas()

    print("----- Criar Tarefa -----")
    titulo = input("Digite o título da tarefa: ")
    desc = input("Digite a descrição da tarefa: ")

    nova_tarefa = {
        "usuario": usuario["login"],
        "titulo": titulo,
        "descricao": desc,
        "concluida": False
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print("Tarefa adicionada com sucesso!")


def listar_tarefas(usuario):
    tarefas = carregar_tarefas()

    print("----- Minhas Tarefas -----")
    encontrou = False
    for tarefa in tarefas:
        if usuario["cargo"] == "admin" or tarefa["usuario"] == usuario["login"]:
            encontrou = True
            status = "Concluída" if tarefa["concluida"] else "Pendente"
            print(f"\nUsuário: {tarefa['usuario']}")
            print(f"Título: {tarefa['titulo']}")
            print(f"Descrição: {tarefa['descricao']}")
            print(f"Status: {status}")
    if not encontrou:
        print("Nenhuma tarefa encontrada.")


def concluir_tarefa(usuario):
    tarefas = carregar_tarefas()

    print("----- Concluir Tarefa -----")
    titulo = input("Título da tarefa a concluir: ")

    for tarefa in tarefas:
        if tarefa["usuario"] == usuario["login"] and tarefa["titulo"] == titulo:
            tarefa["concluida"] = True
            salvar_tarefas(tarefas)
            print("Tarefa concluída!")
            return

    print("Tarefa não encontrada ou sem permissão.")


def menu_tarefas(usuario):
    while True:
        print("\n----- Menu de Tarefas -----")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Concluir Tarefa")
        print("4. Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_tarefa(usuario)
        elif opcao == "2":
            listar_tarefas(usuario)
        elif opcao == "3":
            concluir_tarefa(usuario)
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")
