# Desenvolvimento orientado por especificações (SDD)

Toda mudança no sistema começa por uma especificação escrita **antes** do código. Esta pasta guarda os documentos que orientam o projeto e uma pasta para cada especificação.

## Documentos do projeto

| Arquivo | Conteúdo | Quem mantém |
|---|---|---|
| [`stakeholders_description.md`](stakeholders_description.md) | Expectativas e requisitos funcionais das partes interessadas | Equipe do projeto |
| [`roadmap.md`](roadmap.md) | Sequência de especificações, gerada a partir dos requisitos | Gerado e revisado pela equipe |
| [`constitution.md`](constitution.md) | Regras inegociáveis que toda especificação e todo código devem respeitar | Equipe; atualizado a partir do roadmap |
| [`tech-stack.md`](tech-stack.md) | Tecnologias, versões, infraestrutura e restrições técnicas | Equipe |

Ordem de dependência: `stakeholders_description.md` → `roadmap.md` → `constitution.md` → especificações.

## Especificações

Cada especificação tem:

- **Uma branch:** `spec/AAAA-MM-DD_nome-da-spec`.
- **Uma pasta:** `specs/AAAA-MM-DD_nome-da-spec/`. A data é a de criação da especificação, e o nome usa letras minúsculas sem acento, com palavras separadas por `-` ou `_`.

Cada pasta contém quatro arquivos, criados a partir de [`_templates/`](_templates/):

| Arquivo | Pergunta que responde | Fase |
|---|---|---|
| `spec.md` | **O quê** e **por quê**: problema, requisitos, critérios de aceitação | 1. Especificar |
| `plan.md` | **Como**: desenho técnico, arquivos afetados, riscos | 2. Planejar |
| `tasks.md` | **Em que ordem**: tarefas pequenas e verificáveis | 3. Implementar |
| `validation.md` | **Funcionou?** Evidências de que cada critério de aceitação foi atendido | 4. Validar |

## Branches

| Branch | Para quê |
|---|---|
| `planning` | Planejamento: documentos do projeto (`stakeholders_description.md`, `roadmap.md`, `constitution.md`, `tech-stack.md`) e o `spec.md` e o `plan.md` de cada especificação |
| `spec/AAAA-MM-DD_nome` | Implementação de **uma** especificação: código, `tasks.md` e `validation.md`. Criada a partir de `planning` depois que o `spec.md` e o `plan.md` forem aprovados |
| `main` | Versão publicada. Recebe as especificações concluídas por Pull Request |

## Fluxo

1. **Na branch `planning`**, criar a pasta a partir dos modelos:

   ```bash
   git switch planning && git pull
   cp -r specs/_templates specs/2026-12-01_exemplo
   ```

2. Escrever o `spec.md` e obter a aprovação da equipe **antes** de planejar.
3. Escrever o `plan.md`, conferindo-o contra `constitution.md` e `tech-stack.md`. Fazer commit e push na `planning`.
4. **Criar a branch da especificação** a partir de `planning`:

   ```bash
   git switch -c spec/2026-12-01_exemplo
   ```

5. Quebrar o plano em `tasks.md` e implementar uma tarefa por vez, marcando cada uma como concluída.
6. Preencher o `validation.md` com as evidências de cada critério de aceitação.
7. Abrir um Pull Request para `main`, com o link para a pasta da especificação.
8. Atualizar a situação da especificação no `roadmap.md`, na branch `planning`.

Se a implementação exigir mudanças no `spec.md` ou no `plan.md`, elas são feitas na branch da especificação e registradas no "Histórico de decisões" do `spec.md`.

Uma especificação aprovada só muda por decisão registrada no próprio `spec.md`, na seção "Histórico de decisões".

## Habilidades (skills) dos agentes por fase

Os agentes de IA que trabalham no repositório devem usar as habilidades abaixo, quando disponíveis. Os nomes são os do Claude Code; outros agentes devem usar os equivalentes.

| Fase | Habilidade | Quando usar |
|---|---|---|
| `spec.md` | (nenhuma obrigatória) | Perguntar à equipe quando um requisito for ambíguo, em vez de supor |
| `plan.md` | Modo de planejamento / agente `Plan` | Desenho técnico de mudanças que afetam vários arquivos |
| `plan.md` | `frontend-design` | Especificações com telas novas ou mudanças visuais |
| `plan.md` | `dataviz` | Especificações com gráficos ou painéis de indicadores |
| `tasks.md` | `simplify` | Ao terminar a implementação, antes da validação |
| `validation.md` | `run` | Executar o app e comprovar o funcionamento na interface |
| `validation.md` | `code-review` | Revisar o diff da branch antes do Pull Request |
| `validation.md` | `security-review` | Obrigatória em mudanças de login, credenciais, permissões ou dados pessoais |
