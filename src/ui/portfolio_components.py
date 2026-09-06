"""
Componentes Visuais de Gestão de Carteira e Gráficos Executivos Estilo Power BI (Dark Slate).
Inclui gráficos Pizza de Investimento, Pizza de Valor Real, Barras Verticais de Lucro/Perda e Formulário de Cadastro.
"""

import textwrap
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
    pl_color = "#10B981" if profit_loss >= 0 else "#EF4444"

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💵 Total Investido (Compra)</div>
            <div class="pbi-kpi-value">R$ {total_invested:,.2f}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-neutral">Custo de Aquisição</span> Acumulado</div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c2:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💎 Patrimônio Atual (Real)</div>
            <div class="pbi-kpi-value" style="color:#38BDF8;">R$ {current_val:,.2f}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">● Cotação B3 Ao Vivo</span> a Mercado</div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c3:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">📈 Lucro / Prejuízo Total</div>
            <div class="pbi-kpi-value" style="color:{pl_color};">
                {pl_arrow} R$ {abs(profit_loss):,.2f}
            </div>
            <div class="pbi-kpi-sub">
                <span class="{pl_tag}">{profit_loss_pct:+.2f}%</span> Rentabilidade da Carteira
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c4:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">💰 Proventos Anuais Estimados</div>
            <div class="pbi-kpi-value" style="color:#10B981;">R$ {annual_divs:,.2f}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">~ R$ {monthly_divs:,.2f}/mês</span> em Dividendos</div>
        </div>
        """).strip(), unsafe_allow_html=True)

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
            colors=["#F59E0B", "#38BDF8", "#10B981", "#818CF8", "#F43F5E", "#EC4899", "#A855F7", "#06B6D4", "#EAB308"],
            line=dict(color="#1E293B", width=2)
        )
    )])

    fig.update_layout(
        title=dict(
            text=f"<b>Distribuição do Valor Investido de Compra</b><br><span style='font-size:13px; color:#94A3B8;'>Total Investido: <b>R$ {total_invested:,.2f}</b></span>",
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
            colors=["#38BDF8", "#10B981", "#F59E0B", "#818CF8", "#F43F5E", "#EC4899", "#A855F7", "#06B6D4", "#EAB308"],
            line=dict(color="#1E293B", width=2)
        )
    )])

    fig.update_layout(
        title=dict(
            text=f"<b>Distribuição do Valor Real Atualizado (B3)</b><br><span style='font-size:13px; color:#38BDF8;'>Patrimônio Atual: <b>R$ {total_current:,.2f}</b></span>",
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
    colors = ["#10B981" if val >= 0 else "#EF4444" for val in assets_df["profit_loss"]]

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
            text=f"<b>Lucro / Prejuízo por Ativo Cadastrado (R$)</b> &bull; Resultado Consolidado: <b style='color:{'#10B981' if total_pl>=0 else '#EF4444'};'>{pl_sign}R$ {total_pl:,.2f} ({total_pl_pct:+.2f}%)</b>",
            x=0.02,
            y=0.95
        ),
        paper_bgcolor=PLOTLY_POWERBI_THEME["layout"]["paper_bgcolor"],
        plot_bgcolor=PLOTLY_POWERBI_THEME["layout"]["plot_bgcolor"],
        font=PLOTLY_POWERBI_THEME["layout"]["font"],
        height=380,
        margin=dict(l=40, r=20, t=65, b=40),
        xaxis=dict(gridcolor="#334155", title="Ação (Ticker)"),
        yaxis=dict(gridcolor="#334155", zerolinecolor="#64748B", zerolinewidth=1.5, title="Resultado Nominal (R$)")
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

def render_dividend_alerts_section(alerts_data: Dict[str, Any]):
    """
    Renderiza o painel executivo do Sistema de Alertas de Dividendos do Mês.
    """
    month_name = alerts_data.get("month_name", "Mês Atual")
    has_alerts = alerts_data.get("has_alerts", False)
    paying_stocks = alerts_data.get("paying_stocks", [])
    total_month_payout = alerts_data.get("total_month_payout", 0.0)
    stocks_count = alerts_data.get("stocks_count", 0)
    next_month_name = alerts_data.get("next_month_name", "")
    next_paying = alerts_data.get("next_paying_stocks", [])
    next_month_total = sum(s.get("payout_val", 0.0) for s in next_paying)

    # Banner de Alerta Principal
    if has_alerts:
        banner_border = "#10B981"
        banner_bg = "linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(30, 41, 59, 0.95) 100%)"
        alert_tag = "🚨 ALERTA ATIVO &bull; PAGAMENTOS PREVISTOS"
    else:
        banner_border = "#64748B"
        banner_bg = "linear-gradient(135deg, rgba(100, 116, 139, 0.15) 0%, rgba(30, 41, 59, 0.95) 100%)"
        alert_tag = "ℹ️ RADAR DE PROVENTOS"

    st.markdown(textwrap.dedent(f"""
    <div style="background:{banner_bg}; border:2px solid {banner_border}; border-radius:12px; padding:18px 22px; margin-bottom:18px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <span style="background:{banner_border}33; color:{banner_border}; border:1px solid {banner_border}; padding:3px 10px; border-radius:14px; font-size:11px; font-weight:700; letter-spacing:0.5px;">
                    {alert_tag}
                </span>
                <div style="font-size:20px; font-weight:800; color:#F8FAFC; margin-top:8px;">
                    🚨 Monitor de Proventos: <b>{month_name.upper()}</b>
                </div>
                <div style="font-size:13px; color:#CBD5E1; margin-top:3px;">
                    {f"Você possui <b>{stocks_count} ações</b> na carteira com histórico de pagamentos neste mês!" if has_alerts else "Nenhum ativo com pagamento histórico para este mês. Alterne os meses abaixo para explorar."}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:12px; color:#94A3B8; text-transform:uppercase; font-weight:700;">Previsão a Receber no Mês</div>
                <div style="font-size:28px; font-weight:800; color:#10B981; letter-spacing:-0.5px;">
                    R$ {total_month_payout:,.2f}
                </div>
            </div>
        </div>
    </div>
    """).strip(), unsafe_allow_html=True)

    # 4 Cards Rápidos de Alertas do Mês
    c_a1, c_a2, c_a3, c_a4 = st.columns(4)
    with c_a1:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🔔 Ações Pagadoras ({month_name[:3]})</div>
            <div class="pbi-kpi-value">{stocks_count}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">Ativos da Carteira</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c_a2:
        top_paying_name = f"{paying_stocks[0]['ticker_clean']} (R$ {paying_stocks[0]['payout_val']:,.2f})" if paying_stocks else "-"
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">🏆 Maior Provento do Mês</div>
            <div class="pbi-kpi-value" style="font-size:19px;">{top_paying_name}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">Destaque do Mês</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c_a3:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">⏳ Radar: {next_month_name}</div>
            <div class="pbi-kpi-value" style="color:#38BDF8;">R$ {next_month_total:,.2f}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-positive">{len(next_paying)} ativos</span> no próximo mês</div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c_a4:
        avg_per_stock = (total_month_payout / stocks_count) if stocks_count > 0 else 0.0
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-kpi-card">
            <div class="pbi-kpi-label">📊 Média por Ativo Pagador</div>
            <div class="pbi-kpi-value">R$ {avg_per_stock:,.2f}</div>
            <div class="pbi-kpi-sub"><span class="pbi-tag-neutral">Média do Mês</span></div>
        </div>
        """).strip(), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Detalhamento de cada Ação Pagadora no Mês
    if has_alerts:
        st.markdown(f"##### 💰 Ações da sua Carteira com Proventos em **{month_name}**")
        cols = st.columns(min(3, max(1, len(paying_stocks))))
        
        for idx, stock in enumerate(paying_stocks):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                stock_card_html = f"""
                <div class="pbi-action-card" style="border-left: 4px solid #10B981;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <div>
                            <span class="pbi-action-ticker">{stock['ticker_clean']}</span>
                            <span class="pbi-action-name">{stock['name']}</span>
                        </div>
                        <span style="background:rgba(16, 185, 129, 0.15); color:#10B981; border:1px solid #10B981; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700;">
                            {stock['frequency_label']}
                        </span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:10px; padding:8px; background:#0F172A; border-radius:6px;">
                        <div>
                            <div style="font-size:11px; color:#94A3B8;">Posição em Custódia</div>
                            <div style="font-size:14px; font-weight:700; color:#F8FAFC;">{stock['quantity']} ações</div>
                        </div>
                        <div>
                            <div style="font-size:11px; color:#94A3B8;">DPA Estimado/Ação</div>
                            <div style="font-size:14px; font-weight:700; color:#F8FAFC;">R$ {stock['dpa_distribution']:.2f}</div>
                        </div>
                    </div>
                    <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:12px; color:#94A3B8;">Total a Receber:</span>
                        <span style="font-size:18px; font-weight:800; color:#10B981;">R$ {stock['payout_val']:,.2f}</span>
                    </div>
                </div>
                """
                st.markdown(textwrap.dedent(stock_card_html).strip(), unsafe_allow_html=True)
    else:
        st.info(f"Nenhum ativo da sua carteira possui distribuição regular prevista para o mês de **{month_name}**.")

def render_portfolio_dip_alerts(dip_data: Dict[str, Any]):
    """
    Renderiza os alertas de ativos que estão sendo negociados abaixo do preço médio de compra (Preço < PM).
    """
    has_dips = dip_data.get("has_dip_alerts", False)
    dip_count = dip_data.get("dip_count", 0)
    dip_stocks = dip_data.get("dip_stocks", [])
    total_unrealized_loss = dip_data.get("total_unrealized_loss", 0.0)

    if not has_dips:
        st.markdown(textwrap.dedent("""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px;">
            <span style="color: #10B981; font-weight: 700; font-size: 14px;">
                🎉 Excelente Postura de Carteira!
            </span>
            <div style="color: #E2E8F0; font-size: 13px; margin-top: 4px;">
                Todos os ativos em custódia estão sendo negociados <b>acima ou no mesmo nível</b> do seu Preço Médio de compra!
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)
        return

    st.markdown(textwrap.dedent(f"""
    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(30, 41, 59, 0.95) 100%); border: 2px solid #EF4444; border-radius: 12px; padding: 18px 22px; margin-bottom: 18px; box-shadow: 0 4px 16px rgba(239, 68, 68, 0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="background: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1px solid #EF4444; padding: 3px 10px; border-radius: 14px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;">
                    🔻 ALERTA DE PREÇO MÉDIO &bull; OPORTUNIDADE / RISCO
                </span>
                <div style="font-size: 20px; font-weight: 800; color: #F8FAFC; margin-top: 8px;">
                    ⚠️ {dip_count} {f"Ações Abaixo" if dip_count > 1 else "Ação Abaixo"} do seu Preço Médio de Compra
                </div>
                <div style="font-size: 13px; color: #CBD5E1; margin-top: 3px;">
                    Ativos negociados com desconto em relação ao preço pago. Analise o Preço Teto de Bazin para identificar se há oportunidade de baixar o Preço Médio (PM).
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 12px; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Desconto Total Acumulado</div>
                <div style="font-size: 28px; font-weight: 800; color: #EF4444; letter-spacing: -0.5px;">
                    - R$ {total_unrealized_loss:,.2f}
                </div>
            </div>
        </div>
    </div>
    """).strip(), unsafe_allow_html=True)

    # Cards para cada ação abaixo do Preço Médio
    cols = st.columns(min(3, max(1, len(dip_stocks))))
    for idx, s in enumerate(dip_stocks):
        col_idx = idx % len(cols)
        with cols[col_idx]:
            card_html = f"""
            <div class="pbi-action-card" style="border-left: 4px solid #EF4444;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <span class="pbi-action-ticker">{s['ticker_clean']}</span>
                        <span class="pbi-action-name">{s['name']}</span>
                    </div>
                    <span style="background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid #EF4444; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 800;">
                        {s['diff_pct']:+.2f}%
                    </span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0; padding: 10px; background: #0F172A; border-radius: 6px;">
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Preço Médio Pago</div>
                        <div style="font-size: 15px; font-weight: 700; color: #F8FAFC;">R$ {s['avg_price']:.2f}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Cotação Atual B3</div>
                        <div style="font-size: 15px; font-weight: 700; color: #EF4444;">R$ {s['current_price']:.2f}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Diferença / Ação</div>
                        <div style="font-size: 13px; font-weight: 600; color: #FCA5A5;">- R$ {s['diff_nominal']:.2f}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Teto Bazin (6%)</div>
                        <div style="font-size: 13px; font-weight: 600; color: #10B981;">R$ {s['bazin_target_price']:.2f}</div>
                    </div>
                </div>
                <div style="background: rgba(56, 189, 248, 0.1); border: 1px dashed {s['badge_color']}; border-radius: 6px; padding: 8px 10px; margin-top: 8px;">
                    <div style="font-size: 12px; font-weight: 700; color: {s['badge_color']};">
                        {s['action_badge']}
                    </div>
                    <div style="font-size: 11px; color: #CBD5E1; margin-top: 3px; line-height: 1.3;">
                        {s['action_tip']}
                    </div>
                </div>
            </div>
            """
            st.markdown(textwrap.dedent(card_html).strip(), unsafe_allow_html=True)

