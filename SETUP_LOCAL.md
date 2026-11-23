# Local setup guide

How to configure and run the app on your machine.

## Configuration files

| File | Required? | Committed? | Purpose |
|---|---|---|---|
| `.streamlit/secrets.toml` | **Yes** | No (gitignored) | Login (`[auth]`), Sheets access (`[gcp_service_account]`), local dev bypass (`[dev]`) |
| `.streamlit/secrets.toml.example` | – | Yes | Template for the file above |
| `credentials.json` | Only if not using a service account | No (gitignored) | OAuth "Desktop app" client for Sheets |
| `credentials.json.example` | – | Yes | Template for the file above |
| `token.json` | Auto-generated | No (gitignored) | Created on first OAuth run when using `credentials.json` |
| `../analise_primeira_infancia/tabelas_finais/*.csv` | Optional | Other repo | CSVs for the "Indicadores" page; empty list if missing |

Sheets access uses **one** of these: `[gcp_service_account]` in secrets (checked first) **or** `credentials.json` + `token.json`.

## Steps

### 1. Python environment

```powershell
python -m venv venv_sgc
venv_sgc\Scripts\activate
pip install -r requirements.txt
```

### 2. Secrets file

```powershell
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

Then fill in the sections you need (below).

### 3. Login: pick one

- **Fast (local debugging):** keep `[dev] bypass_login = true` with your email. Delete or comment out `[auth]` and `[auth.google]`. The sidebar shows "Modo dev local".
- **Real Google login:** delete `[dev]` and fill in `[auth]`:
  1. Google Cloud Console → APIs & Services → Credentials → your **Web application** OAuth client.
  2. Copy `client_id` and `client_secret` into `[auth.google]`.
  3. Add `http://localhost:8501/oauth2callback` to the client's **Authorized redirect URIs**.
  4. Generate `cookie_secret` with `python -c "import secrets;print(secrets.token_urlsafe(32))"`.

The email you log in with must be in `USUARIOS_AUTORIZADOS` in `app.py`.

### 4. Google Sheets access: pick one

- **Service account (recommended, same as Streamlit Cloud):** copy the `[gcp_service_account]` block from Streamlit Cloud → app → Settings → Secrets, or fill it in from the service account's JSON key. The spreadsheet must be shared with the account's `client_email` as Editor.
- **Personal OAuth:** remove `[gcp_service_account]` from secrets. Download a **Desktop app** OAuth client JSON from Google Cloud Console and save it as `credentials.json` in the project root (see `credentials.json.example`). On the first run a browser opens to authorize, and `token.json` is created.

### 5. Run

```powershell
python -m streamlit run app.py
```

Open http://localhost:8501. Changes to secrets take effect when you refresh the page.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Error when clicking "Entrar com Google" | `[auth]` missing or incomplete, or redirect URI not registered in Google Cloud |
| `No such file or directory: ...credentials.json` | No `[gcp_service_account]` in secrets and no `credentials.json` (step 4) |
| `PERMISSION_DENIED` / `SpreadsheetNotFound` | Spreadsheet not shared with the service account email |
| "Sua conta Google não está autorizada" | Email not in `USUARIOS_AUTORIZADOS` |
| `invalid_grant` / token expired | Delete `token.json` and run again to re-authorize |
| "Nenhum CSV encontrado" on Indicadores | `../analise_primeira_infancia/tabelas_finais/` doesn't exist next to this repo |

## Security

- Never commit `secrets.toml`, `credentials.json` or `token.json`. They're already in `.gitignore`.
- Never put `[dev]` in Streamlit Cloud secrets: it turns off login.
