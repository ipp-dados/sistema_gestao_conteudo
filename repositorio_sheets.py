
from datetime import datetime, timezone

from conexao_sheets import conectar_planilha

COLUNAS = [
    "id_projeto",
    "id_conteudo",
    "titulo",
    "descricao",
    "texto",
    "status",
    "csv_associado",
    "atualizado_em",
]


def listar_conteudos():
    aba = conectar_planilha()
    return aba.get_all_records()


def cadastrar_conteudo(dados):
    aba = conectar_planilha()
    registros = aba.get_all_records()

    for registro in registros:
        if (
            str(registro["id_projeto"]) == str(dados["id_projeto"])
            and str(registro["id_conteudo"]) == str(dados["id_conteudo"])
        ):
            raise ValueError(
                "Já existe um conteúdo com esses IDs."
            )

    novo_registro = dados.copy()
    novo_registro["atualizado_em"] = (
        datetime.now(timezone.utc).isoformat()
    )

    aba.append_row(
        [novo_registro.get(coluna, "") for coluna in COLUNAS],
        value_input_option="RAW",
    )


def atualizar_conteudo(dados, registro_original):
    aba = conectar_planilha()
    registros = aba.get_all_records()

    campos_monitorados = [
        "titulo",
        "descricao",
        "texto",
        "status",
        "csv_associado",
        "atualizado_em",
    ]

    for numero_linha, registro in enumerate(registros, start=2):
        if (
            str(registro["id_projeto"]) == str(dados["id_projeto"])
            and str(registro["id_conteudo"]) == str(dados["id_conteudo"])
        ):
            alteracoes = [
                campo
                for campo in campos_monitorados
                if str(registro.get(campo, ""))
                != str(registro_original.get(campo, ""))
            ]

            if alteracoes:
                raise ValueError(
                    "Este conteúdo foi alterado desde que "
                    "você abriu o formulário. Atualize a "
                    "página antes de salvar novamente. "
                    "Campos alterados: "
                    + ", ".join(alteracoes)
                )

            novo_registro = dados.copy()
            novo_registro["atualizado_em"] = (
                datetime.now(timezone.utc).isoformat()
            )

            aba.update(
                range_name=f"A{numero_linha}:H{numero_linha}",
                values=[
                    [
                        novo_registro.get(coluna, "")
                        for coluna in COLUNAS
                    ]
                ],
                value_input_option="RAW",
            )
            return

    raise ValueError(
        "Conteúdo não encontrado na planilha."
    )
