"""
Estilos e Temas CSS customizados para reproduzir o visual executivo do Power BI (Dark Slate).
"""

POWERBI_CSS = """
<style>
/* Fonte e Reset Corporativo */
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

/* Fundo da Aplicação */
.stApp {
    background-color: #0B1120;
    color: #F1F5F9;
}

/* Header Estilo Power BI */
.pbi-header-container {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.pbi-header-title {
    font-size: 26px;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.5px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.pbi-header-subtitle {
    font-size: 14px;
    color: #94A3B8;
    margin-top: 4px;
    font-weight: 400;
}

.pbi-badge-live {
    background-color: rgba(16, 185, 129, 0.15);
    border: 1px solid #10B981;
    color: #10B981;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Cartões KPI Power BI */
.pbi-kpi-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    transition: transform 0.2s ease, border-color 0.2s ease;
    height: 100%;
}

.pbi-kpi-card:hover {
    border-color: #F59E0B;
    transform: translateY(-2px);
}

.pbi-kpi-label {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.75px;
    color: #94A3B8;
    margin-bottom: 6px;
}

.pbi-kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 6px;
}

.pbi-kpi-sub {
    font-size: 12px;
    color: #CBD5E1;
    display: flex;
    align-items: center;
    gap: 6px;
}

.pbi-tag-positive {
    color: #10B981;
    font-weight: 600;
}

.pbi-tag-neutral {
    color: #94A3B8;
    font-weight: 600;
}

.pbi-tag-caution {
    color: #F59E0B;
    font-weight: 600;
}

/* Cartão de Ação / Notícia */
.pbi-action-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 14px;
    transition: all 0.2s ease;
}

.pbi-action-card:hover {
    border-color: #38BDF8;
    box-shadow: 0 6px 16px rgba(56, 189, 248, 0.15);
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
    color: #F8FAFC;
}

.pbi-action-name {
    font-size: 13px;
    color: #94A3B8;
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
    font-weight: 600;
    color: #E2E8F0;
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
    color: #94A3B8;
    line-height: 1.4;
}

/* Container de Gráficos */
.pbi-chart-container {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.pbi-chart-title {
    font-size: 15px;
    font-weight: 600;
    color: #F8FAFC;
    margin-bottom: 12px;
    border-left: 4px solid #F59E0B;
    padding-left: 10px;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: #0F172A;
    border-right: 1px solid #334155;
}

/* Abas estilo Power BI */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid #334155;
    background-color: transparent;
    padding-bottom: 6px;
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    background-color: #1E293B;
    border-radius: 6px;
    color: #94A3B8;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #334155;
    padding: 0 16px;
}

.stTabs [aria-selected="true"] {
    background-color: #3B82F6 !important;
    color: #FFFFFF !important;
    border-color: #60A5FA !important;
}

/* Tabelas e Dataframes */
.stDataFrame {
    border: 1px solid #334155;
    border-radius: 8px;
    overflow: hidden;
}
</style>
"""

# Paleta de Cores Power BI Corporativa para Gráficos Plotly (Dark Slate)
PLOTLY_POWERBI_THEME = {
    "layout": {
        "paper_bgcolor": "#1E293B",
        "plot_bgcolor": "#1E293B",
        "font": {
            "family": "Segoe UI, Inter, sans-serif",
            "color": "#E2E8F0",
            "size": 12
        },
        "colorway": ["#F59E0B", "#38BDF8", "#10B981", "#818CF8", "#F43F5E", "#EC4899", "#A855F7"],
        "xaxis": {
            "gridcolor": "#334155",
            "linecolor": "#475569",
            "zerolinecolor": "#475569"
        },
        "yaxis": {
            "gridcolor": "#334155",
            "linecolor": "#475569",
            "zerolinecolor": "#475569"
        },
        "margin": {"l": 40, "r": 20, "t": 40, "b": 40}
    }
}
