from pathlib import Path
from re import subn
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import streamlit as st
from googleapiclient.errors import HttpError
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"
EMAIL_AUTORIZADO = "autorizado@example.com"
LINK = "https://drive.google.com/open?id=arquivo-de-teste"
APROVADO = {"id_conteudo": "aprovado", "status": "Aprovado", "titulo": "Aprovado"}
RASCUNHO = {"id_conteudo": "rascunho", "status": "Rascunho", "titulo": "Rascunho"}


class TesteExportacaoDrive(TestCase):
    def aplicar_patch(self, ajuste):
        self.addCleanup(ajuste.stop)
        return ajuste.start()

    def setUp(self):
        self.usuario = Mock(is_logged_in=True, tokens={"access": "token-ficticio"})
        self.usuario.get.return_value = EMAIL_AUTORIZADO
        self.registros = self.aplicar_patch(
            patch("repositorio_sheets.listar_conteudos", return_value=[APROVADO, RASCUNHO])
        )
        self.aplicar_patch(patch.object(st, "user", self.usuario))
        self.download = self.aplicar_patch(patch.object(st, "download_button", wraps=st.download_button))
        api = self.aplicar_patch(patch("conexao_drive.build"))
        self.criar = api.return_value.files.return_value.create
        self.executar = self.criar.return_value.execute
        self.executar.return_value = {"id": "arquivo-de-teste", "webViewLink": LINK}

    def iniciar_app(self):
        codigo, substituicoes = subn(
            r"(?ms)^USUARIOS_AUTORIZADOS = \{.*?^\}",
            f"USUARIOS_AUTORIZADOS = {{{EMAIL_AUTORIZADO!r}}}",
            APP.read_text(encoding="utf-8"),
        )
        self.assertEqual(substituicoes, 1)
        return AppTest.from_string(codigo, default_timeout=15).run()

    def abrir_exportacao(self):
        app = self.iniciar_app()
        app.radio[0].set_value("Exportação CSV").run()
        self.assertFalse(app.exception)
        return app

    def clicar_envio(self, app):
        app.button(key="enviar_csv_drive").click().run()
        self.assertFalse(app.exception)

    def teste_envios_explicitos_usam_o_mesmo_csv_do_download(self):
        app = self.abrir_exportacao()
        self.criar.assert_not_called()
        self.clicar_envio(app)
        self.assertEqual(app.success[0].value, "CSV salvo em Meu Drive.")
        self.assertEqual(app.get("link_button")[0].proto.url, LINK)
        dados = self.criar.call_args.kwargs
        self.assertRegex(dados["body"]["name"], r"^conteudos_aprovados_\d{4}-\d\d-\d\d_.*Z\.csv$")
        self.assertNotIn("parents", dados["body"])
        csv = dados["media_body"].getbytes(0, dados["media_body"].size())
        self.assertEqual(csv, self.download.call_args.kwargs["data"])
        self.assertIn(b"aprovado", csv)
        self.assertNotIn(b"rascunho", csv)
        app.run()
        self.criar.assert_called_once()
        self.clicar_envio(app)
        self.assertEqual(self.criar.call_count, 2)

    def teste_sem_aprovados(self):
        self.registros.return_value = [RASCUNHO]
        app = self.abrir_exportacao()
        self.assertFalse(app.button)
        self.criar.assert_not_called()

    def teste_sem_token_preserva_download(self):
        self.usuario.tokens = {}
        app = self.abrir_exportacao()
        self.assertFalse(app.button)
        self.download.assert_called_once()
        self.criar.assert_not_called()

    def teste_falhas_preservam_download_sem_expor_erro_bruto(self):
        respostas = [
            (HttpError(SimpleNamespace(status=403, reason="Forbidden"), b"token-ficticio"), "autorização"),
            (TimeoutError("token-ficticio"), "confirmar o envio"),
        ]
        for erro, mensagem in respostas:
            with self.subTest(tipo=type(erro).__name__):
                self.executar.side_effect = erro
                app = self.abrir_exportacao()
                self.clicar_envio(app)
                self.assertIn(mensagem, app.error[0].value)
                self.assertNotIn("token-ficticio", app.error[0].value)
                self.assertTrue(app.get("download_button"))

    def teste_usuario_nao_autorizado(self):
        self.usuario.get.return_value = "fora-da-lista@example.com"
        app = self.iniciar_app()
        self.assertIn("não está autorizada", app.error[0].value)
        self.assertFalse(app.radio)
        self.registros.assert_not_called()
        self.criar.assert_not_called()

    def teste_link_alternativo_quando_drive_retorna_apenas_id(self):
        self.executar.return_value = {"id": "arquivo-de-teste"}
        app = self.abrir_exportacao()
        self.clicar_envio(app)
        self.assertEqual(app.get("link_button")[0].proto.url, LINK)
