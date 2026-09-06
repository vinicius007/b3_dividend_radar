"""
B3 DIVIDEND RADAR - Plataforma Executiva de Recomendação e Análise de Dividendos da B3.
Interface inspirada no Power BI com dados fundamentalistas, notícias em tempo real, gestão de carteira e simuladores.
"""

import streamlit as st
import pandas as pd
import numpy as np
import textwrap
from datetime import datetime, date

# Configuração da página Streamlit (Modo Wide executivo)
st.set_page_config(
    page_title="B3 Dividend Radar | Power BI Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importações dos módulos internos
from src.ui.powerbi_theme import POWERBI_CSS
from src.ui.components import (
    render_kpi_header,
    render_matrix_table,
    render_quadrant_scatter_chart,
    render_radar_comparison_chart,
    render_dividend_history_bars,
    render_monthly_calendar_grid,
    render_news_feed,
    render_passive_income_calculator,
    render_top_dividend_yields_section,
    render_sub_10_bargain_detector
)
from src.data.b3_universe import B3_DIVIDEND_UNIVERSE
from src.engine.recommender import get_ranked_recommendations, get_categorized_portfolios
from src.news.news_collector import fetch_ticker_news
from src.news.sentiment_analyzer import evaluate_company_news_sentiment
from src.data.portfolio_manager import (
    get_portfolio_summary,
    add_transaction,
    delete_transaction,
    load_transactions,
    get_portfolio_monthly_dividend_alerts,
    get_portfolio_dip_alerts,
    MONTH_NAMES
)
from src.ui.portfolio_components import (
    render_portfolio_kpis,
    render_pie_invested_chart,
    render_pie_current_value_chart,
    render_bar_profit_loss_chart,
    render_portfolio_summary_table,
    render_dividend_alerts_section,
    render_portfolio_dip_alerts
)

# Injeção de Estilo CSS Power BI
st.markdown(POWERBI_CSS, unsafe_allow_html=True)

# -------------------------------------------------------------
# CARREGAMENTO DE DADOS COM CACHE
# -------------------------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def load_data(force_refresh: bool = False):
    return get_ranked_recommendations(force_refresh=force_refresh)

# Botão de atualização forçada se solicitado
if "refresh_key" not in st.session_state:
    st.session_state["refresh_key"] = 0

# -------------------------------------------------------------
# SIDEBAR: SLICERS & FILTROS ESTILO POWER BI
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Filtros do Relatório")
    st.caption("Ajuste os parâmetros de triagem da B3")

    if st.button("🔄 Atualizar Dados da B3", use_container_width=True):
        st.cache_data.clear()
        st.session_state["refresh_key"] += 1
        st.rerun()

    st.markdown("---")

    # Carregar dados
    ranked_df = load_data(force_refresh=False)

    # 1. Filtro de Setor
    all_sectors = ["Todos"] + sorted(list(ranked_df["sector"].unique()))
    selected_sector = st.selectbox("Setor de Atuação", all_sectors, index=0)

    # 2. Filtro de Dividend Yield Mínimo
    min_dy = st.slider("Dividend Yield Mínimo (12M)", min_value=0.0, max_value=15.0, value=5.0, step=0.5, format="%.1f%%")

    # 3. Filtro de Preço Teto Bazin
    only_safe_bazin = st.checkbox("Apenas Ações c/ Margem Bazin Positiva (Preço < Teto)", value=False)

    # 4. Filtro de Score Mínimo
    min_score = st.slider("Score de Recomendação Mínimo", min_value=0, max_value=100, value=50, step=5)

    st.markdown("---")
    st.markdown("### 📌 Sobre a Metodologia")
    st.markdown("""
    - **Décio Bazin**: Preço Teto = DPA Médio / 6% a.a.
    - **Benjamin Graham**: $V = \\sqrt{22.5 \\times LPA \\times VPA}$
    - **Score Multicritério**: Yield (35%), ROE (25%), Solvência (20%) e Notícias B3 (20%).
    """)

# -------------------------------------------------------------
# APLICAÇÃO DOS FILTROS NO DATASET
# -------------------------------------------------------------
filtered_df = ranked_df.copy()

if selected_sector != "Todos":
    filtered_df = filtered_df[filtered_df["sector"] == selected_sector]

filtered_df = filtered_df[filtered_df["dy_12m"] >= min_dy]
filtered_df = filtered_df[filtered_df["score"] >= min_score]

if only_safe_bazin:
    filtered_df = filtered_df[filtered_df["bazin_margin_safety"] > 0]

portfolios = get_categorized_portfolios(filtered_df)

# -------------------------------------------------------------
# HEADER EXECUTIVO POWER BI
# -------------------------------------------------------------
st.markdown(f"""
<div class="pbi-header-container">
    <div>
        <div class="pbi-header-title">
            <span>📈</span> B3 DIVIDEND RADAR | RELATÓRIO EXECUTIVO DE PROVENTOS
        </div>
        <div class="pbi-header-subtitle">
            Gestão de Carteira Real, Recomendação de Ações, Valuation (Bazin & Graham), Notícias e Frequência de Distribuição
        </div>
    </div>
    <div style="text-align: right;">
        <span class="pbi-badge-live">● MERCADO AO VIVO B3</span>
        <div style="font-size: 11px; color: #94A3B8; margin-top: 6px;">Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Linha de Cartões KPI Gerais de Mercado
render_kpi_header(filtered_df)
st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# NAVEGAÇÃO PRINCIPAL POR ABAS
# -------------------------------------------------------------
tab_portfolio, tab_top_yields, tab_sub10, tab_overview, tab_growth, tab_monthly, tab_bimonthly, tab_quarterly, tab_deepdive, tab_news, tab_simulator = st.tabs([
    "💼 Minha Carteira & Alertas",
    "💎 Maiores Dividendos B3",
    "🎯 Ações < R$ 10 (Potencial)",
    "📌 Visão Geral do Mercado",
    "🚀 Potencial de Crescimento",
    "🗓️ Dividendos Mensais",
    "⏳ Dividendos Bimestrais",
    "📊 Dividendos Trimestrais",
    "🔍 Raio-X Individual (Bazin & Graham)",
    "📰 Notícias Reais & Sentimento",
    "💰 Simulador de Renda Passiva"
])

# -------------------------------------------------------------
# TAB 0: MINHA CARTEIRA & ALERTAS
# -------------------------------------------------------------
with tab_portfolio:
    st.markdown("### 💼 Painel Executivo da Minha Carteira de Ações & Central de Alertas")
    st.caption("Acompanhamento de posições reais, rentabilidade a mercado, alertas preditivos de proventos e quedas de preço médio")

    # Obter dados consolidados da carteira
    portfolio_summary = get_portfolio_summary(ranked_df)

    # 1. KPIs da Carteira
    render_portfolio_kpis(portfolio_summary)
    st.markdown("<br>", unsafe_allow_html=True)

    # 🚨 SISTEMA DE ALERTAS 1: PROVENTOS A RECEBER NO MÊS
    col_alert_hdr, col_month_sel = st.columns([2.5, 1.2])
    with col_alert_hdr:
        st.markdown("#### 🚨 1. Alertas de Proventos do Mês")
        st.caption("Monitor preditivo em tempo real de proventos a receber na conta para os ativos em custódia")
    with col_month_sel:
        curr_m = datetime.now().month
        month_options = list(range(1, 13))
        selected_alert_month = st.selectbox(
            "📅 Selecionar Mês de Pagamento:",
            options=month_options,
            index=curr_m - 1,
            format_func=lambda m: f"{MONTH_NAMES.get(m, '')} (Mês {m:02d})",
            key="portfolio_alert_month_selector"
        )

    alerts_data = get_portfolio_monthly_dividend_alerts(portfolio_summary, target_month=selected_alert_month)
    render_dividend_alerts_section(alerts_data)
    st.markdown("<br>", unsafe_allow_html=True)

    # 🔻 SISTEMA DE ALERTAS 2: AÇÕES ABAIXO DO VALOR DE COMPRA (PREÇO < PM)
    st.markdown("#### 🔻 2. Alertas de Ações Abaixo do Valor de Compra (Preço < PM)")
    st.caption("Identificação automática de ativos negociados com desconto em relação ao seu preço médio de aquisição")
    dip_data = get_portfolio_dip_alerts(portfolio_summary, ranked_df)
    render_portfolio_dip_alerts(dip_data)
    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Gráficos Solicitados
    st.markdown("#### 📊 Visualizações Executivas de Alocação e Rentabilidade")
    
    # Linha com os dois Gráficos Pizza/Donut
    col_pie1, col_pie2 = st.columns(2)
    with col_pie1:
        st.markdown('<div class="pbi-chart-container">', unsafe_allow_html=True)
        render_pie_invested_chart(portfolio_summary)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pie2:
        st.markdown('<div class="pbi-chart-container">', unsafe_allow_html=True)
        render_pie_current_value_chart(portfolio_summary)
        st.markdown('</div>', unsafe_allow_html=True)

    # Linha com o Gráfico de Barras Verticais de Lucro/Perda
    st.markdown('<div class="pbi-chart-container">', unsafe_allow_html=True)
    render_bar_profit_loss_chart(portfolio_summary)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Posição Detalhada em Tabela
    render_portfolio_summary_table(portfolio_summary)
    st.markdown("---")

    # 4. Tela de Cadastro de Ativo / Atualização de Valores
    col_cad, col_hist = st.columns([1, 1.4])

    with col_cad:
        st.markdown('<div class="pbi-chart-title">📝 Cadastrar / Atualizar Ativo</div>', unsafe_allow_html=True)
        
        all_ticker_choices = sorted([r["ticker_clean"] for r in B3_DIVIDEND_UNIVERSE])
        
        with st.form("form_cadastro_ativo", clear_on_submit=False):
            cad_ticker = st.selectbox("Ação (Ticker B3)", all_ticker_choices, index=0)
            cad_data = st.date_input("Data da Operação", value=date.today())
            cad_qtd = st.number_input("Quantidade de Ações", min_value=1, max_value=1000000, value=100, step=10)
            
            # Sugerir preço atual se disponível
            sugg_price = 25.00
            for r in ranked_df.to_dict("records"):
                if r.get("ticker_clean") == cad_ticker:
                    sugg_price = r.get("price", 25.00)
                    break

            cad_preco = st.number_input(
                "Preço Unitário de Compra (R$)", 
                min_value=0.01, 
                max_value=10000.0, 
                value=float(sugg_price), 
                step=0.10,
                format="%.2f"
            )
            cad_notas = st.text_input("Anotações / Justificativa (Opcional)", value="Aporte em proventos")
            
            valor_total_preview = cad_qtd * cad_preco
            st.info(f"💵 **Valor Total da Operação**: R$ {valor_total_preview:,.2f}")

            submit_btn = st.form_submit_button("💾 Salvar / Atualizar no Portfólio", use_container_width=True)
            if submit_btn:
                add_transaction(
                    ticker=cad_ticker,
                    date_str=cad_data.strftime("%Y-%m-%d"),
                    quantity=int(cad_qtd),
                    price_per_share=float(cad_preco),
                    notes=cad_notas
                )
                st.success(f"✅ Transação registrada com sucesso: {cad_qtd} ações de {cad_ticker} a R$ {cad_preco:.2f}!")
                st.rerun()

    with col_hist:
        st.markdown('<div class="pbi-chart-title">📜 Histórico de Atualizações e Transações</div>', unsafe_allow_html=True)
        
        transactions_list = load_transactions()
        if not transactions_list:
            st.info("Nenhuma transação registrada no histórico.")
        else:
            hist_df = pd.DataFrame(transactions_list)
            
            # Ordenar por data decrescente
            if "date" in hist_df.columns:
                hist_df = hist_df.sort_values(by="date", ascending=False).reset_index(drop=True)

            hist_display = hist_df[["id", "date", "ticker_clean", "quantity", "price_per_share", "total_invested", "notes"]].copy().rename(columns={
                "id": "ID",
                "date": "Data",
                "ticker_clean": "Ação",
                "quantity": "Qtd",
                "price_per_share": "Preço Unit. (R$)",
                "total_invested": "Total Pago (R$)",
                "notes": "Observações"
            })

            st.dataframe(
                hist_display.style.format({
                    "Qtd": "{:d}",
                    "Preço Unit. (R$)": "R$ {:.2f}",
                    "Total Pago (R$)": "R$ {:,.2f}"
                }),
                use_container_width=True,
                height=260
            )

            # Opção de exclusão rápida de transação
            st.markdown("##### 🗑️ Excluir Transação do Histórico")
            col_del_id, col_del_btn = st.columns([2, 1])
            with col_del_id:
                tx_ids = [f"{t.get('id')} - {t.get('ticker_clean')} ({t.get('date')})" for t in transactions_list]
                selected_del = st.selectbox("Selecione o lançamento para remover:", tx_ids, key="del_selector")
            with col_del_btn:
                st.write("")
                st.write("")
                if st.button("Excluir Lançamento", type="secondary", use_container_width=True):
                    raw_id = selected_del.split(" - ")[0]
                    if delete_transaction(raw_id):
                        st.success(f"Transação {raw_id} removida!")
                        st.rerun()

# -------------------------------------------------------------
# TAB 1: MAIORES DIVIDENDOS EM TEMPO REAL
# -------------------------------------------------------------
with tab_top_yields:
    render_top_dividend_yields_section(filtered_df)

# -------------------------------------------------------------
# TAB 2: DETECTOR DE AÇÕES < R$ 10 (ALTO POTENCIAL)
# -------------------------------------------------------------
with tab_sub10:
    render_sub_10_bargain_detector(ranked_df)

# -------------------------------------------------------------
# TAB 3: VISÃO GERAL DO MERCADO
# -------------------------------------------------------------
with tab_overview:
    col_t1, col_t2 = st.columns([1.6, 1])

    with col_t1:
        render_matrix_table(filtered_df, "📊 Ranking Geral de Ações de Dividendos da B3")

    with col_t2:
        st.markdown('<div class="pbi-chart-title">🎯 Matriz de Oportunidades (DY x ROE)</div>', unsafe_allow_html=True)
        render_quadrant_scatter_chart(filtered_df)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Calendário e distribuição de fluxo
    st.markdown('<div class="pbi-chart-title">🗓️ Calendário de Fluxo de Pagamentos da Carteira Selecionada</div>', unsafe_allow_html=True)
    render_monthly_calendar_grid(filtered_df.to_dict("records")[:12])

# -------------------------------------------------------------
# TAB 2: AÇÕES COM POTENCIAL DE CRESCIMENTO (+ DIVIDENDOS)
# -------------------------------------------------------------
with tab_growth:
    st.markdown("""
    ### 🚀 Ações com Alto Potencial de Crescimento e Proventos em Expansão
    Empresas selecionadas com **alto retorno sobre patrimônio (ROE > 14%)**, **crescimento consistente de dividendos por ação (CAGR)**, **baixo endividamento** e expansão contínua de lucros.
    """)

    growth_df = portfolios["crescimento"]
    if growth_df.empty:
        st.info("Nenhuma ação de crescimento atende aos filtros atuais da barra lateral.")
    else:
        c_g1, c_g2 = st.columns([1.5, 1])
        with c_g1:
            render_matrix_table(growth_df, "🏆 Carteira Recomendada: Dividend Growth B3")
        with c_g2:
            st.markdown('<div class="pbi-chart-title">📈 Crescimento Médio de Proventos (CAGR 3 Anos)</div>', unsafe_allow_html=True)
            st.dataframe(
                growth_df[["ticker_clean", "name", "dividend_cagr_3y", "roe", "dy_12m", "verdict"]].rename(columns={
                    "ticker_clean": "Ticker",
                    "name": "Empresa",
                    "dividend_cagr_3y": "CAGR Div. 3Y (%)",
                    "roe": "ROE (%)",
                    "dy_12m": "DY Atual (%)",
                    "verdict": "Status"
                }).style.format({
                    "CAGR Div. 3Y (%)": "{:+.1f}%",
                    "ROE (%)": "{:.1f}%",
                    "DY Atual (%)": "{:.2f}%"
                }).background_gradient(subset=["CAGR Div. 3Y (%)"], cmap="Greens"),
                use_container_width=True
            )

# -------------------------------------------------------------
# TAB 3: AÇÕES COM DIVIDENDOS MENSAIS
# -------------------------------------------------------------
with tab_monthly:
    st.markdown("""
    ### 🗓️ Ações com Proventos Mensais Recorrentes
    Ativos que realizam pagamentos de proventos (Dividendos e JCP) **em praticamente todos os meses do ano**, ideais para quem busca previsibilidade de fluxo de caixa mensal imediato.
    """)

    monthly_df = portfolios["mensal"]
    if monthly_df.empty:
        st.info("Nenhuma ação mensal atende aos filtros atuais.")
    else:
        render_matrix_table(monthly_df, "🗓️ Carteira de Renda Mensal Recorrente")
        st.markdown("<br>", unsafe_allow_html=True)
        render_monthly_calendar_grid(monthly_df.to_dict("records"))

# -------------------------------------------------------------
# TAB 4: AÇÕES COM DIVIDENDOS BIMESTRAIS
# -------------------------------------------------------------
with tab_bimonthly:
    st.markdown("""
    ### ⏳ Ações com Distribuições Bimestrais (~5 a 8 Pagamentos / Ano)
    Empresas com periodicidade frequente de proventos que complementam a renda intercalando distribuições ao longo do ano fiscal.
    """)

    bimonthly_df = portfolios["bimestral"]
    if bimonthly_df.empty:
        st.info("Nenhuma ação bimestral atende aos filtros atuais.")
    else:
        render_matrix_table(bimonthly_df, "⏳ Carteira de Proventos Bimestrais")
        st.markdown("<br>", unsafe_allow_html=True)
        render_monthly_calendar_grid(bimonthly_df.to_dict("records"))

# -------------------------------------------------------------
# TAB 5: AÇÕES COM DIVIDENDOS TRIMESTRAIS
# -------------------------------------------------------------
with tab_quarterly:
    st.markdown("""
    ### 📊 Ações com Distribuições Trimestrais Consolidadas
    Grandes empresas sólidas da bolsa brasileira (bancos estatais, seguradoras, gigantes elétricas e commodities) com políticas formais de proventos a cada 3 meses.
    """)

    quarterly_df = portfolios["trimestral"]
    if quarterly_df.empty:
        st.info("Nenhuma ação trimestral atende aos filtros atuais.")
    else:
        render_matrix_table(quarterly_df, "📊 Carteira de Proventos Trimestrais Estruturados")
        st.markdown("<br>", unsafe_allow_html=True)
        render_monthly_calendar_grid(quarterly_df.to_dict("records")[:8])

# -------------------------------------------------------------
# TAB 6: RAIO-X INDIVIDUAL (BAZIN, GRAHAM E RADAR)
# -------------------------------------------------------------
with tab_deepdive:
    st.markdown("### 🔍 Análise Fundamentalista Detalhada por Ação")
    
    ticker_options = [r["ticker_clean"] for r in ranked_df.to_dict("records")]
    selected_clean_ticker = st.selectbox("Selecione a ação para análise individual aprofundada:", ticker_options, index=0)
    
    stock_row = ranked_df[ranked_df["ticker_clean"] == selected_clean_ticker].iloc[0].to_dict()

    # Cards principais do ativo
    c_d1, c_d2, c_d3, c_d4 = st.columns(4)
    with c_d1:
        st.metric("Cotação Atual", f"R$ {stock_row['price']:.2f}")
    with c_d2:
        st.metric(
            "Preço Teto Bazin (6%)", 
            f"R$ {stock_row['bazin_target_price']:.2f}",
            delta=f"{stock_row['bazin_margin_safety']:+.1f}% de Margem"
        )
    with c_d3:
        st.metric(
            "Valor Justo Graham", 
            f"R$ {stock_row['graham_fair_value']:.2f}",
            delta=f"{stock_row['graham_margin_safety']:+.1f}% de Margem"
        )
    with c_d4:
        st.metric("Dividend Yield (12M)", f"{stock_row['dy_12m']:.2f}%", f"DPA R$ {stock_row['dpa_12m']:.2f}")

    st.markdown("---")

    col_radar, col_hist = st.columns([1, 1.2])

    with col_radar:
        st.markdown('<div class="pbi-chart-title">🎯 Radar Multicritério vs Média B3</div>', unsafe_allow_html=True)
        sector_bench = {
            "dy_12m": ranked_df["dy_12m"].mean(),
            "roe": ranked_df["roe"].mean(),
            "net_margin": ranked_df["net_margin"].mean(),
            "bazin_margin_safety": ranked_df["bazin_margin_safety"].mean(),
            "debt_ebitda": ranked_df["debt_ebitda"].mean()
        }
        render_radar_comparison_chart(stock_row, sector_bench)

    with col_hist:
        st.markdown('<div class="pbi-chart-title">📊 Histórico de Proventos Anuais</div>', unsafe_allow_html=True)
        render_dividend_history_bars(stock_row)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detalhes de Valuation e Indicadores
    col_ind1, col_ind2, col_ind3, col_ind4, col_ind5, col_ind6 = st.columns(6)
    col_ind1.metric("P/L", f"{stock_row['pl']:.1f}")
    col_ind2.metric("P/VP", f"{stock_row['pvp']:.2f}")
    col_ind3.metric("ROE", f"{stock_row['roe']:.1f}%")
    col_ind4.metric("Margem Líquida", f"{stock_row['net_margin']:.1f}%")
    col_ind5.metric("Dívida/EBITDA", f"{stock_row['debt_ebitda']:.1f}x")
    col_ind6.metric("Payout", f"{stock_row['payout']:.1f}%")

    st.info(f"📋 **Descrição & Tese de Investimento**: {stock_row.get('description', '')}")

# -------------------------------------------------------------
# TAB 7: NOTÍCIAS REAIS & ANÁLISE DE SENTIMENTO DA B3
# -------------------------------------------------------------
with tab_news:
    st.markdown("### 📰 Notícias Reais e Monitor de Sentimento do Mercado B3")
    
    col_n_sel, col_n_diag = st.columns([1, 1.8])
    
    with col_n_sel:
        news_ticker = st.selectbox(
            "Filtrar notícias por empresa:", 
            ticker_options, 
            index=ticker_options.index(selected_clean_ticker) if selected_clean_ticker in ticker_options else 0,
            key="news_filter"
        )
        selected_news_stock = ranked_df[ranked_df["ticker_clean"] == news_ticker].iloc[0].to_dict()
        
        # Buscar notícias ao vivo
        live_news = fetch_ticker_news(
            selected_news_stock["ticker"], 
            company_name=selected_news_stock["name"], 
            max_results=5
        )
        sentiment_res = evaluate_company_news_sentiment(live_news)

        sentiment_card_html = f"""
        <div class="pbi-action-card">
            <div style="font-size:12px; color:#94A3B8; font-weight:700;">DIAGNÓSTICO DE SENTIMENTO</div>
            <div style="font-size:24px; font-weight:800; color:{sentiment_res['color']}; margin: 8px 0;">
                {sentiment_res['badge']}
            </div>
            <div style="font-size:13px; color:#CBD5E1; line-height:1.4;">
                {sentiment_res['impact_on_dividends']}
            </div>
            <div style="margin-top:10px; font-size:12px; color:#64748B;">
                Score de Notícias: <b>{sentiment_res['score']:+.2f}</b> (Escala -1.0 a +1.0)
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(sentiment_card_html).strip(), unsafe_allow_html=True)

    with col_n_diag:
        st.markdown(f"#### 🌐 Feed de Notícias em Tempo Real - {selected_news_stock['name']} ({news_ticker})")
        render_news_feed(live_news, stock_ticker=news_ticker)

# -------------------------------------------------------------
# TAB 8: SIMULADOR DE RENDA PASSIVA
# -------------------------------------------------------------
with tab_simulator:
    st.markdown("### 💰 Simulador de Independência Financeira e Renda Passiva de Proventos")
    
    sim_ticker = st.selectbox(
        "Selecione o ativo base para a simulação de patrimônio:", 
        ticker_options,
        index=0,
        key="sim_selector"
    )
    sim_stock = ranked_df[ranked_df["ticker_clean"] == sim_ticker].iloc[0].to_dict()
    
    render_passive_income_calculator(sim_stock)

# -------------------------------------------------------------
# RODAPÉ CORPORATIVO
# -------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 12px; color: #64748B; padding: 10px 0;">
    B3 Dividend Radar &bull; Dados Públicos B3 e Feeds Financeiros em Tempo Real &bull; Desenvolvido em Python &bull; Interface Estilo Power BI
</div>
""", unsafe_allow_html=True)
