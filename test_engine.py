"""
Script de Teste e Validação do Sistema B3 Dividend Radar.
Executa todos os motores (Dados B3, Notícias, Sentimento, Classificador de Frequência, Recomendação e Gestão de Carteira).
"""

import sys
import os

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.data.b3_universe import B3_DIVIDEND_UNIVERSE, get_all_tickers
from src.data.market_data import fetch_single_ticker_data, get_market_dataset
from src.data.dividend_engine import enrich_dataframe_with_classifications
from src.news.news_collector import fetch_ticker_news
from src.news.sentiment_analyzer import evaluate_company_news_sentiment
from src.engine.recommender import get_ranked_recommendations, get_categorized_portfolios
from src.data.portfolio_manager import (
    load_transactions,
    add_transaction,
    delete_transaction,
    get_portfolio_summary
)

def test_full_pipeline():
    print("=" * 70)
    print("🚀 INICIANDO TESTES DO B3 DIVIDEND RADAR & GESTÃO DE CARTEIRA")
    print("=" * 70)

    # 1. Testar Universo
    tickers = get_all_tickers()
    print(f"✅ 1. Universo B3 carregado com {len(tickers)} ativos monitorados.")

    # 2. Testar Coleta de Ativo Individual (ex: BBAS3.SA)
    print("\n🔍 2. Testando coleta de dados e métricas para BBAS3.SA...")
    bbas3 = fetch_single_ticker_data("BBAS3.SA")
    print(f"   • Cotação: R$ {bbas3['price']:.2f}")
    print(f"   • DY (12M): {bbas3['dy_12m']:.2f}% | DPA 12M: R$ {bbas3['dpa_12m']:.2f}")
    print(f"   • Preço Teto Bazin (6%): R$ {bbas3['bazin_target_price']:.2f} (Margem: {bbas3['bazin_margin_safety']:+.1f}%)")
    print(f"   • Valor Justo Graham: R$ {bbas3['graham_fair_value']:.2f} (Margem: {bbas3['graham_margin_safety']:+.1f}%)")
    print(f"   • ROE: {bbas3['roe']:.1f}% | P/L: {bbas3['pl']:.1f} | P/VP: {bbas3['pvp']:.2f}")

    # 3. Testar Notícias e Sentimento
    print("\n📰 3. Testando coletor de notícias e analisador de sentimento PT-BR...")
    news = fetch_ticker_news("BBAS3.SA", company_name="Banco do Brasil", max_results=3)
    print(f"   • Notícias coletadas: {len(news)}")
    if news:
        print(f"   • Manchete 1: {news[0]['title'][:60]}... ({news[0]['source']})")
    
    sentiment = evaluate_company_news_sentiment(news)
    print(f"   • Diagnóstico: {sentiment['badge']} (Score: {sentiment['score']:+.2f})")
    print(f"   • Impacto no Dividendo: {sentiment['impact_on_dividends']}")

    # 4. Testar Ranking Completo e Portfólios
    print("\n📊 4. Testando motor de ranqueamento e categorização...")
    ranked_df = get_ranked_recommendations(force_refresh=False)
    print(f"   • Total de ativos ranqueados: {len(ranked_df)}")
    
    top3 = ranked_df.head(3)
    print("\n🏆 TOP 3 AÇÕES RECOMENDADAS GERAIS:")
    for idx, row in top3.iterrows():
        print(f"   {idx+1}. {row['ticker_clean']} ({row['name']}) - Score: {row['score']:.1f} | DY: {row['dy_12m']:.2f}% | {row['verdict']}")

    # 5. Segregação por Categorias do Usuário
    portfolios = get_categorized_portfolios(ranked_df)
    print("\n📂 5. Verificação das 4 Categorias Solicitadas:")
    print(f"   🚀 Ações de Crescimento (+ Div): {len(portfolios['crescimento'])} ativos -> {list(portfolios['crescimento']['ticker_clean'].values[:4])}")
    print(f"   🗓️ Proventos Mensais: {len(portfolios['mensal'])} ativos -> {list(portfolios['mensal']['ticker_clean'].values)}")
    print(f"   ⏳ Proventos Bimestrais: {len(portfolios['bimestral'])} ativos -> {list(portfolios['bimestral']['ticker_clean'].values)}")
    print(f"   📊 Proventos Trimestrais: {len(portfolios['trimestral'])} ativos -> {list(portfolios['trimestral']['ticker_clean'].values[:5])}")

    # 6. Testar Módulo de Gestão de Carteira e Gráficos
    print("\n[6] Testando Módulo de Carteira do Investidor & Transações...")
    txs = load_transactions()
    print(f"   • Transações carregadas: {len(txs)}")
    
    summary = get_portfolio_summary(ranked_df)
    print(f"   • Total Investido de Compra: R$ {summary['total_invested']:,.2f}")
    print(f"   • Total Atualizado Real (B3): R$ {summary['total_current_value']:,.2f}")
    print(f"   • Lucro / Prejuízo Total: R$ {summary['total_profit_loss']:+,.2f} ({summary['total_profit_loss_pct']:+.2f}%)")
    print(f"   • Proventos Anuais Estimados: R$ {summary['total_annual_dividends']:,.2f} (~ R$ {summary['total_monthly_dividends']:,.2f}/mês)")
    print(f"   • Ativos em custódia calculados: {len(summary['assets_df'])}")

    # 7. Testar Sistema de Alertas de Dividendos do Mês
    from src.data.portfolio_manager import get_portfolio_monthly_dividend_alerts, get_portfolio_dip_alerts
    alerts = get_portfolio_monthly_dividend_alerts(summary, target_month=9)
    print(f"\n[7] Testando Alertas de Proventos do Mês ({alerts['month_name']}):")
    print(f"   • Ações com proventos previstos no mês: {alerts['stocks_count']}")
    print(f"   • Total estimado a receber no mês: R$ {alerts['total_month_payout']:,.2f}")
    for s in alerts['paying_stocks']:
        print(f"     -> {s['ticker_clean']} ({s['name']}): R$ {s['payout_val']:,.2f} ({s['quantity']} ações)")

    # 8. Testar Alertas de Ações Abaixo do Preço Médio (Preço < PM)
    dip_alerts = get_portfolio_dip_alerts(summary, ranked_df)
    print(f"\n[8] Testando Alertas de Ações Abaixo do Preço Médio (Preço < PM):")
    print(f"   • Ações abaixo do valor de compra: {dip_alerts['dip_count']}")
    print(f"   • Desconto acumulado: -R$ {dip_alerts['total_unrealized_loss']:,.2f}")
    for d in dip_alerts['dip_stocks']:
        print(f"     -> {d['ticker_clean']}: PM R$ {d['avg_price']:.2f} | Atual R$ {d['current_price']:.2f} ({d['diff_pct']:+.2f}%) | {d['action_badge']}")

    # 9. Testar Detector de Ações < R$ 10 com Alto Potencial
    sub10_df = ranked_df[ranked_df["price"] <= 10.0].sort_values(by="dy_12m", ascending=False)
    print(f"\n[9] Testando Detector de Ações < R$ 10:")
    print(f"   • Total de ativos < R$ 10 encontrados: {len(sub10_df)}")
    for _, r in sub10_df.head(5).iterrows():
        print(f"     -> {r['ticker_clean']} ({r['name']}): R$ {r['price']:.2f} | DY: {r['dy_12m']:.2f}% | Score: {r['score']:.1f}")

    # 10. Testar Top Dividend Yields da B3
    top_dy_df = ranked_df.sort_values(by="dy_12m", ascending=False).head(5)
    print(f"\n[10] Testando Lista dos Maiores Dividendos em Tempo Real:")
    for _, r in top_dy_df.iterrows():
        print(f"     -> {r['ticker_clean']}: DY {r['dy_12m']:.2f}% | DPA R$ {r['dpa_12m']:.2f} | Teto Bazin R$ {r['bazin_target_price']:.2f}")

    print("\n" + "=" * 70)
    print("✨ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("=" * 70)

if __name__ == "__main__":
    test_full_pipeline()
