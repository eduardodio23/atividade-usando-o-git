import json
import os

def garantir_diretorio(caminho_arquivo: str) -> None:
    """Garante que a pasta do arquivo exista."""
    pasta = os.path.dirname(caminho_arquivo)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)


def salvar_json(caminho_arquivo: str, dados) -> None:
    """
    Salva os dados em um arquivo JSON.
    """
    garantir_diretorio(caminho_arquivo)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def ler_json(caminho_arquivo: str, padrao=None):
   
    if padrao is None:
        padrao = []

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return padrao
    except json.JSONDecodeError:
        return padrao
