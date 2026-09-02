"""
Gerenciador de Carteira e Cadastro de Ativos do Investidor.
Responsável pela persistência local de transações, histórico de atualizações e cálculos de rentabilidade real da B3.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

PORTFOLIO_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "portfolio_transactions.json"
)

def _ensure_data_directory():
    """Garante que a pasta 'data' existe para salvar as transações."""
    data_dir = os.path.dirname(PORTFOLIO_FILE_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)

def load_transactions() -> List[Dict[str, Any]]:
    """Carrega a lista de transações registradas."""
    _ensure_data_directory()
    if not os.path.exists(PORTFOLIO_FILE_PATH):
        # Se não houver arquivo, inicializar com exemplos ilustrativos
        sample_transactions = get_sample_transactions()
        save_transactions(sample_transactions)
        return sample_transactions

    try:
        with open(PORTFOLIO_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def save_transactions(transactions: List[Dict[str, Any]]) -> bool:
    """Salva a lista de transações no arquivo JSON."""
    _ensure_data_directory()
    try:
        with open(PORTFOLIO_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(transactions, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar transações: {e}")
        return False

def add_transaction(ticker: str, date_str: str, quantity: int, price_per_share: float, notes: str = "") -> Dict[str, Any]:
    """Adiciona uma nova transação / aporte de ativo."""
    clean_ticker = ticker.replace(".SA", "").upper().strip()
    full_ticker = f"{clean_ticker}.SA"
    
    total_val = round(float(quantity) * float(price_per_share), 2)
    
    new_tx = {
        "id": str(uuid.uuid4())[:8],
        "ticker": full_ticker,
        "ticker_clean": clean_ticker,
        "date": date_str,
        "quantity": int(quantity),
        "price_per_share": round(float(price_per_share), 2),
        "total_invested": total_val,
        "notes": notes.strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    transactions = load_transactions()
    transactions.append(new_tx)
    save_transactions(transactions)
    return new_tx

def update_transaction(tx_id: str, ticker: str, date_str: str, quantity: int, price_per_share: float, notes: str = "") -> bool:
    """Atualiza uma transação existente no histórico."""
    transactions = load_transactions()
    clean_ticker = ticker.replace(".SA", "").upper().strip()
    full_ticker = f"{clean_ticker}.SA"
    
    found = False
    for tx in transactions:
        if tx.get("id") == tx_id:
            tx["ticker"] = full_ticker
            tx["ticker_clean"] = clean_ticker
            tx["date"] = date_str
            tx["quantity"] = int(quantity)
            tx["price_per_share"] = round(float(price_per_share), 2)
            tx["total_invested"] = round(float(quantity) * float(price_per_share), 2)
            tx["notes"] = notes.strip()
            tx["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break
            
    if found:
        save_transactions(transactions)
    return found

def delete_transaction(tx_id: str) -> bool:
    """Remove uma transação do histórico."""
    transactions = load_transactions()
    new_list = [tx for tx in transactions if tx.get("id") != tx_id]
    if len(new_list) != len(transactions):
        save_transactions(new_list)
        return True
    return False

def get_portfolio_summary(market_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Consolida as transações e calcula métricas completas da carteira do investidor:
    - Total Investido (Custo de Compra)
    - Valor Atualizado Real (com cotação de mercado B3)
    - Lucro/Prejuízo nominal e percentual
    - Proventos estimados anuais e mensais
    """
    transactions = load_transactions()
    if not transactions:
        return {
            "is_empty": True,
            "total_invested": 0.0,
            "total_current_value": 0.0,
            "total_profit_loss": 0.0,
            "total_profit_loss_pct": 0.0,
            "total_annual_dividends": 0.0,
            "total_monthly_dividends": 0.0,
            "assets_df": pd.DataFrame(),
            "transactions": []
        }

    # Criar mapeamento com os dados da B3
    market_map = {}
    if not market_df.empty:
        for _, row in market_df.iterrows():
            clean_t = row.get("ticker_clean", row.get("ticker", "")).replace(".SA", "")
            market_map[clean_t] = row.to_dict()

    # Agrupar transações por ativo
    holdings: Dict[str, Dict[str, Any]] = {}
    for tx in transactions:
        t_clean = tx.get("ticker_clean", "").upper()
        qty = tx.get("quantity", 0)
        cost = tx.get("total_invested", 0.0)

        if t_clean not in holdings:
            holdings[t_clean] = {
                "ticker_clean": t_clean,
                "ticker": tx.get("ticker", f"{t_clean}.SA"),
                "total_quantity": 0,
                "total_invested": 0.0,
                "transaction_count": 0
            }
        holdings[t_clean]["total_quantity"] += qty
        holdings[t_clean]["total_invested"] += cost
        holdings[t_clean]["transaction_count"] += 1

    assets_records = []
    total_portfolio_invested = 0.0
    total_portfolio_current_value = 0.0
    total_annual_dividends = 0.0

    for t_clean, item in holdings.items():
        qty = item["total_quantity"]
        invested = item["total_invested"]
        avg_price = invested / qty if qty > 0 else 0.0

        # Buscar dados de mercado
        m_data = market_map.get(t_clean, {})
        current_price = m_data.get("price", avg_price)
        dpa_12m = m_data.get("dpa_12m", 0.0)
        dy_12m = m_data.get("dy_12m", 0.0)
        name = m_data.get("name", t_clean)
        sector = m_data.get("sector", "Geral")

        current_value = round(qty * current_price, 2)
        profit_loss = round(current_value - invested, 2)
        profit_loss_pct = round((profit_loss / invested) * 100, 2) if invested > 0 else 0.0
        est_dividends = round(qty * dpa_12m, 2)

        total_portfolio_invested += invested
        total_portfolio_current_value += current_value
        total_annual_dividends += est_dividends

        assets_records.append({
            "ticker_clean": t_clean,
            "name": name,
            "sector": sector,
            "quantity": qty,
            "avg_price": round(avg_price, 2),
            "current_price": round(current_price, 2),
            "total_invested": round(invested, 2),
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_pct": profit_loss_pct,
            "dy_12m": dy_12m,
            "dpa_12m": dpa_12m,
            "estimated_annual_dividends": est_dividends,
            "transaction_count": item["transaction_count"]
        })

    assets_df = pd.DataFrame(assets_records)

    # Calcular participações percentuais
    if not assets_df.empty:
        if total_portfolio_invested > 0:
            assets_df["weight_invested_pct"] = (assets_df["total_invested"] / total_portfolio_invested) * 100
        else:
            assets_df["weight_invested_pct"] = 0.0

        if total_portfolio_current_value > 0:
            assets_df["weight_current_pct"] = (assets_df["current_value"] / total_portfolio_current_value) * 100
        else:
            assets_df["weight_current_pct"] = 0.0

        assets_df = assets_df.sort_values(by="current_value", ascending=False).reset_index(drop=True)

    total_profit_loss = round(total_portfolio_current_value - total_portfolio_invested, 2)
    total_profit_loss_pct = round((total_profit_loss / total_portfolio_invested) * 100, 2) if total_portfolio_invested > 0 else 0.0
    total_monthly_dividends = round(total_annual_dividends / 12.0, 2)

    return {
        "is_empty": False,
        "total_invested": round(total_portfolio_invested, 2),
        "total_current_value": round(total_portfolio_current_value, 2),
        "total_profit_loss": total_profit_loss,
        "total_profit_loss_pct": total_profit_loss_pct,
        "total_annual_dividends": round(total_annual_dividends, 2),
        "total_monthly_dividends": total_monthly_dividends,
        "assets_df": assets_df,
        "transactions": transactions
    }

def get_sample_transactions() -> List[Dict[str, Any]]:
    """Gera transações de exemplo iniciais para enriquecer a experiência visual."""
    return [
        {
            "id": "tx-001",
            "ticker": "BBAS3.SA",
            "ticker_clean": "BBAS3",
            "date": "2024-01-15",
            "quantity": 200,
            "price_per_share": 25.50,
            "total_invested": 5100.00,
            "notes": "Aporte inicial focado em dividendos trimestrais",
            "created_at": "2024-01-15 10:00:00"
        },
        {
            "id": "tx-002",
            "ticker": "ITUB4.SA",
            "ticker_clean": "ITUB4",
            "date": "2024-02-10",
            "quantity": 150,
            "price_per_share": 31.80,
            "total_invested": 4770.00,
            "notes": "Compra para fluxo de renda mensal",
            "created_at": "2024-02-10 11:30:00"
        },
        {
            "id": "tx-003",
            "ticker": "TAEE11.SA",
            "ticker_clean": "TAEE11",
            "date": "2024-03-05",
            "quantity": 180,
            "price_per_share": 34.20,
            "total_invested": 6156.00,
            "notes": "Transmissora de energia elétrica para proteção inflacionária",
            "created_at": "2024-03-05 14:15:00"
        },
        {
            "id": "tx-004",
            "ticker": "BBSE3.SA",
            "ticker_clean": "BBSE3",
            "date": "2024-04-20",
            "quantity": 120,
            "price_per_share": 32.40,
            "total_invested": 3888.00,
            "notes": "Seguradora com alto ROE e dividend yield de 2 dígitos",
            "created_at": "2024-04-20 09:45:00"
        },
        {
            "id": "tx-005",
            "ticker": "EGIE3.SA",
            "ticker_clean": "EGIE3",
            "date": "2024-05-12",
            "quantity": 100,
            "price_per_share": 38.50,
            "total_invested": 3850.00,
            "notes": "Geradora de energia limpa com dividend growth",
            "created_at": "2024-05-12 16:00:00"
        }
    ]
