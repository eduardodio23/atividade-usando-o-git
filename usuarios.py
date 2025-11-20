import json
import os

ARQUIVO_USUARIOS = "usuarios.json"
usuario_logado = None # Variável global para armazenar o usuário logado


def carregar_usuarios():
   
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump({}, f)

    try:
        with open(ARQUIVO_USUARIOS, "r") as f:
            usuarios = json.load(f)
    except json.JSONDecodeError:
        usuarios = {}

   
    if "admin" not in usuarios:
        usuarios["admin"] = {
            "nome": "Administrador",
            "email": "admin@sistema.com",
            "senha": "1234",
            "cargo": "admin"
        }
        salvar_usuarios(usuarios)

    return usuarios


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)


def cadastrar_usuario():
    usuarios = carregar_usuarios()

    print("\n--- CADASTRO DE USUÁRIO ---")
    nome = input("Nome: ").strip()
    if not nome:
        print("O nome não pode ser vazio.")
        return cadastrar_usuario()
    email = input("E-mail: ").strip()
    if not "@" in email:
        print("E-mail inválido.")
        return cadastrar_usuario()
    login = input("Login: ").strip()
    if not login:
        print("O login não pode ser vazio.")
        return cadastrar_usuario()
    senha = int(input("Senha (números apenas): ").strip())
    if not senha:
        print("A senha não pode ser vazia.")
        return cadastrar_usuario()
    cargo = input("Cargo (admin/user): ").lower().strip()

    if not nome or not email or not login or not senha:
        print("Todos os campos devem ser preenchidos.")
        return

    if login in usuarios:
        print("Este login já existe.")
        return

    usuarios[login] = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cargo": cargo
    }

    salvar_usuarios(usuarios)
    print("Usuário cadastrado com sucesso!")


def autenticar():
    global usuario_logado
    usuarios = carregar_usuarios()

    print("\n--- LOGIN ---")
    login = input("Login: ").lower()
    senha = int(input("Senha: "))

    if login in usuarios and usuarios[login]["senha"] == senha:
        usuario_logado = login
        print(f"Bem-vindo, {usuarios[login]['nome']}!")
    else:
        print("Login ou senha incorretos.")

def excluir_usuario():
    global usuario_logado
    usuarios = carregar_usuarios()

    print("\n--- EXCLUSÃO DE USUÁRIO ---")
    login = input("Login do usuário a excluir: ").strip()

    if login not in usuarios:
        print("Usuário não encontrado.")
        return
    if login == "admin":
        print("Não é possível excluir o usuário administrador.")
        return
    if usuarios[login]["cargo"] == "admin":
        print("Você não pode excluir outro administrador.")
        return
    if login == usuario_logado:
        print("Você não pode excluir sua própria conta enquanto está logado.")
        return
    if login in usuario_logado:
        print("Este usuário está logado no momento e não pode ser excluído.")
        return

   
    confirmacao = input(f"Tem certeza que deseja excluir o usuário '{login}'? (s/n): ").lower().strip()
    if confirmacao != "s":
        print("Operação cancelada.")
        return

    del usuarios[login]
    salvar_usuarios(usuarios)

    print(f"Usuário '{login}' excluído com sucesso!")

def encerrar_sessao():
    global usuario_logado
    if usuario_logado:
        print(f"Usuário '{usuario_logado}' deslogado com sucesso.")
        usuario_logado = None
    else:
        print("Nenhum usuário está logado.")

def menu():
    global usuario_logado

    while True:
        usuarios = carregar_usuarios()

        cargo = usuarios[usuario_logado]["cargo"] if usuario_logado else None

        print("\n===== MENU USUÁRIO =====")
        print("1 - Login")
        print("2 - Encerrar sessão")
        print("3 - Sair")

        if cargo == "admin":
            print("4 - Cadastrar usuário")
            print("5 - Listar usuários cadastrados")
            print("6 - Excluir usuário")

        print("========================")

        opcao = input("Escolha: ")

        if opcao == "1":
            autenticar()

        elif opcao == "2":
            encerrar_sessao()

        elif opcao == "3":
            print("Saindo...")
            break

        elif opcao == "4":
            if cargo == "admin":
                cadastrar_usuario()
            else:
                print("Apenas administradores podem acessar essa opção.")

        elif opcao == "5":
            if cargo == "admin":
                print("\nUsuários cadastrados:")
                for u in usuarios:
                    print(f"- {u}")
            else:
                print("Apenas administradores podem acessar essa opção.")
        
        elif opcao == "6":
            if cargo == "admin":
                excluir_usuario()
            else:
                print("Apenas administradores podem acessar essa opção.")

        else:
            print("Opção inválida!")


menu()
