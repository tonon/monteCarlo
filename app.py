import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Dashboard Monte Carlo PM", layout="wide")
st.title("📊 Dashboard de Previsibilidade e Métricas Ágeis")
st.markdown("---")

# Cache da conexão com o banco
@st.cache_resource
def get_connection():
    return sqlite3.connect("kanban_local.db")

# Carregar resultados das simulações
def load_results():
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM resultados_monte_carlo", conn)
        df['data_simulacao'] = pd.to_datetime(df['data_simulacao'])
        return df
    except:
        return pd.DataFrame()

# Carregar dados dos cards (histórico + backlog)
def load_cards():
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM cards", conn)
        # Converter colunas de data
        for col in ['createdAt', 'updatedAt', 'dtDone']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    except Exception as e:
        st.warning(f"Erro ao carregar cards: {e}")
        return pd.DataFrame()

# Carregar dados
df_results = load_results()
df_cards = load_cards()

# --- Barra lateral com navegação ---
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione a análise:",
    ["📈 Previsão Monte Carlo", "📉 Análise de Slippage", "⏳ Aging do Backlog"]
)

# -------------------------------------------------------------------
# PÁGINA 1: PREVISÃO MONTE CARLO (já existente, com pequenas melhorias)
# -------------------------------------------------------------------
if pagina == "📈 Previsão Monte Carlo":
    if df_results.empty:
        st.warning("Nenhum resultado de simulação encontrado. Execute `make run` primeiro.")
        st.stop()
    
    # Filtros
    st.sidebar.header("Filtros")
    categorias = st.sidebar.multiselect(
        "Categoria", 
        df_results['categoria'].unique(), 
        default=df_results['categoria'].unique()
    )
    df_filt = df_results[df_results['categoria'].isin(categorias)]
    
    # Indicadores da última simulação
    st.subheader("📌 Última Simulação")
    ultimo = df_results.sort_values('data_simulacao', ascending=False).iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Contexto", ultimo['contexto'])
    col2.metric("Itens Pendentes", f"{ultimo['itens_pendentes']} cards")
    col3.metric("P85 (Dias)", f"{ultimo['p85']} dias")
    col4.metric("P95 (Dias)", f"{ultimo['p95']} dias")
    
    st.markdown("---")
    
    # Gráficos
    col_esq, col_dir = st.columns(2)
    with col_esq:
        fig_linha = px.line(
            df_filt, x="data_simulacao", y="p85", 
            color="contexto", markers=True, 
            title="📈 Evolução do P85 por Simulação"
        )
        st.plotly_chart(fig_linha, use_container_width=True)
    
    with col_dir:
        fig_barra = px.bar(
            df_filt.sort_values('p85'), 
            x="p85", y="contexto", 
            orientation='h', color="p85", 
            title="📊 Prazo Estimado (P85) por Contexto",
            text_auto=True
        )
        st.plotly_chart(fig_barra, use_container_width=True)
    
    st.subheader("📄 Histórico Completo de Simulações")
    st.dataframe(df_filt.sort_values('data_simulacao', ascending=False), use_container_width=True)

# -------------------------------------------------------------------
# PÁGINA 2: ANÁLISE DE SLIPPAGE (escorregamento)
# -------------------------------------------------------------------
elif pagina == "📉 Análise de Slippage":
    st.subheader("📉 Análise de Escorregamento (Estimativa vs. Realizado)")
    
    if df_cards.empty:
        st.warning("Tabela 'cards' não encontrada no banco de dados.")
        st.stop()
    
    # Verifica se as colunas necessárias existem
    required_cols = ['estimated_days', 'actual_days', 'slippage', 'card_type']
    if not all(col in df_cards.columns for col in required_cols):
        st.warning("O banco de dados não possui as colunas de estimativa. Execute o script de geração de dados primeiro.")
        st.stop()
    
    # Filtros
    tipos_disponiveis = df_cards['card_type'].dropna().unique()
    tipos_selecionados = st.multiselect(
        "Tipo de Card", tipos_disponiveis, default=list(tipos_disponiveis)
    )
    
    # Apenas cards concluídos (dtDone não nulo)
    df_concluidos = df_cards[df_cards['dtDone'].notna()].copy()
    df_concluidos = df_concluidos[df_concluidos['card_type'].isin(tipos_selecionados)]
    
    if df_concluidos.empty:
        st.info("Nenhum card concluído com os filtros selecionados.")
        st.stop()
    
    # Colunas para exibição
    col1, col2 = st.columns(2)
    
    with col1:
        # Histograma do slippage
        fig_hist = px.histogram(
            df_concluidos, x='slippage', 
            color='card_type', nbins=20,
            title="Distribuição do Escorregamento (dias)",
            labels={'slippage': 'Escorregamento (dias)', 'count': 'Quantidade'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Boxplot do slippage por tipo
        fig_box = px.box(
            df_concluidos, x='card_type', y='slippage',
            title="Escorregamento por Tipo de Card",
            labels={'card_type': 'Tipo', 'slippage': 'Dias'}
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Tabela resumo estatístico
    st.subheader("📊 Resumo Estatístico do Escorregamento")
    resumo = df_concluidos.groupby('card_type')['slippage'].agg(
        Média='mean', Mediana='median', Desvio_Padrão='std', Mínimo='min', Máximo='max', Quantidade='count'
    ).reset_index()
    st.dataframe(resumo, use_container_width=True)
    
    # Gráfico de barras: slippage médio por sprint (se tiver a coluna sprint)
    if 'sprint' in df_concluidos.columns:
        slippage_sprint = df_concluidos.groupby('sprint')['slippage'].mean().reset_index()
        fig_sprint = px.bar(
            slippage_sprint, x='sprint', y='slippage',
            title="Escorregamento Médio por Sprint",
            labels={'sprint': 'Sprint', 'slippage': 'Escorregamento médio (dias)'}
        )
        st.plotly_chart(fig_sprint, use_container_width=True)

# -------------------------------------------------------------------
# PÁGINA 3: AGING DO BACKLOG
# -------------------------------------------------------------------
elif pagina == "⏳ Aging do Backlog":
    st.subheader("⏳ Aging dos Cards Abertos (Backlog / WIP)")
    
    if df_cards.empty:
        st.warning("Tabela 'cards' não encontrada.")
        st.stop()
    
    # Cards sem data de conclusão
    df_abertos = df_cards[df_cards['dtDone'].isna()].copy()
    if df_abertos.empty:
        st.info("Nenhum card em aberto. Backlog vazio!")
        st.stop()
    
    # Calcular aging (se não existir a coluna)
    if 'aging_days' not in df_abertos.columns:
        hoje = datetime.now()
        df_abertos['aging_days'] = (hoje - df_abertos['createdAt']).dt.days
    else:
        df_abertos['aging_days'] = pd.to_numeric(df_abertos['aging_days'], errors='coerce')
    
    df_abertos = df_abertos.dropna(subset=['aging_days'])
    
    # Filtros
    st.sidebar.header("Filtros de Aging")
    tipos_aging = st.sidebar.multiselect(
        "Tipos de Card", 
        df_abertos['card_type'].dropna().unique(),
        default=df_abertos['card_type'].dropna().unique()
    )
    df_abertos = df_abertos[df_abertos['card_type'].isin(tipos_aging)]
    
    # Distribuição por faixas
    bins = [0, 5, 10, 15, 20, 30, 60, 999]
    labels = ['0-5', '6-10', '11-15', '16-20', '21-30', '31-60', '>60']
    df_abertos['faixa'] = pd.cut(df_abertos['aging_days'], bins=bins, labels=labels, right=False)
    faixa_counts = df_abertos['faixa'].value_counts().sort_index()
    
    fig_faixa = px.bar(
        x=faixa_counts.index, y=faixa_counts.values,
        title="📊 Cards em Aberto por Faixa de Aging",
        labels={'x': 'Faixa (dias)', 'y': 'Quantidade de Cards'}
    )
    st.plotly_chart(fig_faixa, use_container_width=True)
    
    # Boxplot de aging por tipo
    fig_box_age = px.box(
        df_abertos, x='card_type', y='aging_days',
        title="Distribuição de Aging por Tipo de Card",
        labels={'card_type': 'Tipo', 'aging_days': 'Dias em aberto'}
    )
    st.plotly_chart(fig_box_age, use_container_width=True)
    
    # Tabela dos cards mais antigos
    st.subheader("⏰ Cards Mais Antigos (Top 15)")
    top_aged = df_abertos.nlargest(15, 'aging_days')[['_id', 'name', 'card_type', 'lane', 'createdAt', 'aging_days']]
    st.dataframe(top_aged, use_container_width=True)
    
    # Gráfico de tendência: aging médio por tipo ao longo do tempo (opcional)
    if 'createdAt' in df_abertos.columns:
        df_abertos['mes_ano'] = df_abertos['createdAt'].dt.to_period('M').astype(str)
        aging_mensal = df_abertos.groupby(['mes_ano', 'card_type'])['aging_days'].mean().reset_index()
        fig_tendencia = px.line(
            aging_mensal, x='mes_ano', y='aging_days', color='card_type',
            title="📈 Tendência de Aging Médio (por mês de criação)",
            labels={'mes_ano': 'Mês', 'aging_days': 'Aging médio (dias)'}
        )
        st.plotly_chart(fig_tendencia, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Dashboard alimentado pelos dados do banco SQLite | Simulações Monte Carlo + Métricas Ágeis")