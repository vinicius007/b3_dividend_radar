"""
Motor de Recomendação e Ranqueamento Multicritério de Dividendos da B3.
Combina Valuation (Bazin/Graham), Qualidade Operacional, Saúde Financeira e Sentimento de Notícias.
"""

from typing import Dict, List, Any
import pandas as pd
import numpy as np

from src.data.market_data import get_market_dataset, fetch_single_ticker_data
from src.data.dividend_engine import enrich_dataframe_with_classifications
from src.news.news_collector import fetch_ticker_news
from src.news.sentiment_analyzer import evaluate_company_news_sentiment

def calculate_stock_score(stock: Dict[str, Any], sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula pontuação ponderada de 0 a 100 baseada em 4 pilares:
    1. Valuation & Dividend Yield (35%)
    2. Rentabilidade & Eficiência (25%)
    3. Saúde Financeira & Sustentabilidade do Payout (20%)
    4. Sentimento de Notícias Reais da B3 (20%)
    """
    # 1. Valuation & Yield (Max 35 pts)
    dy = stock.get("dy_12m", 0)
    if dy >= 9.0:
        yield_score = 15.0
    elif dy >= 7.0:
        yield_score = 13.0
    elif dy >= 5.5:
        yield_score = 10.0
    elif dy >= 4.0:
        yield_score = 7.0
    else:
        yield_score = 4.0

    bazin_margin = stock.get("bazin_margin_safety", 0)
    if bazin_margin >= 25.0:
        bazin_score = 10.0
    elif bazin_margin >= 10.0:
        bazin_score = 8.0
    elif bazin_margin >= 0.0:
        bazin_score = 6.0
    elif bazin_margin >= -10.0:
        bazin_score = 3.0
    else:
        bazin_score = 0.0

    pl = stock.get("pl", 10.0)
    if 0 < pl <= 6.0:
        val_score = 10.0
    elif 6.0 < pl <= 10.0:
        val_score = 8.0
    elif 10.0 < pl <= 15.0:
        val_score = 5.0
    else:
        val_score = 2.0

    pillar_valuation = yield_score + bazin_score + val_score  # Max 35

    # 2. Rentabilidade & Eficiência (Max 25 pts)
    roe = stock.get("roe", 0)
    if roe >= 25.0:
        roe_score = 15.0
    elif roe >= 18.0:
        roe_score = 13.0
    elif roe >= 13.0:
        roe_score = 10.0
    elif roe >= 8.0:
        roe_score = 6.0
    else:
        roe_score = 2.0

    margin = stock.get("net_margin", 0)
    if margin >= 25.0:
        margin_score = 10.0
    elif margin >= 15.0:
        margin_score = 8.0
    elif margin >= 8.0:
        margin_score = 5.0
    else:
        margin_score = 2.0

    pillar_quality = roe_score + margin_score  # Max 25

    # 3. Saúde Financeira & Payout (Max 20 pts)
    debt_ebitda = stock.get("debt_ebitda", 1.5)
    if debt_ebitda <= 1.0:
        debt_score = 10.0
    elif debt_ebitda <= 2.2:
        debt_score = 8.0
    elif debt_ebitda <= 3.0:
        debt_score = 5.0
    else:
        debt_score = 2.0

    payout = stock.get("payout", 50.0)
    if 40.0 <= payout <= 80.0:
        payout_score = 10.0
    elif (25.0 <= payout < 40.0) or (80.0 < payout <= 92.0):
        payout_score = 7.0
    elif payout > 92.0:
        payout_score = 4.0  # Payout excessivo pode ser arriscado
    else:
        payout_score = 3.0

    pillar_health = debt_score + payout_score  # Max 20

    # 4. Sentimento de Notícias Reais (Max 20 pts)
    sent_score = sentiment_data.get("score", 0.0)
    if sent_score >= 0.35:
        pillar_news = 20.0
    elif sent_score >= 0.10:
        pillar_news = 16.0
    elif sent_score >= -0.10:
        pillar_news = 12.0
    elif sent_score >= -0.35:
        pillar_news = 6.0
    else:
        pillar_news = 0.0

    total_score = round(pillar_valuation + pillar_quality + pillar_health + pillar_news, 1)

    # Classificação de recomendação
    if total_score >= 80.0:
        verdict = "🏆 Oportunidade Forte"
        verdict_badge = "FORTE COMPRA"
        verdict_color = "#10B981"
    elif total_score >= 68.0:
        verdict = "✅ Compra Atrativa"
        verdict_badge = "COMPRA"
        verdict_color = "#34D399"
    elif total_score >= 50.0:
        verdict = "⚖️ Manter / Acompanhar"
        verdict_badge = "NEUTRO"
        verdict_color = "#94A3B8"
    else:
        verdict = "⚠️ Cautela / Aguardar"
        verdict_badge = "CAUTELA"
        verdict_color = "#EF4444"

    return {
        "total_score": total_score,
        "pillar_valuation": pillar_valuation,
        "pillar_quality": pillar_quality,
        "pillar_health": pillar_health,
        "pillar_news": pillar_news,
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "verdict_color": verdict_color
    }

def get_ranked_recommendations(force_refresh: bool = False) -> pd.DataFrame:
    """Gera o ranking completo de recomendações com indicadores, frequência e notícias."""
    df = get_market_dataset(force_refresh=force_refresh)
    df = enrich_dataframe_with_classifications(df)

    scored_records = []
    for _, row in df.iterrows():
        stock_dict = row.to_dict()
        ticker = stock_dict.get("ticker", "")
        clean_ticker = stock_dict.get("ticker_clean", ticker)
        name = stock_dict.get("name", clean_ticker)

        # Coletar notícias e avaliar sentimento
        news = fetch_ticker_news(ticker, company_name=name, max_results=3)
        sentiment = evaluate_company_news_sentiment(news)
        
        # Calcular score
        score_info = calculate_stock_score(stock_dict, sentiment)

        record = {**stock_dict}
        record["score"] = score_info["total_score"]
        record["pillar_val"] = score_info["pillar_valuation"]
        record["pillar_qual"] = score_info["pillar_quality"]
        record["pillar_hlth"] = score_info["pillar_health"]
        record["pillar_news"] = score_info["pillar_news"]
        record["verdict"] = score_info["verdict"]
        record["verdict_badge"] = score_info["verdict_badge"]
        record["verdict_color"] = score_info["verdict_color"]
        
        record["sentiment_score"] = sentiment["score"]
        record["sentiment_label"] = sentiment["label"]
        record["sentiment_badge"] = sentiment["badge"]
        record["news_impact"] = sentiment["impact_on_dividends"]
        record["recent_news_count"] = len(news)
        record["top_news_title"] = news[0]["title"] if news else ""
        record["top_news_link"] = news[0]["link"] if news else ""

        scored_records.append(record)

    ranked_df = pd.DataFrame(scored_records)
    ranked_df = ranked_df.sort_values(by="score", ascending=False).reset_index(drop=True)
    return ranked_df

def get_categorized_portfolios(ranked_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Separa os ativos nos 4 portfólios solicitados pelo usuário:
    1. Ações com Potencial de Crescimento (+ Dividendos)
    2. Ações com Dividendos Mensais
    3. Ações com Dividendos Bimestrais
    4. Ações com Dividendos Trimestrais
    """
    # 1. Potencial de Crescimento
    growth_df = ranked_df[
        (ranked_df["is_growth"] == True) | (ranked_df["frequency"] == "crescimento")
    ].copy().sort_values(by=["dividend_cagr_3y", "score"], ascending=[False, False])

    # 2. Mensais
    monthly_df = ranked_df[
        (ranked_df["frequency"] == "mensal") | (ranked_df["payments_per_year"] >= 10)
    ].copy().sort_values(by=["dy_12m", "score"], ascending=[False, False])

    # 3. Bimestrais
    bimonthly_df = ranked_df[
        (ranked_df["frequency"] == "bimestral") | ((ranked_df["payments_per_year"] >= 5) & (ranked_df["payments_per_year"] <= 8))
    ].copy().sort_values(by=["dy_12m", "score"], ascending=[False, False])

    # 4. Trimestrais
    quarterly_df = ranked_df[
        (ranked_df["frequency"] == "trimestral") | ((ranked_df["payments_per_year"] >= 3) & (ranked_df["payments_per_year"] <= 4))
    ].copy().sort_values(by=["score", "dy_12m"], ascending=[False, False])

    return {
        "crescimento": growth_df,
        "mensal": monthly_df,
        "bimestral": bimonthly_df,
        "trimestral": quarterly_df
    }
