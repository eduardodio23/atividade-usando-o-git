import os
import usuarios
import tarefas
import relatorios

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def menu_principal():
    while True:
        usuario = usuarios.obter_usuario_logado_dict()

        if not usuario:
            limpar_tela()
            print("\n===== SISTEMA TASKFLOW =====")
            print("Nenhum usuário logado.")
            print("1 - Login")
            print("2 - Sair do sistema")

            opc = input("Escolha: ").strip()

            if opc == "1":
                limpar_tela()
                usuarios.autenticar()
                input("\nPressione ENTER para continuar...")
            elif opc == "2":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida.")
                input("\nPressione ENTER para continuar...")

        else:
            limpar_tela()
            print("\n===== SISTEMA TASKFLOW =====")
            print(f"Usuário logado: {usuario['login']} ({usuario['cargo']})")
            print("1 - Menu de Tarefas")
            print("2 - Relatórios")
            print("3 - Encerrar sessão")
            print("4 - Sair do sistema")

            
            if usuario["cargo"] == "admin":
                print("5 - Cadastrar usuário")
                print("6 - Listar usuários cadastrados")
                print("7 - Excluir usuário")

            print("========================")
            opc = input("Escolha: ").strip()

            # opções comuns
            if opc == "1":
                limpar_tela()
                tarefas.menu_tarefas(usuario)
                input("\nPressione ENTER para continuar...")

            elif opc == "2":
                limpar_tela()
                relatorios.menu_relatorios()
                input("\nPressione ENTER para continuar...")

            elif opc == "3":
                limpar_tela()
                usuarios.encerrar_sessao()
                input("\nPressione ENTER para continuar...")

            elif opc == "4":
                print("Saindo do sistema...")
                break

            # opções exclusivas de admin
            elif opc == "5" and usuario["cargo"] == "admin":
                limpar_tela()
                usuarios.cadastrar_usuario()
                input("\nPressione ENTER para continuar...")

            elif opc == "6" and usuario["cargo"] == "admin":
                
                print("\nUsuários cadastrados:")
                usuarios_dict = usuarios.carregar_usuarios()
                for u in usuarios_dict:
                    print(f"- {u}")
            
                input("\nPressione ENTER para continuar...")

            elif opc == "7" and usuario["cargo"] == "admin":
                limpar_tela()
                usuarios.excluir_usuario()
                input("\nPressione ENTER para continuar...")

            else:
                print("Opção inválida!")
                input("\nPressione ENTER para continuar...")
if __name__ == "__main__": 
    menu_principal()