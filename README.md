# 📈 B3 Dividend Radar — Plataforma Executiva de Recomendação e Gestão de Dividendos

Uma plataforma completa em Python com **interface executiva corporativa no estilo Power BI** para triagem, recomendação, valuation e gestão de carteira real de ações pagadoras de dividendos da **B3 (Bolsa de Valores Brasileira)**.

---

## 🔐 Acesso e Autenticação

A plataforma conta com uma tela de login segura com credenciais fixas configuradas para acesso rápido:

- **Usuário**: `admin` *(ou `investidor`)*
- **Senha**: `123` *(ou `admin123` / `b3dividendos`)*
- **Recursos de Sessão**: Controle de acesso por estado (`st.session_state`), exibição de perfil ativo e botão de encerramento de sessão (**Logout**) na barra lateral.

---

## 💼 Módulo "Minha Carteira" & Gestão de Posições Reais

Painel completo para o investidor acompanhar seus ativos em custódia e rentabilidade em tempo real:

1. **Cadastro e Histórico de Transações**:
   - Registro de compras e aportes (Ticker, Data, Quantidade, Preço Unitário e Notas).
   - Persistência local segura em JSON (`data/portfolio_transactions.json`).
   - Opção de edição e exclusão de lançamentos com atualização instantânea.
2. **KPIs Consolidados da Carteira**:
   - 💵 **Total Investido**: Custo total de aquisição acumulado.
   - 💎 **Patrimônio Atual (Real)**: Valor de mercado com cotação ao vivo da B3.
   - 📈 **Lucro / Prejuízo**: Ganho nominal e rentabilidade percentual (+/- %).
   - 💰 **Proventos Anuais Estimados**: Estimativa anual e renda passiva mensal média.
3. **📊 Gráfico "Histórico: Dividendos" Mensal em Barras**:
   - Gráfico de barras verticais verde esmeralda com **valores monetários formatados no topo de cada barra (`R$ XX,XX`)**.
   - Seletor de período interativo (*Últimos 6 Meses, 12 Meses ou Ano Atual*).
   - Linha e legenda para **Meta Mensal de Proventos** configurável (ex.: `Meta 2.000`).
   - Métricas no rodapé: **Média mensal do período** e **Total no período (R$)** consolidado.
   - Expansor com detalhamento dos ativos e valores pagos mês a mês.
4. **Gráficos Executivos de Alocação e Desempenho**:
   - 🍩 Gráfico Pizza/Donut de **Distribuição do Valor Investido de Compra**.
   - 🍩 Gráfico Pizza/Donut de **Distribuição do Valor Real Atualizado (B3)**.
   - 📊 Gráfico de Barras Verticais de **Lucro/Prejuízo por Ativo** (Verde para lucro / Vermelho para perda).
   - 📋 Tabela detalhada de custódia com preços médios, cotações atuais, DY e pesos na carteira.

---

## 🚨 Sistema de Alertas Preditivos da Carteira

- 🔔 **Alertas de Proventos do Mês**: Monitor preditivo em tempo real que identifica quais ações da carteira pagam no mês selecionado (com seletor interativo de Janeiro a Dezembro) e calcula a previsão exata de valor a receber.
- 🔻 **Alertas de Ações Abaixo do Preço Médio (Preço < PM)**: Diagnóstico automático de ativos em custódia com desconto em relação ao custo pago, avaliando se a queda configura oportunidade de aporte com base no **Preço Teto de Bazin** e **Valor Justo de Graham**.

---

## 🏆 Os 4 Grandes Rankings da B3

Módulo de classificação com 4 pilares de análise:

1. 🥇 **AS MAIORES OPORTUNIDADES**: As ações com maior potencial de crescimento em relação ao preço justo (maior margem de segurança entre Décio Bazin e Benjamin Graham).
2. 💰 **AS MAIORES PAGADORAS DE DIVIDENDOS**: Ranking decrescente das empresas com maior Dividend Yield (DY 12M) e proventos por ação (DPA).
3. 🚀 **AS QUE MAIS CRESCERAM**: Ações com maior taxa anualizada de crescimento de dividendos (CAGR 3 anos) e elevado retorno sobre o patrimônio líquido (ROE).
4. 🛡️ **AS QUE MENOS CRESCERAM**: Ações com múltiplos mais descontados da bolsa (menor P/L e menor P/VP para estratégias de *Value Investing* e repique).

---

## 🎯 Categorias de Periodicidade de Proventos

1. 🚀 **Ações com Potencial de Crescimento (+ Dividendos)**: Alto ROE (>14%), expansão contínua de lucros, baixo endividamento e proventos crescentes (`BBSE3`, `EGIE3`, `WEGE3`, `CXSE3`, `EQTL3`, `SUZB3`, `PSSA3`).
2. 🗓️ **Ações com Dividendos Mensais**: Proventos recorrentes em praticamente todos os meses do ano via Dividendos e JCP (`ITUB4`, `BBDC4`, `BEES3`, `BEES4`).
3. ⏳ **Ações com Dividendos Bimestrais**: Ciclo de distribuição frequente (~5 a 8 pagamentos anuais) intercalando proventos (`TRPL4`, `SAPR11`, `SAPR4`).
4. 📊 **Ações com Dividendos Trimestrais**: Companhias sólidas e maduras com políticas estruturadas a cada 3 meses (`BBAS3`, `TAEE11`, `ITSA4`, `CMIG4`, `CPLE6`, `VIVT3`, `CSMG3`, `ABCB4`, `BRSR6`, `BRAP4`, `CSNA3`, `VALE3`, `PETR4`).

---

## 💎 Módulos Estratégicos Especiais

- 💎 **Maiores Dividendos B3 em Tempo Real**: Ranking com filtros por número de ativos e tabela completa com múltiplos fundamentalistas.
- 🎯 **Detector de Ações < R$ 10**: Triagem de ações baratas de alta qualidade e com proventos atrativos para pequenos aportes.
- 📰 **Notícias Reais & Análise de Sentimento em PT-BR**: Feed em tempo real via Google News RSS Brasil e portais financeiros, com analisador léxico que prevê o impacto futuro nos dividendos.
- 💰 **Simulador de Renda Passiva**: Cálculo interativo do patrimônio e número de ações necessárias para atingir metas de renda passiva mensal.

---

## 🧠 Metodologia Fundamentalista

- **Décio Bazin**: $\text{Preço Teto} = \frac{\text{DPA Médio}}{0,06}$ (Yield alvo de 6% a.a.) com cálculo de margem de segurança.
- **Benjamin Graham**: $V_{\text{Graham}} = \sqrt{22,5 \times \text{LPA} \times \text{VPA}}$ com margem de segurança.
- **Score Multicritério (0 a 100)**: Valuation & Yield (35%), Rentabilidade & ROE (25%), Solvência & Payout (20%) e Sentimento de Notícias B3 (20%).

---

## 📁 Estrutura do Projeto

```
b3_dividend_radar/
├── app.py                     # Aplicação Principal Streamlit (Dark Slate Power BI)
├── test_engine.py             # Script de testes e validação de módulos
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação completa
├── data/
│   └── portfolio_transactions.json  # Persistência de transações da carteira
└── src/
    ├── data/
    │   ├── b3_universe.py     # Universo de 33+ ações monitoradas da B3
    │   ├── market_data.py     # Coletor de cotações, múltiplos e Bazin/Graham
    │   ├── dividend_engine.py # Motor de classificação de periodicidade
    │   └── portfolio_manager.py # Gestão de carteira, alertas e histórico mensal
    ├── news/
    │   ├── news_collector.py  # Coletor de notícias ao vivo
    │   └── sentiment_analyzer.py # Analisador de sentimento financeiro PT-BR
    ├── engine/
    │   └── recommender.py     # Motor de pontuação e ranking de recomendação
    └── ui/
        ├── powerbi_theme.py   # Tema Dark Slate e estilos CSS Power BI
        ├── components.py      # Componentes de mercado e rankings da B3
        └── portfolio_components.py # Componentes visuais e gráficos da carteira
```

---

## 🚀 Como Instalar e Executar

### 1. Clonar ou Abrir o Diretório
```powershell
cd C:\Users\Vinic\.gemini\antigravity\scratch\b3_dividend_radar
```

### 2. Ativar o Ambiente Virtual
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Instalar as Dependências
```powershell
pip install -r requirements.txt
```

### 4. Iniciar a Aplicação
```powershell
python -m streamlit run app.py
```
Acesse no seu navegador: `http://localhost:8501` e utilize o usuário `admin` e a senha `123`.
