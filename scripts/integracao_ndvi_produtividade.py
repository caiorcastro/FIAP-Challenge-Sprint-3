"""
Script para integrar NDVI médio anual (suavizado) com produtividade do milho.
Passos:
1. Leitura do NDVI médio por ano (arquivo gerado anteriormente)
2. Leitura dos dados de produtividade do milho
3. Junção dos dados por ano
4. Visualização da relação NDVI x Produtividade
5. Salvamento do dataset integrado para modelagem

Vantagem: Essa integração permite analisar a correlação entre o vigor vegetativo (NDVI) e a produtividade agrícola, baseando a modelagem preditiva em dados reais.
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. Leitura do NDVI médio por ano
df_ndvi = pd.read_csv('../dados_processados/ndvi_medio_por_ano.csv')
print('NDVI médio por ano:')
print(df_ndvi.tail())

# 2. Leitura dos dados de produtividade do milho
df_prod = pd.read_csv('../dados_processados/Produtividade_Milho_-_Sidrolandia.csv')
print('\nProdutividade do milho:')
print(df_prod.head())

# 3. Junção dos dados por ano
df_merged = pd.merge(df_prod, df_ndvi, left_on='Ano', right_on='Ano', how='inner')
print('\nDataset integrado NDVI + Produtividade:')
print(df_merged)

# 4. Visualização da relação NDVI x Produtividade
plt.figure(figsize=(8,5))
plt.scatter(df_merged['Savitzky-Golay'], df_merged['Produtividade (ton/ha)'], color='blue')
plt.xlabel('NDVI Médio Anual (Savitzky-Golay)')
plt.ylabel('Produtividade do Milho (ton/ha)')
plt.title('Relação NDVI Médio Anual x Produtividade do Milho')
plt.grid(True)
plt.tight_layout()
plt.savefig('./resultados/ndvi_vs_produtividade.png')
plt.show()

# 5. Salvar dataset integrado
arquivo_saida = './dados_processados/dataset_integrado_ndvi_produtividade.csv'
df_merged.to_csv(arquivo_saida, index=False)
print(f'\nArquivo {arquivo_saida} salvo com sucesso.')
