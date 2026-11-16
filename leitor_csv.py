
from pathlib import Path
import pandas as pd

# Pasta onde os pipelines da Primeira Infância geram os CSVs
PASTA_CSV = (
    Path(__file__).resolve().parent.parent
    / "analise_primeira_infancia"
    / "tabelas_finais"
)


def listar_csvs():
    """Lista os CSVs disponíveis sem interromper o aplicativo."""
    if not PASTA_CSV.is_dir():
        return []

    return sorted(arquivo.name for arquivo in PASTA_CSV.glob("*.csv"))


def ler_csv(nome_arquivo):
    """Lê um CSV da pasta oficial, sem alterar o arquivo."""
    arquivo = PASTA_CSV / nome_arquivo

    if (
        Path(nome_arquivo).name != nome_arquivo
        or arquivo.suffix.lower() != ".csv"
        or not arquivo.is_file()
    ):
        raise ValueError("Arquivo CSV inválido ou não encontrado.")

    return pd.read_csv(arquivo)


if __name__ == "__main__":
    arquivos = listar_csvs()

    print(f"CSVs encontrados: {len(arquivos)}")

    if arquivos:
        print(f"Primeiro arquivo: {arquivos[0]}")
        print(ler_csv(arquivos[0]).head())
