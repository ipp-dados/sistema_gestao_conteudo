# Plano de exportação CSV para o Google Drive

Especificação [aprovada](spec.md) · Plano **Aprovado** pelo solicitante

## Abordagem

Reaproveitar o cliente Drive v3 de `conexao_drive.py`, a dependência já adicionada em `feature/google-drive` e o CSV gerado pela página de exportação. A mesma sequência de bytes alimenta o download atual e o envio em memória. O envio usa `files.create` com MIME `text/csv`, sem pasta pai explícita, solicitando `id` e `webViewLink`. Cada envio usa um nome com data e hora em UTC, com formato compatível com nomes de arquivos no Windows.

A página oferece **Enviar ao Google Drive** depois da verificação de acesso e quando há dados exportáveis. O estado da sessão controla o envio e a exibição do resultado. A ação desabilita o botão antes da chamada à API, restaura o estado ao terminar e evita repetir a criação em reexecuções do Streamlit. A confirmação usa o link retornado pelo Drive. Verificar com OAuth real se o CSV criado sempre retorna `webViewLink` e tratar separadamente um arquivo criado cuja URL não foi disponibilizada, evitando induzir um novo envio.

## Mudanças por arquivo

| Arquivo | Mudança prevista |
|---|---|
| `conexao_drive.py` | Reusar o cliente autenticado, criar o CSV em memória e devolver os metadados necessários à confirmação. |
| `app.py` | Retirar o diagnóstico temporário do fluxo de navegação e adicionar o envio à página de exportação. Tratar token ausente, falta de permissão e indisponibilidade com mensagens em português. |
| `app_visual_demo.py` | Aplicar eventuais mudanças compartilhadas na geração do CSV. O envio autenticado fica na interface que verifica a conta Google. |
| `AGENTS.md`, `SETUP_LOCAL.md` e `specs/tech-stack.md` | Atualizar a descrição da integração, a configuração existente e o inventário de dependências. |
| `tests/` | Adicionar testes direcionados ao envio e à página de exportação usando `unittest`, mocks e `streamlit.testing.v1.AppTest`. |
| `tasks.md` e `validation.md` | Registrar as tarefas e as evidências de CA1 a CA6 na branch de implementação. |

## Dados, configuração e segurança

O Google Sheets e o CSV local preservam o contrato e as colunas atuais. A operação usa os dados aprovados da exportação existente e transmite o arquivo em memória, inclusive no Streamlit Cloud. A configuração reaproveita o token de acesso do login, o escopo `drive.file` e a API do Drive habilitada no projeto OAuth. Conferir a política de privacidade e atualizá-la no mesmo PR se o envio alterar o compartilhamento descrito.

O modo local com bypass deve preservar o download e indicar que o envio exige login Google. A implementação deve manter o token fora da interface e dos registros. Erros ambíguos de rede não terão nova tentativa automática, pois o Drive pode ter criado o arquivo antes de a resposta se perder.

## Validação

### Ambientes

| Ambiente | Execução | Dados e credenciais |
|---|---|---|
| DEV | Execução local | CSV local por padrão no desenvolvimento ou planilha de DEV configurada explicitamente. Se houver login real, usar cliente de DEV com callback local. |
| HML | Novo app temporário no Community Cloud, com URL própria, repositório `ipp-dados/sistema_gestao_conteudo`, branch `feature/google-drive` e entrada `app.py`. | Planilha dedicada com dados fictícios, cliente OAuth e conta de serviço de HML. |
| PROD | Aplicação existente na `main`. | Aplicação, URL, planilha, OAuth e Secrets atuais preservados nesta etapa. |

### Ordem de implementação e configuração

1. Na branch de homologação, externalizar o ID da planilha para `[sheets].spreadsheet_id` em `st.secrets`. Manter a seleção de CSV local antes dessa leitura. Quando o modo Sheets estiver ativo, exigir um valor não vazio e falhar antes de autenticar ou abrir uma planilha se faltar configuração. Atualizar o modelo de Secrets com valor fictício e verificar os caminhos de CSV local, ID configurado e ID ausente, sem acessar serviços reais. A migração de configuração de PROD deverá anteceder qualquer publicação futura desse código.
2. Definir um subdomínio exclusivo disponível na tela de criação do app de HML. No Google Cloud Console, usar um projeto dedicado à HML, habilitar Google Drive API e Google Sheets API, configurar a tela de consentimento e criar um cliente OAuth do tipo Aplicativo da Web. Registrar exatamente `https://<subdominio-hml>.streamlit.app/oauth2callback`. Para público externo em modo de teste, cadastrar as duas contas necessárias ao ensaio, uma presente e outra ausente de `USUARIOS_AUTORIZADOS`, para distinguir o bloqueio do aplicativo do bloqueio do Google.
3. Criar uma conta de serviço de HML e compartilhar exclusivamente a planilha de HML com ela. Usar permissão de leitor para a exportação. Conceder editor somente se houver teste autorizado de gravação. Na aba `CONTEUDOS`, manter as nove colunas do repositório na ordem prevista e inserir registros fictícios com status variados. O token do login da pessoa usuária autoriza o envio ao Drive. A conta de serviço lê a planilha.
4. No painel do novo app, configurar `[sheets]`, `[gcp_service_account]`, `[auth]` e `[auth.google]`. Usar o callback da HML, um `cookie_secret` novo, `expose_tokens = ["access"]` e os escopos `openid email profile https://www.googleapis.com/auth/drive.file`. Manter `[dev]` apenas no ambiente local e inserir as credenciais somente no painel de Secrets da HML. Implantar quando a revisão com o ID configurável estiver disponível na branch remota.
5. Validar CA1 a CA6 no navegador. Para CA6, observar o botão durante uma resposta atrasada e conferir a quantidade de arquivos criados. Se a latência natural for insuficiente, combinar uma forma temporária de induzir o atraso somente na HML. Registrar resultados e evidências sem dados pessoais ou credenciais.

| Critério | Verificação planejada |
|---|---|
| CA1 | Comparar os bytes do download com os recebidos pelo cliente simulado e verificar que apenas os registros aprovados foram incluídos. |
| CA2 | Verificar ausência de chamadas de criação ao abrir a página, baixar o arquivo ou usar dados sem aprovados. |
| CA3 | Verificar a requisição de criação e o link de sucesso com mocks. Com OAuth real e dados fictícios, conferir o arquivo na raiz de **Meu Drive** e abrir o link. |
| CA4 | Simular ausência de token, permissão insuficiente e indisponibilidade. Conferir mensagens, preservação do download e ausência do token na interface e nos registros. |
| CA5 | Exercitar o bloqueio de conta não autorizada e conferir que o cliente de envio não é chamado. |
| CA6 | Verificar duas criações em dois envios explícitos, o nome com data e hora e a ausência de chamadas extras após reexecução. Com a resposta propositalmente atrasada, verificar o bloqueio visual durante o envio. |

Executar os testes com armazenamento local e Drive simulado. Fazer a validação final no Streamlit Community Cloud com uma conta de teste autorizada e dados fictícios. Registrar cenário, resultado e evidência em `validation.md`, sem credenciais nem dados pessoais. Fazer revisão de código e de segurança antes do PR.

Armazenamento compartilhado, listagem e leitura de CSVs e organização por projeto ficam para incrementos posteriores.
