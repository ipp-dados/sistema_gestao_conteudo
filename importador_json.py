
import json
from pathlib import Path


# Status permitidos no sistema.
STATUS_VALIDOS = {
    "Rascunho",
    "Em revisão",
    "Aprovado",
}


# Campos obrigatórios em cada conteúdo do JSON.
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
    """
    Lê e valida um arquivo JSON de conteúdos.

    Esta função não grava dados no Google Sheets.
    """

    caminho = Path(caminho)

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, dict):
        raise ValueError(
            "O JSON deve conter um objeto."
        )

    projeto = dados.get("projeto")

    if not isinstance(projeto, dict):
        raise ValueError(
            "Projeto inválido."
        )

    id_projeto = projeto.get("id_projeto")

    if (
        not isinstance(id_projeto, str)
        or not id_projeto.strip()
    ):
        raise ValueError(
            "Identificador do projeto inválido."
        )

    conteudos = dados.get("conteudos")

    if not isinstance(conteudos, list):
        raise ValueError(
            "A lista de conteúdos é obrigatória."
        )

    identificadores = set()

    for indice, conteudo in enumerate(
        conteudos,
        start=1
    ):

        if not isinstance(conteudo, dict):
            raise ValueError(
                f"Conteúdo {indice} inválido."
            )

        # Verifica os campos obrigatórios.
        campos_ausentes = (
            CAMPOS_OBRIGATORIOS - conteudo.keys()
        )

        if campos_ausentes:
            raise ValueError(
                f"Conteúdo {indice}: campos ausentes: "
                f"{sorted(campos_ausentes)}"
            )

        # Verifica os tipos dos campos de texto.
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
                    f"Conteúdo {indice}: "
                    f"{campo} deve ser texto."
                )

        identificador = (
            conteudo["id_conteudo"].strip()
        )

        titulo = (
            conteudo["titulo"].strip()
        )

        if not identificador or not titulo:
            raise ValueError(
                f"Conteúdo {indice}: "
                "ID e título são obrigatórios."
            )

        # Impede IDs repetidos dentro do próprio JSON.
        if identificador in identificadores:
            raise ValueError(
                f"Identificador duplicado: "
                f"{identificador}"
            )

        identificadores.add(identificador)

        # Valida o status.
        if conteudo["status"] not in STATUS_VALIDOS:
            raise ValueError(
                f"Conteúdo {indice}: "
                "status inválido."
            )

        # Valida a lista de arquivos de dados.
        arquivos = conteudo["arquivos_dados"]

        if (
            not isinstance(arquivos, list)
            or not all(
                isinstance(nome, str)
                and nome.strip()
                for nome in arquivos
            )
        ):
            raise ValueError(
                f"Conteúdo {indice}: "
                "arquivos_dados inválido."
            )

    return dados


def verificar_duplicidades(
    dados_json,
    registros_sheets
):
    """
    Compara os conteúdos do JSON com os registros
    existentes no Google Sheets.

    Retorna duas listas:
    - novos
    - existentes

    Não altera a planilha.
    """

    id_projeto = (
        dados_json["projeto"]["id_projeto"].strip()
    )

    ids_existentes = {
        (
            str(registro["id_projeto"]).strip(),
            str(registro["id_conteudo"]).strip(),
        )
        for registro in registros_sheets
    }

    novos = []
    existentes = []

    for conteudo in dados_json["conteudos"]:

        identificador = (
            id_projeto,
            conteudo["id_conteudo"].strip(),
        )

        if identificador in ids_existentes:
            existentes.append(conteudo)

        else:
            novos.append(conteudo)

    return novos, existentes


def preparar_conteudo_sheets(
    id_projeto,
    conteudo
):
    """
    Converte um conteúdo do JSON para o formato
    utilizado na planilha Google Sheets.

    O campo atualizado_em será preenchido
    automaticamente pelo repositório.
    """

    arquivos = conteudo["arquivos_dados"]

    return {
        "id_projeto": id_projeto.strip(),

        "id_conteudo": (
            conteudo["id_conteudo"].strip()
        ),

        "titulo": (
            conteudo["titulo"].strip()
        ),

        "descricao": (
            conteudo["descricao"].strip()
        ),

        "texto": conteudo["texto"],

        "status": conteudo["status"],

        "csv_associado": ";".join(arquivos),

        "fonte_texto": conteudo["fonte_texto"],
    }


def validar_conteudos_para_gravacao(
    dados_json,
    conteudos_novos
):
    """
    Verifica se os conteúdos novos possuem
    a origem do texto informada.

    Impede a gravação de conteúdos sem
    rastreabilidade da fonte.

    Não grava nem modifica registros.
    """

    if not isinstance(dados_json, dict):
        raise ValueError(
            "Estrutura do JSON inválida."
        )

    projeto = dados_json.get("projeto", {})

    if not isinstance(projeto, dict):
        raise ValueError(
            "Projeto inválido."
        )

    id_projeto = projeto.get(
        "id_projeto", ""
    )

    if (
        not isinstance(id_projeto, str)
        or not id_projeto.strip()
    ):
        raise ValueError(
            "Identificador do projeto inválido."
        )

    if not conteudos_novos:
        raise ValueError(
            "Não existem conteúdos novos "
            "para importar."
        )

    for conteudo in conteudos_novos:

        identificador = conteudo.get(
            "id_conteudo", ""
        )

        fonte = conteudo.get(
            "fonte_texto", ""
        )

        if (
            not isinstance(fonte, str)
            or not fonte.strip()
        ):
            raise ValueError(
                f"O conteúdo '{identificador}' "
                "não possui fonte_texto preenchida. "
                "Informe a origem do texto "
                "antes de gravar."
            )

    return True


# ============================================================
# TESTE LOCAL DO IMPORTADOR
# ============================================================

if __name__ == "__main__":

    dados = importar_json(
        "modelo_conteudo.json"
    )

    print(
        "JSON validado com sucesso!"
    )

    print(
        "Projeto:",
        dados["projeto"]["id_projeto"]
    )

    print(
        "Conteúdos:",
        len(dados["conteudos"])
    )
