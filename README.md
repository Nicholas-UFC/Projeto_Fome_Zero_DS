# 🍔 Fome Zero - Dashboard de Análise de Restaurantes

Este repositório contém o projeto prático **Fome Zero**, desenvolvido como parte do programa de formação em Análise de Dados da **Comunidade DS**. O objetivo principal é consolidar, tratar e disponibilizar em um painel interativo (Web App) as principais métricas e indicadores de restaurantes cadastrados globalmente na plataforma Zomato.

---

## 🚀 O Projeto

O projeto foi construído utilizando **Python** para o tratamento e limpeza dos dados, modularização de funções utilitárias, e **Streamlit** para a criação de um painel gerencial multipágina interativo e responsivo.

### 📁 Estrutura do Repositório

```text
Empresa Fome Zero/
│
├── database/            # Contém a base de dados original (.csv)
├── notebooks/           # Jupyter Notebooks utilizados para análises exploratórias iniciais
├── streamlit/           # Arquivos das páginas do painel web (Geral, Cidades, Paises, etc.)
├── utils/               # Módulos em Python com funções de limpeza, transformação e sidebar
├── .gitignore           # Arquivos e pastas ignorados pelo controle de versão
├── main.py              # Arquivo de entrada principal do projeto
└── pyproject.toml       # Gerenciamento de dependências

```

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Python 3.10+**
* **Pandas**: Manipulação, limpeza e tratamento dos dados.
* **Streamlit**: Construção da interface gráfica e do painel web.
* **Folium / Streamlit-Folium**: Criação de mapas interativos e clusters de localização.
* **UV / Pip**: Gerenciamento de ambientes e pacotes.

---

## 📊 Funcionalidades do Dashboard

* **Página Geral (`1_🌍_Geral.py`):** Visão macro do negócio com indicadores chave (KPIs) de restaurantes, países, cidades, avaliações e tipos culinários, além de um mapa interativo global.
* **Barra Lateral Dinâmica:** Filtros avançados em cascata por **País** e **Tipo de Culinária**, com opção rápida de seleção total.
* **Download de Dados:** Recurso nativo para exportar a base de dados tratada diretamente pelo painel em formato `.csv`.
* **Navegação Multipágina:** Páginas estruturadas para detalhamento por Cidades, Países e Tipos Culinários.

---

## ⚙️ Como Executar o Projeto Localmente

1. **Clone o repositório ou abra a pasta do projeto** no seu terminal de preferência.
2. **Ative o ambiente virtual** configurado:
```bash
.venv\Scripts\activate

```


3. **Inicie o painel do Streamlit** apontando para o arquivo principal da pasta:
```bash
streamlit run streamlit/1_🌍_Geral.py

```


4. O painel abrirá automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

---

## 👨‍💻 Autor

Projeto desenvolvido por **Bryan Nicholas** com o apoio da **Comunidade DS**.