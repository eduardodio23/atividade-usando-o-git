import json
import os


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")



ARQUIVO_USUARIOS = "usuarios.json"
usuario_logado = None


def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump({}, f)

    try:
        with open(ARQUIVO_USUARIOS, "r") as f:
            usuarios = json.load(f)
    except json.JSONDecodeError:
        usuarios = {}

        # Garantir que exista um usuário admin padrão
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
    if not nome:
        print("O nome não pode ser vazio.")
        return
    if any(char.isdigit() for char in nome):
        print("O nome não pode conter números.")
        return

    email = input("E-mail: ").strip()
    if "@" not in email or "." not in email:
        print("E-mail inválido.")
        return
    if email in usuarios:
        print("Este e-mail já está cadastrado.")
        return

    login = input("Login: ").strip()
    if not login:
        print("O login não pode ser vazio.")
        return
    if login in usuarios:
        print("Este login já existe.")
        return

    senha = input("Senha: ").strip()
    if len(senha) < 4:
        print("A senha deve ter pelo menos 4 caracteres.")
        return

    cargo = input("Cargo (admin/user): ").lower().strip()
    if cargo not in ["admin", "user"]:
        print("Cargo inválido.")
        return

    usuarios[login] = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cargo": cargo
    }

    salvar_usuarios(usuarios)
    print("Usuário cadastrado com sucesso!")


def excluir_usuario():
    usuarios = carregar_usuarios()
    
    for u in usuarios:
      print(f"- {u}")

    login = input("Digite o login do usuário a ser excluído: ")

    if login not in usuarios:
        print("Usuário não encontrado.")
        return

    del usuarios[login]
    salvar_usuarios(usuarios)
    print(f"Usuário '{login}' excluído com sucesso.")


def menu_usuarios():
    global usuario_logado

    while True:
        limpar_tela()
        usuarios_dict = carregar_usuarios()
        cargo = usuarios_dict[usuario_logado]["cargo"] if usuario_logado else None

        print("\n===== MENU USUÁRIO =====")
        print(f"Usuário logado: {usuario_logado if usuario_logado else 'Nenhum'}")
        print("1 - Login")
        print("2 - Encerrar sessão")
        print("3 - Sair do menu de usuário")

        if cargo == "admin":
            print("4 - Cadastrar usuário")
            print("5 - Listar usuários cadastrados")
            print("6 - Excluir usuário")

        print("========================")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            autenticar()
            input("\nPressione ENTER para continuar...")

        elif opcao == "2":
            limpar_tela()
            encerrar_sessao()
            input("\nPressione ENTER para continuar...")

        elif opcao == "3":
            print("Saindo do menu de usuário...")
            break

        elif opcao == "4":
            if cargo == "admin":
                limpar_tela()
                cadastrar_usuario()
            else:
                print("Apenas administradores podem acessar essa opção.")
            input("\nPressione ENTER para continuar...")

        elif opcao == "5":
            if cargo == "admin":
                limpar_tela()
                print("\nUsuários cadastrados:")
                for u in usuarios_dict:
                    print(f"- {u}")
            else:
                print("Apenas administradores podem acessar essa opção.")
            input("\nPressione ENTER para continuar...")

        elif opcao == "6":
            if cargo == "admin":
                limpar_tela()
                print("\n--- EXCLUSÃO DE USUÁRIO ---")
                
                excluir_usuario()
            else:
                print("Apenas administradores podem acessar essa opção.")
            input("\nPressione ENTER para continuar...")

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")
