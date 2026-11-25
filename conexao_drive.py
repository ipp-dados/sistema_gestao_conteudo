from datetime import datetime, timezone
from urllib.parse import quote

import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload


class TokenDriveIndisponivel(RuntimeError):
    """O login atual não disponibiliza um token para o Drive."""


def conectar_drive():
    """Estabelece a conexão com o Google Drive do usuário autenticado."""

    token = st.user.tokens.get("access")

    if not token:
        raise TokenDriveIndisponivel(
            "Token de acesso Google indisponível."
        )

    credenciais = Credentials(token=token)

    return build(
        "drive",
        "v3",
        credentials=credenciais,
        cache_discovery=False,
    )


def testar_conexao_drive():
    """Verifica a comunicação com a API do Google Drive."""

    servico = conectar_drive()

    resultado = servico.about().get(
        fields="user(displayName)"
    ).execute()

    return resultado


def enviar_csv_drive(csv: bytes) -> str:
    """Cria um CSV na raiz de Meu Drive e retorna o link do arquivo."""
    servico = conectar_drive()
    data_hora = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S-%fZ")
    arquivo = servico.files().create(
        body={"name": f"conteudos_aprovados_{data_hora}.csv"},
        media_body=MediaInMemoryUpload(csv, mimetype="text/csv"),
        fields="id,webViewLink",
    ).execute()

    return arquivo.get("webViewLink") or (
        f"https://drive.google.com/open?id={quote(arquivo['id'], safe='')}"
    )
