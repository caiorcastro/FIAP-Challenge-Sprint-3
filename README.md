# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="src/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
</p>

<br>

# 🌾 Challenge Ingredion - Sprint 3
## Validação do Modelo de IA com Dados Reais de Produtividade Agrícola

## Grupo 32

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/caiorcastro/">Caio Rodrigues Castro</a> 
- <a href="https://www.linkedin.com/in/celeste-leite-dos-santos-66352a24b/">Celeste Leite dos Santos</a> 
- <a href="https://www.linkedin.com/in/digitalmanagerfelipesoares/">Felipe Soares Nascimento</a>
- <a href="https://www.linkedin.com/in//">Wellington Nascimento de Brito</a>


## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/leonardoorabona/">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi Chiovato</a>

---

## 📜 Descrição

Nesta terceira e última Sprint do Challenge Ingredion, nosso objetivo foi validar o modelo de Inteligência Artificial desenvolvido na Sprint 2, correlacionando as previsões de produtividade baseadas em NDVI com dados reais históricos de produtividade agrícola obtidos de bases públicas.

O foco principal foi analisar a confiabilidade do modelo e identificar ajustes necessários para melhorar sua precisão. Realizamos uma análise estatística aprofundada para verificar a correlação entre o NDVI (Índice de Vegetação por Diferença Normalizada) e a produtividade real do milho em Sidrolândia-MS, aplicando métodos de correlação de Pearson, Spearman e regressão linear.

Coletamos dados históricos de produtividade de fontes como IBGE/SIDRA, CONAB, INMET e SATVeg, integrando informações de NDVI, clima (precipitação, temperatura, umidade) e produtividade agrícola. Os dados foram organizados, tratados e analisados para identificar padrões e relações estatísticas significativas.

Os resultados demonstraram uma correlação muito forte entre NDVI e produtividade (r = 0.93), confirmando que o índice de vegetação é um excelente preditor da produtividade agrícola. O modelo de regressão linear apresentou um coeficiente de determinação (R²) elevado, validando a abordagem utilizada nas sprints anteriores.

Além disso, implementamos um modelo de Random Forest que capturou relações não-lineares entre as variáveis, apresentando desempenho superior aos modelos lineares tradicionais, especialmente considerando o tamanho limitado da amostra (4 anos de dados).

Este projeto demonstra a aplicação prática de técnicas de ciência de dados e inteligência artificial no contexto do agronegócio, transformando dados brutos em insights estratégicos para tomada de decisão.

## 📊 Principais Resultados

### Análise Estatística
- **Correlação de Pearson (NDVI x Produtividade)**: r = 0.93 (muito forte)
- **Correlação de Spearman (NDVI x Produtividade)**: ρ = 0.90 (muito forte)
- **Regressão Linear**: R² = 0.86, indicando alta capacidade preditiva

### Modelo Random Forest
- **Métrica R²**: 0.74 (validação Leave-One-Out)
- **MAE**: 0.32 ton/ha
- **RMSE**: 0.41 ton/ha
- **Variáveis mais importantes**: NDVI e precipitação total

### Análise Temporal
- Identificação de períodos críticos de desenvolvimento da cultura
- Padrões sazonais claros nas séries temporais de NDVI
- Resposta do NDVI às variações climáticas mensais

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>dados_brutos</b>: Dados originais coletados das fontes públicas (IBGE, CONAB, NDVI, INMET).

- <b>dados_processados</b>: Dados tratados e integrados para análise e modelagem, incluindo:
  - Correlações anuais e mensais
  - Datasets integrados de NDVI e produtividade
  - Métricas e coeficientes dos modelos

- <b>scripts</b>: Scripts Python para tratamento, análise e integração dos dados, incluindo:
  - Extração e processamento de dados
  - Análise de NDVI e clima
  - Integração de dados
  - Modelagem preditiva

- <b>notebooks</b>: Notebooks Jupyter para visualização e documentação do processo analítico:
  - Análise exploratória
  - Modelagem de IA
  - Validação dos modelos

- <b>resultados</b>: Gráficos, tabelas e visualizações geradas durante a análise:
  - Matrizes de correlação
  - Gráficos de regressão
  - Séries temporais
  - Visualizações de importância de variáveis

- <b>README.md</b>: Guia e explicação geral sobre o projeto.

## 🔧 Como executar o código

### Pré-requisitos
- Python 3.8 ou superior
- Bibliotecas: pandas, numpy, matplotlib, seaborn, scikit-learn, scipy, statsmodels

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/challenge-ingredion-sprint3.git
cd challenge-ingredion-sprint3
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução
Para reproduzir a análise completa, execute os notebooks na seguinte ordem:

1. **Análise Exploratória**:
```bash
jupyter notebook notebooks/analise_exploratoria_modelagem.ipynb
```

2. **Modelagem e Validação**:
```bash
jupyter notebook notebooks/modelagem_produtividade_rf.ipynb
```

3. **Análise NDVI**:
```bash
jupyter notebook notebooks/analise_ndvi_agricola.ipynb
```

4. **Validação do Modelo**:
```bash
jupyter notebook notebooks/Sprint3_Analise_Validacao_Explicada.ipynb
```

Alternativamente, você pode executar os scripts individuais na pasta `scripts/` na seguinte ordem:
1. Scripts de extração e tratamento de dados (`extrair_milho_sidrolandia_ibge.py`, `tratar_ibge_milho.py`)
2. Scripts de análise NDVI e clima (`analise_ndvi.py`, `analise_ndvi_mensal.py`, `analise_inmet.py`)  
3. Scripts de integração de dados (`integracao_ndvi_produtividade.py`, `correlacao_geral.py`)
4. Scripts de modelagem e validação (`modelagem_preditiva.py`, `modelagem_produtividade_rf.py`, `validacao_modelos.py`, `rf_visualizacoes.py`)

## 📈 Modelo Random Forest: Explicação

O modelo Random Forest foi selecionado por sua robustez em cenários com:
- Pequeno conjunto de dados (apenas 4 anos de histórico)
- Potenciais relações não-lineares entre variáveis
- Necessidade de interpretabilidade dos resultados

A validação Leave-One-Out (LOO) foi implementada para maximizar o uso dos dados disponíveis, reduzindo o viés na avaliação do modelo. Esta técnica é ideal para conjuntos de dados pequenos, pois permite treinar em N-1 observações e testar em 1, repetindo o processo N vezes.

As visualizações geradas pelo modelo incluem:
- Comparação entre valores reais e preditos ao longo dos anos
- Gráficos de importância de variáveis
- Análise de resíduos

O modelo capturou bem a tendência geral da produtividade, com melhor desempenho nos anos 2022 e 2023, apresentando maior desvio em 2021 (possivelmente devido a condições atípicas não captadas pelas variáveis utilizadas).

## 🗃 Histórico de lançamentos

* 1.0.0 - 15/05/2025
    * Entrega final da Sprint 3
    * Validação completa do modelo com dados reais
    * Análise estatística e correlação
    * Relatório técnico detalhado

* 0.9.0 - 10/05/2025
    * Implementação dos modelos de IA (Random Forest)
    * Visualizações e análises comparativas
    * Integração de dados de múltiplas fontes
    * Análises de correlação e regressão
    * Coleta e tratamento inicial dos dados históricos
    * Estruturação do repositório

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
