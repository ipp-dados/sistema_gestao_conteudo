# Sistema de Gestão de Conteúdo
### Projeto Primeira Infância | Instituto Pereira Passos (IPP)

## 1. Apresentação

O Sistema de Gestão de Conteúdo é um protótipo desenvolvido em Python, com interface construída em Streamlit e integração com o Google Sheets, para apoiar a organização, o cadastro, a edição e a revisão de conteúdos relacionados ao projeto Primeira Infância, no Instituto Municipal de Urbanismo Pereira Passos (IPP).

A aplicação foi concebida para centralizar informações que precisam ser consultadas e atualizadas durante a elaboração de análises, textos e indicadores. Seu desenvolvimento busca reduzir a dispersão de registros, facilitar o acompanhamento das revisões e manter uma estrutura padronizada para os conteúdos.

Nesta fase, o Google Sheets funciona como repositório de dados do protótipo, permitindo validar os fluxos de leitura e gravação antes de avaliar alternativas de armazenamento e integração institucional.

O sistema está em desenvolvimento e utiliza uma planilha de testes. Não constitui, neste estágio, uma solução de produção.

## 2. Objetivos

O objetivo principal é disponibilizar uma interface para gerenciar conteúdos estruturados, com mecanismos básicos de validação e rastreabilidade.

Entre os objetivos específicos estão:

- Centralizar os registros de conteúdo em uma estrutura comum.
- Padronizar a identificação dos projetos e dos conteúdos.
- Permitir o cadastro, a consulta e a edição de informações.
- Acompanhar o estado de revisão de cada conteúdo.
- Associar textos e indicadores aos respectivos arquivos de dados.
- Importar conteúdos estruturados em JSON.
- Identificar registros já cadastrados e evitar duplicidades.
- Preservar informações existentes durante operações de atualização.
- Disponibilizar a exportação dos registros em CSV.
- Preparar a aplicação para futuras melhorias de colaboração, revisão e armazenamento.

## 3. Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Desenvolvimento da lógica da aplicação e integração entre componentes |
| Streamlit | Construção da interface web |
| Pandas | Manipulação e apresentação de dados tabulares |
| Google Sheets API | Leitura e gravação de registros na planilha |
| Gspread | Comunicação com o Google Sheets por meio de Python |
| OAuth 2.0 | Autenticação e autorização de acesso à planilha |
| JSON | Intercâmbio e validação de conteúdos estruturados |
| CSV | Associação de bases de dados e exportação de registros |
| Git e GitHub | Versionamento do código e acompanhamento do desenvolvimento |

A aplicação foi organizada em módulos para separar as responsabilidades de interface, autenticação, persistência e processamento dos arquivos.

## 4. Arquitetura da aplicação

O protótipo utiliza uma arquitetura simples, adequada à validação inicial das funcionalidades.

**Fluxo principal:**

```text
Usuário
   |
   v
Interface Streamlit
   |
   +--> Cadastro, consulta e edição
   |
   +--> Importação e validação de JSON
   |
   +--> Consulta de arquivos CSV
   |
   +--> Exportação de conteúdos
   |
   v
Camada de acesso aos dados
   |
   v
Google Sheets API / Gspread
   |
   v
Planilha Google Sheets
```

O Streamlit concentra a interação com o usuário, enquanto os módulos Python executam as operações de validação e acesso aos dados.

O Google Sheets atua como armazenamento central do protótipo. As operações de gravação são realizadas por meio da API, utilizando credenciais OAuth autorizadas.

Essa organização permite evoluir os componentes de forma independente, inclusive com a possibilidade de substituir futuramente a camada de persistência por um banco de dados institucional.

## 5. Estrutura do projeto

Os principais arquivos e módulos utilizados são:

```text
sistema_gestao_conteudo/
|
|-- app.py
|-- conexao_sheets.py
|-- repositorio_sheets.py
|-- importador_json.py
|-- leitor_csv.py
|-- modelo_conteudo.json
|-- teste_gravacao_sheets.py
|-- requirements.txt
|-- README.md
|-- .gitignore
```

### Responsabilidades dos módulos

**`app.py`**

Arquivo principal da aplicação. Implementa a interface Streamlit e organiza as páginas de navegação, cadastro, consulta, edição, indicadores, importação JSON, revisões e exportação CSV.

**`conexao_sheets.py`**

Responsável pela autenticação e pela conexão com a planilha Google Sheets utilizada pelo sistema.

**`repositorio_sheets.py`**

Concentra as operações de leitura, cadastro e atualização de conteúdos. Também executa verificações para evitar a criação de registros com identificadores já existentes.

**`importador_json.py`**

Realiza a leitura e validação de arquivos JSON, verifica duplicidades e prepara os conteúdos para gravação no formato utilizado pela planilha.

**`leitor_csv.py`**

Reúne as funções utilizadas para localizar e ler arquivos CSV associados aos indicadores.

**`modelo_conteudo.json`**

Fornece um exemplo da estrutura esperada para os arquivos de importação.

**`requirements.txt`**

Relaciona as dependências Python necessárias para executar a aplicação.

**`.gitignore`**

Define arquivos que não devem ser incluídos no versionamento, especialmente credenciais, tokens e arquivos locais de teste.

## 6. Funcionalidades implementadas

### 6.1. Painel inicial

A página inicial apresenta informações resumidas sobre os registros cadastrados, incluindo:

- Total de conteúdos.
- Quantidade de conteúdos em revisão.
- Quantidade de conteúdos aprovados.
- Indicação de conexão com o Google Sheets.

Os valores são obtidos a partir dos registros disponíveis na planilha.

### 6.2. Cadastro de conteúdos

A aplicação permite cadastrar conteúdos informando:

- Identificador do projeto.
- Identificador do conteúdo.
- Título.
- Descrição.
- Texto analítico.
- Status.
- Arquivo CSV associado, quando aplicável.

Antes da gravação, o sistema verifica o preenchimento dos campos obrigatórios do formulário.

A camada de persistência também verifica a existência de registros com a mesma combinação de identificadores, evitando cadastros duplicados em operações sequenciais.

### 6.3. Consulta e pesquisa

Os conteúdos cadastrados podem ser consultados diretamente na interface.

A aplicação disponibiliza uma tabela com os registros e um campo de pesquisa por título ou identificador do conteúdo.

Esse recurso facilita a localização de informações durante as atividades de elaboração e revisão.

### 6.4. Edição de conteúdos

O sistema permite atualizar títulos, descrições, textos, status e associações com arquivos CSV.

Antes de salvar uma edição, a aplicação compara o registro atual da planilha com a versão carregada anteriormente pelo usuário.

Caso identifique alterações externas, a atualização pode ser bloqueada para evitar a substituição inadvertida de informações.

Essa proteção é básica e não equivale a um mecanismo transacional completo para edições simultâneas.

Também foi implementada a preservação do campo `fonte_texto` quando ele não é fornecido pelo formulário de edição.

### 6.5. Controle de status

Os conteúdos utilizam três estados:

| Status | Significado |
|---|---|
| Rascunho | Conteúdo em elaboração |
| Em revisão | Conteúdo em processo de conferência |
| Aprovado | Conteúdo identificado como aprovado no registro |

A página de revisões permite visualizar os conteúdos classificados como **Em revisão**.

Nesta etapa, o controle utiliza o status registrado na planilha. Ainda não existe um fluxo completo de aprovação com identificação individual de revisores e histórico detalhado de decisões.


### 6.6. Consulta e associação de indicadores

A página de indicadores permite selecionar e visualizar arquivos CSV disponíveis no sistema, apresentando seus dados tabulares e a quantidade de registros.

Nos formulários de cadastro e edição de conteúdos, o campo `csv_associado` utiliza uma lista de seleção preenchida automaticamente com os arquivos CSV disponíveis.

O usuário pode selecionar um arquivo ou manter o conteúdo sem associação. Na edição, o sistema também preserva a referência anteriormente cadastrada.

A associação é armazenada no campo `csv_associado` do Google Sheets.

A funcionalidade foi validada por meio do cadastro e da edição de conteúdos de teste, com confirmação da gravação dos nomes dos arquivos na planilha.

Nesta versão, a associação corresponde à referência ao arquivo CSV. A integração com um catálogo institucional completo de indicadores ainda não foi implementada.


### 6.7. Exportação CSV

A aplicação permite exportar exclusivamente os conteúdos que possuem status `Aprovado` no Google Sheets.

A página de exportação apresenta a quantidade de conteúdos aprovados, disponibiliza uma pré-visualização dos registros e permite baixar o arquivo `conteudos_aprovados.csv`.

O arquivo utiliza codificação UTF-8 com BOM e mantém os campos da estrutura de conteúdos, incluindo a identificação do projeto, o status, o CSV associado e a origem do texto.

A funcionalidade foi validada com dois registros aprovados, confirmando que conteúdos em outros estados não são incluídos na exportação.

A aprovação, nesta versão, corresponde ao status registrado na planilha e não representa ainda um processo institucional de autorização para publicação.

### 7.1. Estrutura esperada

O arquivo JSON deve identificar o projeto e conter uma lista de conteúdos.

Exemplo simplificado:

```json
{
  "versao_modelo": "1.0",
  "projeto": {
    "id_projeto": "PRIMEIRA-INFANCIA",
    "nome": "Primeira Infância"
  },
  "conteudos": [
    {
      "id_conteudo": "EXEMPLO-001",
      "titulo": "População de 0 a 6 anos",
      "descricao": "Indicador de população infantil",
      "texto": "",
      "status": "Rascunho",
      "fonte_texto": "",
      "arquivos_dados": [
        "censo_sidra_populacao_0_6_sexo_2022.csv"
      ]
    }
  ]
}
```

O exemplo demonstra o formato esperado. O campo `fonte_texto` está vazio no modelo e deve ser preenchido com a origem correspondente antes de autorizar a gravação.

### 7.2. Etapas de validação

Ao receber um arquivo JSON, o sistema:

1. Verifica se o arquivo pode ser interpretado como JSON.
2. Confere a estrutura do projeto e a presença dos campos obrigatórios.
3. Verifica os tipos de dados esperados.
4. Valida os identificadores e os status permitidos.
5. Identifica identificadores repetidos dentro do próprio arquivo.
6. Compara os conteúdos com os registros existentes no Google Sheets.
7. Separa os conteúdos novos daqueles já cadastrados.
8. Exige o preenchimento de `fonte_texto` para permitir a gravação dos novos registros.
9. Apresenta os dados para conferência do usuário.
10. Solicita confirmação explícita antes de iniciar a importação.

A importação não é iniciada automaticamente após o carregamento do arquivo.

### 7.3. Prevenção de duplicidades

A identificação de duplicidades considera a combinação:

```text
id_projeto + id_conteudo
```

Essa chave permite diferenciar conteúdos pertencentes a projetos distintos.

Os registros já cadastrados são identificados durante a pré-visualização e não são selecionados para nova importação.

Antes da gravação, o sistema consulta novamente os registros existentes para reduzir o risco de duplicidades decorrentes de alterações realizadas após a primeira verificação.

### 7.4. Gravação dos conteúdos

Após a validação e a confirmação do usuário, os novos registros são preparados para a estrutura utilizada pelo Google Sheets.

Os nomes dos arquivos informados em `arquivos_dados` são reunidos no campo `csv_associado`.

O sistema adiciona os registros novos, sem substituir deliberadamente os conteúdos já existentes.

A gravação é realizada registro a registro, sem transação única para todo o lote. Caso ocorra uma falha durante a operação, parte dos conteúdos poderá já ter sido gravada. Nessa situação, é necessário conferir a planilha antes de repetir a importação.

### 7.5. Testes realizados

A funcionalidade foi testada com arquivos JSON de exemplo e uma planilha de testes.

Foram verificados:

- Reconhecimento e leitura do arquivo JSON.
- Identificação de erros de formatação.
- Bloqueio da gravação quando `fonte_texto` está vazio.
- Liberação da confirmação após o preenchimento da origem.
- Identificação de conteúdos novos e já cadastrados.
- Gravação de um novo registro no Google Sheets.
- Preservação dos registros anteriormente cadastrados.
- Identificação de duplicidade após a gravação.
- Persistência do campo `fonte_texto`.
- Preservação da origem do texto após uma edição realizada pela interface.

Os testes confirmaram o funcionamento dos fluxos avaliados, mas não substituem uma suíte automatizada de testes ou uma validação em ambiente de produção.

## 8. Estrutura dos dados no Google Sheets

A planilha de testes utiliza uma aba denominada `CONTEUDOS`.

Os registros seguem a estrutura:

| Coluna | Campo | Finalidade |
|---|---|---|
| A | `id_projeto` | Identificação do projeto |
| B | `id_conteudo` | Identificação do conteúdo |
| C | `titulo` | Título do registro |
| D | `descricao` | Descrição resumida |
| E | `texto` | Conteúdo textual ou analítico |
| F | `status` | Estado de revisão |
| G | `csv_associado` | Referência aos arquivos de dados |
| H | `atualizado_em` | Data e hora da atualização |
| I | `fonte_texto` | Identificação da origem do texto |

O campo `atualizado_em` é preenchido pela aplicação nas operações de gravação e atualização.

O campo `fonte_texto` foi incorporado para apoiar a rastreabilidade dos conteúdos, permitindo registrar a procedência das informações textuais.

A estrutura atual é adequada aos testes do protótipo, mas poderá ser revista conforme os requisitos de integração e governança de dados do IPP.

## 9. Instalação e execução

### 9.1. Pré-requisitos

Para executar o sistema, são necessários:

- Python e um ambiente virtual ou Conda.
- Git, para obtenção e versionamento do código.
- Dependências descritas em `requirements.txt`.
- Credenciais OAuth válidas e autorizadas.
- Acesso à planilha Google Sheets configurada para o protótipo.

### 9.2. Obter o projeto

Após receber autorização de acesso ao repositório privado:

```bash
git clone https://github.com/waleskamarques-eng/sistema_gestao_conteudo.git
cd sistema_gestao_conteudo
```

### 9.3. Configurar o ambiente Python

Exemplo utilizando Conda:

```bash
conda create -n gestao_conteudo python=3.11
conda activate gestao_conteudo
```

Instalar as dependências:

```bash
pip install -r requirements.txt
```

A versão de Python acima é uma referência para criação de ambiente, não uma garantia de que todas as dependências tenham sido validadas especificamente nessa versão.

### 9.4. Configurar a autenticação

O acesso ao Google Sheets utiliza OAuth 2.0.

As credenciais devem ser obtidas e configuradas de acordo com as permissões concedidas ao usuário e com as orientações do responsável pela infraestrutura.

Arquivos de credenciais e tokens não são distribuídos pelo repositório.

### 9.5. Executar a aplicação

Com o ambiente ativo e na pasta do projeto:

```bash
python -m streamlit run app.py
```

O Streamlit disponibilizará um endereço local, normalmente:

```text
http://localhost:8501
```

A aplicação depende de conexão com a planilha para carregar os conteúdos.

## 10. Segurança e integridade dos dados

O projeto adota cuidados básicos para reduzir riscos durante o desenvolvimento e os testes.


### Autenticação

O acesso à planilha Google Sheets utiliza OAuth 2.0 e depende de uma autorização válida.

Os arquivos `credentials.json`, `token.json` e outros arquivos locais de autenticação não devem ser incluídos no repositório Git. O `.gitignore` contém regras para impedir seu versionamento acidental.

Durante os testes, foi necessário renovar a autorização de acesso ao Google Sheets. Dependendo da configuração do aplicativo OAuth e da validade das credenciais, o sistema poderá solicitar uma nova autenticação.

Para uma futura utilização institucional, será necessário avaliar uma estratégia de autenticação centralizada, com armazenamento seguro das credenciais e controle de acesso dos usuários. Uma das alternativas a estudar é a utilização de uma conta de serviço do Google, conforme as políticas de segurança e infraestrutura do IPP.

A autenticação atual atende à validação do protótipo, mas ainda não representa uma solução definitiva para utilização em produção.

### Validação de entrada

A importação JSON verifica a estrutura dos arquivos e impede a gravação de conteúdos que não atendam às regras implementadas.

### Integridade dos registros

O sistema verifica duplicidades por identificador e compara versões dos registros antes de determinadas operações de atualização.

Esses mecanismos reduzem riscos, mas não substituem controles transacionais, restrições de unicidade em banco de dados ou mecanismos completos de concorrência.

### Rastreabilidade

Os campos `atualizado_em` e `fonte_texto` permitem registrar quando um conteúdo foi atualizado e qual origem textual foi informada.

A aplicação ainda não mantém um histórico completo de alterações por usuário.

### Ambiente de testes

A planilha utilizada nesta etapa é destinada à validação do protótipo.

A utilização de dados reais e a integração com infraestrutura institucional dependem de avaliação e autorização da equipe responsável.

## 11. Versionamento e colaboração

O desenvolvimento é versionado com Git e hospedado em um repositório privado no GitHub.

O versionamento permite acompanhar alterações no código, recuperar versões anteriores e organizar a evolução das funcionalidades.

Para colaboração, recomenda-se:

- Criar branches específicas para novas funcionalidades ou correções.
- Registrar commits com mensagens objetivas.
- Utilizar Pull Requests para revisão das alterações.
- Evitar commits diretamente na branch principal durante o trabalho colaborativo.
- Manter credenciais e arquivos locais fora do versionamento.
- Documentar mudanças que afetem o funcionamento do sistema.

A adoção formal dessas práticas pela equipe ainda deverá ser alinhada.

## 12. Limitações atuais

O sistema permanece em fase de protótipo e apresenta limitações conhecidas:

- O Google Sheets é utilizado como armazenamento, sem as garantias transacionais de um banco de dados relacional.
- A prevenção de duplicidades não é totalmente atômica em situações de gravações simultâneas.
- O controle de edição concorrente é básico.
- Não existe autenticação própria de usuários dentro do Streamlit.
- Não há histórico completo de revisões e aprovações por usuário.
- A importação JSON não possui mecanismo de reversão automática de um lote parcialmente gravado.
- A associação entre conteúdos e arquivos CSV ainda não constitui um catálogo institucional completo de indicadores.
- A aplicação ainda não foi validada para utilização em produção.

Essas limitações orientam as próximas etapas de desenvolvimento.

## 13. Próximas etapas

Com as funcionalidades essenciais do MVP implementadas, as próximas atividades deverão priorizar a estabilidade, a rastreabilidade e a adequação do sistema ao uso institucional.

1. **Gestão de revisões e aprovações:** implementar identificação dos responsáveis pelas revisões, registro das decisões e regras de transição entre os status.
2. **Histórico de alterações:** registrar autoria, datas e versões anteriores dos conteúdos.
3. **Validações e testes automatizados:** ampliar os testes de cadastro, edição, importação JSON, associação de indicadores e exportação CSV.
4. **Integração com indicadores:** evoluir a associação de arquivos CSV para um catálogo estruturado, com identificação das fontes e validação das referências.
5. **Autenticação e controle de acesso:** avaliar uma solução centralizada de autenticação, permissões por perfil e armazenamento seguro das credenciais.
6. **Persistência institucional:** estudar a substituição do Google Sheets por uma solução de armazenamento adequada ao uso colaborativo e às necessidades de integridade dos dados.
7. **Usabilidade:** avaliar a interface com os usuários e aprimorar os formulários, filtros e mecanismos de consulta.
8. **Validação institucional:** apresentar o MVP à equipe do IPP, registrar as observações e definir as prioridades de evolução.

As próximas implementações deverão considerar os requisitos do projeto, a infraestrutura disponível e as orientações da equipe responsável.

As prioridades deverão ser definidas conforme as necessidades do projeto e as orientações da equipe.

## 14. Situação do desenvolvimento

**Estado atual:** MVP funcional em ambiente de testes, em processo de validação para apresentação à equipe do Instituto Pereira Passos (IPP).

O sistema possui as seguintes funcionalidades implementadas:

- Painel inicial com indicadores de acompanhamento dos conteúdos.
- Cadastro, consulta, pesquisa e edição de conteúdos.
- Registro e preservação da origem dos textos (`fonte_texto`).
- Integração com o Google Sheets para leitura e atualização dos registros.
- Consulta e visualização de arquivos CSV de indicadores.
- Associação de arquivos CSV aos conteúdos por meio de listas de seleção no cadastro e na edição.
- Controle básico dos status Rascunho, Em revisão e Aprovado.
- Exportação CSV restrita aos conteúdos com status Aprovado.
- Importação de arquivos JSON com validação, pré-visualização e identificação de registros duplicados.

### Validações realizadas

Em 04/11/2026, foram realizados testes funcionais no ambiente do IPP, incluindo:

- Restabelecimento da autenticação e conexão com o Google Sheets.
- Cadastro e edição de conteúdos com associação de indicadores CSV.
- Confirmação da persistência dos registros na planilha.
- Alteração de status de Rascunho para Em revisão e, posteriormente, para Aprovado.
- Confirmação da identificação de dois conteúdos aprovados na exportação.
- Identificação de um registro já cadastrado durante a validação de importação JSON, sem nova gravação.

### Pendências para conclusão da validação do MVP

- Realizar um teste adicional de importação de um arquivo JSON com conteúdo novo.
- Executar uma verificação final do sistema após reinicialização.
- Consolidar a documentação e preparar a demonstração das funcionalidades.

O MVP utiliza uma planilha de testes e ainda não possui autenticação própria de usuários, histórico completo de revisões ou infraestrutura de produção.

A próxima etapa será apresentar o protótipo à equipe, coletar observações e definir os requisitos para sua evolução.