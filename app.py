import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np
from datetime import datetime

# ================================
# CONFIGURAÇÃO DO DASHBOARD
# ================================
st.set_page_config(
    page_title="Spotify Dashboard",
    layout="wide",
    page_icon="🎧"
)

SPOTIFY_GREEN = "#1DB954"

# ================================
# CARREGAR DADOS
# ================================
csv_path = os.path.join("data", "spotify_data_clean.csv")

df = pd.read_csv(csv_path)

# Ajuste de colunas
df.columns = df.columns.str.strip()
if "artist_genres" in df.columns:
    df["artist_genres"] = df["artist_genres"].fillna("Unknown")


# ================================
# SIDEBAR (FILTROS)
# ================================
st.sidebar.title("🎧 Filtros Spotify")

min_pop, max_pop = int(df["Popularidade da faixa"].min()), int(df["Popularidade da faixa"].max())

pop_filter = st.sidebar.slider(
    "Filtrar por popularidade:",
    min_pop, max_pop,
    (min_pop, max_pop)
)

artists = st.sidebar.multiselect(
    "Artistas",
    sorted(df["Nome do artista"].dropna().astype(str).unique()),
    default=None,
    placeholder="Selecione os artistas"
)

genres = st.sidebar.multiselect(
    "Gêneros",
    sorted(df["Gêneros do artista"].dropna().astype(str).unique()),
    default=None,
    placeholder="Selecione os gêneros"
)

# ================================
# APLICAR FILTROS
# ================================
df_filtered = df[
    (df["Popularidade da faixa"] >= pop_filter[0]) &
    (df["Popularidade da faixa"] <= pop_filter[1])
]

if artists:
    df_filtered = df_filtered[df_filtered["Nome do artista"].isin(artists)]

if genres:
    df_filtered = df_filtered[df_filtered["Gêneros do artista"].isin(genres)]


# ================================
# TÍTULO
# ================================
st.image("assets/Header.png", use_container_width=True)

data_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")

st.markdown(
    f"<p style='text-align:right; color:gray;'>Atualizado em: {data_atualizacao}</p>",
    unsafe_allow_html=True
)


st.divider()

# ================================
# MÉTRICAS
# ================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Faixas", len(df_filtered), border=True)
col2.metric("Popularidade Média", round(df_filtered["Popularidade da faixa"].mean(), 1), border=True)
col3.metric(
    "Artista com mais seguidores",
    df_filtered.loc[df_filtered["Seguidores do artista"].idxmax()]["Nome do artista"],
    border=True
)
col4.metric(
    "Faixa mais longa",
    f"{df_filtered['Duração da faixa (min)'].max():.2f} min",
    border=True
)

st.divider()

col1, col2 = st.columns(2)

# ================================
# 1️⃣ Top 10 Faixas Mais Populares (Altair)
# ================================
with col1.container(border=True):
    st.markdown("### 🎧 Top 10 Faixas Mais Populares")

    df_filtered["Popularidade da faixa"] = pd.to_numeric(df_filtered["Popularidade da faixa"], errors="coerce")

    top_tracks = df_filtered.sort_values("Popularidade da faixa", ascending=False).head(10)

    chart_tracks = (
        alt.Chart(top_tracks)
        .mark_bar(color=SPOTIFY_GREEN)
        .encode(
            y=alt.Y("Nome da faixa:N", sort="-x", title="Faixa"),
            x=alt.X("Popularidade da faixa:Q", title="Popularidade"),
            tooltip=["Nome da faixa", "Popularidade da faixa"]
        )
        .properties(height=420)
    )

    text_tracks = (
        alt.Chart(top_tracks)
        .mark_text(
            align="left",
            baseline="middle",
            dx=6,
            color="black",
            fontSize=12
        )
        .encode(
            y=alt.Y("Nome da faixa:N", sort="-x"),
            x="Popularidade da faixa:Q",
            text=alt.Text("Popularidade da faixa:Q", format=".0f")
        )
        .properties(height=420)
    )

    st.altair_chart(chart_tracks + text_tracks, use_container_width=True)


# ================================
# 2️⃣ Top 10 Artistas Mais Populares (Altair)
# ================================
with col2.container(border=True):
    st.markdown("### 🎙️ Top 10 Artistas Mais Populares")

    df_filtered["Popularidade do artista"] = pd.to_numeric(df_filtered["Popularidade do artista"], errors="coerce")

    top_artists = (
        df_filtered.groupby("Nome do artista")["Popularidade do artista"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    top_artists["Popularidade do artista"] = top_artists["Popularidade do artista"].round(0)

    chart_artists = (
        alt.Chart(top_artists)
        .mark_bar(color=SPOTIFY_GREEN)
        .encode(
            y=alt.Y("Nome do artista:N", sort="-x"),
            x=alt.X("Popularidade do artista:Q"),
            tooltip=["Nome do artista", "Popularidade do artista"]
        )
        .properties(height=420)
    )

    text_artists = (
        alt.Chart(top_artists)
        .mark_text(
            align="left",
            baseline="middle",
            dx=6,
            color="black",
            fontSize=12
        )
        .encode(
            y=alt.Y("Nome do artista:N", sort="-x"),
            x="Popularidade do artista:Q",
            text=alt.Text("Popularidade do artista:Q", format=".0f")
        )
        .properties(height=420)
    )

    st.altair_chart(chart_artists + text_artists, use_container_width=True)


# ================================
# 3️⃣ Top 10 Gêneros com Mais Faixas (Altair)
# ================================
with st.container(border=True):
    st.markdown("### 🎼 Top 10 Gêneros com Mais Faixas")

    genre_counts = (
        df_filtered["Gêneros do artista"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    genre_counts.columns = ["Gênero", "Número de faixas"]

    chart_genres = (
        alt.Chart(genre_counts)
        .mark_bar(color=SPOTIFY_GREEN)
        .encode(
            y=alt.Y("Gênero:N", sort="-x"),
            x=alt.X("Número de faixas:Q"),
            tooltip=["Gênero", "Número de faixas"]
        )
        .properties(height=400)
    )

    text_genres = (
        alt.Chart(genre_counts)
        .mark_text(align="left", baseline="middle", dx=3, color="black")
        .encode(
            y=alt.Y("Gênero:N", sort="-x"),
            x="Número de faixas:Q",
            text="Número de faixas:Q"
        )
        .properties(height=400)
    )

    st.altair_chart(chart_genres + text_genres, use_container_width=True)

# ================================
# Gráfico Adicional: Top 20 Faixas mais populares
# ================================
top_faixas = df.nlargest(20, "Popularidade da faixa")[["Nome da faixa", "Popularidade da faixa"]]

with st.container(border=True):
    st.markdown("### 🎵 Top 20 Faixas mais populares")
    graf1 = (
        alt.Chart(top_faixas)
        .mark_bar(color="#1DB954")
        .encode(
            x=alt.X("Popularidade da faixa:Q"),
            y=alt.Y("Nome da faixa:N", sort="-x"),
            tooltip=["Nome da faixa", "Popularidade da faixa"]
        )
        .properties(title="Top 20 Faixas mais populares", height=500)
    )
    st.altair_chart(graf1, use_container_width=True)

# ================================
# DIVISOR
# ================================
with st.container(border=True):
    st.markdown("### ⏱️ Análise da Duração das Faixas")
    graf2 = (
        alt.Chart(df)
        .mark_bar(color="#1DB954")
        .encode(
            x=alt.X("Duração da faixa (min):Q", bin=alt.Bin(maxbins=30)),
            y="count()",
            tooltip=["count()"]
        )
        .properties(title="Distribuição da duração das faixas")
    )
    st.altair_chart(graf2, use_container_width=True)

# ================================
# DIVISOR
# ================================
with st.container(border=True):
    st.markdown("### 📊 Popularidade vs Duração da Faixa")
    graf3 = (
        alt.Chart(df)
        .mark_circle(size=80, color="#1DB954")
        .encode(
            x="Duração da faixa (min):Q",
            y="Popularidade da faixa:Q",
            tooltip=["Nome da faixa", "Duração da faixa (min)", "Popularidade da faixa"]
        )
        .properties(title="Popularidade x Duração da Faixa")
    )
    st.altair_chart(graf3, use_container_width=True)

# ================================
# DIVISOR
# ================================
top_artistas = df.groupby("Nome do artista")["Popularidade do artista"].mean().reset_index()
top_artistas = top_artistas.nlargest(15, "Popularidade do artista")

with st.container(border=True):
    st.markdown("### 🎤 Top 15 Artistas mais populares")
    graf4 = (
        alt.Chart(top_artistas)
        .mark_bar(color="#1DB954")
        .encode(
            x=alt.X("Nome do artista:N", sort="-y"),
            y="Popularidade do artista:Q",
            tooltip=["Nome do artista", "Popularidade do artista"]
        )
        .properties(title="Top 15 Artistas mais populares", height=400)
    )
    st.altair_chart(graf4, use_container_width=True)


st.divider()

# ================================
# RODAPÉ
# ================================
st.markdown(
    "<p style='text-align:center; color:gray;'>Dados fornecidos por Spotify | Desenvolvido por Lucas Pablo</p>",
    unsafe_allow_html=True
)
