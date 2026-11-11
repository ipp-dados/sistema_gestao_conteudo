
from pathlib import Path

import gspread
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow

PASTA_PROJETO = Path(__file__).resolve().parent

SPREADSHEET_ID = "1LkM1kHIQX4gQNrjqFDGN82oN91JxnGcpGBBeBEmRNP4"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

ARQUIVO_CREDENCIAIS = PASTA_PROJETO / "credentials.json"
ARQUIVO_TOKEN = PASTA_PROJETO / "token.json"


def obter_credenciais():
    # No servidor, utiliza a conta de serviço.
    if "gcp_service_account" in st.secrets:
        dados_conta = dict(st.secrets["gcp_service_account"])

        return ServiceAccountCredentials.from_service_account_info(
            dados_conta,
            scopes=SCOPES,
        )

    # No computador local, mantém a autenticação atual.
    credenciais = None

    if ARQUIVO_TOKEN.exists():
        credenciais = Credentials.from_authorized_user_file(
            str(ARQUIVO_TOKEN), SCOPES
        )

    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(ARQUIVO_CREDENCIAIS), SCOPES
            )
            credenciais = flow.run_local_server(port=0)

        ARQUIVO_TOKEN.write_text(
            credenciais.to_json(), encoding="utf-8"
        )

    return credenciais


def conectar_planilha():
    credenciais = obter_credenciais()

    cliente = gspread.authorize(credenciais)
    planilha = cliente.open_by_key(SPREADSHEET_ID)

    return planilha.worksheet("CONTEUDOS")


if __name__ == "__main__":
    aba = conectar_planilha()
    print("Conexão realizada com sucesso!")
    print("Aba acessada:", aba.title)
    print("Total de registros:", len(aba.get_all_records()))
