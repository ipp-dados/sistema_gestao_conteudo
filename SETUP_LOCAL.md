# Guia de configuração do ambiente local

Este guia explica como configurar e executar o sistema no seu computador. Também mostra como criar o projeto no Google Cloud e obter os arquivos de credenciais.

## Visão geral: o que precisa ser configurado

O sistema usa o Google em três partes independentes. Cada uma tem uma credencial própria:

| Parte | Para que serve | Credencial | Onde fica | Obrigatória localmente? |
|---|---|---|---|---|
| **Login** (`st.login`) | Tela "Entrar com Google" e controle de usuários autorizados | Cliente OAuth do tipo **Aplicativo da Web** | `[auth.google]` no `secrets.toml` | Não: pode ser ignorado com `[dev] bypass_login` |
| **Planilha** (Google Sheets) | Leitura e gravação dos conteúdos | Cliente OAuth do tipo **App para computador** (`credentials.json`) **ou** uma **conta de serviço** (`[gcp_service_account]`) | Raiz do projeto ou `secrets.toml` | Não: pode ser substituída por um CSV local |
| **Google Drive** | Envio do CSV de aprovados para Meu Drive | Usa o token do login (escopo `drive.file`) | `[auth]` + `[auth.google]` | Não |

Para testar só a interface, não é preciso configurar nada no Google (veja o [Caminho rápido](#caminho-rápido-sem-google)).

### Arquivos de configuração

| Arquivo | Versionado? | Finalidade |
|---|---|---|
| `.streamlit/secrets.toml` | Não (`.gitignore`) | Configuração principal: `[dev]`, `[auth]`, `[auth.google]`, `[gcp_service_account]` |
| `.streamlit/secrets.toml.example` | Sim | Modelo do arquivo acima |
| `credentials.json` | Não (`.gitignore`) | Cliente OAuth "App para computador", usado para acessar a planilha |
| `credentials.json.example` | Sim | Modelo do arquivo acima |
| `token.json` | Não (`.gitignore`) | Gerado automaticamente no primeiro acesso à planilha com `credentials.json` |
| `dados_locais/conteudos.csv` | Não (`.gitignore`) | Armazenamento local, quando o modo CSV está ativo |
| `../analise_primeira_infancia/tabelas_finais/*.csv` | Outro repositório | CSVs da página "Indicadores". Se a pasta não existir, a lista fica vazia |

## 1. Ambiente Python

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> No Ubuntu/Debian, se aparecer o erro `ensurepip is not available`, instale o pacote `python3-venv` (`sudo apt install python3-venv`) ou use o [uv](https://docs.astral.sh/uv/): `uv venv .venv && uv pip install -p .venv/bin/python -r requirements.txt`.

## 2. Arquivo `secrets.toml`

Copie o modelo:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml          # Linux/macOS
copy .streamlit\secrets.toml.example .streamlit\secrets.toml        # Windows
```

Gere um valor para `cookie_secret` e cole-o na seção `[auth]`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Caminho rápido (sem Google)

Para rodar a interface sem nenhuma credencial do Google, deixe a seção `[dev]` assim:

```toml
[dev]
bypass_login = true
email = "seu-email@gmail.com"        # precisa estar em USUARIOS_AUTORIZADOS (app.py)
armazenamento = "csv"
arquivo_csv = "dados_locais/conteudos.csv"
```

- `bypass_login` pula a tela de login. A barra lateral mostra "Modo dev local".
- `armazenamento = "csv"` grava os conteúdos em `dados_locais/conteudos.csv` em vez da planilha. O arquivo é criado vazio, com o cabeçalho, no primeiro uso. Para inserir dados de exemplo, importe `modelo_conteudo.json` na página "Importação JSON". A interface continua exibindo "Google Sheets", porque esses textos estão fixos no código.

Depois, siga para o [passo 5](#5-executar).

**Nunca** inclua a seção `[dev]` nos Secrets do Streamlit Cloud: ela desativa o login.

## 3. Configurar o projeto no Google Cloud

Faça esta etapa uma vez por projeto. Se outra pessoa da equipe já tiver um projeto configurado, ela pode adicionar você como usuário de teste (passo 3.3) e enviar as credenciais por um canal seguro. Nesse caso, pule para o passo 3.4 ou 3.5.

> O Google Cloud Console mudou recentemente o nome de alguns menus. Abaixo aparecem os dois nomes quando for o caso: o novo, **Google Auth Platform**, e o antigo, **APIs e serviços → Tela de consentimento OAuth**.

### 3.1. Criar o projeto

1. Acesse https://console.cloud.google.com/ com a sua conta Google.
2. No seletor de projetos (barra superior), clique em **Novo projeto**, dê um nome (por exemplo, `gestao-conteudo-local`) e clique em **Criar**.
3. Confirme que o novo projeto está selecionado na barra superior.

### 3.2. Ativar as APIs

Em **APIs e serviços → Biblioteca**, pesquise e ative:

- **Google Sheets API**: necessária para acessar a planilha.
- **Google Drive API**: necessária para enviar o CSV para Meu Drive.

### 3.3. Configurar a tela de consentimento

1. Abra **Google Auth Platform** (ou **APIs e serviços → Tela de consentimento OAuth**) e clique em **Começar**.
2. **Informações do app**: informe um nome (por exemplo, "Sistema de Gestão de Conteúdo") e seu e-mail de suporte.
3. **Público-alvo**: escolha **Externo**. O app fica no status **Em teste**, que é o adequado para o desenvolvimento.
4. **Dados de contato**: informe seu e-mail e conclua.
5. Em **Público-alvo → Usuários de teste**, adicione o e-mail de **cada pessoa** que vai fazer login ou acessar a planilha pelo app. Enquanto o app estiver em teste, somente esses usuários conseguem autorizar o acesso.

> Com o app no status "Em teste", a autorização expira após cerca de 7 dias. Quando isso acontecer, apague `token.json` e autorize novamente.

### 3.4. Cliente "App para computador": `credentials.json` (acesso à planilha)

Este cliente permite que o Python acesse a planilha **com a sua própria conta Google**.

1. Vá em **Google Auth Platform → Clientes** (ou **APIs e serviços → Credenciais**) → **Criar cliente** (ou **Criar credenciais → ID do cliente OAuth**).
2. **Tipo de aplicativo**: **App para computador**. Informe um nome e clique em **Criar**.
3. Clique em **Fazer download do JSON**.
4. Salve o arquivo na **raiz do projeto** com o nome `credentials.json`. O conteúdo deve começar com a chave `"installed"`, como em `credentials.json.example`.
5. No `secrets.toml`, **não** deixe a seção `[gcp_service_account]` com valores fictícios. Se ela existir, o sistema tentará usá-la em vez do `credentials.json`.
6. Remova `armazenamento = "csv"` da seção `[dev]`, se estiver presente, e preencha `spreadsheet_id` na seção `[sheets]` com o ID da planilha do ambiente.
7. Teste a conexão fora do Streamlit:

   ```bash
   python conexao_sheets.py
   ```

   O navegador abrirá a tela de autorização do Google. Escolha sua conta. Na mensagem "O Google não verificou este app", clique em **Continuar**, porque o app é seu e está em teste. Em seguida, permita o acesso às planilhas. Se tudo der certo, o terminal mostra `Conexão realizada com sucesso!` e o arquivo `token.json` é criado. As execuções seguintes reutilizam esse token.

A sua conta precisa ter acesso de **Editor** à planilha (veja o [passo 4](#4-planilha)).

### 3.5. Cliente "Aplicativo da Web": seção `[auth.google]` (login no sistema)

Este cliente é usado pela tela "Entrar com Google" (`st.login`). É um cliente **diferente** do `credentials.json`.

1. Em **Clientes → Criar cliente**, escolha o tipo **Aplicativo da Web**.
2. Em **URIs de redirecionamento autorizados**, adicione:
   - `http://localhost:8501/oauth2callback` (ambiente local)
   - `https://<seu-app>.streamlit.app/oauth2callback` (Streamlit Cloud, se for o caso)
3. Clique em **Criar** e copie o **ID do cliente** e a **Chave secreta do cliente**. Também é possível baixar o JSON com esses dados.
4. Preencha o `secrets.toml`:

   ```toml
   [auth]
   redirect_uri = "http://localhost:8501/oauth2callback"
   cookie_secret = "<valor gerado no passo 2>"
   expose_tokens = "access"

   [auth.google]
   client_id = "<ID do cliente>.apps.googleusercontent.com"
   client_secret = "<chave secreta do cliente>"
   server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
   client_kwargs = { scope = "openid email profile https://www.googleapis.com/auth/drive.file" }
   ```

5. Remova `bypass_login` da seção `[dev]` (ou remova a seção inteira).
6. Confirme que o seu e-mail está em `USUARIOS_AUTORIZADOS`, em `app.py`.

Se você baixou o JSON do cliente web, este comando imprime os campos já no formato do `secrets.toml`:

```bash
python -c "import json,sys; c=json.load(open(sys.argv[1]))['web']; print('client_id = \"%s\"\nclient_secret = \"%s\"' % (c['client_id'], c['client_secret']))" client_secret_web.json
```

### 3.6. Conta de serviço: seção `[gcp_service_account]` (alternativa ao `credentials.json`)

É a mesma forma de acesso usada no Streamlit Cloud. O sistema acessa a planilha com uma conta "robô", sem abrir o navegador.

1. Vá em **IAM e administrador → Contas de serviço → Criar conta de serviço**, informe um nome e conclua. Não é preciso atribuir papéis no projeto.
2. Abra a conta criada → aba **Chaves** → **Adicionar chave → Criar nova chave → JSON**. O arquivo será baixado.
3. Converta o JSON para o formato do `secrets.toml`:

   ```bash
   python -c "import json,sys; d=json.load(open(sys.argv[1])); print('[gcp_service_account]'); [print(f'{k} = {json.dumps(v)}') for k, v in d.items()]" chave-conta-servico.json
   ```

   Cole a saída no final do `secrets.toml`, no lugar da seção de exemplo.
4. **Compartilhe a planilha** com o e-mail da conta de serviço (campo `client_email`, terminado em `iam.gserviceaccount.com`), com permissão de **Editor**.
5. Guarde o arquivo JSON fora do repositório, ou apague-o depois de copiar os dados.

> Em contas institucionais, a criação de chaves de conta de serviço pode estar bloqueada por política da organização. Nesse caso, use o `credentials.json` (passo 3.4) ou peça a liberação ao administrador.

## 4. Planilha

O sistema acessa a aba **`CONTEUDOS`** da planilha definida em `[sheets].spreadsheet_id` nos Secrets. Use o trecho entre `/d/` e `/edit` na URL da planilha. A conta usada na conexão precisa de permissão de leitor para consultar e exportar ou de editor para gravar.

Ao criar uma planilha nova para testes, a aba `CONTEUDOS` precisa ter, na linha 1, exatamente estas colunas, nesta ordem (A a I):

```text
id_projeto | id_conteudo | titulo | descricao | texto | status | csv_associado | atualizado_em | fonte_texto
```

## 5. Executar

```bash
python -m streamlit run app.py
```

Abra http://localhost:8501. Alterações no `secrets.toml` passam a valer quando a página é recarregada.

## Problemas comuns

| Sintoma | Causa provável / solução |
|---|---|
| Erro ao clicar em "Entrar com Google" | `[auth]` ausente ou incompleto, ou URI de redirecionamento não cadastrado no cliente **Aplicativo da Web** |
| `redirect_uri_mismatch` | O `redirect_uri` do `secrets.toml` não é idêntico ao cadastrado no Google Cloud |
| "Acesso bloqueado" / `access_denied` | Seu e-mail não está em **Usuários de teste** (passo 3.3) |
| "Sua conta Google não está autorizada" | E-mail fora de `USUARIOS_AUTORIZADOS` (`app.py`) |
| `No such file or directory: ...credentials.json` | Não há `[gcp_service_account]` no `secrets.toml` nem `credentials.json` na raiz |
| Erro de chave privada / `invalid_grant` com conta de serviço | A seção `[gcp_service_account]` tem valores fictícios ou está incompleta. Preencha-a ou remova-a |
| `SpreadsheetNotFound` / `PERMISSION_DENIED` | A conta usada não tem acesso à planilha (passo 4) |
| `Google Sheets API has not been used in project` | A API não foi ativada (passo 3.2) |
| `WorksheetNotFound` | A planilha não tem a aba `CONTEUDOS` |
| `invalid_grant` / token expirado | Apague `token.json` e execute novamente para reautorizar |
| "Nenhum CSV encontrado" em Indicadores | A pasta `../analise_primeira_infancia/tabelas_finais/` não existe ao lado deste repositório |

## Segurança

- Nunca versione `secrets.toml`, `credentials.json`, `token.json` nem chaves JSON de contas de serviço. Eles já estão no `.gitignore`.
- Não envie credenciais por e-mail ou chat aberto. Prefira um gerenciador de senhas ou canal seguro da equipe.
- Nunca adicione a seção `[dev]` aos Secrets do Streamlit Cloud.
