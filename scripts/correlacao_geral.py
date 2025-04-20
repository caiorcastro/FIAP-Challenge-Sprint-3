"""
Script para gerar matrizes de correlação e gráficos entre NDVI, clima (INMET) e produtividade (IBGE),
tanto na granularidade anual quanto mensal.
Salva outputs em dados_processados/ e resultados/.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Correlação ANUAL ---
# Carregar dados processados
prod = pd.read_csv('../dados_processados/Produtividade_Milho_-_Sidrolandia.csv')
ndvi_ano = pd.read_csv('../dados_processados/ndvi_medio_por_ano.csv')
clima_ano = pd.read_csv('../dados_processados/inmet_clima_anual.csv')

# Juntar tudo por Ano
anual = prod.merge(ndvi_ano, on='Ano', how='inner')
anual = anual.merge(clima_ano, on='Ano', how='inner')
anual.to_csv('../dados_processados/integrado_anual.csv', index=False)

# Matriz de correlação anual
corr_anual = anual.corr(numeric_only=True)
corr_anual.to_csv('../dados_processados/correlacao_anual.csv')

plt.figure(figsize=(8,6))
sns.heatmap(corr_anual, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Matriz de Correlação Anual (NDVI, Clima, Produtividade)')
plt.tight_layout()
plt.savefig('../resultados/correlacao_anual_heatmap.png')
plt.close()

# --- Correlação MENSAL ---
ndvi_mensal = pd.read_csv('../dados_processados/ndvi_mensal.csv')
clima_mensal = pd.read_csv('../dados_processados/inmet_clima_mensal.csv')

# Juntar por Ano e Mes
mensal = ndvi_mensal.merge(clima_mensal, on=['Ano','Mes'], how='inner')
mensal.to_csv('../dados_processados/integrado_mensal.csv', index=False)

corr_mensal = mensal.corr(numeric_only=True)
corr_mensal.to_csv('../dados_processados/correlacao_mensal.csv')

plt.figure(figsize=(8,6))
sns.heatmap(corr_mensal, annot=True, cmap='viridis', fmt='.2f')
plt.title('Matriz de Correlação Mensal (NDVI, Clima)')
plt.tight_layout()
plt.savefig('../resultados/correlacao_mensal_heatmap.png')
plt.close()

print('Matrizes de correlação anual e mensal salvas em dados_processados/ e resultados/.')
