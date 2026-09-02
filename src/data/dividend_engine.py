"""
Motor de Classificação de Proventos e Frequência de Pagamentos.
Identifica ativos mensais, bimestrais, trimestrais e de potencial de crescimento.
"""

from typing import Dict, List, Any
import pandas as pd
import numpy as np

def classify_dividend_frequency(row: Dict[str, Any]) -> str:
    """
    Classifica a periodicidade real de pagamentos:
    - 'mensal': 10 a 12+ distribuições por ano (ex.: ITUB4, BBDC4, BEES3)
    - 'bimestral': 5 a 8 distribuições por ano (ex.: TRPL4, SAPR11)
    - 'trimestral': 3 a 4 distribuições por ano (ex.: BBAS3, TAEE11, ITSA4, CMIG4, CPLE6)
    - 'crescimento': empresas com forte expansão patrimonial, alto ROE e DPA crescente
    """
    default_cat = row.get("default_category", "trimestral")
    payments_per_year = row.get("payments_per_year", 4)
    
    # Avaliação dinâmica por contagem de pagamentos anuais
    if payments_per_year >= 10:
        return "mensal"
    elif 5 <= payments_per_year <= 8:
        return "bimestral"
    elif 3 <= payments_per_year <= 4:
        return "trimestral"
    
    return default_cat

def is_growth_dividend_stock(row: Dict[str, Any]) -> bool:
    """
    Critérios para Ações de Potencial de Crescimento com Dividendos:
    1. ROE >= 14%
    2. Crescimento histórico de dividendos (CAGR 3 anos >= 5%) ou Lucro consistente
    3. Dívida Líquida / EBITDA <= 2.8x (saúde financeira)
    4. Margem Líquida >= 8%
    """
    roe = row.get("roe", 0)
    cagr = row.get("dividend_cagr_3y", 0)
    debt_ebitda = row.get("debt_ebitda", 0)
    margin = row.get("net_margin", 0)

    is_growth = (roe >= 14.0) and (cagr >= 5.0) and (debt_ebitda <= 2.8) and (margin >= 8.0)
    return bool(is_growth or row.get("default_category") == "crescimento")

def calculate_monthly_cashflow_schedule(stocks_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Gera a matriz mensal de distribuição de dividendos (Janeiro a Dezembro)
    para o portfólio selecionado.
    """
    months = [
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
        "Jul", "Ago", "Set", "Out", "Nov", "Dez"
    ]
    
    records = []
    for stock in stocks_data:
        ticker = stock.get("ticker_clean", stock.get("ticker"))
        dy = stock.get("dy_12m", 0)
        p_months = stock.get("payment_months", [3, 6, 9, 12])
        dpa = stock.get("dpa_12m", 0)
        num_payments = len(p_months) if len(p_months) > 0 else 1
        dpa_per_pay = round(dpa / num_payments, 3)

        row_dict = {
            "Ticker": ticker,
            "Empresa": stock.get("name", ticker),
            "Frequência": stock.get("frequency_label", "Trimestral"),
            "DY (12M)": f"{dy:.2f}%"
        }
        for m_idx, m_name in enumerate(months, start=1):
            if m_idx in p_months:
                row_dict[m_name] = f"R$ {dpa_per_pay:.2f}"
            else:
                row_dict[m_name] = "-"
        records.append(row_dict)
    
    return pd.DataFrame(records)

def enrich_dataframe_with_classifications(df: pd.DataFrame) -> pd.DataFrame:
    """Enriquece o DataFrame com rótulos e categorias de dividendos."""
    if df.empty:
        return df
    
    # Classificação de frequência
    df["frequency"] = df.apply(lambda r: classify_dividend_frequency(r.to_dict()), axis=1)
    
    # Potencial de crescimento
    df["is_growth"] = df.apply(lambda r: is_growth_dividend_stock(r.to_dict()), axis=1)

    # Rótulos legíveis para a interface Power BI
    freq_labels = {
        "mensal": "🗓️ Mensal (12x/ano)",
        "bimestral": "⏳ Bimestral (6x/ano)",
        "trimestral": "📊 Trimestral (4x/ano)",
        "crescimento": "🚀 Potencial Crescimento"
    }
    df["frequency_label"] = df["frequency"].map(freq_labels).fillna("📊 Trimestral (4x/ano)")
    
    return df
