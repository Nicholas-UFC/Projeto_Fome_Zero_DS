import streamlit as st


def render_sidebar(df):
    """Função que renderiza a barra lateral com filtros dinâmicos de País e Culinária."""

    st.sidebar.title("🍔 Fome Zero!")
    st.sidebar.markdown("---")

    st.sidebar.markdown("### Filtros")

    # -----------------------------
    # 1. FILTRO DE PAÍSES
    # -----------------------------
    st.sidebar.markdown("**1. Escolha os países:**")
    paises_disponiveis = sorted(df["country"].unique().tolist())
    selecionar_todos_paises = st.sidebar.checkbox(
        "Selecionar Todos os Países", value=True
    )

    if selecionar_todos_paises:
        paises_selecionados = st.sidebar.multiselect(
            label="Países", options=paises_disponiveis, default=paises_disponiveis
        )
    else:
        paises_selecionados = st.sidebar.multiselect(
            label="Países", options=paises_disponiveis, default=[]
        )

    # -----------------------------
    # 2. FILTRO DE CULINÁRIAS (Em Cascata)
    # -----------------------------
    st.sidebar.markdown("**2. Escolha os tipos de culinária:**")

    # Filtra o df temporariamente só para saber quais culinárias sobraram nos países escolhidos
    if paises_selecionados:
        df_temp = df[df["country"].isin(paises_selecionados)]
    else:
        df_temp = df

    # Extrai as culinárias disponíveis baseadas no país
    culinarias_disponiveis = sorted(df_temp["cuisines"].dropna().unique().tolist())
    selecionar_todas_culinarias = st.sidebar.checkbox(
        "Selecionar Todas as Culinárias", value=True
    )

    if selecionar_todas_culinarias:
        culinarias_selecionadas = st.sidebar.multiselect(
            label="Culinárias",
            options=culinarias_disponiveis,
            default=culinarias_disponiveis,
        )
    else:
        culinarias_selecionadas = st.sidebar.multiselect(
            label="Culinárias", options=culinarias_disponiveis, default=[]
        )

    st.sidebar.markdown("---")

    # -----------------------------
    # 3. BOTÃO DE DOWNLOAD
    # -----------------------------
    with st.sidebar:
        st.markdown("### Download de Dados")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar Dados Tratados",
            data=csv,
            file_name="dados_tratados_fome_zero.csv",
            mime="text/csv",
        )

    # Retorna AS DUAS listas de escolhas do usuário
    return paises_selecionados, culinarias_selecionadas
