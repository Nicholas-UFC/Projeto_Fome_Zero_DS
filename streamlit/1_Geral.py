import os
import sys

import folium
import pandas as pd
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from utils.sidebar import render_sidebar

import streamlit as st

# 1. Configuração da página (Deve ser o primeiro comando do Streamlit)
st.set_page_config(page_title="Visão Geral", page_icon="🌍", layout="wide")

# 2. Ajuste de diretório para importar seus scripts corretamente[cite: 1]
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

# 3. Importando os módulos de utilidades construídos no seu projeto[cite: 1]
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
    """
    Carrega o dataset e aplica todo o pipeline de limpeza do projeto.
    O cache evita que o Streamlit faça isso toda vez que a página for recarregada.
    """
    file_path = os.path.join("..", "database", "zomato.csv")  # [cite: 1]
    df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")  # [cite: 1]

    # Executando a esteira de tratamento de dados[cite: 1]
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

# Cabeçalho Principal[cite: 1]
st.title("🍔 Fome Zero!")

st.header("O Melhor lugar para encontrar seu mais novo restaurante favorito!")
st.subheader("Temos as seguintes marcas dentro da nossa plataforma:")

# Cálculos de Métricas[cite: 1]
qtd_restaurantes = len(df)
qtd_paises = df["country"].nunique()
qtd_cidades = df["city"].nunique()
soma_avaliacoes = df["votes"].sum()
qtd_culinarias = df["cuisines"].nunique()

# Desenhando as colunas para os KPIs no Streamlit
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Restaurantes Cadastrados", value=qtd_restaurantes)

with col2:
    st.metric(label="Países Cadastrados", value=qtd_paises)

with col3:
    st.metric(label="Cidades Cadastradas", value=qtd_cidades)

with col4:
    # Formatação especial (ex: 4.195.634)[cite: 1]
    avaliacoes_formatadas = f"{soma_avaliacoes:,.0f}".replace(",", ".")
    st.metric(label="Avaliações na Plataforma", value=avaliacoes_formatadas)

with col5:
    st.metric(label="Tipos de Culinárias", value=qtd_culinarias)

# Linha de separação visual
st.markdown("---")

# ==========================================
# MAPA INTERATIVO (FOLIUM)
# ==========================================
st.subheader("Nossas Marcas Pelo Mundo")

# Criando o mapa base centralizado e o Cluster de marcadores[cite: 1]
mapa = folium.Map(location=[20, 0], zoom_start=2)
cluster = MarkerCluster().add_to(mapa)

# Lendo os dados para gerar os pinos[cite: 1]
for index, linha in df.iterrows():
    folium.Marker(
        location=[linha["latitude"], linha["longitude"]],
        popup=linha["restaurant_name"],
        tooltip=linha["cuisines"],
        icon=folium.Icon(icon="home", color="blue", prefix="glyphicon"),
    ).add_to(cluster)

# Renderiza o mapa folium dentro do Streamlit, forçando o uso do limite da tela
st_folium(mapa, width=1024, height=600, use_container_width=True, returned_objects=[])
