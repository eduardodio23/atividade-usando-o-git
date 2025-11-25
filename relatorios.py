from datetime import datetime, date
import os

import usuarios
import tarefas

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

CAMINHO_PASTA_RELATORIOS = "relatorios"


def _garantir_pasta_relatorios():
    if not os.path.exists(CAMINHO_PASTA_RELATORIOS):
        os.makedirs(CAMINHO_PASTA_RELATORIOS, exist_ok=True)


# =========== INTEGRAÇÕES ===========

def obter_usuario_logado_dict():
    return usuarios.obter_usuario_logado_dict()


def usuario_atual_eh_admin() -> bool:
    usuario = obter_usuario_logado_dict()
    if not usuario:
        return False
    return usuario.get("cargo") == "admin"


def carregar_tarefas_sistema():
    return tarefas.carregar_tarefas()


# ========== FILTRAGENS ===========

def filtrar_tarefas_concluidas(lista_tarefas: list) -> list:
    return [t for t in lista_tarefas if t.get("concluida") is True]


def filtrar_tarefas_pendentes(lista_tarefas: list) -> list:
    return [t for t in lista_tarefas if not t.get("concluida")]


def filtrar_tarefas_por_usuario(lista_tarefas: list, login_usuario: str) -> list:
    return [t for t in lista_tarefas if t.get("usuario") == login_usuario]


def obter_lista_usuarios_pelas_tarefas(lista_tarefas: list) -> list:
    logins = sorted({t.get("usuario") for t in lista_tarefas if t.get("usuario")})
    return logins


# =========== FORMATAÇÃO TEXTO ===========

def _formatar_tarefa_texto(tarefa: dict, mostrar_usuario: bool = False) -> str:
    status = "Concluída" if tarefa.get("concluida") else "Pendente"

    base = (
        f"Título: {tarefa.get('titulo')}\n"
        f"Descrição: {tarefa.get('descricao', '')}\n"
        f"Status: {status}\n"
    )

    if mostrar_usuario:
        base += f"Usuário: {tarefa.get('usuario', '-')}\n"

    base += "----------------------------------------\n"
    return base


def gerar_relatorio_texto(tarefas_lista: list, titulo_relatorio: str, mostrar_usuario: bool = False) -> str:
    data_hoje = date.today().strftime("%d/%m/%Y")
    linha_titulo = f"===== {titulo_relatorio} ====="
    linhas = [
        linha_titulo,
        f"Data de emissão: {data_hoje}",
        f"Total de tarefas: {len(tarefas_lista)}",
        ""
    ]

    for t in tarefas_lista:
        linhas.append(_formatar_tarefa_texto(t, mostrar_usuario=mostrar_usuario))

    return "\n".join(linhas)


# =========== EXPORTAÇÃO TXT ===========

def exportar_relatorio_txt(nome_arquivo: str, conteudo: str) -> str:
    _garantir_pasta_relatorios()

    caminho = os.path.join(CAMINHO_PASTA_RELATORIOS, nome_arquivo)

    if not caminho.lower().endswith(".txt"):
        caminho += ".txt"

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

    return caminho


# =========== GERAÇÃO + EXPORTAÇÃO ===========

def gerar_e_exportar_relatorio_concluidas(lista_tarefas: list, sufixo_nome, mostrar_usuario: bool = False) -> str:
    tarefas_filtradas = filtrar_tarefas_concluidas(lista_tarefas)
    titulo = f"Relatório de Pendencias de Tarefas do Usuário: {sufixo_nome}"
    conteudo = gerar_relatorio_texto(
        tarefas_filtradas,
        titulo,
        mostrar_usuario
    )

    data_hoje = date.today().strftime("%d-%m-%Y")
    nome_arquivo = f"relatorio_concluidas_{data_hoje}{sufixo_nome}.txt"
    return exportar_relatorio_txt(nome_arquivo, conteudo)


def gerar_e_exportar_relatorio_pendentes(lista_tarefas: list, sufixo_nome, mostrar_usuario: bool = False) -> str:
    tarefas_filtradas = filtrar_tarefas_pendentes(lista_tarefas)
    titulo = f"Relatório de Pendencias de Tarefas do Usuário: {sufixo_nome}"
    conteudo = gerar_relatorio_texto(
        tarefas_filtradas,
        titulo,
        mostrar_usuario
    )

    data_hoje = date.today().strftime("%d-%m-%Y")
    nome_arquivo = f"relatorio_pendentes_{data_hoje}_{sufixo_nome}.txt"
    return exportar_relatorio_txt(nome_arquivo, conteudo)

def gerar_e_exportar_relatorio_geral_usuario(lista_tarefas: list, sufixo_nome, mostrar_usuario: bool = False) -> str:
    # filtra só as tarefas desse usuário
    tarefas_usuario = filtrar_tarefas_por_usuario(lista_tarefas, sufixo_nome)

    titulo = f"Relatório Geral de Tarefas do Usuário: {sufixo_nome}"
    conteudo = gerar_relatorio_texto(
        tarefas_usuario,
        titulo,
        mostrar_usuario
    )

    data_hoje = date.today().strftime("%d-%m-%Y")
    nome_arquivo = f"relatorio_geral_{sufixo_nome}_{data_hoje}.txt"
    return exportar_relatorio_txt(nome_arquivo, conteudo)


# =========== MENU RELATÓRIOS ===========

def menu_relatorios():
    usuario = obter_usuario_logado_dict()
    if not usuario:
        print("Nenhum usuário logado. Faça login antes de acessar relatórios.")
        return

    eh_admin = usuario_atual_eh_admin()

    while True:
        lista_tarefas = carregar_tarefas_sistema()

        limpar_tela()
        print("\n===== MENU DE RELATÓRIOS =====")
        print(f"Usuário logado: {usuario['login']} ({usuario['cargo']})")

        if eh_admin:
            print("1 - Relatório GERAL - tarefas concluídas (TODOS usuários)")
            print("2 - Relatório GERAL - tarefas pendentes (TODOS usuários)")
            print("3 - Relatório POR USUÁRIO (escolher um usuário)")
            print("4 - MEU relatório GERAL (todas as MINHAS tarefas)")
            print("0 - Voltar")
        else:
            print("1 - Minhas tarefas concluídas")
            print("2 - Minhas tarefas pendentes")
            print("3 - Meu relatório GERAL (todas as minhas tarefas)")
            print("0 - Voltar")

        opc = input("Escolha uma opção: ").strip()

        if opc == "0":
            break

        if eh_admin:
            if opc == "1":
                limpar_tela()
                caminho = gerar_e_exportar_relatorio_concluidas(
                    lista_tarefas, mostrar_usuario=True, sufixo_nome="_geral"
                )
                print(f"\nRelatório gerado em: {caminho}")
                input("\nPressione ENTER para continuar...")

            elif opc == "2":
                limpar_tela()
                caminho = gerar_e_exportar_relatorio_pendentes(
                    lista_tarefas, mostrar_usuario=True, sufixo_nome="_geral"
                )
                print(f"\nRelatório gerado em: {caminho}")
                input("\nPressione ENTER para continuar...")

            elif opc == "3":
                limpar_tela()
                logins = obter_lista_usuarios_pelas_tarefas(lista_tarefas)
                if not logins:
                    print("Não há tarefas cadastradas para nenhum usuário.")
                    input("\nPressione ENTER para continuar...")
                    continue

                print("\nUsuários com tarefas:")
                for idx, login in enumerate(logins, start=1):
                    print(f"{idx} - {login}")

                escolha = input("Escolha o usuário pelo número: ").strip()
                if not escolha.isdigit() or not (1 <= int(escolha) <= len(logins)):
                    print("Opção inválida.")
                    input("\nPressione ENTER para continuar...")
                    continue

                usuario_escolhido = logins[int(escolha) - 1]

                print("\n1 - Tarefas concluídas")
                print("2 - Tarefas pendentes")
                print("3 - Relatório GERAL desse usuário (todas as tarefas)")

                tipo_rel = input("Escolha o tipo de relatório: ").strip()
                tarefas_usuario = filtrar_tarefas_por_usuario(lista_tarefas, usuario_escolhido)
                sufixo = f"_{usuario_escolhido}"

                limpar_tela()
                if tipo_rel == "1":
                    caminho = gerar_e_exportar_relatorio_concluidas(
                        tarefas_usuario, mostrar_usuario=True, sufixo_nome=sufixo
                    )
                elif tipo_rel == "2":
                    caminho = gerar_e_exportar_relatorio_pendentes(
                        tarefas_usuario, mostrar_usuario=True, sufixo_nome=sufixo
                    )
                elif tipo_rel == "3":
                    caminho = gerar_e_exportar_relatorio_geral_usuario(
                        lista_tarefas, usuario_escolhido, mostrar_usuario=True
                    )
                else:
                    print("Opção inválida.")
                    input("\nPressione ENTER para continuar...")
                    continue

                print(f"\nRelatório gerado em: {caminho}")
                input("\nPressione ENTER para continuar...")

            elif opc == "4":
                limpar_tela()
                
                caminho = gerar_e_exportar_relatorio_geral_usuario(
                    lista_tarefas, usuario["login"], mostrar_usuario=False
                )
                print(f"\nRelatório gerado em: {caminho}")
                input("\nPressione ENTER para continuar...")

            else:
                print("Opção inválida.")
                input("\nPressione ENTER para continuar...")

        # USUÁRIO NORMAL
        else:
            minhas_tarefas = filtrar_tarefas_por_usuario(lista_tarefas, usuario["login"])

            if opc == "1":
                limpar_tela()
                caminho = gerar_e_exportar_relatorio_concluidas(
                    minhas_tarefas, mostrar_usuario=False, sufixo_nome=f"_{usuario['login']}"
                )
                print(f"\nRelatório gerado em: {caminho}")
                input("\nPressione ENTER para continuar...")

            elif opc == "2":
                limpar_tela()
                caminho = gerar_e_exportar_relatorio_pendentes(
                    minhas_tarefas, mostrar_usuario=False, sufixo_nome=f"_{usuario['login']}"
                )
                print(f"\nRelatório gerado em: {caminho}")
                input("\nPressione ENTER para continuar...")

            elif opc == "3":
                limpar_tela()
                caminho = gerar_e_exportar_relatorio_geral_usuario(
                    lista_tarefas, usuario["login"], mostrar_usuario=False
                )
                print(f"\nRelatório gerado em: {caminho}")
                input("\nPressione ENTER para continuar...")

            else:
                print("Opção inválida.")
                input("\nPressione ENTER para continuar...")