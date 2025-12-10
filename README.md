## 🎵 Spotify Dashboard – Interativo com Streamlit

Um dashboard completo para analisar músicas, artistas, álbuns e métricas musicais usando **Streamlit, Altair, Plotly, pandas e Python.** Com visual inspirado no Spotify e visualizações modernas.

![Preview do Dashboard]("Preview.png")

### 🧩 Funcionalidades
- 🔍 Filtros interativos por artista, gênero e ano
- 📊 Gráficos Altair & Plotly completamente interativos
- 🎙️ Top artistas mais populares
- 💽 Top álbuns mais populares
- 🎵 Faixas mais populares
- ⏱️ Distribuição de duração das músicas
- 🎧 Análise de faixas explícitas
- 📅 Lançamentos por ano

### 📂 Estrutura do Projeto
```
SPOTIFY
├── assets/
    └── Header.png
├── data/
    ├── analise.ipynb
    └── spotify_data_clean.csv
├── images
    └── Preview.png
├── app.py
├── README.md
```

### 🛠️ Tecnologias Utilizadas
- Python 3.10+
- Streamlit
- Altair
- Plotly
- pandas & numpy
- GitHub + Streamlit Cloud

### ▶️ Como Rodar Localmente

#### 1️⃣ Clone o repositório:

```
git clone https://github.com/Lucasbig6/spotify_dashboard.git
cd spotify-dashboard
```

#### 2️⃣ Crie um ambiente virtual (opcional):

```
python -m venv .venv
source .venv/bin/activate
```
#### 3️⃣ Instale as dependências:

```
pip install -r requirements.txt
```
#### 4️⃣ Execute o dashboard:

```
streamlit run app.py
```
