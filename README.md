# 📈 B3 Dividend Radar - Plataforma de Recomendação de Ações de Dividendos

Uma plataforma completa em Python com **interface executiva inspirada no Power BI** para triagem, recomendação e análise fundamentalista de ações pagadoras de dividendos da **B3 (Bolsa de Valores Brasileira)**.

---

## 🎯 Categorias de Ações Contempladas

1. 🚀 **Ações com Potencial de Crescimento (+ Dividendos)**: Empresas com alto ROE (>14%), expansão contínua de receita/lucro líquido, baixo endividamento e histórico crescente de proventos por ação (CAGR de dividendos). Exemplos: `BBSE3`, `EGIE3`, `WEGE3`, `EQTL3`, `CXSE3`, `PSSA3`, `SUZB3`.
2. 🗓️ **Ações com Dividendos Mensais**: Ativos que remuneram seus acionistas em praticamente todos os meses do ano via Dividendos e Juros sobre Capital Próprio (JCP), ideais para fluxo de caixa constante. Exemplos: `ITUB4` (Itaú), `BBDC4` (Bradesco), `BEES3` (Banestes).
3. ⏳ **Ações com Dividendos Bimestrais**: Ativos com ciclo de distribuição frequente (~5 a 8 pagamentos anuais), intercalando proventos para o investidor. Exemplos: `TRPL4` (ISA Cteep), `SAPR11` (Sanepar).
4. 📊 **Ações com Dividendos Trimestrais**: Companhias sólidas e maduras com políticas estruturadas de proventos a cada 3 meses. Exemplos: `BBAS3` (Banco do Brasil), `TAEE11` (Taesa), `ITSA4` (Itaúsa), `CMIG4` (Cemig), `CPLE6` (Copel), `VIVT3` (Telefônica Brasil), `CSMG3` (Copasa), `VALE3`, `PETR4`.

---

## 🧠 Metodologia e Funcionalidades

- **Avaliação de Dados Reais da B3**:
  - Coleta automática de cotações, múltiplos fundamentalistas (P/L, P/VP, ROE, Margem Líquida, Dívida Líquida/EBITDA, Payout) e histórico de proventos via `yfinance`.
  - **Preço Teto de Décio Bazin**: $Preço\_Teto = \frac{DPA\_Médio}{0,06}$ (Yield alvo de 6% a.a.) com cálculo da Margem de Segurança.
  - **Valor Justo de Benjamin Graham**: $V_{Graham} = \sqrt{22,5 \times LPA \times VPA}$.
- **Análise de Notícias Reais & Sentimento em PT-BR**:
  - Feed em tempo real via **Google News RSS Brasil** e portais financeiros (InfoMoney, Valor Econômico, Exame, Seu Dinheiro, Money Times).
  - Algoritmo de sentimento financeiro calibrado para o mercado brasileiro, diagnosticando o impacto nos proventos futuros (Positivo, Neutro, Cautela, Negativo).
- **Motor de Recomendação Multicritério**:
  - Pontuação ponderada de 0 a 100 pontos: Valuation e Yield (35%), Rentabilidade e ROE (25%), Solvência e Payout (20%) e Notícias B3 (20%).
  - Badges claras de veredito: `🏆 Oportunidade Forte`, `✅ Compra Atrativa`, `⚖️ Manter / Acompanhar`, `⚠️ Cautela`.
- **Interface Executiva Estilo Power BI**:
  - Paleta Slate Dark executiva corporativa.
  - Cartões KPI com indicadores de variação e tendências.
  - Slicers/Filtros interativos por setor, yield mínimo, score e preço teto.
  - Matriz de dados com formatação condicional (heatmaps de cores).
  - Gráfico de dispersão e quadrantes (Dividend Yield vs ROE).
  - Radar multicritério comparando a ação selecionada vs Média Setorial da B3.
  - Calendário anual de fluxo de caixa mensal.
  - Simulador de independência financeira e renda passiva.

---

## 📁 Estrutura do Projeto

```
b3_dividend_radar/
├── app.py                     # Ponto de entrada do Dashboard Streamlit (Power BI Style)
├── test_engine.py             # Script de teste e validação de todos os módulos
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação do projeto
└── src/
    ├── data/
    │   ├── b3_universe.py     # Catálogo de ações líquidas e pagadoras da B3
    │   ├── market_data.py     # Coletor de dados da B3, múltiplos e Bazin/Graham
    │   └── dividend_engine.py # Classificador de periodicidade (Mensal/Bimestral/Trimestral)
    ├── news/
    │   ├── news_collector.py  # Coletor de notícias ao vivo (Google News & Yahoo)
    │   └── sentiment_analyzer.py # Analisador de sentimento financeiro PT-BR
    ├── engine/
    │   └── recommender.py     # Motor de pontuação e ranking de recomendação
    └── ui/
        ├── powerbi_theme.py   # CSS executivo e paleta Power BI
        └── components.py      # Componentes e gráficos Plotly customizados
```

---

## 🚀 Como Instalar e Executar

### 1. Criar e Ativar Ambiente Virtual (Recomendado)
No terminal Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar Dependências
```powershell
pip install -r requirements.txt
```

### 3. Executar Testes de Validação
```powershell
python test_engine.py
```

### 4. Iniciar a Aplicação (Dashboard Estilo Power BI)
```powershell
streamlit run app.py
```
A aplicação será aberta automaticamente no seu navegador padrão em: `http://localhost:8501`.
