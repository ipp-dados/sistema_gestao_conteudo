# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Codex, Copilot, Cursor, etc.) when working with code in this repository.

## Project

A Streamlit prototype (IPP / Primeira Infância project) for registering, editing, reviewing and exporting editorial content. Google Sheets is the only datastore, and the spreadsheet is a test sheet, not production. The code, UI text, comments and commit history are in Brazilian Portuguese; keep new code and UI strings in Portuguese. It is deployed on Streamlit Cloud, so anything that runs there reads `st.secrets` from the Cloud settings, not from the repo.

## Commands

The venv is managed with `uv`, because system Python lacks `python3-venv`. It runs Python 3.10, so there is no `tomllib`.

```bash
uv venv .venv && uv pip install -p .venv/bin/python -r requirements.txt
.venv/bin/streamlit run app.py               # main app (login + all pages)
.venv/bin/streamlit run app_visual_demo.py   # older UI variant, no login gate
.venv/bin/python conexao_sheets.py           # smoke test: connect and count rows
.venv/bin/python leitor_csv.py               # smoke test: list/read indicator CSVs
.venv/bin/python teste_gravacao_sheets.py    # writes a test row to the sheet (real write)
```

Os testes da exportação para o Drive rodam com `python -m unittest discover -s tests`. Não há linter nem etapa de build. Para exercitar uma página sem navegador, use `streamlit.testing.v1.AppTest.from_file("app.py")`.

## Spec-driven development

All work follows the spec-driven workflow in `specs/README.md`. Read `specs/constitution.md` and `specs/tech-stack.md` before planning or writing code; a plan that breaks a constitution rule needs an amendment first.

- Project documents (`stakeholders_description.md`, `roadmap.md`, `constitution.md`, `tech-stack.md`) and each spec's `spec.md` + `plan.md` are written on the `planning` branch.
- Each spec is implemented on its own branch `spec/YYYY-MM-DD_name`, created from `planning`, with its folder `specs/YYYY-MM-DD_name/` (copied from `specs/_templates/`). `tasks.md` and `validation.md` are filled there.
- Do not implement without an approved `spec.md` and `plan.md`. Every acceptance criterion needs evidence in `validation.md`.
- Skills per phase (Claude Code names): `plan.md` → plan mode / `Plan` agent, `frontend-design` (UI), `dataviz` (charts); `tasks.md` → `simplify`; `validation.md` → `run`, `code-review`, and `security-review` for auth/credentials/permissions/personal data.

## Configuration

Everything goes in `.streamlit/secrets.toml` (gitignored; the template is `.streamlit/secrets.toml.example`; the full guide is `SETUP_LOCAL.md`):

- `[dev] bypass_login = true` + `email`: skips `st.login`. The email must still be in `USUARIOS_AUTORIZADOS` in `app.py`.
- `[dev] armazenamento = "csv"` (+ optional `arquivo_csv`, default `dados_locais/conteudos.csv`): stores data in a local CSV instead of Sheets.
- `[auth]` / `[auth.google]`: `st.login` needs a **Web application** OAuth client with redirect `http://localhost:8501/oauth2callback`. `expose_tokens = "access"` and the `drive.file` scope are for the Google Drive integration in progress.
- Sheets credentials, checked in this order in `conexao_sheets.obter_credenciais()`: a `[gcp_service_account]` block in secrets (used on Cloud), otherwise `credentials.json` (a **Desktop app** OAuth client) plus `token.json`, which is created by a browser flow on the first run. Leaving a placeholder `[gcp_service_account]` in secrets breaks the fallback.

`[dev]` must never be added to the Streamlit Cloud secrets.

## Architecture

The modules form a single path from the app to the datastore:

`app.py` → `repositorio_sheets.py` → `conexao_sheets.conectar_planilha()` → aba `CONTEUDOS` da planilha definida em `[sheets].spreadsheet_id` nos Secrets do ambiente, ou `armazenamento_local.AbaCSV` no modo CSV.

- **Datastore contract:** the repository layer only uses `get_all_records()`, `append_row()`, `update(range_name="A{n}:I{n}", ...)` and `.title`. `AbaCSV` implements exactly these. If you use any other worksheet method, add it to `AbaCSV` too.
- **Columns:** the 9 columns listed in `repositorio_sheets.COLUNAS` (mirrored in `armazenamento_local.COLUNAS_PADRAO`). Their order matters: updates write positionally to `A:I`, and row 1 is the header. The record key is the pair (`id_projeto`, `id_conteudo`).
- **Optimistic concurrency:** `atualizar_conteudo(dados, registro_original)` re-reads the row and refuses to save if any monitored field differs from the snapshot taken when the form was opened. `app.py` keeps that snapshot in `st.session_state`. `atualizado_em` is always set server-side (UTC ISO).
- **Status workflow:** `Rascunho` → `Em revisão` → `Aprovado`. "Exportação CSV" exports only `Aprovado` rows.
- **JSON import** (`importador_json.py`): validates a file shaped like `modelo_conteudo.json` (a `projeto` plus a list of `conteudos` with `CAMPOS_OBRIGATORIOS`), checks for duplicates against the current records, and maps each item to a sheet row with `preparar_conteudo_sheets` (`arquivos_dados` becomes `csv_associado`). It never writes on its own; `app.py` calls `cadastrar_conteudo` for each row.
- **Indicator CSVs** (`leitor_csv.py`): read-only, from the sibling repo `../analise_primeira_infancia/tabelas_finais/`. If that folder is missing, the list is empty. `app.py` also accepts a manually uploaded CSV, which is not stored (Cloud has no persistent disk).
- **Navigation:** `app.py` is one script. A sidebar `st.radio` picks the page (Início, Conteúdos, Indicadores, Importação JSON, Revisões, Exportação CSV). Success messages survive `st.rerun()` through `st.session_state["mensagem_sucesso"]`.
- `conexao_drive.py` usa o token do login para enviar o CSV de aprovados à raiz de Meu Drive. Com `bypass_login`, apenas o download fica disponível.
- `app_visual_demo.py` is a near-copy of `app.py` without the auth gate. Changes to shared behavior may need to be made in both files.

## Branches

The full branch policy is in `specs/README.md` ("Política de branches"). In short: the shared repo is always `ipp-dados/sistema_gestao_conteudo` (`origin`) and all PRs target it, `main` only takes PRs, `planning` is merged with `main` after every merged PR, and `spec/...` branches are deleted after their merge. Do not change `feature/google-drive` without the owner's agreement.

`main` is the deployed app. `planning` holds the project and planning documents. `spec/YYYY-MM-DD_name` branches implement one spec each. `feature/google-drive` (Waleska) is the Drive integration work in progress. `initial_setup` holds the local-dev setup (login bypass, CSV storage, templates, `specs/` structure) with `feature/google-drive` merged in.
