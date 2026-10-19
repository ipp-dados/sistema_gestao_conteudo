
from datetime import datetime, timezone
from conexao_sheets import conectar_planilha

aba = conectar_planilha()

id_teste = "CONT-TESTE-001"

registros = aba.get_all_records()

existe = any(
    str(registro["id_conteudo"]) == id_teste
    for registro in registros
)

if existe:
    print("O registro de teste já existe. Nenhuma linha foi adicionada.")
else:
    aba.append_row(
        [
            "PRIMEIRA-INFANCIA",
            id_teste,
            "Teste de integração",
            "Registro fictício para validar a conexão",
            "Texto de teste criado pelo Python.",
            "Rascunho",
            "",
            datetime.now(timezone.utc).isoformat()
        ],
        value_input_option="RAW"
    )

    print("Registro de teste gravado com sucesso!")
