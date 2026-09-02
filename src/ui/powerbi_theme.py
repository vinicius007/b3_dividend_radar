"""
Estilos e Temas CSS customizados para reproduzir o visual executivo do Power BI.
"""

POWERBI_CSS = """
<style>
/* Fonte e Reset Corporativo */
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

/* Fundo da Aplicação em Tom de Azul Clarinho */
.stApp {
    background-color: #EBF3FA;
    color: #0F172A;
}

/* Header Estilo Power BI com Gradiente Azul */
.pbi-header-container {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #1E40AF 100%);
    border: 1px solid #BAE6FD;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(2, 132, 199, 0.18);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.pbi-header-title {
    font-size: 26px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.pbi-header-subtitle {
    font-size: 14px;
    color: #E0F2FE;
    margin-top: 4px;
    font-weight: 400;
}

.pbi-badge-live {
    background-color: rgba(255, 255, 255, 0.2);
    border: 1px solid #FFFFFF;
    color: #FFFFFF;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    backdrop-filter: blur(4px);
}

/* Cartões KPI Power BI em Fundo Branco com Sombra e Borda Azul Suave */
.pbi-kpi-card {
    background: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 4px 12px rgba(14, 116, 144, 0.08);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}

.pbi-kpi-card:hover {
    border-color: #0284C7;
    box-shadow: 0 6px 18px rgba(2, 132, 199, 0.16);
    transform: translateY(-2px);
}

.pbi-kpi-label {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.75px;
    color: #0369A1;
    margin-bottom: 6px;
}

.pbi-kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 6px;
}

.pbi-kpi-sub {
    font-size: 12px;
    color: #475569;
    display: flex;
    align-items: center;
    gap: 6px;
}

.pbi-tag-positive {
    color: #059669;
    font-weight: 700;
}

.pbi-tag-neutral {
    color: #64748B;
    font-weight: 700;
}

.pbi-tag-caution {
    color: #D97706;
    font-weight: 700;
}

/* Cartão de Ação / Notícia */
.pbi-action-card {
    background: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 3px 10px rgba(14, 116, 144, 0.06);
    transition: all 0.2s ease;
}

.pbi-action-card:hover {
    border-color: #0284C7;
    box-shadow: 0 6px 16px rgba(2, 132, 199, 0.14);
}

.pbi-action-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.pbi-action-ticker {
    font-size: 18px;
    font-weight: 700;
    color: #0F172A;
}

.pbi-action-name {
    font-size: 13px;
    color: #475569;
    margin-left: 8px;
}

.pbi-action-score-pill {
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}

.pbi-news-title {
    font-size: 14px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 6px;
    line-height: 1.4;
}

.pbi-news-meta {
    font-size: 12px;
    color: #64748B;
    display: flex;
    gap: 12px;
    margin-bottom: 8px;
}

.pbi-news-summary {
    font-size: 13px;
    color: #334155;
    line-height: 1.4;
}

/* Container de Gráficos */
.pbi-chart-container {
    background: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(14, 116, 144, 0.08);
}

.pbi-chart-title {
    font-size: 15px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 12px;
    border-left: 4px solid #0284C7;
    padding-left: 10px;
}

/* Barra Lateral (Sidebar) em Azul Suave */
[data-testid="stSidebar"] {
    background-color: #E2EEF9;
    border-right: 1px solid #BAE6FD;
}

/* Abas estilo Power BI */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid #BAE6FD;
    background-color: transparent;
    padding-bottom: 6px;
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    background-color: #FFFFFF;
    border-radius: 6px;
    color: #334155;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #BAE6FD;
    padding: 0 16px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.stTabs [aria-selected="true"] {
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
    border-color: #0284C7 !important;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3) !important;
}

/* Tabelas e Dataframes */
.stDataFrame {
    border: 1px solid #BAE6FD;
    border-radius: 8px;
    overflow: hidden;
    background-color: #FFFFFF;
}
</style>
"""

# Paleta de Cores Power BI Corporativa para Gráficos Plotly em Tema Claro / Azul Suave
PLOTLY_POWERBI_THEME = {
    "layout": {
        "paper_bgcolor": "#FFFFFF",
        "plot_bgcolor": "#FFFFFF",
        "font": {
            "family": "Segoe UI, Inter, sans-serif",
            "color": "#0F172A",
            "size": 12
        },
        "colorway": ["#0284C7", "#059669", "#D97706", "#7C3AED", "#DC2626", "#DB2777", "#2563EB"],
        "xaxis": {
            "gridcolor": "#E2E8F0",
            "linecolor": "#CBD5E1",
            "zerolinecolor": "#CBD5E1"
        },
        "yaxis": {
            "gridcolor": "#E2E8F0",
            "linecolor": "#CBD5E1",
            "zerolinecolor": "#CBD5E1"
        },
        "margin": {"l": 40, "r": 20, "t": 40, "b": 40}
    }
}
