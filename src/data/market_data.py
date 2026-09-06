"""
Coletor de Dados de Mercado da B3 via yfinance com cálculos fundamentalistas
e sistema de fallback resiliente.
"""

import math
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

try:
    import yfinance as yf
except ImportError:
    yf = None

from src.data.b3_universe import B3_DIVIDEND_UNIVERSE, get_universe_map

# Cache em memória
_MARKET_CACHE: Dict[str, Any] = {}
_CACHE_TIMESTAMP = 0
CACHE_TTL_SECONDS = 300  # 5 minutos

# Dados de referência fundamentalistas robustos para garantir funcionamento contínuo
FALLBACK_FUNDAMENTALS: Dict[str, Dict[str, Any]] = {
    "BBAS3.SA": {
        "price": 28.50, "dpa_12m": 2.45, "dpa_3y_avg": 2.25, "dy_12m": 8.60,
        "pl": 4.10, "pvp": 0.78, "roe": 19.8, "net_margin": 14.5, "debt_ebitda": 0.0,
        "lpa": 6.95, "vpa": 36.50, "dividend_cagr_3y": 12.4, "payout": 45.0,
        "payments_per_year": 8, "payment_months": [3, 5, 6, 8, 9, 11, 12]
    },
    "ITUB4.SA": {
        "price": 34.80, "dpa_12m": 2.78, "dpa_3y_avg": 2.40, "dy_12m": 7.98,
        "pl": 8.20, "pvp": 1.65, "roe": 21.2, "net_margin": 18.2, "debt_ebitda": 0.0,
        "lpa": 4.24, "vpa": 21.10, "dividend_cagr_3y": 14.5, "payout": 55.0,
        "payments_per_year": 12, "payment_months": list(range(1, 13))
    },
    "BBDC4.SA": {
        "price": 14.20, "dpa_12m": 0.95, "dpa_3y_avg": 0.98, "dy_12m": 6.69,
        "pl": 9.50, "pvp": 0.92, "roe": 11.5, "net_margin": 10.8, "debt_ebitda": 0.0,
        "lpa": 1.49, "vpa": 15.43, "dividend_cagr_3y": 3.2, "payout": 40.0,
        "payments_per_year": 12, "payment_months": list(range(1, 13))
    },
    "ITSA4.SA": {
        "price": 10.30, "dpa_12m": 0.88, "dpa_3y_avg": 0.79, "dy_12m": 8.54,
        "pl": 6.80, "pvp": 1.15, "roe": 18.4, "net_margin": 88.0, "debt_ebitda": 0.3,
        "lpa": 1.51, "vpa": 8.95, "dividend_cagr_3y": 9.8, "payout": 45.0,
        "payments_per_year": 4, "payment_months": [3, 6, 9, 12]
    },
    "SANB11.SA": {
        "price": 27.90, "dpa_12m": 2.10, "dpa_3y_avg": 1.95, "dy_12m": 7.52,
        "pl": 8.90, "pvp": 1.18, "roe": 14.2, "net_margin": 12.0, "debt_ebitda": 0.0,
        "lpa": 3.13, "vpa": 23.64, "dividend_cagr_3y": 6.5, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [2, 5, 8, 11]
    },
    "BEES3.SA": {
        "price": 9.80, "dpa_12m": 0.82, "dpa_3y_avg": 0.75, "dy_12m": 8.36,
        "pl": 6.20, "pvp": 1.25, "roe": 19.5, "net_margin": 16.0, "debt_ebitda": 0.0,
        "lpa": 1.58, "vpa": 7.84, "dividend_cagr_3y": 10.2, "payout": 50.0,
        "payments_per_year": 12, "payment_months": list(range(1, 13))
    },
    "BEES4.SA": {
        "price": 10.20, "dpa_12m": 0.90, "dpa_3y_avg": 0.82, "dy_12m": 8.82,
        "pl": 6.40, "pvp": 1.30, "roe": 19.5, "net_margin": 16.0, "debt_ebitda": 0.0,
        "lpa": 1.59, "vpa": 7.84, "dividend_cagr_3y": 10.5, "payout": 50.0,
        "payments_per_year": 12, "payment_months": list(range(1, 13))
    },
    "ABCB4.SA": {
        "price": 24.80, "dpa_12m": 2.15, "dpa_3y_avg": 1.95, "dy_12m": 8.67,
        "pl": 5.80, "pvp": 0.85, "roe": 15.5, "net_margin": 22.0, "debt_ebitda": 0.0,
        "lpa": 4.28, "vpa": 29.18, "dividend_cagr_3y": 14.2, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [1, 4, 7, 10]
    },
    "BRSR6.SA": {
        "price": 13.50, "dpa_12m": 1.18, "dpa_3y_avg": 1.08, "dy_12m": 8.74,
        "pl": 6.20, "pvp": 0.52, "roe": 9.0, "net_margin": 11.5, "debt_ebitda": 0.0,
        "lpa": 2.18, "vpa": 25.96, "dividend_cagr_3y": 8.5, "payout": 40.0,
        "payments_per_year": 4, "payment_months": [3, 6, 9, 12]
    },
    "BRAP4.SA": {
        "price": 19.80, "dpa_12m": 2.10, "dpa_3y_avg": 2.45, "dy_12m": 10.61,
        "pl": 5.10, "pvp": 0.95, "roe": 18.5, "net_margin": 95.0, "debt_ebitda": -0.1,
        "lpa": 3.88, "vpa": 20.84, "dividend_cagr_3y": 7.5, "payout": 85.0,
        "payments_per_year": 4, "payment_months": [4, 5, 11, 12]
    },
    "BBSE3.SA": {
        "price": 35.60, "dpa_12m": 3.65, "dpa_3y_avg": 3.20, "dy_12m": 10.25,
        "pl": 8.60, "pvp": 5.80, "roe": 68.5, "net_margin": 82.0, "debt_ebitda": -0.5,
        "lpa": 4.14, "vpa": 6.14, "dividend_cagr_3y": 18.2, "payout": 88.0,
        "payments_per_year": 2, "payment_months": [2, 8]
    },
    "CXSE3.SA": {
        "price": 14.80, "dpa_12m": 1.22, "dpa_3y_avg": 1.05, "dy_12m": 8.24,
        "pl": 11.20, "pvp": 3.40, "roe": 31.5, "net_margin": 76.0, "debt_ebitda": -0.8,
        "lpa": 1.32, "vpa": 4.35, "dividend_cagr_3y": 15.0, "payout": 90.0,
        "payments_per_year": 4, "payment_months": [2, 5, 8, 11]
    },
    "PSSA3.SA": {
        "price": 36.40, "dpa_12m": 2.80, "dpa_3y_avg": 2.35, "dy_12m": 7.69,
        "pl": 9.80, "pvp": 1.95, "roe": 22.0, "net_margin": 9.5, "debt_ebitda": 0.0,
        "lpa": 3.71, "vpa": 18.66, "dividend_cagr_3y": 16.8, "payout": 55.0,
        "payments_per_year": 2, "payment_months": [4, 10]
    },
    "TAEE11.SA": {
        "price": 35.10, "dpa_12m": 3.48, "dpa_3y_avg": 3.60, "dy_12m": 9.91,
        "pl": 9.10, "pvp": 1.70, "roe": 19.8, "net_margin": 45.0, "debt_ebitda": 3.4,
        "lpa": 3.85, "vpa": 20.65, "dividend_cagr_3y": 5.1, "payout": 75.0,
        "payments_per_year": 4, "payment_months": [5, 8, 11, 12]
    },
    "TRPL4.SA": {
        "price": 25.80, "dpa_12m": 2.38, "dpa_3y_avg": 2.20, "dy_12m": 9.22,
        "pl": 6.80, "pvp": 0.98, "roe": 15.4, "net_margin": 48.0, "debt_ebitda": 2.3,
        "lpa": 3.79, "vpa": 26.32, "dividend_cagr_3y": 8.5, "payout": 75.0,
        "payments_per_year": 6, "payment_months": [1, 4, 6, 8, 10, 12]
    },
    "EGIE3.SA": {
        "price": 40.50, "dpa_12m": 3.15, "dpa_3y_avg": 3.10, "dy_12m": 7.78,
        "pl": 10.50, "pvp": 3.10, "roe": 29.5, "net_margin": 26.0, "debt_ebitda": 2.2,
        "lpa": 3.86, "vpa": 13.06, "dividend_cagr_3y": 11.2, "payout": 65.0,
        "payments_per_year": 3, "payment_months": [5, 8, 12]
    },
    "CPLE6.SA": {
        "price": 9.85, "dpa_12m": 0.78, "dpa_3y_avg": 0.68, "dy_12m": 7.92,
        "pl": 7.90, "pvp": 1.15, "roe": 15.0, "net_margin": 16.5, "debt_ebitda": 1.8,
        "lpa": 1.25, "vpa": 8.56, "dividend_cagr_3y": 14.0, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [4, 6, 9, 12]
    },
    "CMIG4.SA": {
        "price": 11.60, "dpa_12m": 1.28, "dpa_3y_avg": 1.20, "dy_12m": 11.03,
        "pl": 5.40, "pvp": 1.08, "roe": 21.0, "net_margin": 14.0, "debt_ebitda": 1.4,
        "lpa": 2.15, "vpa": 10.74, "dividend_cagr_3y": 8.9, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [4, 6, 9, 12]
    },
    "EQTL3.SA": {
        "price": 32.50, "dpa_12m": 1.15, "dpa_3y_avg": 0.95, "dy_12m": 3.54,
        "pl": 12.80, "pvp": 1.85, "roe": 16.2, "net_margin": 8.5, "debt_ebitda": 2.8,
        "lpa": 2.54, "vpa": 17.56, "dividend_cagr_3y": 20.4, "payout": 30.0,
        "payments_per_year": 2, "payment_months": [4, 11]
    },
    "SAPR11.SA": {
        "price": 28.20, "dpa_12m": 2.15, "dpa_3y_avg": 1.95, "dy_12m": 7.62,
        "pl": 5.80, "pvp": 0.88, "roe": 16.0, "net_margin": 24.0, "debt_ebitda": 1.6,
        "lpa": 4.86, "vpa": 32.04, "dividend_cagr_3y": 12.1, "payout": 40.0,
        "payments_per_year": 6, "payment_months": [2, 4, 6, 8, 10, 12]
    },
    "SAPR4.SA": {
        "price": 5.64, "dpa_12m": 0.43, "dpa_3y_avg": 0.39, "dy_12m": 7.62,
        "pl": 5.80, "pvp": 0.88, "roe": 16.0, "net_margin": 24.0, "debt_ebitda": 1.6,
        "lpa": 0.97, "vpa": 6.41, "dividend_cagr_3y": 12.1, "payout": 40.0,
        "payments_per_year": 6, "payment_months": [2, 4, 6, 8, 10, 12]
    },
    "CSMG3.SA": {
        "price": 21.50, "dpa_12m": 1.92, "dpa_3y_avg": 1.70, "dy_12m": 8.93,
        "pl": 6.90, "pvp": 0.95, "roe": 14.5, "net_margin": 18.0, "debt_ebitda": 1.5,
        "lpa": 3.12, "vpa": 22.63, "dividend_cagr_3y": 11.5, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [3, 6, 9, 12]
    },
    "CMIG3.SA": {
        "price": 9.75, "dpa_12m": 0.95, "dpa_3y_avg": 0.90, "dy_12m": 9.74,
        "pl": 5.10, "pvp": 0.98, "roe": 20.5, "net_margin": 15.5, "debt_ebitda": 1.3,
        "lpa": 1.91, "vpa": 9.95, "dividend_cagr_3y": 14.0, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [4, 6, 9, 12]
    },
    "VIVT3.SA": {
        "price": 52.30, "dpa_12m": 4.10, "dpa_3y_avg": 3.80, "dy_12m": 7.84,
        "pl": 14.20, "pvp": 1.22, "roe": 8.9, "net_margin": 10.5, "debt_ebitda": 0.4,
        "lpa": 3.68, "vpa": 42.86, "dividend_cagr_3y": 7.8, "payout": 85.0,
        "payments_per_year": 4, "payment_months": [4, 7, 10, 12]
    },
    "TIMS3.SA": {
        "price": 17.60, "dpa_12m": 1.35, "dpa_3y_avg": 1.05, "dy_12m": 7.67,
        "pl": 13.50, "pvp": 1.62, "roe": 12.5, "net_margin": 12.0, "debt_ebitda": 0.7,
        "lpa": 1.30, "vpa": 10.86, "dividend_cagr_3y": 18.0, "payout": 75.0,
        "payments_per_year": 4, "payment_months": [1, 4, 7, 10]
    },
    "KLBN11.SA": {
        "price": 21.80, "dpa_12m": 1.55, "dpa_3y_avg": 1.48, "dy_12m": 7.11,
        "pl": 8.50, "pvp": 2.30, "roe": 28.0, "net_margin": 15.0, "debt_ebitda": 3.2,
        "lpa": 2.56, "vpa": 9.48, "dividend_cagr_3y": 6.8, "payout": 30.0,
        "payments_per_year": 4, "payment_months": [2, 5, 8, 11]
    },
    "KLBN4.SA": {
        "price": 4.36, "dpa_12m": 0.31, "dpa_3y_avg": 0.30, "dy_12m": 7.11,
        "pl": 8.50, "pvp": 2.30, "roe": 28.0, "net_margin": 15.0, "debt_ebitda": 3.2,
        "lpa": 0.51, "vpa": 1.90, "dividend_cagr_3y": 6.8, "payout": 30.0,
        "payments_per_year": 4, "payment_months": [2, 5, 8, 11]
    },
    "RANI3.SA": {
        "price": 7.65, "dpa_12m": 0.65, "dpa_3y_avg": 0.60, "dy_12m": 8.50,
        "pl": 6.20, "pvp": 1.45, "roe": 23.5, "net_margin": 18.0, "debt_ebitda": 1.8,
        "lpa": 1.23, "vpa": 5.28, "dividend_cagr_3y": 14.5, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [3, 5, 8, 11]
    },
    "SUZB3.SA": {
        "price": 58.40, "dpa_12m": 2.10, "dpa_3y_avg": 1.80, "dy_12m": 3.60,
        "pl": 7.20, "pvp": 1.75, "roe": 26.0, "net_margin": 22.0, "debt_ebitda": 2.7,
        "lpa": 8.11, "vpa": 33.37, "dividend_cagr_3y": 15.0, "payout": 25.0,
        "payments_per_year": 2, "payment_months": [5, 12]
    },
    "PETR4.SA": {
        "price": 38.90, "dpa_12m": 6.20, "dpa_3y_avg": 7.80, "dy_12m": 15.94,
        "pl": 4.30, "pvp": 1.25, "roe": 29.0, "net_margin": 24.0, "debt_ebitda": 0.8,
        "lpa": 9.05, "vpa": 31.12, "dividend_cagr_3y": 25.0, "payout": 45.0,
        "payments_per_year": 4, "payment_months": [2, 5, 8, 11]
    },
    "VALE3.SA": {
        "price": 57.20, "dpa_12m": 5.40, "dpa_3y_avg": 5.80, "dy_12m": 9.44,
        "pl": 5.80, "pvp": 1.30, "roe": 23.5, "net_margin": 21.0, "debt_ebitda": 0.6,
        "lpa": 9.86, "vpa": 44.00, "dividend_cagr_3y": 4.5, "payout": 50.0,
        "payments_per_year": 2, "payment_months": [3, 9]
    },
    "GGBR4.SA": {
        "price": 18.90, "dpa_12m": 1.25, "dpa_3y_avg": 1.55, "dy_12m": 6.61,
        "pl": 6.40, "pvp": 0.72, "roe": 12.0, "net_margin": 8.0, "debt_ebitda": 0.5,
        "lpa": 2.95, "vpa": 26.25, "dividend_cagr_3y": -2.0, "payout": 30.0,
        "payments_per_year": 4, "payment_months": [3, 5, 8, 11]
    },
    "CSNA3.SA": {
        "price": 12.40, "dpa_12m": 1.15, "dpa_3y_avg": 1.40, "dy_12m": 9.27,
        "pl": 8.50, "pvp": 0.82, "roe": 10.5, "net_margin": 6.5, "debt_ebitda": 2.8,
        "lpa": 1.46, "vpa": 15.12, "dividend_cagr_3y": 5.2, "payout": 45.0,
        "payments_per_year": 4, "payment_months": [4, 5, 11, 12]
    },
    "VBBR3.SA": {
        "price": 24.10, "dpa_12m": 1.65, "dpa_3y_avg": 1.30, "dy_12m": 6.85,
        "pl": 11.50, "pvp": 1.80, "roe": 16.5, "net_margin": 3.8, "debt_ebitda": 1.9,
        "lpa": 2.10, "vpa": 13.38, "dividend_cagr_3y": 22.0, "payout": 45.0,
        "payments_per_year": 2, "payment_months": [4, 12]
    },
    "WEGE3.SA": {
        "price": 51.20, "dpa_12m": 1.35, "dpa_3y_avg": 1.05, "dy_12m": 2.64,
        "pl": 32.50, "pvp": 9.20, "roe": 30.5, "net_margin": 17.5, "debt_ebitda": -0.2,
        "lpa": 1.57, "vpa": 5.56, "dividend_cagr_3y": 24.5, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [3, 8, 10, 12]
    },
    "PRIO3.SA": {
        "price": 44.50, "dpa_12m": 0.00, "dpa_3y_avg": 0.00, "dy_12m": 0.00,
        "pl": 7.80, "pvp": 2.10, "roe": 32.0, "net_margin": 42.0, "debt_ebitda": 0.9,
        "lpa": 5.70, "vpa": 21.19, "dividend_cagr_3y": 30.0, "payout": 0.0,
        "payments_per_year": 0, "payment_months": []
    },
    "RADL3.SA": {
        "price": 25.80, "dpa_12m": 0.42, "dpa_3y_avg": 0.38, "dy_12m": 1.63,
        "pl": 34.00, "pvp": 6.10, "roe": 19.5, "net_margin": 3.4, "debt_ebitda": 1.1,
        "lpa": 0.76, "vpa": 4.23, "dividend_cagr_3y": 16.5, "payout": 35.0,
        "payments_per_year": 4, "payment_months": [3, 6, 9, 12]
    }
}

def calculate_bazin_target_price(dpa_avg: float, target_yield: float = 0.06) -> float:
    """
    Fórmula de Décio Bazin:
    Preço Teto = DPA Médio / Yield Alvo (default 6% ao ano)
    """
    if target_yield <= 0 or dpa_avg <= 0:
        return 0.0
    return round(dpa_avg / target_yield, 2)

def calculate_graham_fair_value(lpa: float, vpa: float) -> float:
    """
    Fórmula de Benjamin Graham:
    Valor Justo = sqrt(22.5 * LPA * VPA)
    """
    if lpa <= 0 or vpa <= 0:
        return 0.0
    return round(math.sqrt(22.5 * lpa * vpa), 2)

def calculate_margin_of_safety(fair_price: float, current_price: float) -> float:
    """Margem de Segurança (%) = ((Preço Justo ou Teto - Preço Atual) / Preço Atual) * 100"""
    if current_price <= 0 or fair_price <= 0:
        return 0.0
    return round(((fair_price - current_price) / current_price) * 100, 2)

def fetch_single_ticker_data(ticker: str, force_refresh: bool = False) -> Dict[str, Any]:
    """Coleta os dados ao vivo do yfinance com fallback transparente e robusto."""
    global _MARKET_CACHE, _CACHE_TIMESTAMP

    # Verificar cache
    if not force_refresh and ticker in _MARKET_CACHE and (time.time() - _CACHE_TIMESTAMP) < CACHE_TTL_SECONDS:
        return _MARKET_CACHE[ticker]

    universe_map = get_universe_map()
    meta = universe_map.get(ticker, {
        "name": ticker,
        "sector": "Outros",
        "subsector": "Geral",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": ""
    })

    fallback = FALLBACK_FUNDAMENTALS.get(ticker, {
        "price": 20.0, "dpa_12m": 1.20, "dpa_3y_avg": 1.10, "dy_12m": 6.0,
        "pl": 8.0, "pvp": 1.2, "roe": 15.0, "net_margin": 15.0, "debt_ebitda": 1.5,
        "lpa": 2.50, "vpa": 16.66, "dividend_cagr_3y": 8.0, "payout": 50.0,
        "payments_per_year": 4, "payment_months": [3, 6, 9, 12]
    })

    data: Dict[str, Any] = {
        "ticker": ticker,
        "ticker_clean": ticker.replace(".SA", ""),
        "name": meta.get("name", ticker),
        "sector": meta.get("sector", "Geral"),
        "subsector": meta.get("subsector", "Geral"),
        "default_category": meta.get("default_category", "trimestral"),
        "description": meta.get("description", ""),
        "is_live_data": False,
        "dividend_history": []
    }

    # Tentar coletar via yfinance
    if yf is not None:
        try:
            yt = yf.Ticker(ticker)
            info = yt.info or {}
            
            # Cotação
            price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
            if not price or price <= 0:
                price = fallback["price"]
            else:
                data["is_live_data"] = True

            data["price"] = round(float(price), 2)

            # Histórico de dividendos
            try:
                divs = yt.dividends
                if isinstance(divs, pd.Series) and not divs.empty:
                    # Últimos 3 anos de dividendos
                    recent_divs = divs[divs.index >= (pd.Timestamp.now(tz=divs.index.tz) - pd.DateOffset(years=3))]
                    dpa_12m = float(divs[divs.index >= (pd.Timestamp.now(tz=divs.index.tz) - pd.DateOffset(years=1))].sum())
                    dpa_3y_avg = float(recent_divs.sum() / 3.0) if len(recent_divs) > 0 else dpa_12m

                    # Salvar lista estruturada de eventos de dividendos
                    hist_list = []
                    for dt, val in recent_divs.items():
                        hist_list.append({
                            "date": dt.strftime("%Y-%m-%d"),
                            "year": dt.year,
                            "month": dt.month,
                            "value": round(float(val), 4)
                        })
                    data["dividend_history"] = hist_list
                else:
                    dpa_12m = fallback["dpa_12m"]
                    dpa_3y_avg = fallback["dpa_3y_avg"]
            except Exception:
                dpa_12m = fallback["dpa_12m"]
                dpa_3y_avg = fallback["dpa_3y_avg"]

            data["dpa_12m"] = round(dpa_12m if dpa_12m > 0 else fallback["dpa_12m"], 2)
            data["dpa_3y_avg"] = round(dpa_3y_avg if dpa_3y_avg > 0 else fallback["dpa_3y_avg"], 2)

            # Dividend Yield
            if data["price"] > 0:
                data["dy_12m"] = round((data["dpa_12m"] / data["price"]) * 100, 2)
            else:
                data["dy_12m"] = fallback["dy_12m"]

            # Múltiplos e Indicadores
            data["pl"] = round(float(info.get("trailingPE") or fallback["pl"]), 2)
            data["pvp"] = round(float(info.get("priceToBook") or fallback["pvp"]), 2)
            
            # ROE (retorno sobre patrimônio líquido)
            roe_val = info.get("returnOnEquity")
            if roe_val is not None:
                data["roe"] = round(float(roe_val) * 100, 2)
            else:
                data["roe"] = fallback["roe"]

            # Margem Líquida
            profit_margin = info.get("profitMargins")
            if profit_margin is not None:
                data["net_margin"] = round(float(profit_margin) * 100, 2)
            else:
                data["net_margin"] = fallback["net_margin"]

            # LPA e VPA
            lpa_val = info.get("trailingEps")
            data["lpa"] = round(float(lpa_val if lpa_val is not None else fallback["lpa"]), 2)
            
            book_val = info.get("bookValue")
            data["vpa"] = round(float(book_val if book_val is not None else fallback["vpa"]), 2)

            # Endividamento
            debt_ebitda = fallback["debt_ebitda"]
            data["debt_ebitda"] = debt_ebitda

            # Payout e CAGR
            data["payout"] = round(float(info.get("payoutRatio", 0) * 100) if info.get("payoutRatio") else fallback["payout"], 1)
            data["dividend_cagr_3y"] = fallback["dividend_cagr_3y"]
            data["payment_months"] = fallback.get("payment_months", [3, 6, 9, 12])
            data["payments_per_year"] = fallback.get("payments_per_year", 4)

        except Exception as e:
            # Em caso de qualquer erro de rede / rate limit, usar fallback seguro
            data.update(fallback)
            data["price"] = fallback["price"]
            data["dpa_12m"] = fallback["dpa_12m"]
            data["dpa_3y_avg"] = fallback["dpa_3y_avg"]
            data["dy_12m"] = fallback["dy_12m"]
    else:
        data.update(fallback)

    # Se não temos histórico de dividendos criado pelo yfinance, sintetizar baseado no fallback
    if not data.get("dividend_history"):
        curr_year = datetime.now().year
        synthetic_hist = []
        p_months = data.get("payment_months", [3, 6, 9, 12])
        if p_months:
            div_per_pay = round(data["dpa_12m"] / len(p_months), 3) if len(p_months) > 0 else 0
            for yr in range(curr_year - 2, curr_year + 1):
                for m in p_months:
                    synthetic_hist.append({
                        "date": f"{yr}-{m:02d}-15",
                        "year": yr,
                        "month": m,
                        "value": div_per_pay
                    })
        data["dividend_history"] = synthetic_hist

    # Cálculos de Métricas Consagradas de Investimento
    # 1. Preço Teto de Décio Bazin (Yield 6%)
    data["bazin_target_price"] = calculate_bazin_target_price(data["dpa_3y_avg"], target_yield=0.06)
    data["bazin_margin_safety"] = calculate_margin_of_safety(data["bazin_target_price"], data["price"])

    # 2. Valor Justo de Benjamin Graham
    data["graham_fair_value"] = calculate_graham_fair_value(data["lpa"], data["vpa"])
    data["graham_margin_safety"] = calculate_margin_of_safety(data["graham_fair_value"], data["price"])

    return data

def get_market_dataset(force_refresh: bool = False) -> pd.DataFrame:
    """Retorna um DataFrame completo com todos os ativos do universo monitorado."""
    global _MARKET_CACHE, _CACHE_TIMESTAMP

    results = []
    for item in B3_DIVIDEND_UNIVERSE:
        ticker = item["ticker"]
        tdata = fetch_single_ticker_data(ticker, force_refresh=force_refresh)
        _MARKET_CACHE[ticker] = tdata
        results.append(tdata)

    _CACHE_TIMESTAMP = time.time()
    df = pd.DataFrame(results)
    return df
