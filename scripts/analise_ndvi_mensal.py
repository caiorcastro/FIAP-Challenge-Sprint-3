"""
Script para calcular NDVI médio mensal a partir dos dados brutos de satélite.
Salva tabela tratada e gráficos para integração com clima e produtividade.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caminho do arquivo NDVI
df = pd.read_excel('../dados_brutos/NDVI/satveg_NDVI_EVI_combinado.xlsx')

# Converter a coluna de data para datetime
if not pd.api.types.is_datetime64_any_dtype(df['Data']):
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)

# Extrair ano e mês
if 'Ano' not in df:
    df['Ano'] = df['Data'].dt.year
if 'Mes' not in df:
    df['Mes'] = df['Data'].dt.month

# Calcular NDVI médio mensal (usando Savitzky-Golay suavizado se existir, senão NDVI bruto)
col_ndvi = 'Savitzky-Golay' if 'Savitzky-Golay' in df.columns else 'NDVI'
ndvi_mensal = df.groupby(['Ano', 'Mes'])[col_ndvi].mean().reset_index()
ndvi_mensal.columns = ['Ano', 'Mes', 'NDVI_medio']
ndvi_mensal.to_csv('../dados_processados/ndvi_mensal.csv', index=False)

# Gráfico: NDVI médio mensal por ano
os.makedirs('../resultados', exist_ok=True)
plt.figure(figsize=(12,6))
for ano, grupo in ndvi_mensal.groupby('Ano'):
    plt.plot(grupo['Mes'], grupo['NDVI_medio'], marker='o', label=str(ano))
plt.title('NDVI Médio Mensal por Ano - Sidrolândia-MS')
plt.xlabel('Mês')
plt.ylabel('NDVI Médio (suavizado)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('../resultados/ndvi_mensal_por_ano.png')
plt.close()

# Boxplot NDVI mensal (todos os anos)
plt.figure(figsize=(10,5))
sns.boxplot(x='Mes', y='NDVI_medio', data=ndvi_mensal, color='green')
plt.title('Distribuição Mensal do NDVI Médio (Todos os Anos)')
plt.xlabel('Mês')
plt.ylabel('NDVI Médio')
plt.tight_layout()
plt.savefig('../resultados/ndvi_mensal_boxplot.png')
plt.close()

print('NDVI mensal salvo em dados_processados/ndvi_mensal.csv e gráficos em resultados/.')
