"""
Componentes Visuais de Gestão de Carteira e Gráficos Executivos Estilo Power BI.
Inclui gráficos Pizza de Investimento, Pizza de Valor Real, Barras Verticais de Lucro/Perda e Formulário de Cadastro.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from src.ui.powerbi_theme import PLOTLY_POWERBI_THEME
from src.data.portfolio_manager import (
    load_transactions,
    add_transaction,
    delete_transaction,
    get_portfolio_summary
)

def render_portfolio_kpis(summary: Dict[str, Any]):
    """Renderiza os 4 cartões de KPI consolidados da carteira do investidor."""
    total_invested = summary.get("total_invested", 0.0)
    current_val = summary.get("total_current_value", 0.0)
    profit_loss = summary.get("total_profit_loss", 0.0)
    profit_loss_pct = summary.get("total_profit_loss_pct", 0.0)
    annual_divs = summary.get("total_annual_dividends", 0.0)
    monthly_divs = summary.get("total_monthly_dividends", 0.0)

    pl_tag = "pbi-tag-positive" if profit_loss >= 0 else "pbi-tag-caution"
    pl_arrow = "▲" if profit_loss >= 0 else "▼"
    pl_color = "#059669" if profit_loss >= 0 else "#DC2626"

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💵 Total Investido (Compra)</div>
            <div class="pbi-kpi-value">R$ {total_invested:,.2f}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-neutral">Custo de Aquisição</span> Acumulado</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💎 Patrimônio Atual (Real)</div>
            <div class="pbi-kpi-value" style="color:#0284C7;">R$ {current_val:,.2f}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">● Cotação B3 Ao Vivo</span> a Mercado</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">📈 Lucro / Prejuízo Total</div>
            <div class="pbi-kpi-value" style="color:{pl_color};">
                {pl_arrow} R$ {abs(profit_loss):,.2f}
            </div>
            <div class="pbi-kpi-sub">
                <span class="{pl_tag}">{profit_loss_pct:+.2f}%</span> Rentabilidade da Carteira
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💰 Proventos Anuais Estimados</div>
            <div class="pbi-kpi-value" style="color:#059669;">R$ {annual_divs:,.2f}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">~ R$ {monthly_divs:,.2f}/mês</span> em Dividendos</div>
        </div>
        """, unsafe_allow_html=True)

def render_pie_invested_chart(summary: Dict[str, Any]):
    """
    Gráfico 1: Valor Investido de Compra dos Ativos (Formato Pizza / Donut estilo Power BI).
    Exibe distribuição por ação e o Total Investido no centro.
    """
    assets_df = summary.get("assets_df", pd.DataFrame())
    total_invested = summary.get("total_invested", 0.0)

    if assets_df.empty:
        st.info("Nenhum ativo cadastrado para gerar o gráfico de investimento.")
        return

    fig = go.Figure(data=[go.Pie(
        labels=assets_df["ticker_clean"],
        values=assets_df["total_invested"],
        hole=0.55,
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Valor Investido: R$ %{value:,.2f}<br>Participação: %{percent}<extra></extra>",
        marker=dict(
            colors=["#0284C7", "#059669", "#D97706", "#7C3AED", "#2563EB", "#DB2777", "#F59E0B", "#10B981", "#6366F1"],
            line=dict(color="#FFFFFF", width=2)
        )
    )])

    fig.update_layout(
        title=dict(
            text=f"<b>Distribuição do Valor Investido de Compra</b><br><span style='font-size:13px; color:#475569;'>Total Investido: <b>R$ {total_invested:,.2f}</b></span>",
            x=0.05,
            y=0.95
        ),
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=380,
        margin=dict(l=20, r=20, t=70, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )

    st.plotly_chart(fig, use_container_width=True)

def render_pie_current_value_chart(summary: Dict[str, Any]):
    """
    Gráfico 2: Valor Real Atualizado dos Ativos (Formato Pizza / Donut estilo Power BI).
    Exibe distribuição por ação e o Patrimônio Total Atualizado no centro.
    """
    assets_df = summary.get("assets_df", pd.DataFrame())
    total_current = summary.get("total_current_value", 0.0)

    if assets_df.empty:
        st.info("Nenhum ativo cadastrado para gerar o gráfico de valor atualizado.")
        return

    fig = go.Figure(data=[go.Pie(
        labels=assets_df["ticker_clean"],
        values=assets_df["current_value"],
        hole=0.55,
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Valor Atual B3: R$ %{value:,.2f}<br>Participação: %{percent}<extra></extra>",
        marker=dict(
            colors=["#0284C7", "#059669", "#D97706", "#7C3AED", "#2563EB", "#DB2777", "#F59E0B", "#10B981", "#6366F1"],
            line=dict(color="#FFFFFF", width=2)
        )
    )])

    fig.update_layout(
        title=dict(
            text=f"<b>Distribuição do Valor Real Atualizado (B3)</b><br><span style='font-size:13px; color:#0284C7;'>Patrimônio Atual: <b>R$ {total_current:,.2f}</b></span>",
            x=0.05,
            y=0.95
        ),
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=380,
        margin=dict(l=20, r=20, t=70, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )

    st.plotly_chart(fig, use_container_width=True)

def render_bar_profit_loss_chart(summary: Dict[str, Any]):
    """
    Gráfico 3: Lucro / Prejuízo dos Ativos Cadastrados (Formato Barra Vertical estilo Power BI).
    Exibe barras verdes (lucro) ou vermelhas (perda) por ação e valor total atualizado.
    """
    assets_df = summary.get("assets_df", pd.DataFrame())
    total_pl = summary.get("total_profit_loss", 0.0)
    total_pl_pct = summary.get("total_profit_loss_pct", 0.0)

    if assets_df.empty:
        st.info("Nenhum ativo cadastrado para gerar o gráfico de lucro/perda.")
        return

    # Cores condicionais: Verde para lucro, Vermelho para prejuízo
    colors = ["#059669" if val >= 0 else "#DC2626" for val in assets_df["profit_loss"]]

    fig = go.Figure(data=[go.Bar(
        x=assets_df["ticker_clean"],
        y=assets_df["profit_loss"],
        marker_color=colors,
        text=[f"R$ {v:,.2f} ({p:+.1f}%)" for v, p in zip(assets_df["profit_loss"], assets_df["profit_loss_pct"])],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Lucro/Prejuízo: R$ %{y:,.2f}<br>Preço Médio: R$ %{customdata[0]:.2f}<br>Preço Atual: R$ %{customdata[1]:.2f}<br>Qtd: %{customdata[2]} ações<extra></extra>",
        customdata=assets_df[["avg_price", "current_price", "quantity"]].values
    )])

    pl_sign = "+" if total_pl >= 0 else ""
    fig.update_layout(
        title=dict(
            text=f"<b>Lucro / Prejuízo por Ativo Cadastrado (R$)</b> &bull; Resultado Consolidado: <b style='color:{'#059669' if total_pl>=0 else '#DC2626'};'>{pl_sign}R$ {total_pl:,.2f} ({total_pl_pct:+.2f}%)</b>",
            x=0.02,
            y=0.95
        ),
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=380,
        margin=dict(l=40, r=20, t=65, b=40),
        xaxis=dict(gridcolor="#E2E8F0", title="Ação (Ticker)"),
        yaxis=dict(gridcolor="#E2E8F0", zerolinecolor="#475569", zerolinewidth=1.5, title="Resultado Nominal (R$)")
    )

    st.plotly_chart(fig, use_container_width=True)

def render_portfolio_summary_table(summary: Dict[str, Any]):
    """Tabela detalhada consolidada dos ativos em custódia."""
    assets_df = summary.get("assets_df", pd.DataFrame())
    if assets_df.empty:
        return

    st.markdown('<div class="pbi-chart-title">📋 Posição Detalhada da Carteira por Ativo</div>', unsafe_allow_html=True)
    
    display_df = assets_df[[
        "ticker_clean", "name", "quantity", "avg_price", "current_price",
        "total_invested", "current_value", "profit_loss", "profit_loss_pct",
        "dy_12m", "estimated_annual_dividends", "weight_current_pct"
    ]].copy().rename(columns={
        "ticker_clean": "Ticker",
        "name": "Empresa",
        "quantity": "Qtd",
        "avg_price": "Preço Médio (R$)",
        "current_price": "Cotação Atual (R$)",
        "total_invested": "Total Investido (R$)",
        "current_value": "Valor Atual (R$)",
        "profit_loss": "Lucro/Prejuízo (R$)",
        "profit_loss_pct": "Rentabilidade (%)",
        "dy_12m": "DY 12M (%)",
        "estimated_annual_dividends": "Proventos Estimados/Ano (R$)",
        "weight_current_pct": "Peso na Carteira (%)"
    })

    st.dataframe(
        display_df.style.format({
            "Qtd": "{:d}",
            "Preço Médio (R$)": "R$ {:.2f}",
            "Cotação Atual (R$)": "R$ {:.2f}",
            "Total Investido (R$)": "R$ {:,.2f}",
            "Valor Atual (R$)": "R$ {:,.2f}",
            "Lucro/Prejuízo (R$)": "R$ {:+,.2f}",
            "Rentabilidade (%)": "{:+.2f}%",
            "DY 12M (%)": "{:.2f}%",
            "Proventos Estimados/Ano (R$)": "R$ {:,.2f}",
            "Peso na Carteira (%)": "{:.1f}%"
        }).background_gradient(
            subset=["Rentabilidade (%)"], cmap="RdYlGn"
        ).background_gradient(
            subset=["Peso na Carteira (%)"], cmap="Blues"
        ),
        use_container_width=True
    )
