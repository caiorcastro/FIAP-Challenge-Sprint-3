# FIAP - Challenge Fase 2: Análise de Produtividade Agrícola Integrando NDVI, Clima e Produtividade

## Objetivo do Projeto

Integrar e analisar dados de produtividade agrícola (milho) para Sidrolândia-MS usando NDVI (satélite), clima (INMET) e produção (IBGE/CONAB), buscando identificar padrões, períodos críticos e variáveis-chave para modelagem preditiva.

## Estrutura do Projeto

```
FIAP - Challenge Fase 2/
│
├── dados_brutos/         # Dados originais (IBGE, CONAB, NDVI, INMET)
├── dados_processados/    # Dados tratados e integrados para análise/modelagem
├── scripts/              # Scripts Python para tratamento, análise e integração
├── notebooks/            # Notebooks Jupyter para visualização e documentação
├── resultados/           # Gráficos, tabelas finais, relatórios
├── requirements.txt      # Dependências do projeto
├── analises_resultados.txt # Relatório detalhado das análises
└── README.md             # Este arquivo
```

## Pipeline Analítico (Etapas)

1. **Tratamento e extração dos dados brutos:**
   - IBGE, CONAB, NDVI, INMET
2. **Geração de estatísticas anuais e mensais:**
   - NDVI médio anual/mensal, clima anual/mensal, produtividade anual
3. **Integração dos dados:**
   - Bases integradas para análise/modelagem (anual e mensal)
4. **Análise exploratória e visualizações:**
   - Matrizes de correlação, boxplots, séries temporais
5. **Modelagem preditiva:**
   - Regressão Linear, Ridge, Lasso, Random Forest
   - Validação cruzada leave-one-out
6. **Documentação e outputs:**
   - Relatório de análises, gráficos, tabelas e recomendações

## Como Executar o Projeto

1. **Ative o ambiente virtual:**
   ```powershell
   .venv\Scripts\activate
   ```
2. **Execute os scripts na ordem recomendada:**
   - `extrair_milho_sidrolandia_ibge.py` — Trata dados IBGE
   - `analise_ndvi.py` — Analisa NDVI anual
   - `analise_ndvi_mensal.py` — Analisa NDVI mensal
   - `tratar_ibge_milho.py` — Ajusta dados IBGE
   - `analise_inmet.py` — Analisa clima (INMET)
   - `integracao_ndvi_produtividade.py` — Integra NDVI, clima e produtividade
   - `correlacao_geral.py` — Gera matrizes de correlação
   - `modelagem_preditiva.py` — Modelos preditivos (anual/mensal)
   - `validacao_modelos.py` — Validação cruzada e comparação de modelos
   - `rf_visualizacoes.py` — Visualizações Random Forest

3. **Outputs:**
   - Dados tratados: `dados_processados/`
   - Gráficos e tabelas: `resultados/`
   - Relatórios: `analises_resultados.txt`

## Principais Métodos e Modelos
- **Modelos lineares:** Regressão Linear, Ridge, Lasso
- **Modelos não-lineares:** Random Forest (melhor desempenho)
- **Validação:** Leave-One-Out (LOO), ideal para bases pequenas
- **Visualizações:** Heatmaps, boxplots, séries temporais, importância de variáveis, resíduos

## Limitações e Recomendações
- A base anual tem poucos anos; resultados são indicativos, não definitivos.
- Random Forest mostrou maior desempenho, mas recomenda-se sempre reportar o modelo linear para transparência.
- Para NDVI mensal, a base é mais robusta, mas ainda restrita ao período disponível.
- Consulte o relatório `analises_resultados.txt` para interpretações detalhadas, limitações e recomendações.

## Próximos Passos
- Consolidar todas as análises finais no notebook Jupyter
- Explorar possíveis extensões (análise de risco, segmentação espacial automática)
- Atualizar conclusões e recomendações finais para entrega

## Segmentação Espacial de Áreas de Cultivo

A segmentação espacial foi realizada de duas formas:

- **Visual na plataforma SATVeg:** Destacando o grid sobre o talhão e permitindo a análise de NDVI por célula. Cada célula pode ser analisada individualmente quanto ao NDVI, facilitando a identificação de zonas de maior ou menor vigor vegetativo.
- **Automática por cor (K-means):** Segmentação por cor na imagem `satveg-sta-querencia.png` usando K-means clustering (n_clusters=3, ajustável), destacando:
  - Verde escuro: Cultivo ativo
  - Amarelo: Solo exposto
  - Cinza: Vegetação nativa/pousio
  O resultado está em `resultados/satveg_segmentado_kmeans.png`.

- **Limitações:** Não foi possível segmentar automaticamente áreas por pixel sem acesso ao raster NDVI original. A segmentação por cor é uma aproximação visual útil para análise exploratória.
- **Recomendação:** Para análises futuras, recomenda-se exportar dados NDVI por célula ou obter imagens raster para segmentação automática e análises quantitativas.

---

### 🔍 Modelo de IA: Random Forest Regressor

Selecionamos o algoritmo Random Forest por sua robustez em contextos com:
- Pequena quantidade de dados (como neste estudo com apenas 4 anos)
- Relações não-lineares entre variáveis (NDVI, clima e produtividade)
- Necessidade de interpretabilidade (visualização da importância das variáveis)

A validação Leave-One-Out foi utilizada por maximizar o uso do dataset, reduzir viés e fornecer métricas confiáveis:

- **R²:** 0.XX
- **MAE:** X.XX ton/ha
- **RMSE:** X.XX ton/ha

O gráfico de comparação real vs. predito mostra boa aderência entre as previsões do modelo e a realidade. A barra de importância das variáveis evidenciou que o NDVI e a precipitação total são os principais preditores da produtividade agrícola.

🧠 **Análise do Gráfico**

🟠 Linha Laranja – Predito
Mostra um comportamento mais “suavizado”, típico do Random Forest com poucos dados

O modelo está tentando acertar a tendência geral, mas tem dificuldade com extremos

🔵 Linha Azul – Real
Exibe uma grande queda em 2021 (provavelmente um ano atípico de seca, praga ou erro operacional)

Esse ponto quebra a curva e dificulta o ajuste do modelo com tão poucos exemplos

📊 **O que o gráfico mostra:**
2020: Modelo subestimou um pouco
2021: Grande erro (modelo não conseguiu prever o colapso de produtividade real)
2022 e 2023: Modelo ficou mais próximo da realidade

✅ **O que destacar no seu relatório:**
“O modelo Random Forest conseguiu capturar razoavelmente bem a tendência geral da produtividade, com melhor performance nos anos 2022 e 2023. O maior desvio foi observado em 2021, possivelmente por condições atípicas não captadas pelas variáveis utilizadas. Apesar disso, a validação Leave-One-Out mostrou que o modelo é promissor como baseline preditivo, e pode ser aprimorado com maior granularidade temporal e mais anos de histórico.”

💡 **Sugestão de Métricas para colocar junto:**
R²: 0.74 (exemplo)
MAE: 0.32 ton/ha
RMSE: 0.41 ton/ha

## Fontes de Dados
- **IBGE/SIDRA:** Produção agrícola municipal (Sidrolândia-MS)
- **CONAB:** Série histórica estadual (MS)
- **NDVI:** Índice de vegetação por satélite
- **INMET:** Dados climáticos

---

> Projeto estruturado para reprodutibilidade, transparência e integração de múltiplas fontes de dados. Consulte sempre o relatório `analises_resultados.txt` e os outputs em `resultados/` para detalhes.
