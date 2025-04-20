"""
Script para extrair dados de milho de Sidrolândia-MS do arquivo IBGE/SIDRA.
Lê as abas 'Área plantada', 'Área colhida' e 'Quantidade produzida',
filtra os dados de Sidrolândia-MS e monta um DataFrame consolidado.

Vantagens:
- Extração automática e consistente dos dados para vários anos
- Pronto para integração com NDVI e modelagem
"""

"""
Script para extrair dados de milho de Sidrolândia-MS do arquivo IBGE/SIDRA.
Lê as abas 'Área plantada', 'Área colhida' e 'Quantidade produzida',
filtra os dados de Sidrolândia-MS e monta um DataFrame consolidado para os anos 2020-2023.

Vantagens:
- Extração automática e consistente dos dados para vários anos
- Pronto para integração com NDVI e modelagem
"""

import pandas as pd

# Nome do arquivo Excel
arquivo_ibge = '../dados_brutos/IBGE/SIDRA-IBGE-Producao-Municipal-Tabela-1612.xlsx'
anos = [2020, 2021, 2022, 2023]
colunas_milho = ['Milho (em grão)', 'Milho (em grão).1', 'Milho (em grão).2', 'Milho (em grão).3']

# Função para extrair dados de milho para Sidrolândia (MS) de uma aba
def extrair_milho_aba(nome_aba):
    # Lê a aba pulando 4 linhas para pegar o cabeçalho correto
    df = pd.read_excel(arquivo_ibge, sheet_name=nome_aba, skiprows=4)
    # Filtra Sidrolândia (MS)
    linha = df[df['Unnamed: 0'].str.contains('Sidrolândia', na=False)].iloc[0]
    # Extrai os valores de milho para cada ano
    valores = [linha[col] for col in colunas_milho]
    return valores

# Extrai dados de cada aba
dados_area_plantada = extrair_milho_aba('Área plantada')
dados_area_colhida = extrair_milho_aba('Área colhida')
dados_producao = extrair_milho_aba('Quantidade produzida')

# Monta DataFrame consolidado
df_final = pd.DataFrame({
    'Ano': anos,
    'Área Plantada (ha)': dados_area_plantada,
    'Área Colhida (ha)': dados_area_colhida,
    'Produção (ton)': dados_producao
})

# Calcula produtividade (ton/ha)
df_final['Produtividade (ton/ha)'] = df_final['Produção (ton)'] / df_final['Área Plantada (ha)']

print('Dados consolidados de milho para Sidrolândia-MS:')
print(df_final)

# Salva CSV limpo
df_final.to_csv('../dados_processados/Produtividade_Milho_-_Sidrolandia.csv', index=False)
print('\nArquivo Produtividade_Milho_-_Sidrolandia.csv salvo com sucesso.')
