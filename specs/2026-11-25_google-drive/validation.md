# Validação da exportação CSV para o Google Drive

**Situação** · Testes locais concluídos. Validação final no Streamlit Community Cloud pendente.

Em 25/11/2026, `python -m unittest discover -s tests -v` executou seis testes com sucesso no Streamlit 1.58.0. A execução foi repetida após isolar a lista de acesso nos testes com endereços fictícios do domínio `example.com`. Os testes de interface usaram `AppTest`, registros sintéticos e cliente Drive simulado. Nenhum arquivo real foi criado e nenhuma planilha foi alterada.

| Critério | Evidência local | Pendência no Community Cloud |
|---|---|---|
| CA1 | Bytes enviados iguais aos do download, com aprovados e sem rascunhos. | Comparar o CSV baixado com o arquivo criado usando dados de teste. |
| CA2 | Abrir a página, reexecutá-la e navegar com uma lista sem aprovados não chamou a criação. | Verificar pelo navegador que clicar no download não cria um arquivo. |
| CA3 | A requisição omitiu a pasta pai e a interface exibiu o link retornado. Outro teste verificou o link alternativo quando a API devolve apenas o ID. | Confirmar OAuth real, criação na raiz e abertura do link. |
| CA4 | Sessão sem token manteve o download. Falhas simuladas de permissão e timeout geraram mensagens sem expor o erro bruto. | Confirmar o comportamento na implantação com uma conta de teste. |
| CA5 | Uma conta fora da lista foi bloqueada antes da navegação, da leitura dos registros e do envio. | Confirmar o bloqueio com uma conta de teste fora da lista. |
| CA6 | Dois cliques em envios sucessivos causaram duas chamadas de criação. O nome tem data e hora. Uma reexecução sem clique não causou outra chamada. | Verificar o botão desabilitado durante um envio com resposta atrasada. |

## Revisão de código e segurança

Em 26/11/2026, `python -m unittest discover -s tests -v` passou com **9 testes** em Python 3.12.10 e Streamlit 1.67.0. Os seis testes de regressão do Drive passaram e os três testes da configuração demonstraram que:

- O modo CSV local abre um arquivo temporário sem exigir ID nem autenticar no Google.
- Com ID configurado, o cliente simulado abre a planilha correspondente e seleciona a aba `CONTEUDOS`.
- Se a configuração estiver ausente ou o ID for vazio ou de tipo inválido, a conexão falha com uma mensagem de configuração antes da autenticação.

O modelo de Secrets foi validado como TOML. Os testes não acessaram serviços reais nem alteraram configurações de PROD. A validação de OAuth e Drive reais segue pendente na HML.

- A verificação de acesso precede a tela de exportação. O token permanece no cliente autenticado e a interface exibe mensagens fixas para falhas.
- A criação usa `drive.file`, sem chamadas para modificar permissões de compartilhamento. A operação ocorre em memória e não altera a planilha.
- `git diff --check` passou. Os arquivos de credenciais locais permaneceram fora do índice Git.

## Ambiente para a validação final

Usar uma implantação de teste no Streamlit Community Cloud direcionada à branch autorizada, com OAuth de conta de teste, URI de callback da implantação e dados fictícios em uma planilha de teste. As credenciais devem ser configuradas no painel de Secrets do Cloud. Registrar o resultado de cada pendência na tabela, sem copiar credenciais para o repositório.
