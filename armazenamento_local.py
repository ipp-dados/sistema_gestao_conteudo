"""Armazenamento local em CSV para testes, no lugar do Google Sheets.

Ativado apenas pelo secrets.toml local:

    [dev]
    armazenamento = "csv"
    arquivo_csv = "dados_locais/conteudos.csv"   # opcional

A classe AbaCSV imita os métodos de gspread.Worksheet usados pelo sistema
(get_all_records, append_row, update e title), para que repositorio_sheets.py
funcione sem alterações. Nunca configure isso no Streamlit Cloud.
"""

import csv
import os
import re
import tempfile
from pathlib import Path

COLUNAS_PADRAO = [
    "id_projeto",
    "id_conteudo",
    "titulo",
    "descricao",
    "texto",
    "status",
    "csv_associado",
    "atualizado_em",
    "fonte_texto",
]


class AbaCSV:
    def __init__(self, caminho, colunas=COLUNAS_PADRAO):
        self.caminho = Path(caminho)
        self.title = f"CSV local ({self.caminho.name})"

        if not self.caminho.exists():
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
            self._gravar([list(colunas)])

    def _ler(self):
        with self.caminho.open(newline="", encoding="utf-8") as arquivo:
            return list(csv.reader(arquivo))

    def _gravar(self, linhas):
        # Grava em arquivo temporário e substitui, para não corromper o CSV.
        descritor, temporario = tempfile.mkstemp(
            dir=self.caminho.parent, suffix=".tmp"
        )
        with os.fdopen(descritor, "w", newline="", encoding="utf-8") as arquivo:
            csv.writer(arquivo).writerows(linhas)
        os.replace(temporario, self.caminho)

    def get_all_records(self):
        linhas = self._ler()
        if not linhas:
            return []
        cabecalho, dados = linhas[0], linhas[1:]
        return [
            {
                coluna: (linha[i] if i < len(linha) else "")
                for i, coluna in enumerate(cabecalho)
            }
            for linha in dados
            if any(celula.strip() for celula in linha)
        ]

    def append_row(self, valores, value_input_option=None):
        linhas = self._ler()
        linhas.append(["" if v is None else str(v) for v in valores])
        self._gravar(linhas)

    def update(self, range_name, values, value_input_option=None):
        # Aceita intervalos de uma linha no formato "A5:I5" (linha 1 = cabeçalho).
        correspondencia = re.fullmatch(r"[A-Z]+(\d+):[A-Z]+(\d+)", range_name)
        if not correspondencia or correspondencia[1] != correspondencia[2]:
            raise ValueError(f"Intervalo não suportado no CSV local: {range_name}")

        indice = int(correspondencia[1]) - 1
        linhas = self._ler()
        if indice < 1 or indice >= len(linhas):
            raise ValueError(f"Linha {indice + 1} não existe no CSV local.")

        linhas[indice] = ["" if v is None else str(v) for v in values[0]]
        self._gravar(linhas)
