import os
import sys

import pandas as pd
import plotly.express as px
from utils.sidebar import render_sidebar

import streamlit as st

# 1. Configuração da página
st.set_page_config(page_title="Visão Culinárias", page_icon="🍽️", layout="wide")

# 2. Ajuste de diretório para importar utilidades[cite: 4]
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from utils.add_country_name import add_country_name
from utils.adjust_cuisines import adjust_cuisines
from utils.clean_data import clean_data
from utils.convert_to_usd import convert_to_usd
from utils.create_color_name import create_color_name
from utils.create_price_tye import create_price_tye
from utils.create_unique_restaurant_name import create_unique_restaurant_name
from utils.rename_columns import rename_columns


# ==========================================
# CARREGAMENTO E LIMPEZA DE DADOS
# ==========================================
@st.cache_data
def load_data():
    """Carrega o dataset e aplica todo o pipeline de limpeza do projeto."""
    file_path = os.path.join("..", "database", "zomato.csv")
    df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")

    df = (
        df.pipe(rename_columns)
        .pipe(add_country_name)
        .pipe(clean_data)
        .pipe(convert_to_usd)
        .pipe(create_price_tye)
        .pipe(create_color_name)
        .pipe(adjust_cuisines)
        .pipe(create_unique_restaurant_name)
    )
    return df


df = load_data()

# 1. Carrega os dados normalmente
df = load_data()

# 2. Chama a barra lateral e guarda os países escolhidos na variável
paises_selecionados, culinarias_selecionadas = render_sidebar(df)

# 3. FILTRA O DATAFRAME COM BASE NA ESCOLHA DO USUÁRIO
df = df[df["country"].isin(paises_selecionados)]
df = df[df["cuisines"].isin(culinarias_selecionadas)]

# (Opcional de segurança) Se o usuário desmarcar tudo, evitamos que quebre mostrando um aviso:
if df.empty:
    st.warning(
        "⚠️ Por favor, selecione pelo menos um país na barra lateral para visualizar os dados."
    )
    st.stop()  # Para a execução aqui caso esteja vazio

# ==========================================
# CONSTRUÇÃO DO PAINEL (VISUAL)
# ==========================================
st.title("🍽️ Visão Tipos Culinários")

# ---------------------------------------------------------
# SEÇÃO 1: MÉTRICAS DOS MELHORES RESTAURANTES[cite: 4]
# ---------------------------------------------------------
st.markdown("### Melhores Restaurantes dos Principais Tipos Culinários")

# 1. Pegando os 5 tipos culinários com MAIS restaurantes
top_5_culinarias = df["cuisines"].value_counts().head(5).index

# 2. Filtrando a base e ordenando (Desempate por votos)
df_top_5 = df[df["cuisines"].isin(top_5_culinarias)]
df_top_5_ordenado = df_top_5.sort_values(
    by=["cuisines", "aggregate_rating", "votes"], ascending=[True, False, False]
)

# 3. Pegando o melhor restaurante de cada culinária
melhores_restaurantes = df_top_5_ordenado.groupby("cuisines").first().reset_index()

# 4. Criando as 5 colunas no Streamlit
colunas = st.columns(5)
for index, row in melhores_restaurantes.iterrows():
    with colunas[index]:
        st.metric(
            label=f"{row['cuisines']}: {row['restaurant_name']}",
            value=f"{row['aggregate_rating']}/5.0",
            help=f"Total de Votos: {row['votes']}",
        )

st.markdown("---")

# ---------------------------------------------------------
# SEÇÃO 2: TABELA GERAL (Top 10 Restaurantes)[cite: 4]
# ---------------------------------------------------------
st.markdown("### Top 10 Restaurantes")

colunas_selecionadas = [
    "restaurant_name",
    "country",
    "city",
    "cuisines",
    "average_cost_for_two_cost_in_usd",
    "aggregate_rating",
    "votes",
]
df_tabela = df[colunas_selecionadas]

# Ordenando: 1º nota, 2º votos
df_ordenado = df_tabela.sort_values(
    by=["aggregate_rating", "votes"], ascending=[False, False]
)

# Tradução das colunas
traducao_colunas = {
    "restaurant_name": "Nome do Restaurante",
    "country": "País",
    "city": "Cidade",
    "cuisines": "Tipo de Culinária",
    "average_cost_for_two_cost_in_usd": "Preço para Dois (USD)",
    "aggregate_rating": "Avaliação Média",
    "votes": "Total de Votos",
}
df_traduzido = df_ordenado.rename(columns=traducao_colunas).head(10)

# Exibe a tabela no Streamlit (hide_index esconde os números das linhas originais)
st.dataframe(df_traduzido, use_container_width=True, hide_index=True)

st.markdown("---")

# ---------------------------------------------------------
# SEÇÃO 3: GRÁFICOS DE CULINÁRIAS (Lado a Lado)[cite: 4]
# ---------------------------------------------------------
col1, col2 = st.columns(2)

# Preparando o dataframe base para os gráficos (Agrupamento e arredondamento)
estatisticas_culinarias = (
    df.groupby("cuisines")
    .agg(
        media_avaliacao=("aggregate_rating", "mean"),
        quantidade_avaliacoes=("votes", "sum"),
    )
    .reset_index()
)
# Arredondando para garantir que o desempate pelos votos funcione perfeitamente
estatisticas_culinarias["media_avaliacao"] = estatisticas_culinarias[
    "media_avaliacao"
].round(2)

with col1:
    # Gráfico: Top 10 Melhores Culinárias[cite: 4]
    melhores_10 = estatisticas_culinarias.sort_values(
        by=["media_avaliacao", "quantidade_avaliacoes"], ascending=[False, False]
    ).head(10)

    fig1 = px.bar(
        melhores_10,
        x="cuisines",
        y="media_avaliacao",
        title="Top 10 Melhores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "media_avaliacao": "Nota Média",
            "quantidade_avaliacoes": "Total de Votos",
        },
        text_auto=".2f",
        hover_data=["quantidade_avaliacoes"],
        color="cuisines",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig1.update_layout(
        xaxis_tickangle=-45,
        title_x=0.5,
        showlegend=False,
        xaxis_categoryorder="total descending",
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Gráfico: Top 10 Piores Culinárias[cite: 4]
    piores_10 = estatisticas_culinarias.sort_values(
        by=["media_avaliacao", "quantidade_avaliacoes"],
        ascending=[
            True,
            False,
        ],  # True para pegar a menor nota, False para usar o maior número de votos no desempate
    ).head(10)

    fig2 = px.bar(
        piores_10,
        x="cuisines",
        y="media_avaliacao",
        title="Top 10 Piores Tipos de Culinárias (Desempate: Mais Votos)",
        labels={
            "cuisines": "Tipo de Culinária",
            "media_avaliacao": "Nota Média",
            "quantidade_avaliacoes": "Total de Votos",
        },
        text_auto=".2f",
        hover_data=["quantidade_avaliacoes"],
        color="cuisines",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    # A ordem aqui é por array para garantir que fique ordenado do pior para o "menos pior"
    fig2.update_layout(
        xaxis_tickangle=-45,
        title_x=0.5,
        showlegend=False,
        xaxis_categoryorder="array",
        xaxis_categoryarray=piores_10["cuisines"],
    )
    st.plotly_chart(fig2, use_container_width=True)
