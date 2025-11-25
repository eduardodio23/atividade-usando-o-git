from datetime import datetime
import json
import os
import usuarios

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
    

TAREFAS = "tarefas.json"


def carregar_tarefas():
    if not os.path.exists(TAREFAS):
        with open(TAREFAS, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, ensure_ascii=False, indent=4)

    with open(TAREFAS, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []


def salvar_tarefas(tarefas):
    with open(TAREFAS, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=4)


def adicionar_tarefa(usuario):
    tarefas = carregar_tarefas()

    print("----- Criar Tarefa -----")
    titulo = input("Digite o título da tarefa: ").strip()
    desc = input("Digite a descrição da tarefa: ").strip()
    

    if not titulo:
        print("Título não pode ser vazio.")
        return

    # data/hora da criação da tarefa
    agora = datetime.now()
    data_criacao = agora.strftime("%d/%m/%Y")
    hora_criacao = agora.strftime("%H:%M")

    nova_tarefa = {
        "usuario": usuario["login"],
        "titulo": titulo,
        "descricao": desc,
        "concluida": False,
        "data_criacao": data_criacao,
        "hora_criacao": hora_criacao
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print("Tarefa adicionada com sucesso!")


def excluir_tarefa(usuario):
    tarefas = carregar_tarefas()

    if not tarefas:
        print("Não há tarefas para excluir.")
        return

    print("----- Excluir Tarefa -----")
    titulo = input("Digite o título exato da tarefa a ser excluída: ").strip()

    for tarefa in tarefas:
        # admin pode excluir qualquer tarefa, usuário só as dele
        if (usuario["cargo"] == "admin" or tarefa["usuario"] == usuario["login"]) and tarefa["titulo"] == titulo:
            tarefas.remove(tarefa)
            salvar_tarefas(tarefas)
            print("Tarefa excluída com sucesso!")
            return

    print("Tarefa não encontrada ou você não tem permissão.")


def editar_tarefa(usuario):
    tarefas = carregar_tarefas()

    if not tarefas:
        print("Não há tarefas para editar.")
        return

    print("----- Editar Tarefa -----")
    titulo = input("Digite o título da tarefa que deseja editar: ").strip()

    for tarefa in tarefas:
        # admin pode editar qualquer tarefa, usuário só as dele
        if (usuario["cargo"] == "admin" or tarefa["usuario"] == usuario["login"]) and tarefa["titulo"] == titulo:
            print("\nTarefa encontrada:")
            print(f"Título atual: {tarefa['titulo']}")
            print(f"Descrição atual: {tarefa['descricao']}")
            print(f"Status atual: {'Concluída' if tarefa['concluida'] else 'Pendente'}")

            novo_titulo = input("Novo título (deixe vazio para manter): ").strip()
            nova_desc = input("Nova descrição (deixe vazio para manter): ").strip()

            if novo_titulo:
                tarefa["titulo"] = novo_titulo
            if nova_desc:
                tarefa["descricao"] = nova_desc

            salvar_tarefas(tarefas)
            print("Tarefa atualizada com sucesso!")
            return

    print("Tarefa não encontrada ou você não tem permissão.")

def adicionar_tarefa_para_usuario_admin(admin):
    if admin["cargo"] != "admin":
        print("Apenas administradores podem usar esta opção.")
        return

    tarefas = carregar_tarefas()
    usuarios_dict = usuarios.carregar_usuarios()

    if not usuarios_dict:
        print("Não há usuários cadastrados.")
        return

    print("----- Criar Tarefa para Usuário -----")
    print("Usuários disponíveis:")
    for login in usuarios_dict:
        print(f"- {login}")

    login_destino = input("Digite o login do usuário que receberá a tarefa: ").strip()

    if login_destino not in usuarios_dict:
        print("Usuário não encontrado.")
        return

    titulo = input("Digite o título da tarefa: ").strip()
    desc = input("Digite a descrição da tarefa: ").strip()

    if not titulo:
        print("Título não pode ser vazio.")
        return

    agora = datetime.now()
    data_criacao = agora.strftime("%d/%m/%Y")
    hora_criacao = agora.strftime("%H:%M")

    nova_tarefa = {
        "usuario": login_destino,
        "titulo": titulo,
        "descricao": desc,
        "concluida": False,
        "data_criacao": data_criacao,
        "hora_criacao": hora_criacao
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print(f"Tarefa adicionada com sucesso para o usuário '{login_destino}'!")

def listar_tarefas(usuario):
    tarefas = carregar_tarefas()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    print("----- Minhas Tarefas -----")
    encontrou = False
    for tarefa in tarefas:
        if usuario["cargo"] == "admin" or tarefa["usuario"] == usuario["login"]:
            encontrou = True
            status = "Concluída" if tarefa["concluida"] else "Pendente"
            print("\n----------------------------")
            print(f"Usuário: {tarefa['usuario']}")
            print(f"Título: {tarefa['titulo']}")
            print(f"Descrição: {tarefa['descricao']}")
            print(f"Status: {status}")

            # data/hora de criação
            if "data_criacao" in tarefa and "hora_criacao" in tarefa:
                print(f"Criada em: {tarefa['data_criacao']} às {tarefa['hora_criacao']}")

            # data/hora de conclusão (se já concluída)
            if tarefa.get("concluida") and "data_conclusao" in tarefa and "hora_conclusao" in tarefa:
                print(f"Concluída em: {tarefa['data_conclusao']} às {tarefa['hora_conclusao']}")

    if not encontrou:
        print("Nenhuma tarefa encontrada.")

def concluir_tarefa(usuario):
    tarefas = carregar_tarefas()

    if not tarefas:
        print("Não há tarefas para concluir.")
        return

    print("----- Concluir Tarefa -----")
    titulo = input("Título da tarefa a concluir: ").strip()

    for tarefa in tarefas:
        # admin pode concluir qualquer tarefa, usuário só as dele
        if ((usuario["cargo"] == "admin") or (tarefa["usuario"] == usuario["login"])) and tarefa["titulo"] == titulo:
            if tarefa.get("concluida"):
                print("Essa tarefa já está concluída.")
                return

            tarefa["concluida"] = True

            agora = datetime.now()
            tarefa["data_conclusao"] = agora.strftime("%d/%m/%Y")
            tarefa["hora_conclusao"] = agora.strftime("%H:%M")

            salvar_tarefas(tarefas)
            print("Tarefa concluída!")
            return

    print("Tarefa não encontrada ou sem permissão.")

def menu_tarefas(usuario):
    while True:
        limpar_tela()
        print("\n----- Menu de Tarefas -----")
        print("1. Adicionar Tarefa (para mim)")
        print("2. Listar Tarefas")
        print("3. Concluir Tarefa")
        print("4. Editar Tarefa")
        print("5. Excluir Tarefa")

        if usuario["cargo"] == "admin":
            print("6. Adicionar Tarefa para outro usuário")

        print("0. Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            adicionar_tarefa(usuario)
            input("\nPressione ENTER para continuar...")

        elif opcao == "2":
            limpar_tela()
            listar_tarefas(usuario)
            input("\nPressione ENTER para continuar...")

        elif opcao == "3":
            limpar_tela()
            concluir_tarefa(usuario)
            input("\nPressione ENTER para continuar...")

        elif opcao == "4":
            limpar_tela()
            editar_tarefa(usuario)
            input("\nPressione ENTER para continuar...")

        elif opcao == "5":
            limpar_tela()
            excluir_tarefa(usuario)
            input("\nPressione ENTER para continuar...")

        elif opcao == "6" and usuario["cargo"] == "admin":
            limpar_tela()
            adicionar_tarefa_para_usuario_admin(usuario)
            input("\nPressione ENTER para continuar...")

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")