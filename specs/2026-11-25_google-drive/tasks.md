# Tarefas da exportação CSV para o Google Drive

- [x] Implementar cliente Drive v3 e diagnóstico inicial, entregues no commit `11cc569`.
- [x] Reaproveitar o CSV do download e criar um arquivo em memória na raiz de Meu Drive a cada envio explícito.
- [x] Exibir resultado, manter o download disponível e substituir o diagnóstico temporário pelo envio na página de exportação.
- [x] Atualizar a documentação funcional e a política de privacidade.
- [x] Adicionar testes simulados da criação, do conteúdo exportado e das falhas de envio.
- [x] Executar os seis testes simulados e registrar a revisão de código e segurança e as evidências locais em `validation.md`.
- [x] Registrar a decisão de separar DEV, HML e PROD e a ordem de implantação.
- [x] Externalizar o ID da planilha para `[sheets].spreadsheet_id` e verificar ID configurado, configuração ausente ou inválida e modo CSV local. Executar a regressão da exportação.
- [ ] Preparar projeto Google, consentimento, cliente web, conta de serviço e planilha fictícia dedicados à HML.
- [ ] Implantar `app.py` da branch `feature/google-drive` em um novo app do Community Cloud com URL e Secrets próprios.
- [ ] Validar OAuth real, CSV, destino, link, bloqueio durante o envio, falhas e controle de acesso. Registrar as evidências de CA1 a CA6.
