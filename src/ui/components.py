"""
Componentes Visuais Interativos Estilo Power BI para Streamlit e Plotly.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from src.ui.powerbi_theme import PLOTLY_POWERBI_THEME

def render_kpi_header(ranked_df: pd.DataFrame):
    """Renderiza a linha superior de cartões de KPI executivos estilo Power BI."""
    if ranked_df.empty:
        return

    top_yield_stock = ranked_df.sort_values(by="dy_12m", ascending=False).iloc[0]
    top_score_stock = ranked_df.iloc[0]
    avg_dy = ranked_df["dy_12m"].mean()
    safe_bazin_count = len(ranked_df[ranked_df["bazin_margin_safety"] > 0])
    total_stocks = len(ranked_df)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">📊 Ativos Monitorados</div>
            <div class="pbi-kpi-value">{total_stocks}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">● B3 Ao Vivo</span> 100% Cobertos</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💰 DY Médio Carteira</div>
            <div class="pbi-kpi-value">{avg_dy:.2f}%</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">▲ Acima Selic Real</span> Últimos 12M</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🏆 Top Score Geral</div>
            <div class="pbi-kpi-value">{top_score_stock['ticker_clean']}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">★ Score {top_score_stock['score']:.1f}</span> {top_score_stock['verdict_badge']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🔥 Maior Dividend Yield</div>
            <div class="pbi-kpi-value">{top_yield_stock['dy_12m']:.2f}%</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">{top_yield_stock['ticker_clean']}</span> DPA R$ {top_yield_stock['dpa_12m']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🛡️ Abaixo Preço Teto</div>
            <div class="pbi-kpi-value">{safe_bazin_count} <span style="font-size:16px;color:#64748B;">/ {total_stocks}</span></div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">Décio Bazin (6%)</span> c/ Margem</div>
        </div>
        """, unsafe_allow_html=True)

def render_matrix_table(df: pd.DataFrame, title: str = "Matriz Fundamentalista de Proventos B3"):
    """Renderiza a matriz de dados com formatação estilo tabela do Power BI."""
    st.markdown(f'<div class="pbi-chart-title">{title}</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("Nenhuma ação encontrada com os filtros selecionados.")
        return

    display_cols = [
        "ticker_clean", "name", "sector", "frequency_label", "price", 
        "dy_12m", "dpa_12m", "bazin_target_price", "bazin_margin_safety", 
        "pl", "roe", "score", "verdict"
    ]
    
    # Filtrar apenas colunas existentes
    existing_cols = [c for c in display_cols if c in df.columns]
    table_df = df[existing_cols].copy()

    rename_map = {
        "ticker_clean": "Ticker",
        "name": "Empresa",
        "sector": "Setor",
        "frequency_label": "Frequência",
        "price": "Cotação (R$)",
        "dy_12m": "DY 12M (%)",
        "dpa_12m": "DPA 12M (R$)",
        "bazin_target_price": "Teto Bazin (R$)",
        "bazin_margin_safety": "Margem Bazin (%)",
        "pl": "P/L",
        "roe": "ROE (%)",
        "score": "Score (0-100)",
        "verdict": "Recomendação"
    }
    table_df = table_df.rename(columns=rename_map)

    # Formatação condicional moderna
    st.dataframe(
        table_df.style.format({
            "Cotação (R$)": "R$ {:.2f}",
            "DY 12M (%)": "{:.2f}%",
            "DPA 12M (R$)": "R$ {:.2f}",
            "Teto Bazin (R$)": "R$ {:.2f}",
            "Margem Bazin (%)": "{:+.1f}%",
            "P/L": "{:.1f}",
            "ROE (%)": "{:.1f}%",
            "Score (0-100)": "{:.1f}"
        }).background_gradient(
            subset=["DY 12M (%)"], cmap="YlGn"
        ).background_gradient(
            subset=["Score (0-100)"], cmap="Blues"
        ).background_gradient(
            subset=["ROE (%)"], cmap="Purples"
        ),
        use_container_width=True,
        height=min(450, 40 + len(table_df) * 35)
    )

def render_quadrant_scatter_chart(df: pd.DataFrame):
    """
    Gráfico de Dispersão / Quadrantes Estilo Power BI:
    Eixo X: P/L (Valuation) ou Margem Bazin
    Eixo Y: Dividend Yield (%)
    Tamanho da Bolha: ROE (%)
    Cor: Categoria / Frequência
    """
    if df.empty:
        return

    fig = px.scatter(
        df,
        x="roe",
        y="dy_12m",
        size="score",
        color="frequency_label",
        hover_name="ticker_clean",
        hover_data={
            "name": True,
            "price": ":.2f",
            "dpa_12m": ":.2f",
            "bazin_target_price": ":.2f",
            "bazin_margin_safety": ":.1f",
            "score": ":.1f",
            "verdict": True
        },
        labels={
            "roe": "Retorno sobre Patrimônio Líquido - ROE (%)",
            "dy_12m": "Dividend Yield 12M (%)",
            "frequency_label": "Frequência de Proventos",
            "score": "Score Geral"
        },
        title="Matriz de Oportunidades: Dividend Yield vs Rentabilidade (ROE)",
        color_discrete_sequence=["#10B981", "#38BDF8", "#F59E0B", "#818CF8", "#F43F5E"]
    )

    # Linhas de referência de qualidade
    fig.add_hline(y=6.0, line_dash="dash", line_color="#F59E0B", annotation_text="Meta Bazin: 6% DY", annotation_position="bottom right")
    fig.add_vline(x=15.0, line_dash="dash", line_color="#38BDF8", annotation_text="Benchmark ROE: 15%", annotation_position="top left")

    fig.update_layout(
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=420,
        margin={"l": 40, "r": 20, "t": 50, "b": 40},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(gridcolor="#E2E8F0")
    fig.update_yaxes(gridcolor="#E2E8F0")

    st.plotly_chart(fig, use_container_width=True)

def render_radar_comparison_chart(selected_stock: Dict[str, Any], sector_avg: Dict[str, float]):
    """Gráfico Radar comparando a ação selecionada vs Média Setorial da B3."""
    categories = ['Dividend Yield', 'ROE', 'Margem Líquida', 'Margem Bazin', 'Saúde Dívida']
    
    # Normalizar valores para escala 0 a 100 para o Radar
    stock_vals = [
        min(100, selected_stock.get("dy_12m", 0) * 8),
        min(100, selected_stock.get("roe", 0) * 3),
        min(100, selected_stock.get("net_margin", 0) * 2),
        min(100, max(0, selected_stock.get("bazin_margin_safety", 0) + 50)),
        min(100, max(0, 100 - (selected_stock.get("debt_ebitda", 1.5) * 25)))
    ]

    bench_vals = [
        min(100, sector_avg.get("dy_12m", 7.0) * 8),
        min(100, sector_avg.get("roe", 16.0) * 3),
        min(100, sector_avg.get("net_margin", 20.0) * 2),
        min(100, max(0, sector_avg.get("bazin_margin_safety", 10.0) + 50)),
        min(100, max(0, 100 - (sector_avg.get("debt_ebitda", 1.8) * 25)))
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=stock_vals,
        theta=categories,
        fill='toself',
        name=selected_stock.get("ticker_clean", "Ação"),
        line_color='#0284C7',
        fillcolor='rgba(2, 132, 199, 0.25)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=bench_vals,
        theta=categories,
        fill='toself',
        name='Média Setor B3',
        line_color='#D97706',
        fillcolor='rgba(217, 119, 6, 0.15)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#E2E8F0', color='#475569'),
            angularaxis=dict(gridcolor='#E2E8F0', color='#0F172A')
        ),
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=380,
        margin={"l": 40, "r": 40, "t": 30, "b": 30},
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )

    st.plotly_chart(fig, use_container_width=True)

def render_dividend_history_bars(stock_data: Dict[str, Any]):
    """Gráfico de Barras do Histórico de Pagamentos de Proventos."""
    hist = stock_data.get("dividend_history", [])
    if not hist:
        st.info("Histórico de distribuições não disponível.")
        return

    hist_df = pd.DataFrame(hist)
    if "year" not in hist_df.columns:
        return

    yearly_sum = hist_df.groupby("year")["value"].sum().reset_index()

    fig = px.bar(
        yearly_sum,
        x="year",
        y="value",
        text_auto=".2f",
        title=f"Evolução de Dividendos Pagos por Ação (DPA) - {stock_data.get('ticker_clean')}",
        labels={"year": "Ano", "value": "Proventos por Ação (R$)"},
        color_discrete_sequence=["#059669"]
    )

    fig.update_layout(
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=320,
        margin={"l": 40, "r": 20, "t": 45, "b": 35}
    )
    fig.update_xaxes(gridcolor="#E2E8F0", dtick=1)
    fig.update_yaxes(gridcolor="#E2E8F0")

    st.plotly_chart(fig, use_container_width=True)

def render_monthly_calendar_grid(stocks: List[Dict[str, Any]]):
    """Exibe o mapa de calor de meses de pagamento de dividendos."""
    months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    
    rows = []
    for s in stocks:
        p_m = s.get("payment_months", [])
        row = {"Ticker": s.get("ticker_clean", s.get("ticker"))}
        for i, m in enumerate(months, start=1):
            row[m] = "💰 Pago" if i in p_m else ""
        rows.append(row)

    cal_df = pd.DataFrame(rows).set_index("Ticker")
    
    st.markdown("##### 📅 Calendário de Fluxo de Proventos Anual")
    st.dataframe(
        cal_df,
        use_container_width=True
    )

def render_news_feed(news_items: List[Dict[str, Any]], stock_ticker: str = ""):
    """Renderiza a lista de notícias corporativas com badges de sentimento e links reais."""
    if not news_items:
        st.info("Nenhuma notícia recente encontrada para este ativo.")
        return

    for item in news_items:
        title = item.get("title", "")
        source = item.get("source", "Mercado")
        pub = item.get("published", "")
        link = item.get("link", "#")
        summary = item.get("summary", "")
        score = item.get("sentiment_score", 0.0)

        if score >= 0.2:
            tag_color = "#10B981"
            tag_text = "POSITIVO"
        elif score <= -0.2:
            tag_color = "#EF4444"
            tag_text = "NEGATIVO"
        else:
            tag_color = "#94A3B8"
            tag_text = "NEUTRO"

        st.markdown(f"""
        <div class="pbi-action-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                <div class="pbi-news-title">{title}</div>
                <span style="background:{tag_color}22; color:{tag_color}; border:1px solid {tag_color}; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; white-space:nowrap; margin-left:12px;">
                    {tag_text}
                </span>
            </div>
            <div class="pbi-news-meta">
                <span>📰 <b>{source}</b></span>
                <span>⏱️ {pub}</span>
            </div>
            <div class="pbi-news-summary">{summary}</div>
            <div style="margin-top:10px;">
                <a href="{link}" target="_blank" style="color:#38BDF8; font-size:12px; font-weight:600; text-decoration:none;">
                    🔗 Ler matéria completa no portal &rarr;
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_passive_income_calculator(selected_stock: Dict[str, Any]):
    """Simulador Interativo de Renda Passiva de Dividendos."""
    st.markdown('<div class="pbi-chart-title">💰 Simulador de Renda Passiva e Independência Financeira</div>', unsafe_allow_html=True)
    
    col_input, col_result = st.columns([1, 1.4])
    
    with col_input:
        target_monthly_income = st.number_input(
            "Meta de Renda Mensal Desejada (R$)",
            min_value=500.0,
            max_value=100000.0,
            value=2500.0,
            step=500.0
        )
        
        price = selected_stock.get("price", 20.0)
        dpa = selected_stock.get("dpa_12m", 1.5)
        dy = selected_stock.get("dy_12m", 7.5)
        ticker = selected_stock.get("ticker_clean", "Ativo")

    with col_result:
        target_annual_income = target_monthly_income * 12
        shares_needed = int(target_annual_income / dpa) if dpa > 0 else 0
        capital_needed = shares_needed * price

        c1, c2 = st.columns(2)
        with c1:
            st.metric(
                label=f"Ações de {ticker} Necessárias",
                value=f"{shares_needed:,}".replace(",", ".")
            )
        with c2:
            st.metric(
                label="Patrimônio Total Estimado",
                value=f"R$ {capital_needed:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

        st.caption(f"💡 Baseado no dividendo pago nos últimos 12 meses (R$ {dpa:.2f}/ação, DY {dy:.2f}%). Reinvestindo proventos, o tempo para atingir a meta diminui expressivamente pelo efeito dos juros compostos.")
