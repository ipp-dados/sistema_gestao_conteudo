# Constituição do projeto

Regras que toda especificação, todo plano e todo código devem respeitar. Um plano que contrarie uma regra precisa de uma emenda aprovada pela equipe **antes** da implementação.

**Situação:** versão inicial, com as regras já conhecidas do código e da documentação. Os princípios de produto (seção 1) serão completados a partir do [`roadmap.md`](roadmap.md), depois que os requisitos forem registrados em [`stakeholders_description.md`](stakeholders_description.md).

## 1. Princípios de produto

> A preencher a partir do roadmap: público, objetivos e prioridades que orientam as decisões.

## 2. Processo de desenvolvimento

1. Nenhuma mudança de comportamento sem especificação. Toda funcionalidade ou correção relevante tem uma pasta em `specs/` e uma branch `spec/AAAA-MM-DD_nome` (ver [`README.md`](README.md)).
2. O `spec.md` é aprovado antes do `plan.md`, e o `plan.md` antes da implementação.
3. Nada entra em `main` sem Pull Request e sem `validation.md` preenchido.
4. Não se fazem commits diretamente em `main`.
5. Mudanças que afetem o funcionamento do sistema atualizam a documentação (`README.md`, `SETUP_LOCAL.md` ou `AGENTS.md`) no mesmo Pull Request.

## 3. Idioma

1. Código (nomes de funções e variáveis), comentários, textos da interface, mensagens de erro e documentação são escritos em português do Brasil.
2. Mensagens de commit e Pull Requests seguem o mesmo idioma.

## 4. Segurança e credenciais

1. Nunca versionar `secrets.toml`, `credentials.json`, `token.json`, chaves de conta de serviço ou qualquer outra credencial. Apenas os modelos `*.example`, com valores fictícios, vão para o repositório.
2. A seção `[dev]` do `secrets.toml` (login ignorado, armazenamento CSV) é exclusiva do ambiente local e nunca é configurada no Streamlit Cloud.
3. O acesso ao sistema exige login Google, e o e-mail precisa estar em `USUARIOS_AUTORIZADOS` (`app.py`).
4. Credenciais são compartilhadas apenas por canais seguros da equipe, nunca por e-mail ou chat aberto.
5. Mudanças em login, credenciais, permissões ou dados pessoais passam por revisão de segurança antes do merge.

## 5. Dados e privacidade

1. O sistema trabalha prioritariamente com dados públicos. Não são inseridos dados pessoais sensíveis, sigilosos ou institucionais de acesso restrito sem autorização e proteção adequadas ([`POLITICA_PRIVACIDADE.md`](../POLITICA_PRIVACIDADE.md)).
2. Uma funcionalidade que mude quais dados são coletados ou como são compartilhados atualiza a política de privacidade no mesmo Pull Request.
3. O uso de dados reais e a integração com a infraestrutura institucional do IPP dependem de autorização da equipe responsável.
4. A planilha atual é de testes e não é tratada como fonte oficial.

## 6. Integridade dos registros

1. Cada conteúdo é identificado pelo par (`id_projeto`, `id_conteudo`), que não pode se repetir.
2. A gravação nunca sobrescreve uma alteração feita por outra pessoa. Antes de salvar uma edição, o registro atual é comparado com a versão aberta no formulário, e a gravação é recusada se houver diferença.
3. O campo `atualizado_em` é preenchido pelo sistema, em UTC e no formato ISO 8601, nunca pelo usuário.
4. A origem do texto (`fonte_texto`) é obrigatória na importação e é preservada nas edições.
5. Importações exigem pré-visualização e confirmação explícita do usuário. Nada é gravado automaticamente ao carregar um arquivo.
6. Os status válidos são `Rascunho`, `Em revisão` e `Aprovado`. Somente conteúdos `Aprovado` são exportados.

## 7. Arquitetura

1. O acesso aos dados passa exclusivamente por `repositorio_sheets.py`. A interface não acessa a planilha diretamente.
2. Toda forma de armazenamento implementa o mesmo contrato usado pelo repositório (hoje `get_all_records`, `append_row`, `update` e `title`). Um método novo no contrato é implementado em todas as formas de armazenamento, inclusive no CSV local (`armazenamento_local.py`).
3. A ordem das colunas (`COLUNAS`) só muda com uma especificação que inclua a migração dos dados existentes.
4. O sistema precisa funcionar no Streamlit Cloud, que não tem disco persistente. Nada que precise ser guardado pode depender de arquivos locais em produção.
5. Mudanças de comportamento compartilhado entre `app.py` e `app_visual_demo.py` são feitas nos dois arquivos, enquanto ambos existirem.

## 8. Qualidade e validação

1. Cada critério de aceitação do `spec.md` tem uma evidência correspondente no `validation.md`.
2. Testes que gravam dados usam o armazenamento CSV local ou uma planilha de testes própria, nunca a planilha compartilhada da equipe.

## 9. Agentes de IA

1. Quando houver dúvida sobre requisito, escopo, prioridade ou qualquer decisão que caiba à equipe, o agente pergunta antes de agir, em vez de supor. Para isso, usa a ferramenta de perguntas estruturadas do próprio agente (`AskUserQuestion` no Claude Code; o equivalente em outros agentes).
2. As perguntas são agrupadas: o agente reúne todas as dúvidas pendentes e as faz de uma só vez, em vez de interromper o trabalho a cada dúvida.
3. Não se pergunta o que pode ser respondido pelo código, pela documentação ou por estas regras.

## Emendas

| Data | Regra | Mudança | Motivo | Aprovada por |
|---|---|---|---|---|
| 2026-11-24 | 9.1–9.3 | Inclusão da seção "Agentes de IA" | Evitar suposições dos agentes e reduzir interrupções | leoaucar |
