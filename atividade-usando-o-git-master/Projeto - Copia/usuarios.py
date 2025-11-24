import json
import os

ARQUIVO_USUARIOS = "usuarios.json"
usuario_logado = None  # login do usuário logado (string)


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


def obter_usuario_logado_dict():
   

    global usuario_logado
    if usuario_logado is None:
        return None

    usuarios = carregar_usuarios()

    if usuario_logado not in usuarios:
        return None

    dados = usuarios[usuario_logado].copy()
    dados["login"] = usuario_logado
    return dados


def autenticar():
    global usuario_logado
    usuarios = carregar_usuarios()

    print("\n--- LOGIN ---")
    login = input("Login: ")
    senha = input("Senha: ")

    if login in usuarios and usuarios[login]["senha"] == senha:
        usuario_logado = login
        print(f"Bem-vindo, {usuarios[login]['nome']}!")
    else:
        print("Login ou senha incorretos.")


def encerrar_sessao():
    global usuario_logado
    usuario_logado = None
    print("Sessão encerrada.")


def cadastrar_usuario():
    usuarios = carregar_usuarios()

    print("\n--- CADASTRO DE USUÁRIO ---")
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip()
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
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


def menu_usuarios():
    global usuario_logado

    while True:
        usuarios_dict = carregar_usuarios()
        cargo = usuarios_dict[usuario_logado]["cargo"] if usuario_logado else None

        print("\n===== MENU USUÁRIO =====")
        print("1 - Login")
        print("2 - Encerrar sessão")
        print("3 - Sair do menu de usuário")

        if cargo == "admin":
            print("4 - Cadastrar usuário")
            print("5 - Listar usuários cadastrados")

        print("========================")

        opcao = input("Escolha: ")

        if opcao == "1":
            autenticar()

        elif opcao == "2":
            encerrar_sessao()

        elif opcao == "3":
            print("Saindo do menu de usuário...")
            break

        elif opcao == "4":
            if cargo == "admin":
                cadastrar_usuario()
            else:
                print("Apenas administradores podem acessar essa opção.")

        elif opcao == "5":
            if cargo == "admin":
                print("\nUsuários cadastrados:")
                for u in usuarios_dict:
                    print(f"- {u}")
            else:
                print("Apenas administradores podem acessar essa opção.")

        else:
            print("Opção inválida!")
