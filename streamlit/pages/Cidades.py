import os
import sys

import pandas as pd
import plotly.express as px
from utils.sidebar import render_sidebar

import streamlit as st

# 1. Configuração da página (Obrigatório ser o primeiro comando)
st.set_page_config(page_title="Visão Cidades", page_icon="🏙️", layout="wide")

# 2. Ajuste de diretório para importar os scripts de utilidades
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
# CARREGAMENTO E LIMPEZA DE DADOS (COM CACHE)
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
st.title("🏙️ Visão Cidades")
st.markdown("---")

# ---------------------------------------------------------
# LINHA 1: TELA CHEIA (Gráfico 1)
# ---------------------------------------------------------
# Adicionei 'country' no groupby para as cores baterem com a sua imagem
cidade_quantidade_restaurantes = (
    df.groupby(["country", "city"])
    .size()
    .reset_index(name="quantidade")
    .sort_values(by="quantidade", ascending=False)
)
top_10_cidades = cidade_quantidade_restaurantes.head(10)

fig1 = px.bar(
    top_10_cidades,
    x="city",
    y="quantidade",
    title="Top 10 Cidades com mais Restaurantes na Base de Dados",
    labels={
        "city": "Cidade",
        "quantidade": "Quantidade de Restaurantes",
        "country": "País",
    },
    text_auto=".2f",  # Adicionado .2f para mostrar as casas decimais como na sua imagem (80.00)
    color="country",
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig1.update_layout(xaxis_tickangle=0, title_x=0, xaxis_categoryorder="total descending")
st.plotly_chart(fig1, use_container_width=True)


# ---------------------------------------------------------
# LINHA 2: DUAS COLUNAS LADO A LADO (Gráficos 2 e 3)
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    filtro_bom = df["aggregate_rating"] >= 4
    cidade_quantidade_restaurantes_nota_alta = (
        df.loc[filtro_bom, :]
        .groupby(["country", "city"])
        .size()
        .reset_index(name="quantidade")
        .sort_values(by="quantidade", ascending=False)
    )
    top_7_cidades_boas = cidade_quantidade_restaurantes_nota_alta.head(7)

    fig2 = px.bar(
        top_7_cidades_boas,
        x="city",
        y="quantidade",
        title="Top 7 Cidades com Restaurantes com média de avaliação acima de 4",
        labels={
            "city": "Cidade",
            "quantidade": "Quantidade de Restaurantes",
            "country": "País",
        },
        text_auto=".2f",
        color="country",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig2.update_layout(
        xaxis_tickangle=0, title_x=0, xaxis_categoryorder="total descending"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    filtro_ruim = df["aggregate_rating"] <= 2.5
    cidade_quantidade_restaurantes_nota_baixa = (
        df.loc[filtro_ruim, :]
        .groupby(["country", "city"])
        .size()
        .reset_index(name="quantidade")
        .sort_values(by="quantidade", ascending=False)
    )
    top_7_cidades_ruins = cidade_quantidade_restaurantes_nota_baixa.head(7)

    fig3 = px.bar(
        top_7_cidades_ruins,
        x="city",
        y="quantidade",
        title="Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5",
        labels={
            "city": "Cidade",
            "quantidade": "Quantidade de Restaurantes",
            "country": "País",
        },
        text_auto=".2f",
        color="country",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig3.update_layout(
        xaxis_tickangle=0, title_x=0, xaxis_categoryorder="total descending"
    )
    st.plotly_chart(fig3, use_container_width=True)


# ---------------------------------------------------------
# LINHA 3: TELA CHEIA (Gráfico 4)
# ---------------------------------------------------------
cidades_tipos_culinarios = (
    df.groupby(["country", "city"])["cuisines"]
    .nunique()
    .reset_index(name="quantidade_tipos_culinarios")
    .sort_values(by="quantidade_tipos_culinarios", ascending=False)
)
top_10_cidades_culinaria = cidades_tipos_culinarios.head(10)

fig4 = px.bar(
    top_10_cidades_culinaria,
    x="city",
    y="quantidade_tipos_culinarios",
    title="Top 10 Cidades mais restaurantes com tipos culinários distintos",
    labels={
        "city": "Cidade",
        "quantidade_tipos_culinarios": "Tipos Culinários Únicos",
        "country": "País",
    },
    text_auto=True,  # Sem decimais aqui, pois são tipos culinários inteiros
    color="country",
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig4.update_layout(xaxis_tickangle=0, title_x=0, xaxis_categoryorder="total descending")
st.plotly_chart(fig4, use_container_width=True)
