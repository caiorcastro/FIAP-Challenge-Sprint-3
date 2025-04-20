"""
Script para tratar o arquivo IBGE (SIDRA) e extrair os dados de milho para Sidrolândia-MS.
Passos:
1. Ler o arquivo Excel, pulando linhas descritivas.
2. Filtrar apenas a cultura 'Milho' e o município 'Sidrolândia'.
3. Selecionar e renomear as colunas essenciais: Ano, Produção, Área Plantada, Produtividade.
4. Salvar um CSV limpo para integração com NDVI.
"""

import pandas as pd

# 1. Ler o arquivo Excel (pular linhas descritivas)
arquivo_ibge = '../dados_brutos/IBGE/SIDRA-IBGE-Producao-Municipal-Tabela-1612.xlsx'
# Geralmente os dados começam após algumas linhas, vamos tentar pular as 4 primeiras linhas
df = pd.read_excel(arquivo_ibge, skiprows=4)

# 2. Exibir as primeiras linhas e colunas para entender o formato
df_head = df.head()
print('Primeiras linhas após pular cabeçalho:')
print(df_head)
print('\nColunas:')
print(df.columns)

# 3. Filtrar apenas Sidrolândia-MS e Milho
df_filtrado = df[(df['Unnamed: 1'] == 'Sidrolândia') & (df['Unnamed: 3'] == 'Milho (em grão)')]

# 4. Selecionar e renomear as colunas essenciais
# Supondo que as colunas de interesse sejam:
# 'Unnamed: 2' = Ano, 'Unnamed: 4' = Área Plantada, 'Unnamed: 5' = Área Colhida, 'Unnamed: 6' = Produção, 'Unnamed: 7' = Rendimento Médio

df_final = df_filtrado[['Unnamed: 2', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 7']].copy()
df_final.columns = ['Ano', 'Área Plantada', 'Produção', 'Produtividade (kg/ha)']

# 5. Converter produtividade para ton/ha (dividir por 1000)
df_final['Produtividade (ton/ha)'] = df_final['Produtividade (kg/ha)'] / 1000

# 6. Salvar CSV limpo
df_final[['Ano', 'Produção', 'Área Plantada', 'Produtividade (ton/ha)']].to_csv('Produtividade_Milho_-_Sidrolandia.csv', index=False)
print('\nArquivo Produtividade_Milho_-_Sidrolandia.csv salvo com sucesso.')
