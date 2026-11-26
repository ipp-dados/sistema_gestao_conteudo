import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import conexao_sheets
from armazenamento_local import AbaCSV


class TesteConexaoSheets(unittest.TestCase):
    def setUp(self):
        self.secrets = {}
        secrets_simulados = patch.object(conexao_sheets.st, "secrets", self.secrets)
        credenciais_simuladas = patch.object(conexao_sheets, "obter_credenciais")
        autorizacao_simulada = patch.object(conexao_sheets.gspread, "authorize")
        for simulacao in (secrets_simulados, credenciais_simuladas, autorizacao_simulada):
            self.addCleanup(simulacao.stop)
        secrets_simulados.start()
        self.obter_credenciais = credenciais_simuladas.start()
        self.autorizar = autorizacao_simulada.start()

    def test_csv_local_funciona_sem_configuracao_da_planilha(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "conteudos.csv"
            self.secrets["dev"] = {"armazenamento": "csv", "arquivo_csv": str(caminho)}

            aba = conexao_sheets.conectar_planilha()

            self.assertIsInstance(aba, AbaCSV)
            self.assertEqual(aba.get_all_records(), [])
        self.obter_credenciais.assert_not_called()
        self.autorizar.assert_not_called()

    def test_sheets_abre_a_aba_da_planilha_configurada(self):
        self.secrets["sheets"] = {"spreadsheet_id": "  id-ficticio-hml  "}
        cliente = self.autorizar.return_value
        planilha = cliente.open_by_key.return_value

        aba = conexao_sheets.conectar_planilha()

        self.obter_credenciais.assert_called_once_with()
        self.autorizar.assert_called_once_with(self.obter_credenciais.return_value)
        cliente.open_by_key.assert_called_once_with("id-ficticio-hml")
        planilha.worksheet.assert_called_once_with("CONTEUDOS")
        self.assertIs(aba, planilha.worksheet.return_value)

    def test_sheets_sem_id_valido_falha_antes_de_autenticar(self):
        configuracoes_invalidas = (
            {},
            {"sheets": {}},
            {"sheets": {"spreadsheet_id": " "}},
            {"sheets": {"spreadsheet_id": 123}},
        )
        for configuracao in configuracoes_invalidas:
            with self.subTest(configuracao=configuracao):
                self.secrets.clear()
                self.secrets.update(configuracao)
                with self.assertRaisesRegex(ValueError, r"\[sheets\]\.spreadsheet_id"):
                    conexao_sheets.conectar_planilha()
        self.obter_credenciais.assert_not_called()
        self.autorizar.assert_not_called()
