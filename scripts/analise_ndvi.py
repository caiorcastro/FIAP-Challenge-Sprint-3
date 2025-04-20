"""
Script para análise do NDVI suavizado (Savitzky-Golay) para Sidrolândia-MS.
Este script realiza:
1. Leitura dos dados NDVI do arquivo Excel
2. Visualização do NDVI suavizado ao longo do tempo
3. Cálculo do NDVI médio por ano

Vantagem do filtro Savitzky-Golay: plt.savefig('../resultados/ndvi_serie_temporal.png'), removendo ruídos e facilitando a identificação de padrões reais do ciclo da cultura.
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. Leitura dos dados NDVI do arquivo Excel
arquivo_ndvi = '../../dados_brutos/NDVI/satveg_NDVI_EVI_combinado.xlsx'
arquivo_ndvi = '../dados_brutos/NDVI/satveg_NDVI_EVI_combinado.xlsx'
df = pd.read_excel(arquivo_ndvi)

# Exibe as primeiras linhas para conferência
df_head = df[['Data', 'Savitzky-Golay', 'Ano']].head()
print('Primeiras linhas do NDVI suavizado:')
print(df_head)

# 2. Visualização do NDVI suavizado ao longo do tempo
plt.figure(figsize=(12, 5))
plt.plot(pd.to_datetime(df['Data'], dayfirst=True), df['Savitzky-Golay'], label='NDVI Suavizado (Golay)', color='green')
plt.xlabel('Data')
plt.ylabel('NDVI Suavizado')
plt.title('NDVI Suavizado (Savitzky-Golay) ao longo do tempo')
plt.legend()
plt.tight_layout()
plt.show()

# 3. Cálculo do NDVI médio por ano
df_ano = df.groupby('Ano')['Savitzky-Golay'].mean().reset_index()
print('\nNDVI médio por ano:')
print(df_ano)

# 4. (Opcional) Salvar resultados em CSV para uso posterior
df_ano.to_csv('../dados_processados/ndvi_medio_por_ano.csv', index=False)
print('\nArquivo ndvi_medio_por_ano.csv salvo com sucesso.')
