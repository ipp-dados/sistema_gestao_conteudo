# Plano: [nome]

Especificação: [`spec.md`](spec.md) · Situação: Rascunho / Aprovado

> Descreva **como** atender à especificação. Escreva o plano só depois que o `spec.md` for aprovado.

## Habilidades usadas

Marque as que se aplicam (ver [`specs/README.md`](../README.md#habilidades-skills-dos-agentes-por-fase)):

- [ ] Modo de planejamento / agente `Plan`: mudança que afeta vários arquivos
- [ ] `frontend-design`: telas novas ou mudanças visuais
- [ ] `dataviz`: gráficos ou painéis de indicadores

## Abordagem

Resumo da solução e por que foi escolhida.

## Alternativas consideradas

| Alternativa | Por que não foi escolhida |
|---|---|
| | |

## Mudanças por arquivo

| Arquivo | Mudança |
|---|---|
| | |

## Dados e armazenamento

Mudanças em colunas, formatos ou no contrato de armazenamento (`get_all_records`, `append_row`, `update`). Se houver, descreva a migração dos dados existentes e a atualização do CSV local (`armazenamento_local.py`).

## Configuração e credenciais

Novas seções ou chaves no `secrets.toml`, novas APIs ou escopos do Google. Atualize `secrets.toml.example` e `SETUP_LOCAL.md`.

## Conferência com a constituição e o tech stack

- [ ] Respeita [`constitution.md`](../constitution.md). Se não respeitar, indique a emenda necessária.
- [ ] Usa apenas tecnologias de [`tech-stack.md`](../tech-stack.md). Se precisar de outra, atualize o arquivo neste plano.
- [ ] Funciona no Streamlit Cloud (sem disco persistente).
- [ ] Se mudar comportamento compartilhado, altera `app.py` e `app_visual_demo.py`.

## Riscos

| Risco | Mitigação |
|---|---|
| | |

## Estratégia de validação

Como cada critério de aceitação será comprovado: teste manual na interface, `streamlit.testing`, script ou teste automatizado.
