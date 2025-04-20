"""
Script para análise exploratória dos dados climáticos do INMET para Sidrolândia-MS.
Gera estatísticas anuais e mensais de precipitação, temperatura e outras variáveis,
salva tabelas tratadas e gráficos para integração com NDVI e produtividade.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caminho do arquivo INMET
df = pd.read_excel('../dados_brutos/INMET/sidrolandia_inmet_combinado.xlsx')

# Identificar automaticamente as colunas principais (precipitação, temperatura, umidade)
def get_col_by_keyword(df, keywords):
    for col in df.columns:
        for kw in keywords:
            if kw.lower() in col.lower():
                return col
    return None

col_precip = get_col_by_keyword(df, ['precip'])
col_temp = get_col_by_keyword(df, ['bulbo seco', 'temperatura do ar'])
col_umid = get_col_by_keyword(df, ['umidade relativa'])

# Padronizar nomes para o resto do script
if col_precip:
    df = df.rename(columns={col_precip: 'Precipitacao (mm)'})
if col_temp:
    df = df.rename(columns={col_temp: 'Temp (C)'})
if col_umid:
    df = df.rename(columns={col_umid: 'Umidade (%)'})

# Converter Data para datetime
if not pd.api.types.is_datetime64_any_dtype(df['Data']):
    df['Data'] = pd.to_datetime(df['Data'])

# Adicionar colunas Ano/Mes
if 'Ano' not in df:
    df['Ano'] = df['Data'].dt.year
if 'Mes' not in df:
    df['Mes'] = df['Data'].dt.month

# --- Estatísticas anuais ---
clima_anual = df.groupby('Ano').agg({
    'Precipitacao (mm)': 'sum',
    'Temp (C)': 'mean',
    'Umidade (%)': 'mean'
}).reset_index()
clima_anual.columns = ['Ano', 'Precipitacao_total_mm', 'Temp_media_C', 'Umidade_media']
clima_anual.to_csv('../dados_processados/inmet_clima_anual.csv', index=False)

# --- Estatísticas mensais ---
clima_mensal = df.groupby(['Ano', 'Mes']).agg({
    'Precipitacao (mm)': 'sum',
    'Temp (C)': 'mean',
    'Umidade (%)': 'mean'
}).reset_index()
clima_mensal.columns = ['Ano', 'Mes', 'Precipitacao_total_mm', 'Temp_media_C', 'Umidade_media']
clima_mensal.to_csv('../dados_processados/inmet_clima_mensal.csv', index=False)

# --- Gráficos anuais ---
os.makedirs('../resultados', exist_ok=True)
plt.figure(figsize=(8,5))
plt.bar(clima_anual['Ano'], clima_anual['Precipitacao_total_mm'], color='royalblue')
plt.title('Precipitação Total Anual (mm) - Sidrolândia-MS')
plt.ylabel('mm')
plt.xlabel('Ano')
plt.tight_layout()
plt.savefig('../resultados/inmet_precipitacao_anual.png')
plt.close()

plt.figure(figsize=(8,5))
plt.plot(clima_anual['Ano'], clima_anual['Temp_media_C'], marker='o', color='tomato')
plt.title('Temperatura Média Anual (°C) - Sidrolândia-MS')
plt.ylabel('°C')
plt.xlabel('Ano')
plt.tight_layout()
plt.savefig('../resultados/inmet_temp_media_anual.png')
plt.close()

# --- Gráficos mensais (média por mês ao longo dos anos) ---
plt.figure(figsize=(10,5))
sns.boxplot(x='Mes', y='Precipitacao_total_mm', data=clima_mensal, color='royalblue')
plt.title('Distribuição Mensal da Precipitação (mm)')
plt.ylabel('mm')
plt.xlabel('Mês')
plt.tight_layout()
plt.savefig('../resultados/inmet_precipitacao_mensal_boxplot.png')
plt.close()

plt.figure(figsize=(10,5))
sns.boxplot(x='Mes', y='Temp_media_C', data=clima_mensal, color='tomato')
plt.title('Distribuição Mensal da Temperatura Média (°C)')
plt.ylabel('°C')
plt.xlabel('Mês')
plt.tight_layout()
plt.savefig('../resultados/inmet_temp_media_mensal_boxplot.png')
plt.close()

print('Análises climáticas anuais e mensais salvas em dados_processados/ e resultados/.')
