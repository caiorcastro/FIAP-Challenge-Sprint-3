"""
Análise estatística completa para validação do modelo de IA
Aplica testes de correlação de Pearson, Spearman e regressão linear
aos dados integrados de NDVI, clima e produtividade.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import statsmodels.api as sm
from statsmodels.formula.api import ols
import os

# Criar diretórios se não existirem
os.makedirs('../resultados', exist_ok=True)
os.makedirs('../dados_processados', exist_ok=True)

print("Iniciando análise estatística completa...")

# Carregar dados integrados
df_anual = pd.read_csv('../dados_processados/integrado_anual.csv')
df_mensal = pd.read_csv('../dados_processados/integrado_mensal.csv')

# 1. Análise de correlação de Pearson (paramétrica)
print("\n1. Calculando correlações de Pearson...")

# 1.1 Correlação anual
cols_anual = ['Produtividade (ton/ha)', 'Savitzky-Golay', 'Precipitacao_total_mm', 
             'Temp_media_C', 'Umidade_media']

# Matriz de correlação completa
corr_anual = df_anual[cols_anual].corr()
corr_anual.to_csv('../dados_processados/correlacao_pearson_anual.csv')

# Calculando p-valores para correlação de Pearson
p_values_anual = pd.DataFrame(np.zeros((len(cols_anual), len(cols_anual))), 
                             index=cols_anual, columns=cols_anual)

for i, col1 in enumerate(cols_anual):
    for j, col2 in enumerate(cols_anual):
        if i != j:
            corr, p_value = pearsonr(df_anual[col1], df_anual[col2])
            p_values_anual.loc[col1, col2] = p_value
        else:
            p_values_anual.loc[col1, col2] = 1.0

p_values_anual.to_csv('../dados_processados/correlacao_pearson_pvalores_anual.csv')

# 1.2 Correlação mensal (principais variáveis)
cols_mensal = ['NDVI_medio', 'Precipitacao_total_mm', 'Temp_media_C', 'Umidade_media']
corr_mensal = df_mensal[cols_mensal].corr()
corr_mensal.to_csv('../dados_processados/correlacao_pearson_mensal.csv')

# 2. Análise de correlação de Spearman (não-paramétrica)
print("\n2. Calculando correlações de Spearman...")

# 2.1 Correlação de Spearman anual
spearman_anual = df_anual[cols_anual].corr(method='spearman')
spearman_anual.to_csv('../dados_processados/correlacao_spearman_anual.csv')

# Calculando p-valores para correlação de Spearman
p_values_spearman = pd.DataFrame(np.zeros((len(cols_anual), len(cols_anual))), 
                                index=cols_anual, columns=cols_anual)

for i, col1 in enumerate(cols_anual):
    for j, col2 in enumerate(cols_anual):
        if i != j:
            corr, p_value = spearmanr(df_anual[col1], df_anual[col2])
            p_values_spearman.loc[col1, col2] = p_value
        else:
            p_values_spearman.loc[col1, col2] = 1.0

p_values_spearman.to_csv('../dados_processados/correlacao_spearman_pvalores_anual.csv')

# 3. Regressão linear simples (NDVI x Produtividade)
print("\n3. Executando regressão linear simples...")
X = df_anual['Savitzky-Golay']
y = df_anual['Produtividade (ton/ha)']
X = sm.add_constant(X)  # Adicionar constante (intercepto)

model = sm.OLS(y, X).fit()
predictions = model.predict(X)

# Salvar resultados da regressão
with open('../dados_processados/regressao_linear_simples.txt', 'w') as f:
    f.write(model.summary().as_text())

# Gráfico de dispersão com linha de regressão
plt.figure(figsize=(8, 6))
sns.regplot(x='Savitzky-Golay', y='Produtividade (ton/ha)', data=df_anual, 
           line_kws={"color": "red"})
plt.title(f'Regressão Linear: NDVI x Produtividade\nR² = {model.rsquared:.3f}, p = {model.pvalues[1]:.3f}')
plt.tight_layout()
plt.savefig('../resultados/regression.png', dpi=200)

# 4. Regressão múltipla (NDVI + Clima x Produtividade)
print("\n4. Executando regressão múltipla...")
formula = 'Produtividade (ton/ha) ~ Savitzky-Golay + Precipitacao_total_mm + Temp_media_C'
model_multi = ols(formula, data=df_anual).fit()

# Salvar resultados da regressão múltipla
with open('../dados_processados/regressao_multipla.txt', 'w') as f:
    f.write(model_multi.summary().as_text())

# 5. Matriz de correlação com valores de significância
print("\n5. Gerando matriz de correlação visual...")
plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_anual, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Plotar matriz de correlação
ax = sns.heatmap(
    corr_anual, 
    annot=True,
    mask=mask,
    cmap=cmap,
    vmax=1,
    vmin=-1,
    center=0,
    square=True,
    linewidths=.5,
    fmt=".2f"
)
plt.title('Matriz de Correlação (Pearson) - Dados Anuais')
plt.tight_layout()
plt.savefig('../resultados/corr_matrix.png', dpi=200)

# 6. Pairplot para visualização multivariada
print("\n6. Gerando pairplot...")
plt.figure(figsize=(12, 10))
sns.pairplot(df_anual[cols_anual], kind='reg', diag_kind='kde')
plt.tight_layout()
plt.savefig('../resultados/pairplot.png', dpi=200)

# 7. Série temporal de NDVI e produtividade
print("\n7. Gerando série temporal...")
plt.figure(figsize=(12, 6))
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Ano')
ax1.set_ylabel('Produtividade (ton/ha)', color=color)
ax1.plot(df_anual['Ano'], df_anual['Produtividade (ton/ha)'], marker='o', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('NDVI médio', color=color)
ax2.plot(df_anual['Ano'], df_anual['Savitzky-Golay'], marker='s', color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Série Temporal: NDVI e Produtividade')
plt.tight_layout()
plt.savefig('../resultados/time_series.png', dpi=200)

# 8. Análise de defasagem (lag) entre NDVI mensal e precipitação
print("\n8. Analisando defasagem (lag) temporal...")
# Preparando dados para análise de lag
df_mensal_sorted = df_mensal.sort_values(['Ano', 'Mes'])

# Criar coluna de precipitação defasada (1 mês)
df_mensal_sorted['Precipitacao_lag1'] = df_mensal_sorted['Precipitacao_total_mm'].shift(1)

# Calcular correlação com NDVI atual
lag_corr = pearsonr(
    df_mensal_sorted.iloc[1:]['NDVI_medio'], 
    df_mensal_sorted.iloc[1:]['Precipitacao_lag1']
)[0]

with open('../dados_processados/lag_analysis.txt', 'w') as f:
    f.write(f"Correlação entre NDVI e precipitação com lag de 1 mês: {lag_corr:.3f}\n")
    f.write("Esta análise indica quanto o NDVI atual responde à precipitação do mês anterior.")

print("\nAnálise estatística completa finalizada.")
print(f"Resultados salvos em '../dados_processados/' e '../resultados/'") 