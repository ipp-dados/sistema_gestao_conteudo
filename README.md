# Sistema de Gestão de Conteúdo

## Sobre o projeto

Protótipo de um sistema de gestão de conteúdo desenvolvido para apoiar a organização, edição e revisão coletiva dos textos e indicadores do projeto Primeira Infância, no Instituto Municipal de Urbanismo Pereira Passos (IPP).

O sistema utiliza Python, Streamlit e Google Sheets, permitindo trabalhar com conteúdos estruturados e acompanhar seu processo de revisão.

## Funcionalidades

- Cadastro e consulta de conteúdos.
- Edição de títulos, descrições e textos.
- Associação de conteúdos a arquivos CSV.
- Controle de status: Rascunho, Em revisão e Aprovado.
- Identificação de alterações realizadas por outros usuários antes de salvar uma edição.
- Exportação dos registros para CSV.
- Painel com informações gerais dos conteúdos cadastrados.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Google Sheets API
- Gspread
- OAuth 2.0

## Estrutura do projeto

```text
sistema_gestao_conteudo/
├── app.py
├── conexao_sheets.py
├── repositorio_sheets.py
├── teste_gravacao_sheets.py
├── requirements.txt
├── README.md
└── .gitignore
```

Os arquivos `credentials.json` e `token.json` são utilizados localmente para autenticação e não devem ser versionados.

## Como executar

1. Clonar o repositório.
2. Criar e ativar um ambiente Python.
3. Instalar as dependências:

```bash
pip install -r requirements.txt
```

4. Configurar as credenciais OAuth autorizadas para acesso à planilha Google Sheets de teste.
5. Executar:

```bash
python -m streamlit run app.py
```

6. Acessar o endereço local informado pelo Streamlit, normalmente `http://localhost:8501`.

## Situação atual

O protótipo já permite cadastrar, consultar, editar e exportar conteúdos armazenados no Google Sheets.

Também foi testada a identificação de alterações realizadas diretamente na planilha durante uma edição aberta no Streamlit. A proteção implementada é básica e ainda não garante controle transacional de edições exatamente simultâneas.

A seção de indicadores permanece em desenvolvimento.

## Próximas etapas

- Validar o protótipo com a equipe do IPP.
- Aperfeiçoar o controle de usuários e revisões.
- Organizar o catálogo de indicadores e as relações com os arquivos CSV.
- Avaliar a migração para um banco de dados institucional.
- Integrar o sistema ao fluxo de trabalho da equipe.

## Segurança

As credenciais de autenticação não devem ser publicadas no GitHub. A planilha utilizada nesta fase é de teste. O acesso à infraestrutura institucional depende de autorização e validação da equipe responsável.