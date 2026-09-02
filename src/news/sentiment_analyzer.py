"""
Analisador de Sentimento Financeiro em Português para Mercado B3 e Ações de Dividendos.
Processa manchetes, resumos e notícias corporativas gerando pontuação e diagnóstico.
"""

from typing import Dict, List, Any, Tuple
import re

# Dicionário de termos financeiros positivos e pesos
POSITIVE_FINANCIAL_TERMS: Dict[str, float] = {
    # Proventos e remuneração ao acionista
    "dividendo": 1.5,
    "dividendos": 1.8,
    "juros sobre capital": 1.6,
    "jcp": 1.6,
    "provento": 1.4,
    "proventos": 1.5,
    "bonificação": 1.6,
    "recompra de ações": 1.8,
    "recompra": 1.5,
    "payout elevado": 2.0,
    "dividend yield alto": 2.0,
    "dividendos bilionários": 2.5,
    "dividendos extraordinários": 2.5,
    "aprova distribuição": 2.0,
    "anuncia pagamento": 2.0,
    
    # Resultados e Finanças
    "lucro recorde": 2.5,
    "lucro líquido cresce": 2.2,
    "alta no lucro": 2.0,
    "salto no lucro": 2.2,
    "lucro avança": 1.8,
    "supera projeções": 2.0,
    "superou expectativas": 2.2,
    "forte geração de caixa": 2.2,
    "caixa livre": 1.6,
    "ebitda recorde": 2.0,
    "ebitda avança": 1.8,
    "roe elevado": 1.8,
    "rentabilidade recorde": 2.0,
    "eficiência operacional": 1.5,
    "receita cresce": 1.5,
    "expansão": 1.4,
    "desalavancagem": 1.8,
    "redução de dívida": 1.8,
    "disciplina de capital": 1.7,
    "recomendação de compra": 1.9,
    "compra": 1.2,
    "otimismo": 1.3,
    "resiliente": 1.4,
    "resiliência": 1.5
}

# Dicionário de termos financeiros negativos e pesos
NEGATIVE_FINANCIAL_TERMS: Dict[str, float] = {
    # Cortes e restrições de proventos
    "corte de dividendos": 3.0,
    "redução de dividendos": 2.5,
    "suspensão de dividendos": 3.0,
    "corta proventos": 2.8,
    "cancela distribuição": 3.0,
    "sem dividendos": 2.5,
    
    # Resultados ruins e riscos
    "prejuízo": 2.8,
    "prejuízo líquido": 3.0,
    "queda no lucro": 2.2,
    "lucro despenca": 2.8,
    "tombo no lucro": 2.8,
    "lucro recua": 1.8,
    "abaixo do esperado": 2.0,
    "frustra mercado": 2.2,
    "decepciona": 2.0,
    "endividamento crítico": 2.8,
    "alta da dívida": 2.0,
    "alavancagem elevada": 2.2,
    "inadimplência sobe": 2.0,
    "pressão nas margens": 1.7,
    "rebaixamento": 2.2,
    "rebaixa": 2.0,
    "recomendação de venda": 2.5,
    "risco regulatório": 2.0,
    "investigação": 2.2,
    "multa": 2.0,
    "processo judicial": 1.8,
    "crise": 2.0,
    "cautela": 1.3,
    "pessimismo": 1.5
}

def analyze_text_sentiment(text: str) -> Tuple[float, List[str], List[str]]:
    """
    Analisa um texto financeiro e retorna:
    - score normalizado de -1.0 a +1.0
    - lista de termos positivos encontrados
    - lista de termos negativos encontrados
    """
    if not text:
        return 0.0, [], []

    text_lower = text.lower()
    pos_score = 0.0
    neg_score = 0.0
    pos_found = []
    neg_found = []

    for term, weight in POSITIVE_FINANCIAL_TERMS.items():
        if term in text_lower:
            pos_score += weight
            pos_found.append(term)

    for term, weight in NEGATIVE_FINANCIAL_TERMS.items():
        if term in text_lower:
            neg_score += weight
            neg_found.append(term)

    total_score = pos_score - neg_score
    magnitude = pos_score + neg_score + 1.0
    
    # Normalização entre -1.0 e 1.0 usando tangente hiperbólica simples
    normalized = max(-1.0, min(1.0, total_score / (magnitude if magnitude > 0 else 1.0)))
    
    return round(normalized, 3), pos_found, neg_found

def evaluate_company_news_sentiment(news_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Consolida o sentimento de um conjunto de notícias recentes da empresa.
    """
    if not news_list:
        return {
            "score": 0.0,
            "label": "Neutro",
            "badge": "⚪ Neutro",
            "color": "#94A3B8",
            "pos_keywords": [],
            "neg_keywords": [],
            "impact_on_dividends": "Neutro / Sem notícias de impacto recente"
        }

    scores = []
    all_pos = []
    all_neg = []

    for item in news_list:
        full_text = f"{item.get('title', '')} {item.get('summary', '')}"
        score, pos, neg = analyze_text_sentiment(full_text)
        item["sentiment_score"] = score
        scores.append(score)
        all_pos.extend(pos)
        all_neg.extend(neg)

    avg_score = sum(scores) / len(scores) if scores else 0.0
    avg_score = round(avg_score, 2)

    # Classificação em faixas
    if avg_score >= 0.35:
        label = "Muito Positivo"
        badge = "🟢 Muito Positivo"
        color = "#10B981"
        impact = "🚀 Favorável: Notícias indicam proventos robustos ou resultados acima da média"
    elif 0.10 <= avg_score < 0.35:
        label = "Positivo"
        badge = "🟢 Positivo"
        color = "#34D399"
        impact = "✅ Saudável: Manutenção e fluxo regular de dividendos confirmados"
    elif -0.10 < avg_score < 0.10:
        label = "Neutro"
        badge = "⚪ Neutro"
        color = "#94A3B8"
        impact = "⚖️ Estável: Proventos em linha com o histórico da empresa"
    elif -0.35 < avg_score <= -0.10:
        label = "Cautela"
        badge = "🟡 Cautela"
        color = "#F59E0B"
        impact = "⚠️ Atenção: Pressões de curto prazo ou margens sob monitoramento"
    else:
        label = "Negativo"
        badge = "🔴 Negativo"
        color = "#EF4444"
        impact = "🚨 Risco: Notícias apontam queda no lucro ou revisão na política de proventos"

    return {
        "score": avg_score,
        "label": label,
        "badge": badge,
        "color": color,
        "pos_keywords": list(set(all_pos))[:5],
        "neg_keywords": list(set(all_neg))[:5],
        "impact_on_dividends": impact
    }
