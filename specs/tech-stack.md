# Tecnologias do projeto

Inventário do que o sistema usa hoje e das restrições técnicas que valem para todos os planos. Uma tecnologia nova entra aqui antes de entrar no código, por meio de uma especificação.

## Linguagem e ambiente

| Item | Versão / escolha | Observações |
|---|---|---|
| Python | 3.10 ou superior | Testado localmente com 3.10. O `tomllib` só existe a partir do 3.11 |
| Ambiente virtual | venv, uv ou Conda | Ver [`SETUP_LOCAL.md`](../SETUP_LOCAL.md) |
| Dependências | `requirements.txt` | **Sem versões fixadas**, exceto `Authlib>=1.3.2` e `httpx>=0.27.0` |

## Bibliotecas

Versões instaladas no ambiente local em 24/11/2026:

| Biblioteca | Versão | Uso |
|---|---|---|
| streamlit | 1.65.0 | Interface, navegação, login (`st.login`) e `st.secrets` |
| pandas | 2.3.3 | Leitura de CSVs de indicadores e exportação |
| gspread | 6.2.1 | Leitura e gravação no Google Sheets |
| google-auth | 2.63.1 | Credenciais de conta de serviço e OAuth |
| google-auth-oauthlib | 1.5.0 | Autorização no navegador para o `credentials.json` |
| google-auth-httplib2 | 0.4.4 | Transporte HTTP das APIs Google |
| Authlib | 1.9.10 | Exigida pelo `st.login` |
| httpx | 0.28.1 | Exigida pelo login Google no Streamlit |
| requests | 2.34.2 | Requisições HTTP |

## Serviços e infraestrutura

| Serviço | Uso | Configuração |
|---|---|---|
| Streamlit Community Cloud | Hospedagem do app | Secrets na área de configurações do app; sem disco persistente |
| Google Sheets | Armazenamento dos conteúdos (aba `CONTEUDOS`) | `SPREADSHEET_ID` em `conexao_sheets.py` |
| Google OAuth 2.0 | Login (cliente **Aplicativo da Web**) e acesso à planilha (cliente **App para computador**) | `[auth]`, `[auth.google]`, `credentials.json` |
| Conta de serviço Google | Acesso à planilha no Cloud | `[gcp_service_account]` |
| Google Drive API | Envio de arquivos CSV (em desenvolvimento) | Escopo `drive.file`, via token do login |
| GitHub (`ipp-dados/sistema_gestao_conteudo`) | Código e Pull Requests | Fork de `waleskamarques-eng/sistema_gestao_conteudo` |

## Armazenamento

| Modo | Quando | Implementação |
|---|---|---|
| Google Sheets | Padrão; obrigatório no Cloud | `conexao_sheets.py` |
| CSV local | Desenvolvimento e testes (`[dev] armazenamento = "csv"`) | `armazenamento_local.py`, arquivo em `dados_locais/` |

Estrutura dos registros: 9 colunas, nesta ordem: `id_projeto`, `id_conteudo`, `titulo`, `descricao`, `texto`, `status`, `csv_associado`, `atualizado_em`, `fonte_texto`.

## Fontes de dados externas

- CSVs de indicadores lidos do repositório vizinho `../analise_primeira_infancia/tabelas_finais/` (somente leitura).
- Arquivos JSON de importação no formato de `modelo_conteudo.json`.

## Restrições e lacunas conhecidas

- O Google Sheets não oferece transações nem restrições de unicidade. A troca por um banco de dados (por exemplo, PostgreSQL) está em avaliação e depende das políticas de dados do IPP.
- No status "Em teste", a autorização OAuth expira em cerca de 7 dias.
- Não há suíte de testes automatizados, linter nem integração contínua.
- As dependências não têm versões fixadas, o que pode mudar o comportamento entre instalações.

## Decisões pendentes

| Tema | Opções | Situação |
|---|---|---|
| Armazenamento definitivo | Google Sheets, PostgreSQL gerenciado, infraestrutura do IPP | Em aberto |
| Testes automatizados | pytest + `streamlit.testing` | Em aberto |
| Fixação de versões | `requirements.txt` com versões fixas ou arquivo de lock | Em aberto |
