"""
Universo de Ações Pagadoras de Dividendos e Ativos Líquidos da B3.
Contém catálogo curado de empresas tradicionais e atrativas em proventos.
"""

from typing import Dict, List, Any

B3_DIVIDEND_UNIVERSE: List[Dict[str, Any]] = [
    # --- BANCOS E SERVIÇOS FINANCEIROS ---
    {
        "ticker": "BBAS3.SA",
        "ticker_clean": "BBAS3",
        "name": "Banco do Brasil",
        "sector": "Financeiro",
        "subsector": "Bancos",
        "default_category": "trimestral",
        "payout_target": 0.45,
        "description": "Maior banco em carteira agro do Brasil, alto ROE histórico e política consolidada de 8 distribuições anuais (trimestrais + antecipações)."
    },
    {
        "ticker": "ITUB4.SA",
        "ticker_clean": "ITUB4",
        "name": "Itaú Unibanco",
        "sector": "Financeiro",
        "subsector": "Bancos",
        "default_category": "mensal",
        "payout_target": 0.50,
        "description": "Maior banco privado da América Latina. Paga proventos mensais recorrentes (JCP mensal) além de dividendos complementares robustos."
    },
    {
        "ticker": "BBDC4.SA",
        "ticker_clean": "BBDC4",
        "name": "Bradesco",
        "sector": "Financeiro",
        "subsector": "Bancos",
        "default_category": "mensal",
        "payout_target": 0.40,
        "description": "Um dos maiores conglomerados bancários do país, distribui JCP mensal a todos os acionistas com adicionais semestrais."
    },
    {
        "ticker": "ITSA4.SA",
        "ticker_clean": "ITSA4",
        "name": "Itaúsa",
        "sector": "Financeiro",
        "subsector": "Holdings",
        "default_category": "trimestral",
        "payout_target": 0.45,
        "description": "Holding controladora do Itaú com participação em Dexco, Alpargatas, CCR e Copa Energia. Distribuição trimestral regular de JCP/dividendos."
    },
    {
        "ticker": "SANB11.SA",
        "ticker_clean": "SANB11",
        "name": "Banco Santander Brasil",
        "sector": "Financeiro",
        "subsector": "Bancos",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": "Subsidiária do grupo espanhol Santander, histórico forte de remuneração trimestral e boa rentabilidade de dividendos."
    },
    {
        "ticker": "BEES3.SA",
        "ticker_clean": "BEES3",
        "name": "Banestes ON",
        "sector": "Financeiro",
        "subsector": "Bancos Regionais",
        "default_category": "mensal",
        "payout_target": 0.50,
        "description": "Banco do Estado do Espírito Santo (Ações Ordinárias). Pagamento mensal regular de proventos com dividend yield elevado."
    },
    {
        "ticker": "BEES4.SA",
        "ticker_clean": "BEES4",
        "name": "Banestes PN",
        "sector": "Financeiro",
        "subsector": "Bancos Regionais",
        "default_category": "mensal",
        "payout_target": 0.50,
        "description": "Banco do Estado do Espírito Santo (Ações Preferenciais). Distribuição mensal recorrente de JCP/dividendos com yield atrativo."
    },
    {
        "ticker": "ABCB4.SA",
        "ticker_clean": "ABCB4",
        "name": "Banco ABC Brasil",
        "sector": "Financeiro",
        "subsector": "Bancos / Middle Market",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": "Banco focado no segmento corporativo e middle-market, ROE consistente próximo a 15-17%, P/L atrativo e remuneração regular em proventos."
    },
    {
        "ticker": "BRSR6.SA",
        "ticker_clean": "BRSR6",
        "name": "Banrisul",
        "sector": "Financeiro",
        "subsector": "Bancos Estaduais",
        "default_category": "trimestral",
        "payout_target": 0.40,
        "description": "Banco do Estado do Rio Grande do Sul, negociando com expressivo desconto patrimonial (P/VP baixo), distribuindo proventos trimestrais via JCP."
    },
    {
        "ticker": "BRAP4.SA",
        "ticker_clean": "BRAP4",
        "name": "Bradespar",
        "sector": "Financeiro",
        "subsector": "Holdings",
        "default_category": "trimestral",
        "payout_target": 0.85,
        "description": "Holding de investimentos controlada pelo Bradesco com participação estratégica na Vale (VALE3). Repassa dividendos massivos de mineração aos acionistas."
    },

    # --- SEGUROS E PREVIDÊNCIA ---
    {
        "ticker": "BBSE3.SA",
        "ticker_clean": "BBSE3",
        "name": "BB Seguridade",
        "sector": "Financeiro",
        "subsector": "Seguros",
        "default_category": "crescimento",
        "payout_target": 0.85,
        "description": "Líder em seguros rurais e previdência, modelo asset-light com ROE superior a 50%, payout próximo a 80-90% e alto potencial de crescimento."
    },
    {
        "ticker": "CXSE3.SA",
        "ticker_clean": "CXSE3",
        "name": "Caixa Seguridade",
        "sector": "Financeiro",
        "subsector": "Seguros",
        "default_category": "trimestral",
        "payout_target": 0.90,
        "description": "Braço segurador da Caixa Econômica Federal. Forte geração de caixa livre, distribuição trimestral e payout elevado."
    },
    {
        "ticker": "PSSA3.SA",
        "ticker_clean": "PSSA3",
        "name": "Porto Seguro",
        "sector": "Financeiro",
        "subsector": "Seguros",
        "default_category": "crescimento",
        "payout_target": 0.50,
        "description": "Líder em seguro de automóveis e serviços residenciais/saúde. Alta solidez patrimonial e histórico consistente de proventos."
    },

    # --- ENERGIA ELÉTRICA (TRANSMISSÃO E GERAÇÃO) ---
    {
        "ticker": "TAEE11.SA",
        "ticker_clean": "TAEE11",
        "name": "Taesa",
        "sector": "Utilidade Pública",
        "subsector": "Energia Elétrica / Transmissão",
        "default_category": "trimestral",
        "payout_target": 0.75,
        "description": "Uma das maiores transmissoras do país com receitas previsíveis reajustadas por IPCA/IGP-M. Distribuição trimestral clássica para dividendos."
    },
    {
        "ticker": "TRPL4.SA",
        "ticker_clean": "TRPL4",
        "name": "ISA Cteep",
        "sector": "Utilidade Pública",
        "subsector": "Energia Elétrica / Transmissão",
        "default_category": "bimestral",
        "payout_target": 0.75,
        "description": "Responsável por grande parte da transmissão de energia em SP e no Brasil. Fluxo de caixa protegido pela RBSE e frequente remuneração."
    },
    {
        "ticker": "EGIE3.SA",
        "ticker_clean": "EGIE3",
        "name": "Engie Brasil",
        "sector": "Utilidade Pública",
        "subsector": "Energia Elétrica / Geração",
        "default_category": "crescimento",
        "payout_target": 0.55,
        "description": "Maior geradora privada de energia 100% renovável do Brasil. Excelente governança, expansão de capacidade e dividendos de alto nível."
    },
    {
        "ticker": "CPLE6.SA",
        "ticker_clean": "CPLE6",
        "name": "Copel",
        "sector": "Utilidade Pública",
        "subsector": "Energia Elétrica",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": "Companhia Paranaense de Energia recém-privatizada. Ganho expressivo de eficiência, desalavancagem e política de dividendos atrativa."
    },
    {
        "ticker": "CMIG4.SA",
        "ticker_clean": "CMIG4",
        "name": "Cemig",
        "sector": "Utilidade Pública",
        "subsector": "Energia Elétrica",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": "Companhia Energética de Minas Gerais, grande geradora e distribuidora com yields tradicionalmente elevados de dois dígitos."
    },
    {
        "ticker": "EQTL3.SA",
        "ticker_clean": "EQTL3",
        "name": "Equatorial Energia",
        "sector": "Utilidade Pública",
        "subsector": "Energia / Distribuição e Saneamento",
        "default_category": "crescimento",
        "payout_target": 0.30,
        "description": "Consagrada pela disciplina na alocação de capital e turnaround operacional. Forte crescimento patrimonial com proventos crescentes."
    },

    # --- SANEAMENTO E UTILIDADES ---
    {
        "ticker": "SAPR11.SA",
        "ticker_clean": "SAPR11",
        "name": "Sanepar Unit",
        "sector": "Utilidade Pública",
        "subsector": "Saneamento",
        "default_category": "bimestral",
        "payout_target": 0.40,
        "description": "Companhia de saneamento do Paraná com múltiplos atrativos de P/L e P/VP abaixo do valor patrimonial, remunerando via JCP."
    },
    {
        "ticker": "SAPR4.SA",
        "ticker_clean": "SAPR4",
        "name": "Sanepar PN",
        "sector": "Utilidade Pública",
        "subsector": "Saneamento",
        "default_category": "bimestral",
        "payout_target": 0.40,
        "description": "Ações preferenciais da Sanepar negociando abaixo de R$ 6,00, com dividend yield superior a 7,5% e desconto patrimonial expressivo."
    },
    {
        "ticker": "CSMG3.SA",
        "ticker_clean": "CSMG3",
        "name": "Copasa",
        "sector": "Utilidade Pública",
        "subsector": "Saneamento",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": "Companhia de saneamento de MG, política formal de payout de 50% dos lucros com proventos trimestrais bem regulares."
    },

    # --- TELECOMUNICAÇÕES ---
    {
        "ticker": "VIVT3.SA",
        "ticker_clean": "VIVT3",
        "name": "Telefônica Brasil (Vivo)",
        "sector": "Comunicações",
        "subsector": "Telecomunicações",
        "default_category": "trimestral",
        "payout_target": 0.80,
        "description": "Líder em telefonia móvel e fibra óptica no Brasil. Excelente geração de caixa livre, programa massivo de recompra e dividendos/JCP."
    },
    {
        "ticker": "TIMS3.SA",
        "ticker_clean": "TIMS3",
        "name": "TIM Brasil",
        "sector": "Comunicações",
        "subsector": "Telecomunicações",
        "default_category": "trimestral",
        "payout_target": 0.70,
        "description": "Forte expansão no 5G e pós-pago, rentabilidade crescente e compromisso público de distribuição agressiva de proventos aos acionistas."
    },

    # --- PAPEL, CELULOSE & MATERIAIS BÁSICOS ---
    {
        "ticker": "KLBN11.SA",
        "ticker_clean": "KLBN11",
        "name": "Klabin Unit",
        "sector": "Materiais Básicos",
        "subsector": "Papel e Celulose / Embalagens",
        "default_category": "trimestral",
        "payout_target": 0.20,
        "description": "Maior produtora e exportadora de papéis para embalagens do Brasil, política formal de dividendos atrelada ao EBITDA desalavancado."
    },
    {
        "ticker": "KLBN4.SA",
        "ticker_clean": "KLBN4",
        "name": "Klabin PN",
        "sector": "Materiais Básicos",
        "subsector": "Papel e Celulose / Embalagens",
        "default_category": "trimestral",
        "payout_target": 0.20,
        "description": "Ações preferenciais da Klabin cotadas abaixo de R$ 5,00, excelente veículo de acumulação com proventos trimestrais consistentes."
    },
    {
        "ticker": "RANI3.SA",
        "ticker_clean": "RANI3",
        "name": "Irani Papel e Embalagens",
        "sector": "Materiais Básicos",
        "subsector": "Papel e Embalagens",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": "Empresa líder em embalagens sustentáveis de papelão ondulado, cotada abaixo de R$ 10,00, com ROE elevado e política de payout de 50% trimestral."
    },
    {
        "ticker": "CMIG3.SA",
        "ticker_clean": "CMIG3",
        "name": "Cemig ON",
        "sector": "Utilidade Pública",
        "subsector": "Energia Elétrica",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": "Ações ordinárias da Cemig negociadas abaixo de R$ 10,00 com direito a voto e histórico robusto de dividend yield de dois dígitos."
    },
    {
        "ticker": "SUZB3.SA",
        "ticker_clean": "SUZB3",
        "name": "Suzano",
        "sector": "Materiais Básicos",
        "subsector": "Papel e Celulose",
        "default_category": "crescimento",
        "payout_target": 0.25,
        "description": "Maior produtora global de celulose de eucalipto, baixo custo de caixa, alta geração e forte potencial de valorização em dólar."
    },

    # --- COMMODITIES, SIDERURGIA & PETRÓLEO ---
    {
        "ticker": "PETR4.SA",
        "ticker_clean": "PETR4",
        "name": "Petrobras PN",
        "sector": "Petróleo e Gás",
        "subsector": "Exploração e Refino",
        "default_category": "trimestral",
        "payout_target": 0.45,
        "description": "Gigante do pré-sal brasileiro com custo de extração ultracompetitivo e política de proventos trimestrais atrelada ao fluxo de caixa livre."
    },
    {
        "ticker": "VALE3.SA",
        "ticker_clean": "VALE3",
        "name": "Vale",
        "sector": "Materiais Básicos",
        "subsector": "Mineração",
        "default_category": "trimestral",
        "payout_target": 0.50,
        "description": "Uma das maiores mineradoras de minério de ferro de alto teor e níquel do mundo, política de proventos baseada em geração de caixa."
    },
    {
        "ticker": "GGBR4.SA",
        "ticker_clean": "GGBR4",
        "name": "Gerdau",
        "sector": "Materiais Básicos",
        "subsector": "Siderurgia",
        "default_category": "trimestral",
        "payout_target": 0.30,
        "description": "Multinacional brasileira de aços longos com forte presença nos EUA e Brasil, histórico disciplinado de dividendos e recompras."
    },
    {
        "ticker": "CSNA3.SA",
        "ticker_clean": "CSNA3",
        "name": "CSN (Siderúrgica Nacional)",
        "sector": "Materiais Básicos",
        "subsector": "Siderurgia e Mineração",
        "default_category": "trimestral",
        "payout_target": 0.40,
        "description": "Um dos maiores conglomerados siderúrgicos e de mineração do Brasil, forte histórico de proventos e dividend yield em momentos de ciclo de alta."
    },
    {
        "ticker": "VBBR3.SA",
        "ticker_clean": "VBBR3",
        "name": "Vibra Energia",
        "sector": "Petróleo e Gás",
        "subsector": "Distribuição de Combustíveis",
        "default_category": "crescimento",
        "payout_target": 0.40,
        "description": "Líder na distribuição de combustíveis no Brasil (postos Petrobras), expansão em renováveis e margens crescentes."
    },

    # --- POTENCIAL DE CRESCIMENTO & EXCELÊNCIA OPERACIONAL ---
    {
        "ticker": "WEGE3.SA",
        "ticker_clean": "WEGE3",
        "name": "WEG",
        "sector": "Bens Industriais",
        "subsector": "Equipamentos Elétricos e Motores",
        "default_category": "crescimento",
        "payout_target": 0.50,
        "description": "Referência global em eficiência energética, ROE acima de 25-30%, crescimento constante de lucros e proventos reinvestidos."
    },
    {
        "ticker": "PRIO3.SA",
        "ticker_clean": "PRIO3",
        "name": "PRIO (PetroRio)",
        "sector": "Petróleo e Gás",
        "subsector": "Exploração e Produção",
        "default_category": "crescimento",
        "payout_target": 0.20,
        "description": "Maior produtora independente de óleo e gás do Brasil, crescimento acelerado de produção, com expansão de capacidade de distribuição."
    },
    {
        "ticker": "RADL3.SA",
        "ticker_clean": "RADL3",
        "name": "Raia Drogasil",
        "sector": "Consumo Não Cíclico",
        "subsector": "Comércio Farmacêutico",
        "default_category": "crescimento",
        "payout_target": 0.35,
        "description": "Líder indiscutível no varejo farmacêutico nacional, expansão contínua de lojas, ROE elevado e remuneração constante via JCP."
    }
]

def get_all_tickers() -> List[str]:
    """Retorna lista de todos os tickers com sufixo .SA da B3."""
    return [item["ticker"] for item in B3_DIVIDEND_UNIVERSE]

def get_universe_map() -> Dict[str, Dict[str, Any]]:
    """Retorna dicionário indexado pelo ticker puro ou com .SA."""
    mapping = {}
    for item in B3_DIVIDEND_UNIVERSE:
        mapping[item["ticker"]] = item
        mapping[item["ticker_clean"]] = item
    return mapping
