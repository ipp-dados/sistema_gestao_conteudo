
import pandas as pd
import streamlit as st
from leitor_csv import listar_csvs, ler_csv
from importador_json import importar_json, verificar_duplicidades

from repositorio_sheets import (
    listar_conteudos,
    cadastrar_conteudo,
    atualizar_conteudo,
)

st.set_page_config(
    page_title="Gestão de Conteúdo | Primeira Infância",
    page_icon="📚",
    layout="wide",
)

st.title("Sistema de Gestão de Conteúdo")
st.caption(
    "Projeto Primeira Infância | Protótipo com Google Sheets"
)

pagina = st.sidebar.radio(
    "Navegação",
    [
        "Início",
        "Conteúdos",
        "Indicadores",
        "Importação JSON",
        "Revisões",
        "Exportação CSV",
    ],
)

# Exibe mensagens após recarregar a página.
if "mensagem_sucesso" in st.session_state:
    st.success(st.session_state.pop("mensagem_sucesso"))

try:
    conteudos = listar_conteudos()
except Exception as erro:
    st.error(
        f"Não foi possível acessar o Google Sheets: {erro}"
    )
    st.stop()


if pagina == "Início":
    st.subheader("Painel inicial")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Conteúdos cadastrados",
        len(conteudos),
    )

    col2.metric(
        "Em revisão",
        sum(
            c["status"] == "Em revisão"
            for c in conteudos
        ),
    )

    col3.metric(
        "Aprovados",
        sum(
            c["status"] == "Aprovado"
            for c in conteudos
        ),
    )

    st.success("Sistema conectado ao Google Sheets.")


elif pagina == "Conteúdos":
    st.subheader("Cadastro de conteúdos")

    with st.form("cadastro", clear_on_submit=True):
        id_projeto = st.text_input(
            "ID do projeto",
            value="PRIMEIRA-INFANCIA",
        )

        id_conteudo = st.text_input(
            "ID do conteúdo",
            placeholder="CONT-003",
        )

        titulo = st.text_input("Título")

        descricao = st.text_area("Descrição")

        texto = st.text_area(
            "Texto analítico",
            height=180,
        )

        status = st.selectbox(
            "Status",
            ["Rascunho", "Em revisão", "Aprovado"],
        )

        csv_associado = st.text_input(
            "CSV associado (opcional)"
        )

        salvar = st.form_submit_button(
            "Salvar conteúdo"
        )

    if salvar:
        dados = {
            "id_projeto": id_projeto.strip(),
            "id_conteudo": id_conteudo.strip(),
            "titulo": titulo.strip(),
            "descricao": descricao.strip(),
            "texto": texto,
            "status": status,
            "csv_associado": csv_associado.strip(),
        }

        if not all(
            [
                dados["id_projeto"],
                dados["id_conteudo"],
                dados["titulo"],
                dados["descricao"],
            ]
        ):
            st.error(
                "Preencha os IDs, o título e a descrição."
            )
        else:
            try:
                cadastrar_conteudo(dados)

                st.session_state["mensagem_sucesso"] = (
                    "Conteúdo salvo no Google Sheets!"
                )

                st.rerun()

            except Exception as erro:
                st.error(str(erro))

    st.divider()
    st.subheader("Consultar conteúdos")

    if conteudos:
        busca = st.text_input(
            "Buscar por título ou ID"
        )

        filtrados = [
            c
            for c in conteudos
            if busca.lower()
            in (
                str(c["titulo"])
                + " "
                + str(c["id_conteudo"])
            ).lower()
        ]

        st.dataframe(
            pd.DataFrame(filtrados),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.subheader("Editar conteúdo")

        opcoes = {
            (
                f"{c['id_projeto']} | "
                f"{c['id_conteudo']} - "
                f"{c['titulo']}"
            ): c
            for c in conteudos
        }

        escolha = st.selectbox(
            "Selecione um conteúdo",
            list(opcoes.keys()),
        )

        atual = opcoes[escolha]

        # Guarda a versão original ao abrir a edição.
        chave_registro = (
            f"{atual['id_projeto']}|"
            f"{atual['id_conteudo']}"
        )

        chave_original = (
            f"original_{chave_registro}"
        )

        if (
            st.session_state.get("registro_selecionado")
            != chave_registro
        ):
            st.session_state["registro_selecionado"] = (
                chave_registro
            )
            st.session_state[chave_original] = atual.copy()

        registro_original = (
            st.session_state[chave_original]
        )

        with st.form(
            f"edicao_{chave_registro}"
        ):
            novo_titulo = st.text_input(
                "Editar título",
                value=registro_original["titulo"],
            )

            nova_descricao = st.text_area(
                "Editar descrição",
                value=registro_original["descricao"],
            )

            novo_texto = st.text_area(
                "Editar texto",
                value=registro_original["texto"],
                height=180,
            )

            status_opcoes = [
                "Rascunho",
                "Em revisão",
                "Aprovado",
            ]

            status_atual = str(
                registro_original["status"]
            )

            if status_atual not in status_opcoes:
                status_atual = "Rascunho"

            novo_status = st.selectbox(
                "Editar status",
                status_opcoes,
                index=status_opcoes.index(
                    status_atual
                ),
            )

            novo_csv = st.text_input(
                "Editar CSV associado",
                value=registro_original[
                    "csv_associado"
                ],
            )

            atualizar = st.form_submit_button(
                "Atualizar conteúdo"
            )

        if atualizar:
            if (
                not novo_titulo.strip()
                or not nova_descricao.strip()
            ):
                st.error(
                    "Título e descrição são obrigatórios."
                )
            else:
                dados_atualizados = {
                    "id_projeto": atual["id_projeto"],
                    "id_conteudo": atual["id_conteudo"],
                    "titulo": novo_titulo.strip(),
                    "descricao": nova_descricao.strip(),
                    "texto": novo_texto,
                    "status": novo_status,
                    "csv_associado": novo_csv.strip(),
                }

                try:
                    atualizar_conteudo(
                        dados_atualizados,
                        registro_original,
                    )

                    st.session_state.pop(
                        chave_original, None
                    )
                    st.session_state.pop(
                        "registro_selecionado", None
                    )

                    st.session_state[
                        "mensagem_sucesso"
                    ] = (
                        "Conteúdo atualizado "
                        "no Google Sheets!"
                    )

                    st.rerun()

                except ValueError as erro:
                    st.error(str(erro))

                except Exception as erro:
                    st.error(
                        f"Erro ao atualizar: {erro}"
                    )
    else:
        st.info(
            "Nenhum conteúdo encontrado."
        )


elif pagina == "Indicadores":
    st.subheader("Indicadores da Primeira Infância")

    st.write("Consulte os CSVs gerados pelos pipelines do projeto.")

    try:
        arquivos = listar_csvs()

        if arquivos:
            arquivo_selecionado = st.selectbox(
                "Selecione um arquivo CSV:",
                arquivos
            )

            dados = ler_csv(arquivo_selecionado)

            st.success(f"Arquivo carregado: {arquivo_selecionado}")

            st.write(f"Total de registros: {len(dados)}")

            st.dataframe(
                dados,
                width="stretch",
                hide_index=True
            )
        else:
            st.info("Nenhum CSV encontrado.")

    except (
        FileNotFoundError,
        ValueError,
        OSError,
        UnicodeError,
        pd.errors.ParserError
    ) as erro:
        st.error(f"Não foi possível carregar os CSVs: {erro}")


elif pagina == "Importação JSON":
    st.subheader("Importação de conteúdos por JSON")

    st.write(
        "Carregue e valide os conteúdos padronizados "
        "antes de importá-los para o sistema."
    )

    arquivo_json = st.file_uploader(
        "Selecione um arquivo JSON",
        type=["json"]
    )

    if arquivo_json is not None:
        import tempfile
        from pathlib import Path

        caminho_temporario = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".json",
                delete=False
            ) as arquivo:
                arquivo.write(arquivo_json.getvalue())
                caminho_temporario = Path(arquivo.name)

            dados = importar_json(caminho_temporario)

            st.success("JSON validado com sucesso!")

            st.write(
                "Projeto:",
                dados["projeto"]["id_projeto"]
            )

            st.write(
                "Total de conteúdos:",
                len(dados["conteudos"])
            )

            st.dataframe(
                pd.DataFrame(dados["conteudos"]),
                width="stretch",
                hide_index=True
            )

            # Compara os conteúdos do JSON com o Google Sheets.
            st.subheader("Verificação de duplicidades")

            novos, existentes = verificar_duplicidades(
                dados,
                conteudos
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Conteúdos novos",
                len(novos)
            )

            col2.metric(
                "Já cadastrados",
                len(existentes)
            )

            if novos:
                st.write("Conteúdos novos:")
                st.dataframe(
                    pd.DataFrame(novos),
                    width="stretch",
                    hide_index=True
                )

            if existentes:
                st.warning(
                    "Estes conteúdos já existem no Google Sheets "
                    "e não devem ser cadastrados novamente."
                )

                st.dataframe(
                    pd.DataFrame(existentes),
                    width="stretch",
                    hide_index=True
                )

            st.info(
                "Modo de pré-visualização: "
                "nenhum conteúdo foi gravado no Google Sheets."
            )

        except (ValueError, OSError, UnicodeError) as erro:
            st.error(f"Erro na importação: {erro}")

        finally:
            if caminho_temporario is not None:
                caminho_temporario.unlink(missing_ok=True)


elif pagina == "Revisões":
    st.subheader("Controle de revisões")

    em_revisao = [
        c
        for c in conteudos
        if c["status"] == "Em revisão"
    ]

    if em_revisao:
        st.dataframe(
            pd.DataFrame(em_revisao),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info(
            "Nenhum conteúdo em revisão."
        )


elif pagina == "Exportação CSV":
    st.subheader("Exportação de conteúdos")

    if conteudos:
        df = pd.DataFrame(conteudos)

        st.download_button(
            "Baixar CSV",
            data=df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="conteudos_teste.csv",
            mime="text/csv",
        )
    else:
        st.info(
            "Nenhum conteúdo disponível para exportação."
        )
