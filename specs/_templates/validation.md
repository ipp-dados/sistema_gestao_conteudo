# Validação: [nome]

Especificação: [`spec.md`](spec.md) · Data: · Responsável:

> Comprove cada critério de aceitação com uma evidência: comando e saída, captura de tela, registro criado no CSV local ou na planilha de testes. Nunca use a planilha compartilhada da equipe para testes de gravação.

## Habilidades usadas

- [ ] `run`: executar o app e comprovar o funcionamento na interface
- [ ] `code-review`: revisão do diff da branch
- [ ] `security-review`: **obrigatória** se a especificação mexer em login, credenciais, permissões ou dados pessoais

## Ambiente

| Item | Valor |
|---|---|
| Branch / commit | |
| Armazenamento | CSV local / planilha de testes |
| Login | `bypass_login` / Google |

## Critérios de aceitação

| Critério | Resultado | Evidência |
|---|---|---|
| CA1 | Atendido / Não atendido | |

## Regressão

O que já funcionava e continua funcionando:

- [ ] Cadastro de conteúdo
- [ ] Edição, com bloqueio quando o registro foi alterado por outra pessoa
- [ ] Importação JSON (pré-visualização, duplicidades, confirmação)
- [ ] Exportação CSV apenas de conteúdos `Aprovado`
- [ ] Login e `USUARIOS_AUTORIZADOS`

## Revisões

| Revisão | Resultado | Pendências |
|---|---|---|
| `code-review` | | |
| `security-review` | | |

## Conclusão

- [ ] Todos os critérios atendidos
- [ ] Documentação atualizada
- [ ] Pronto para Pull Request
