import os
import sys

import pandas as pd
import plotly.express as px
from utils.sidebar import render_sidebar

import streamlit as st

# 1. Configuração da página
st.set_page_config(page_title="Visão Países", page_icon="🌎", layout="wide")

# 2. Ajuste de diretório para importar utilidades
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
st.title("🌎 Visão Países")
st.markdown("---")

# ---------------------------------------------------------
# LINHA 1: TELA CHEIA (Gráfico 1 - Restaurantes por País)[cite: 3]
# ---------------------------------------------------------
restaurantes_por_pais = (
    df.groupby("country")
    .size()
    .reset_index(name="quantidade_restaurantes")
    .sort_values(by="quantidade_restaurantes", ascending=False)
)
top_10_paises = restaurantes_por_pais.head(10)

fig1 = px.bar(
    top_10_paises,
    x="country",
    y="quantidade_restaurantes",
    title="Top 10 Quantidade de Restaurantes Registrados por País",
    labels={"country": "País", "quantidade_restaurantes": "Quantidade de Restaurantes"},
    text_auto=".0f",
    color="country",
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig1.update_layout(
    xaxis_tickangle=0,
    title_x=0,
    showlegend=False,
    xaxis_categoryorder="total descending",
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------
# LINHA 2: TELA CHEIA (Gráfico 2 - Cidades por País)[cite: 3]
# ---------------------------------------------------------
cidades_por_pais = (
    df.groupby("country")["city"]
    .nunique()
    .reset_index(name="quantidade_cidades")
    .sort_values(by="quantidade_cidades", ascending=False)
)
top_10_paises_cidades = cidades_por_pais.head(10)

fig2 = px.bar(
    top_10_paises_cidades,
    x="country",
    y="quantidade_cidades",
    title="Top 10 Países com Mais Cidades Registradas",
    labels={"country": "País", "quantidade_cidades": "Quantidade de Cidades"},
    text_auto=".0f",
    color="country",
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig2.update_layout(
    xaxis_tickangle=0,
    title_x=0,
    showlegend=False,
    xaxis_categoryorder="total descending",
)
st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------
# LINHA 3: DUAS COLUNAS LADO A LADO (Gráficos 3 e 4)
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    # Gráfico 3 - Média de Avaliações[cite: 3]
    media_avaliacoes_por_pais = (
        df.groupby("country")["votes"]
        .mean()
        .round(2)
        .reset_index(name="media_avaliacoes")
        .sort_values(by="media_avaliacoes", ascending=False)
    )
    top_7_media_avaliacoes = media_avaliacoes_por_pais.head(7)

    fig3 = px.bar(
        top_7_media_avaliacoes,
        x="country",
        y="media_avaliacoes",
        title="Top 7 Média de Avaliações Feitas por País",
        labels={"country": "País", "media_avaliacoes": "Média de Avaliações (Votos)"},
        text_auto=".2f",
        color="country",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig3.update_layout(
        xaxis_tickangle=0,
        title_x=0,
        showlegend=False,
        xaxis_categoryorder="total descending",
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Gráfico 4 - Média de Preço em USD[cite: 3]
    pais_valor_medio_prato_2_pessoas = (
        df.groupby("country")["average_cost_for_two_cost_in_usd"]
        .mean()
        .round(2)
        .reset_index(name="media_preco_usd")
        .sort_values(by="media_preco_usd", ascending=False)
    )
    top_7_preco_pais_usd = pais_valor_medio_prato_2_pessoas.head(7)

    fig4 = px.bar(
        top_7_preco_pais_usd,
        x="country",
        y="media_preco_usd",
        title="Top 7 Média de Preço (Prato para 2) em USD",
        labels={"country": "País", "media_preco_usd": "Média de Preço (USD)"},
        text_auto=".2f",
        color="country",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig4.update_layout(
        xaxis_tickangle=0,
        title_x=0,
        showlegend=False,
        xaxis_categoryorder="total descending",
    )
    st.plotly_chart(fig4, use_container_width=True)
