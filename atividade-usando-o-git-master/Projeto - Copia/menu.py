import usuarios
import tarefas
import relatorios


def menu_principal():
    while True:
        print("\n===== SISTEMA TASKFLOW =====")
        print("1 - Menu de Usuário (login / cadastro)")
        print("2 - Menu de Tarefas")
        print("3 - Relatórios")
        print("4 - Sair")

        opc = input("Escolha: ").strip()

        if opc == "1":
            usuarios.menu_usuarios()

        elif opc == "2":
            usuario = usuarios.obter_usuario_logado_dict()
            if not usuario:
                print("Nenhum usuário logado. Faça login primeiro.")
            else:
                tarefas.menu_tarefas(usuario)

        elif opc == "3":
            relatorios.menu_relatorios()

        elif opc == "4":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()
