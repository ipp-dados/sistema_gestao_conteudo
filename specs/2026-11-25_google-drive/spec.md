# Especificação da exportação CSV para o Google Drive

| Campo | Valor |
|---|---|
| Pasta | `specs/2026-11-25_google-drive` |
| Branch com a implementação inicial | `feature/google-drive` |
| Situação | Aprovada para planejamento |
| Origem | Integração em andamento identificada no [roadmap](../roadmap.md) |

## Contexto e objetivo

A página **Exportação CSV** permite baixar os conteúdos aprovados. A proposta é oferecer também o envio desse CSV ao Google Drive da conta autenticada, mediante uma ação explícita na página de exportação.

## Trabalho já realizado

- O commit `11cc569` adicionou `conexao_drive.py`, que usa o token de acesso do login Google para criar o cliente da API Drive v3.
- O mesmo commit adicionou `google-api-python-client` às dependências e incluiu em `app.py` um diagnóstico temporário que consulta o perfil com `about.get` e informa sucesso ou falha.
- A configuração local já documenta o escopo `drive.file` e a exposição do token de acesso. A página de exportação já gera o CSV de aprovados.
- A existência desse código foi verificada por inspeção. A execução com OAuth real e o envio de um arquivo ainda precisam de evidência.

## Usuários afetados

Pessoas autorizadas a acessar o sistema que precisam guardar no Google Drive os conteúdos aprovados para uso editorial.

## Requisitos

| ID | Requisito | Prioridade |
|---|---|---|
| R1 | Enviar ao Drive o mesmo CSV de conteúdos aprovados disponível para download, somente quando o usuário solicitar o envio. | Essencial |
| R2 | Informar o resultado do envio, oferecer o link **Abrir no Google Drive** após o sucesso e preservar o download local em caso de falha ou indisponibilidade da integração. | Essencial |
| R3 | Usar a conta Google autenticada e o escopo `drive.file`, sem exibir ou registrar o token. | Essencial |
| R4 | Criar um novo CSV na raiz de **Meu Drive** a cada envio explícito, com data e hora no nome, e impedir outro envio pela mesma interface enquanto o primeiro estiver em andamento. | Essencial |

## Fora do escopo

- Escolha de pasta, atualização de arquivos existentes, sincronização automática, alteração de permissões de compartilhamento e mudanças no armazenamento editorial em Google Sheets.

## Critérios de aceitação e testes previstos

| ID | Resultado esperado | Evidência prevista |
|---|---|---|
| CA1 | Com registros em estados diferentes, o CSV enviado corresponde ao download e contém apenas os aprovados. | Teste automatizado com registros sintéticos e API simulada, comparando os bytes dos dois CSVs. |
| CA2 | Ao abrir a página, ao baixar o CSV ou quando não há aprovados, nenhum arquivo é enviado ao Drive. | Testes automatizados de interface com API simulada e verificação das chamadas de criação de arquivo. |
| CA3 | Ao solicitar um envio com conta autorizada e permissão válida, a interface confirma a criação na raiz de **Meu Drive** e oferece um link que abre o arquivo criado. | Teste de interface com API simulada e teste manual com conta autorizada e dados sintéticos, incluindo a conferência do destino e do link. |
| CA4 | Sem token, com permissão insuficiente ou com a API indisponível, a interface informa a falha, mantém o download e preserva o sigilo do token. | Testes automatizados com falhas simuladas e revisão de segurança das mensagens e dos registros. |
| CA5 | Uma conta fora da lista de usuários autorizados não acessa a exportação nem inicia um envio. | Teste de controle de acesso e revisão da ordem entre a verificação de acesso e a ação de envio. |
| CA6 | Enquanto o envio está em andamento, a interface impede uma segunda solicitação. Dois envios explícitos sucessivos criam dois arquivos, cada um com data e hora no nome. | Teste com API simulada para verificar duas criações após duas ações concluídas e teste manual com resposta atrasada para verificar o bloqueio durante o envio. |

## Regras da constituição envolvidas

- Seções 2 e 8, aprovação e evidência para cada critério.
- Seções 4 e 5, controle de acesso, credenciais, revisão de segurança e privacidade.
- Seções 6.6 e 7.4–7.5, exportação apenas de aprovados, compatibilidade com o Streamlit Cloud e comportamento compartilhado entre as duas interfaces.

## Histórico de decisões

| Data | Registro | Motivo |
|---|---|---|
| 2026-11-25 | O rascunho incorpora a conexão inicial existente e define critérios de teste para a continuação da feature. | Aproveitar o trabalho da branch e estabelecer a evidência necessária para concluir a integração. |
| 2026-11-25 | Aprovados a raiz de **Meu Drive** como destino, a criação de um novo CSV por envio explícito com data e hora no nome e o link **Abrir no Google Drive** após o sucesso. | Definir o comportamento da primeira entrega. |
