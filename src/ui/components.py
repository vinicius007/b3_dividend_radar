"""
Componentes Visuais Interativos Estilo Power BI para Streamlit e Plotly.
"""

import textwrap
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
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">📊 Ativos Monitorados</div>
            <div class="pbi-kpi-value">{total_stocks}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">● B3 Ao Vivo</span> 100% Cobertos</div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💰 DY Médio Carteira</div>
            <div class="pbi-kpi-value">{avg_dy:.2f}%</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">▲ Acima Selic Real</span> Últimos 12M</div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with col3:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🏆 Top Score Geral</div>
            <div class="pbi-kpi-value">{top_score_stock['ticker_clean']}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">★ Score {top_score_stock['score']:.1f}</span> {top_score_stock['verdict_badge']}</div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with col4:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🔥 Maior Dividend Yield</div>
            <div class="pbi-kpi-value">{top_yield_stock['dy_12m']:.2f}%</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">{top_yield_stock['ticker_clean']}</span> DPA R$ {top_yield_stock['dpa_12m']:.2f}</div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with col5:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🛡️ Abaixo Preço Teto</div>
            <div class="pbi-kpi-value">{safe_bazin_count} <span style="font-size:16px;color:#64748B;">/ {total_stocks}</span></div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">Décio Bazin (6%)</span> c/ Margem</div>
        </div>
        """).strip(), unsafe_allow_html=True)

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
    fig.update_xaxes(gridcolor="#334155")
    fig.update_yaxes(gridcolor="#334155")

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
        line_color='#38BDF8',
        fillcolor='rgba(56, 189, 248, 0.25)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=bench_vals,
        theta=categories,
        fill='toself',
        name='Média Setor B3',
        line_color='#F59E0B',
        fillcolor='rgba(245, 158, 11, 0.15)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#334155', color='#94A3B8'),
            angularaxis=dict(gridcolor='#334155', color='#F8FAFC')
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
        color_discrete_sequence=["#10B981"]
    )

    fig.update_layout(
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=320,
        margin={"l": 40, "r": 20, "t": 45, "b": 35}
    )
    fig.update_xaxes(gridcolor="#334155", dtick=1)
    fig.update_yaxes(gridcolor="#334155")

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

        news_card_html = f"""
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
        """
        st.markdown(textwrap.dedent(news_card_html).strip(), unsafe_allow_html=True)

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

def render_top_dividend_yields_section(market_df: pd.DataFrame):
    """
    Renderiza o painel executivo: Lista das Ações com Dividendos Mais Rentáveis em Tempo Real.
    """
    if market_df.empty:
        st.info("Nenhum ativo disponível para exibir o ranking de maiores proventos.")
        return

    # Ordenar por Dividend Yield 12M decrescente
    sorted_df = market_df.sort_values(by="dy_12m", ascending=False).reset_index(drop=True)

    # Controles no topo
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.markdown("### 💎 Ações com Maiores Dividendos da B3 em Tempo Real")
        st.caption("Ranking dinâmico das empresas mais rentáveis em proventos com análise de sustentabilidade e valuation")
    with col_c2:
        top_n = st.selectbox("Quantidade de Ativos no Ranking:", [5, 10, 15, 20, "Todos"], index=1, key="top_dy_selector")

    if top_n != "Todos":
        display_df = sorted_df.head(int(top_n)).copy()
    else:
        display_df = sorted_df.copy()

    # Destaque da Ação Campeã em Dividend Yield
    top_stock = sorted_df.iloc[0]
    
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">👑 Maior Dividend Yield B3</div>
            <div class="pbi-kpi-value" style="color:#10B981;">{top_stock['ticker_clean']} ({top_stock['dy_12m']:.2f}%)</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">{top_stock['name']}</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with col_k2:
        avg_top_yield = display_df["dy_12m"].mean()
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">📊 Yield Médio do Grupo</div>
            <div class="pbi-kpi-value">{avg_top_yield:.2f}%</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">Top {len(display_df)} Pagadoras</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with col_k3:
        safe_count = len(display_df[display_df["bazin_margin_safety"] > 0])
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🛡️ Com Margem Bazin Positiva</div>
            <div class="pbi-kpi-value" style="color:#38BDF8;">{safe_count} de {len(display_df)}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">Preço < Teto Bazin</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with col_k4:
        avg_roe = display_df["roe"].mean()
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💎 Retorno Médio s/ PL (ROE)</div>
            <div class="pbi-kpi-value">{avg_roe:.1f}%</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-neutral">Rentabilidade do Capital</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico de Barras Horizontais das Maiores Pagadoras
    fig = px.bar(
        display_df.sort_values(by="dy_12m", ascending=True),
        x="dy_12m",
        y="ticker_clean",
        orientation="h",
        text_auto=".2f",
        title=f"Top {len(display_df)} Maiores Dividend Yields da B3 (%)",
        labels={"dy_12m": "Dividend Yield 12M (%)", "ticker_clean": "Ação"},
        color="dy_12m",
        color_continuous_scale="Greens"
    )

    fig.update_layout(
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=340,
        margin={"l": 40, "r": 20, "t": 45, "b": 35}
    )
    fig.update_xaxes(gridcolor="#334155")
    fig.update_yaxes(gridcolor="#334155")
    st.plotly_chart(fig, use_container_width=True)

    # Tabela Detalhada com Badges e Múltiplos
    table_df = display_df[[
        "ticker_clean", "name", "sector", "price", "dy_12m", "dpa_12m",
        "bazin_target_price", "bazin_margin_safety", "roe", "pl", "pvp", "payout", "verdict"
    ]].copy().rename(columns={
        "ticker_clean": "Ticker",
        "name": "Empresa",
        "sector": "Setor",
        "price": "Cotação (R$)",
        "dy_12m": "Dividend Yield (%)",
        "dpa_12m": "DPA 12M (R$)",
        "bazin_target_price": "Teto Bazin (R$)",
        "bazin_margin_safety": "Margem Bazin (%)",
        "roe": "ROE (%)",
        "pl": "P/L",
        "pvp": "P/VP",
        "payout": "Payout (%)",
        "verdict": "Diagnóstico"
    })

    st.dataframe(
        table_df.style.format({
            "Cotação (R$)": "R$ {:.2f}",
            "Dividend Yield (%)": "{:.2f}%",
            "DPA 12M (R$)": "R$ {:.2f}",
            "Teto Bazin (R$)": "R$ {:.2f}",
            "Margem Bazin (%)": "{:+.1f}%",
            "ROE (%)": "{:.1f}%",
            "P/L": "{:.1f}",
            "P/VP": "{:.2f}",
            "Payout (%)": "{:.1f}%"
        }).background_gradient(
            subset=["Dividend Yield (%)"], cmap="Greens"
        ).background_gradient(
            subset=["Margem Bazin (%)"], cmap="RdYlGn"
        ),
        use_container_width=True
    )

def render_sub_10_bargain_detector(market_df: pd.DataFrame):
    """
    Renderiza o Detector de Ações < R$ 10 com Alto Potencial de Dividendos e Valorização.
    """
    if market_df.empty:
        st.info("Nenhum dado disponível para análise.")
        return

    st.markdown("### 🎯 Detector de Ações Abaixo de R$ 10 com Alto Potencial")
    st.caption("Filtro inteligente para investidores que buscam ativos baratos (acessíveis a pequenos aportes) com proventos elevados e margem de segurança")

    col_s1, col_s2, col_s3 = st.columns([1.5, 1, 1])
    with col_s1:
        max_price = st.slider("Cotação Máxima por Ação (R$):", min_value=5.0, max_value=15.0, value=10.0, step=0.5, format="R$ %.2f")
    with col_s2:
        min_sub_dy = st.slider("DY Mínimo Desejado:", min_value=0.0, max_value=12.0, value=5.0, step=0.5, format="%.1f%%")
    with col_s3:
        order_by = st.selectbox("Ordenar Resultados Por:", ["Score de Recomendação", "Maior Dividend Yield", "Menor Preço", "Maior Margem Bazin"])

    # Filtrar ações abaixo do teto de preço
    sub_df = market_df[market_df["price"] <= max_price].copy()
    sub_df = sub_df[sub_df["dy_12m"] >= min_sub_dy]

    if order_by == "Score de Recomendação":
        sub_df = sub_df.sort_values(by="score", ascending=False)
    elif order_by == "Maior Dividend Yield":
        sub_df = sub_df.sort_values(by="dy_12m", ascending=False)
    elif order_by == "Menor Preço":
        sub_df = sub_df.sort_values(by="price", ascending=True)
    elif order_by == "Maior Margem Bazin":
        sub_df = sub_df.sort_values(by="bazin_margin_safety", ascending=False)

    sub_df = sub_df.reset_index(drop=True)

    if sub_df.empty:
        st.warning(f"Nenhuma ação encontrada com cotação abaixo de R$ {max_price:.2f} e DY mínimo de {min_sub_dy:.1f}%. Tente relaxar os filtros.")
        return

    # KPIs do Detector
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🎯 Ações < R$ {max_price:.0f} Encontradas</div>
            <div class="pbi-kpi-value" style="color:#38BDF8;">{len(sub_df)} ativos</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">Oportunidades B3</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c2:
        cheapest = sub_df.sort_values(by="price").iloc[0]
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🪙 Menor Preço Nominal</div>
            <div class="pbi-kpi-value">{cheapest['ticker_clean']} (R$ {cheapest['price']:.2f})</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">{cheapest['name']}</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c3:
        best_yield_sub = sub_df.sort_values(by="dy_12m", ascending=False).iloc[0]
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💎 Maior DY do Grupo</div>
            <div class="pbi-kpi-value" style="color:#10B981;">{best_yield_sub['ticker_clean']} ({best_yield_sub['dy_12m']:.2f}%)</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">DPA: R$ {best_yield_sub['dpa_12m']:.2f}</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c4:
        avg_score = sub_df["score"].mean()
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">⭐ Score Médio de Qualidade</div>
            <div class="pbi-kpi-value">{avg_score:.1f} / 100</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-neutral">Média Ponderada</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cards Visuais com Destaque de Oportunidade
    st.markdown(f"#### 🔍 Oportunidades em Destaque (< R$ {max_price:.2f})")
    cols = st.columns(min(3, max(1, len(sub_df))))
    
    for idx, row in sub_df.head(6).iterrows():
        col_idx = idx % len(cols)
        with cols[col_idx]:
            bazin_ok = row["bazin_margin_safety"] > 0
            badge_teto = f"🟢 Margem Bazin: {row['bazin_margin_safety']:+.1f}%" if bazin_ok else f"🟡 Teto: R$ {row['bazin_target_price']:.2f}"
            
            card_sub10_html = f"""
            <div class="pbi-action-card" style="border-top: 4px solid #38BDF8;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div>
                        <span class="pbi-action-ticker">{row['ticker_clean']}</span>
                        <span class="pbi-action-name">{row['name']}</span>
                    </div>
                    <span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid #38BDF8; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">
                        {row['sector']}
                    </span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0; padding: 10px; background: #0F172A; border-radius: 6px;">
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Cotação Atual</div>
                        <div style="font-size: 16px; font-weight: 800; color: #F8FAFC;">R$ {row['price']:.2f}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Dividend Yield</div>
                        <div style="font-size: 16px; font-weight: 800; color: #10B981;">{row['dy_12m']:.2f}%</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">P/L & P/VP</div>
                        <div style="font-size: 13px; font-weight: 600; color: #CBD5E1;">{row['pl']:.1f} | {row['pvp']:.2f}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">ROE</div>
                        <div style="font-size: 13px; font-weight: 600; color: #CBD5E1;">{row['roe']:.1f}%</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; font-size: 12px;">
                    <span style="color: #94A3B8;">Preço Justo Graham: <b>R$ {row['graham_fair_value']:.2f}</b></span>
                    <span style="color: {'#10B981' if bazin_ok else '#F59E0B'}; font-weight: 700;">{badge_teto}</span>
                </div>
            </div>
            """
            st.markdown(textwrap.dedent(card_sub10_html).strip(), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabela Completa do Detector
    det_table = sub_df[[
        "ticker_clean", "name", "price", "dy_12m", "dpa_12m", "bazin_target_price",
        "bazin_margin_safety", "graham_fair_value", "graham_margin_safety", "roe", "pl", "pvp", "score", "verdict"
    ]].copy().rename(columns={
        "ticker_clean": "Ticker",
        "name": "Empresa",
        "price": "Cotação (R$)",
        "dy_12m": "DY 12M (%)",
        "dpa_12m": "DPA 12M (R$)",
        "bazin_target_price": "Teto Bazin (R$)",
        "bazin_margin_safety": "Margem Bazin (%)",
        "graham_fair_value": "Justo Graham (R$)",
        "graham_margin_safety": "Margem Graham (%)",
        "roe": "ROE (%)",
        "pl": "P/L",
        "pvp": "P/VP",
        "score": "Score (0-100)",
        "verdict": "Recomendação"
    })

    st.dataframe(
        det_table.style.format({
            "Cotação (R$)": "R$ {:.2f}",
            "DY 12M (%)": "{:.2f}%",
            "DPA 12M (R$)": "R$ {:.2f}",
            "Teto Bazin (R$)": "R$ {:.2f}",
            "Margem Bazin (%)": "{:+.1f}%",
            "Justo Graham (R$)": "R$ {:.2f}",
            "Margem Graham (%)": "{:+.1f}%",
            "ROE (%)": "{:.1f}%",
            "P/L": "{:.1f}",
            "P/VP": "{:.2f}",
            "Score (0-100)": "{:.1f}"
        }).background_gradient(
            subset=["DY 12M (%)"], cmap="Greens"
        ).background_gradient(
            subset=["Score (0-100)"], cmap="Blues"
        ),
        use_container_width=True
    )

def render_market_four_rankings_dashboard(ranked_df: pd.DataFrame):
    """
    Renderiza o painel executivo dos 4 Grandes Rankings da B3 (conforme layout de referência):
    1. AS MAIORES OPORTUNIDADES (Maior potencial em relação ao preço justo)
    2. AS MAIORES PAGADORAS DE DIVIDENDOS (Maior DY 12M e proventos)
    3. AS QUE MAIS CRESCERAM (Maior crescimento de cotação / CAGR de dividendos)
    4. AS QUE MENOS CRESCERAM (Menor crescimento / ações mais descontadas da bolsa)
    """
    if ranked_df.empty:
        st.info("Nenhum dado disponível para exibir os rankings.")
        return

    st.markdown("### 🏆 Grandes Rankings de Ações da B3")
    st.caption("Selecione um dos 4 pilares estratégicos abaixo para explorar a análise detalhada:")

    # Opções do Ranking
    ranking_options = [
        "1. As Maiores Oportunidades",
        "2. As Maiores Pagadoras de Dividendos",
        "3. As Que Mais Cresceram",
        "4. As Que Menos Cresceram"
    ]

    # Renderizar os 4 cards visuais com estilo da imagem de referência
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(textwrap.dedent("""
        <div class="pbi-action-card" style="border-left: 4px solid #38BDF8; min-height: 110px;">
            <div style="display: flex; align-items: flex-start; gap: 10px;">
                <div style="font-size: 22px; line-height: 1;">🥇</div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #F8FAFC; line-height: 1.2;">AS MAIORES OPORTUNIDADES</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 5px; line-height: 1.3;">As ações com maior potencial de crescimento em relação ao preço justo.</div>
                </div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c2:
        st.markdown(textwrap.dedent("""
        <div class="pbi-action-card" style="border-left: 4px solid #10B981; min-height: 110px;">
            <div style="display: flex; align-items: flex-start; gap: 10px;">
                <div style="font-size: 22px; line-height: 1;">💰</div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #F8FAFC; line-height: 1.2;">AS MAIORES PAGADORAS DE DIVIDENDOS</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 5px; line-height: 1.3;">As ações que mais pagaram dividendos nos últimos 12 meses.</div>
                </div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c3:
        st.markdown(textwrap.dedent("""
        <div class="pbi-action-card" style="border-left: 4px solid #F59E0B; min-height: 110px;">
            <div style="display: flex; align-items: flex-start; gap: 10px;">
                <div style="font-size: 22px; line-height: 1;">🚀</div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #F8FAFC; line-height: 1.2;">AS QUE MAIS CRESCERAM</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 5px; line-height: 1.3;">As ações com maior crescimento da sua cotação e proventos.</div>
                </div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c4:
        st.markdown(textwrap.dedent("""
        <div class="pbi-action-card" style="border-left: 4px solid #818CF8; min-height: 110px;">
            <div style="display: flex; align-items: flex-start; gap: 10px;">
                <div style="font-size: 22px; line-height: 1;">🛡️</div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #F8FAFC; line-height: 1.2;">AS QUE MENOS CRESCERAM</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 5px; line-height: 1.3;">As ações com menor crescimento da sua cotação (mais descontadas).</div>
                </div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    selected_rank = st.radio(
        "Selecione a categoria para visualização aprofundada:",
        ranking_options,
        horizontal=True,
        key="selected_market_rank_tab"
    )

    st.markdown("---")

    # 1. AS MAIORES OPORTUNIDADES
    if "Oportunidades" in selected_rank:
        st.markdown("#### 🎯 As Maiores Oportunidades (Maior Desconto vs Preço Justo)")
        st.caption("Ações com maior margem de segurança entre o Preço Justo de Graham e o Preço Teto de Décio Bazin")
        
        # Calcular média ponderada das margens de Bazin e Graham
        df_opp = ranked_df.copy()
        df_opp["avg_margin_safety"] = (df_opp["bazin_margin_safety"] + df_opp["graham_margin_safety"]) / 2.0
        df_opp = df_opp.sort_values(by="avg_margin_safety", ascending=False).reset_index(drop=True)

        top_opp = df_opp.iloc[0]
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("🏆 Maior Desconto Global", f"{top_opp['ticker_clean']}", f"Margem Graham: {top_opp['graham_margin_safety']:+.1f}%")
        with k2:
            st.metric("Teto Bazin Médio", f"R$ {df_opp['bazin_target_price'].head(10).mean():.2f}")
        with k3:
            st.metric("Preço Justo Graham Médio", f"R$ {df_opp['graham_fair_value'].head(10).mean():.2f}")
        with k4:
            st.metric("Dividend Yield Médio Top 10", f"{df_opp['dy_12m'].head(10).mean():.2f}%")

        # Gráfico de Barras do Upside / Margem de Segurança
        fig = px.bar(
            df_opp.head(10).sort_values(by="graham_margin_safety", ascending=True),
            x="graham_margin_safety",
            y="ticker_clean",
            orientation="h",
            text_auto=".1f",
            title="Top 10 Ações com Maior Potencial de Crescimento vs Preço Justo Graham (%)",
            labels={"graham_margin_safety": "Margem de Segurança Graham (%)", "ticker_clean": "Ação"},
            color="graham_margin_safety",
            color_continuous_scale="Blues"
        )
        fig.update_layout(
            paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
            plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
            font=PLOTLY_POWERBI_THEME["layout"]["font"],
            height=340,
            margin={"l": 40, "r": 20, "t": 45, "b": 35}
        )
        fig.update_xaxes(gridcolor="#334155")
        fig.update_yaxes(gridcolor="#334155")
        st.plotly_chart(fig, use_container_width=True)

        render_matrix_table(df_opp.head(15), "📋 Tabela das 15 Maiores Oportunidades em Relação ao Preço Justo")

    # 2. AS MAIORES PAGADORAS DE DIVIDENDOS
    elif "Pagadoras" in selected_rank:
        st.markdown("#### 💰 As Maiores Pagadoras de Dividendos (Últimos 12 Meses)")
        st.caption("Ranking oficial das empresas que entregaram os maiores proventos aos acionistas")
        
        df_div = ranked_df.sort_values(by="dy_12m", ascending=False).reset_index(drop=True)
        top_div = df_div.iloc[0]

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("👑 Campeã de Yield", f"{top_div['ticker_clean']}", f"DY 12M: {top_div['dy_12m']:.2f}%")
        with k2:
            st.metric("DY Médio Top 10", f"{df_div['dy_12m'].head(10).mean():.2f}%")
        with k3:
            st.metric("DPA Médio Top 10", f"R$ {df_div['dpa_12m'].head(10).mean():.2f}")
        with k4:
            st.metric("Payout Médio", f"{df_div['payout'].head(10).mean():.1f}%")

        fig = px.bar(
            df_div.head(10).sort_values(by="dy_12m", ascending=True),
            x="dy_12m",
            y="ticker_clean",
            orientation="h",
            text_auto=".2f",
            title="Top 10 Maiores Pagadoras de Dividendos da B3 (Yield %)",
            labels={"dy_12m": "Dividend Yield 12M (%)", "ticker_clean": "Ação"},
            color="dy_12m",
            color_continuous_scale="Greens"
        )
        fig.update_layout(
            paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
            plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
            font=PLOTLY_POWERBI_THEME["layout"]["font"],
            height=340,
            margin={"l": 40, "r": 20, "t": 45, "b": 35}
        )
        fig.update_xaxes(gridcolor="#334155")
        fig.update_yaxes(gridcolor="#334155")
        st.plotly_chart(fig, use_container_width=True)

        render_matrix_table(df_div.head(15), "📋 Tabela das 15 Maiores Pagadoras de Dividendos")

    # 3. AS QUE MAIS CRESCERAM
    elif "Mais Cresceram" in selected_rank:
        st.markdown("#### 🚀 As Que Mais Cresceram (Expansão de Dividendos & Rentabilidade)")
        st.caption("Empresas com forte taxa de crescimento de proventos (CAGR 3 anos) e elevado retorno sobre capital (ROE)")
        
        df_grow = ranked_df.sort_values(by=["dividend_cagr_3y", "roe"], ascending=[False, False]).reset_index(drop=True)
        top_grow = df_grow.iloc[0]

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("⭐ Líder em Crescimento", f"{top_grow['ticker_clean']}", f"CAGR: {top_grow['dividend_cagr_3y']:+.1f}%")
        with k2:
            st.metric("CAGR Médio Top 10", f"{df_grow['dividend_cagr_3y'].head(10).mean():.1f}% a.a.")
        with k3:
            st.metric("ROE Médio Top 10", f"{df_grow['roe'].head(10).mean():.1f}%")
        with k4:
            st.metric("Margem Líquida Média", f"{df_grow['net_margin'].head(10).mean():.1f}%")

        fig = px.bar(
            df_grow.head(10).sort_values(by="dividend_cagr_3y", ascending=True),
            x="dividend_cagr_3y",
            y="ticker_clean",
            orientation="h",
            text_auto=".1f",
            title="Top 10 Ações com Maior Crescimento Anualizado de Proventos (CAGR 3 Anos %)",
            labels={"dividend_cagr_3y": "CAGR de Proventos 3Y (%)", "ticker_clean": "Ação"},
            color="dividend_cagr_3y",
            color_continuous_scale="YlOrRd"
        )
        fig.update_layout(
            paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
            plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
            font=PLOTLY_POWERBI_THEME["layout"]["font"],
            height=340,
            margin={"l": 40, "r": 20, "t": 45, "b": 35}
        )
        fig.update_xaxes(gridcolor="#334155")
        fig.update_yaxes(gridcolor="#334155")
        st.plotly_chart(fig, use_container_width=True)

        render_matrix_table(df_grow.head(15), "📋 Tabela das 15 Ações com Maior Crescimento de Dividendos e Lucros")

    # 4. AS QUE MENOS CRESCERAM
    else:
        st.markdown("#### 🛡️ As Que Menos Cresceram (Mais Descontadas / Menor Preço)")
        st.caption("Ações negociadas com os menores múltiplos de valuation (menor P/L e menor P/VP), com grande potencial de valorização acumulada")
        
        # Ordenar por menor P/L e menor P/VP
        df_value = ranked_df[ranked_df["pl"] > 0].copy().sort_values(by=["pl", "pvp"], ascending=[True, True]).reset_index(drop=True)
        top_val = df_value.iloc[0]

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("💎 Menor P/L da B3", f"{top_val['ticker_clean']}", f"P/L: {top_val['pl']:.1f}x")
        with k2:
            st.metric("P/L Médio do Grupo", f"{df_value['pl'].head(10).mean():.1f}x")
        with k3:
            st.metric("P/VP Médio do Grupo", f"{df_value['pvp'].head(10).mean():.2f}x")
        with k4:
            st.metric("Yield Médio deste Grupo", f"{df_value['dy_12m'].head(10).mean():.2f}%")

        fig = px.bar(
            df_value.head(10).sort_values(by="pl", ascending=False),
            x="pl",
            y="ticker_clean",
            orientation="h",
            text_auto=".1f",
            title="Top 10 Ações Mais Baratas por Preço sobre Lucro (Menor P/L)",
            labels={"pl": "Preço / Lucro (P/L)", "ticker_clean": "Ação"},
            color="pl",
            color_continuous_scale="Purples_r"
        )
        fig.update_layout(
            paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
            plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
            font=PLOTLY_POWERBI_THEME["layout"]["font"],
            height=340,
            margin={"l": 40, "r": 20, "t": 45, "b": 35}
        )
        fig.update_xaxes(gridcolor="#334155")
        fig.update_yaxes(gridcolor="#334155")
        st.plotly_chart(fig, use_container_width=True)

        render_matrix_table(df_value.head(15), "📋 Tabela das 15 Ações com Menor Crescimento de Cotação (Deep Value)")


