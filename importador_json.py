
import json
from pathlib import Path

STATUS_VALIDOS = {"Rascunho", "Em revisão", "Aprovado"}

CAMPOS_OBRIGATORIOS = {
    "id_conteudo",
    "titulo",
    "descricao",
    "texto",
    "status",
    "fonte_texto",
    "arquivos_dados",
}


def importar_json(caminho):
    """Lê e valida conteúdos de um arquivo JSON."""
    caminho = Path(caminho)

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, dict):
        raise ValueError("O JSON deve conter um objeto.")

    projeto = dados.get("projeto")

    if not isinstance(projeto, dict):
        raise ValueError("Projeto inválido.")

    id_projeto = projeto.get("id_projeto")

    if not isinstance(id_projeto, str) or not id_projeto.strip():
        raise ValueError("Identificador do projeto inválido.")

    conteudos = dados.get("conteudos")

    if not isinstance(conteudos, list):
        raise ValueError("A lista de conteúdos é obrigatória.")

    identificadores = set()

    for indice, conteudo in enumerate(conteudos, start=1):
        if not isinstance(conteudo, dict):
            raise ValueError(f"Conteúdo {indice} inválido.")

        campos_ausentes = CAMPOS_OBRIGATORIOS - conteudo.keys()

        if campos_ausentes:
            raise ValueError(
                f"Conteúdo {indice}: campos ausentes: "
                f"{sorted(campos_ausentes)}"
            )

        for campo in (
            "id_conteudo",
            "titulo",
            "descricao",
            "texto",
            "status",
            "fonte_texto",
        ):
            if not isinstance(conteudo[campo], str):
                raise ValueError(
                    f"Conteúdo {indice}: {campo} deve ser texto."
                )

        identificador = conteudo["id_conteudo"].strip()

        if not identificador or not conteudo["titulo"].strip():
            raise ValueError(
                f"Conteúdo {indice}: ID e título são obrigatórios."
            )

        if identificador in identificadores:
            raise ValueError(
                f"Identificador duplicado: {identificador}"
            )

        identificadores.add(identificador)

        if conteudo["status"] not in STATUS_VALIDOS:
            raise ValueError(
                f"Conteúdo {indice}: status inválido."
            )

        arquivos = conteudo["arquivos_dados"]

        if not isinstance(arquivos, list) or not all(
            isinstance(nome, str) and nome.strip()
            for nome in arquivos
        ):
            raise ValueError(
                f"Conteúdo {indice}: arquivos_dados inválido."
            )

    return dados


if __name__ == "__main__":
    dados = importar_json("modelo_conteudo.json")

    print("JSON validado com sucesso!")
    print("Projeto:", dados["projeto"]["id_projeto"])
    print("Conteúdos:", len(dados["conteudos"]))
