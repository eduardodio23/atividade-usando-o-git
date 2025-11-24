from datetime import datetime, date
import os

import usuarios
import tarefas

CAMINHO_PASTA_RELATORIOS = "relatorios"


def _garantir_pasta_relatorios():
    if not os.path.exists(CAMINHO_PASTA_RELATORIOS):
        os.makedirs(CAMINHO_PASTA_RELATORIOS, exist_ok=True)


# =========== AUX USUÁRIO / TAREFAS ===========

def obter_usuario_logado_dict():
    return usuarios.obter_usuario_logado_dict()


def usuario_atual_eh_admin() -> bool:
    usuario = obter_usuario_logado_dict()
    if not usuario:
        return False
    return usuario.get("cargo") == "admin"


def carregar_tarefas_sistema():
    return tarefas.carregar_tarefas()


# =========== FILTROS ===========

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
    linha_titulo = f"===== {titulo_relatorio} ====="
    linhas = [linha_titulo, f"Total de tarefas: {len(tarefas_lista)}", ""]

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

def gerar_e_exportar_relatorio_concluidas(lista_tarefas: list, mostrar_usuario: bool = False, sufixo_nome: str = "") -> str:
    tarefas_filtradas = filtrar_tarefas_concluidas(lista_tarefas)
    conteudo = gerar_relatorio_texto(tarefas_filtradas, "Relatório de Tarefas Concluídas", mostrar_usuario)
    nome_arquivo = f"relatorio_concluidas{sufixo_nome}.txt"
    return exportar_relatorio_txt(nome_arquivo, conteudo)


def gerar_e_exportar_relatorio_pendentes(lista_tarefas: list, mostrar_usuario: bool = False, sufixo_nome: str = "") -> str:
    tarefas_filtradas = filtrar_tarefas_pendentes(lista_tarefas)
    conteudo = gerar_relatorio_texto(tarefas_filtradas, "Relatório de Tarefas Pendentes", mostrar_usuario)
    nome_arquivo = f"relatorio_pendentes{sufixo_nome}.txt"
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

        print("\n===== MENU DE RELATÓRIOS =====")
        print(f"Usuário logado: {usuario['login']} ({usuario['cargo']})")

        if eh_admin:
            print("1 - Relatório GERAL - tarefas concluídas")
            print("2 - Relatório GERAL - tarefas pendentes")
            print("3 - Relatório POR USUÁRIO")
            print("0 - Voltar")
        else:
            print("1 - Minhas tarefas concluídas")
            print("2 - Minhas tarefas pendentes")
            print("0 - Voltar")

        opc = input("Escolha uma opção: ").strip()

        if opc == "0":
            break

        # ADMIN
        if eh_admin:
            if opc == "1":
                caminho = gerar_e_exportar_relatorio_concluidas(
                    lista_tarefas, mostrar_usuario=True, sufixo_nome="_geral"
                )
                print(f"\nRelatório gerado em: {caminho}")

            elif opc == "2":
                caminho = gerar_e_exportar_relatorio_pendentes(
                    lista_tarefas, mostrar_usuario=True, sufixo_nome="_geral"
                )
                print(f"\nRelatório gerado em: {caminho}")

            elif opc == "3":
                logins = obter_lista_usuarios_pelas_tarefas(lista_tarefas)
                if not logins:
                    print("Não há tarefas cadastradas para nenhum usuário.")
                    continue

                print("\nUsuários com tarefas:")
                for idx, login in enumerate(logins, start=1):
                    print(f"{idx} - {login}")

                escolha = input("Escolha o usuário pelo número: ").strip()
                if not escolha.isdigit() or not (1 <= int(escolha) <= len(logins)):
                    print("Opção inválida.")
                    continue

                usuario_escolhido = logins[int(escolha) - 1]
                tarefas_usuario = filtrar_tarefas_por_usuario(lista_tarefas, usuario_escolhido)

                print("\n1 - Tarefas concluídas")
                print("2 - Tarefas pendentes")
                tipo_rel = input("Escolha o tipo de relatório: ").strip()

                sufixo = f"_{usuario_escolhido}"

                if tipo_rel == "1":
                    caminho = gerar_e_exportar_relatorio_concluidas(
                        tarefas_usuario, mostrar_usuario=True, sufixo_nome=sufixo
                    )
                elif tipo_rel == "2":
                    caminho = gerar_e_exportar_relatorio_pendentes(
                        tarefas_usuario, mostrar_usuario=True, sufixo_nome=sufixo
                    )
                else:
                    print("Opção inválida.")
                    continue

                print(f"\nRelatório gerado em: {caminho}")
            else:
                print("Opção inválida.")

        # USUÁRIO NORMAL
        else:
            minhas_tarefas = filtrar_tarefas_por_usuario(lista_tarefas, usuario["login"])

            if opc == "1":
                caminho = gerar_e_exportar_relatorio_concluidas(
                    minhas_tarefas, mostrar_usuario=False, sufixo_nome=f"_{usuario['login']}"
                )
                print(f"\nRelatório gerado em: {caminho}")

            elif opc == "2":
                caminho = gerar_e_exportar_relatorio_pendentes(
                    minhas_tarefas, mostrar_usuario=False, sufixo_nome=f"_{usuario['login']}"
                )
                print(f"\nRelatório gerado em: {caminho}")

            else:
                print("Opção inválida.")
