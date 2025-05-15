"""
Visualizações avançadas para o modelo Random Forest
Script gera diversos gráficos para análise do modelo RF:
- Comparação real vs predito
- Importância das variáveis
- Análise de resíduos
- Distribuição dos erros
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import LeaveOneOut
import os

# Criar diretórios se não existirem
os.makedirs('../resultados', exist_ok=True)

# Carrega dados
df_anual = pd.read_csv('../dados_processados/integrado_anual.csv')
print("Dados carregados: ", df_anual.shape)

# Preparação dos dados
X = df_anual[['Savitzky-Golay', 'Precipitacao_total_mm', 'Temp_media_C', 'Umidade_media']]
y = df_anual['Produtividade (ton/ha)']

# Validação Leave-One-Out para Random Forest
loo = LeaveOneOut()
y_true, y_pred = [], []

for train_idx, test_idx in loo.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred.append(model.predict(X_test)[0])
    y_true.append(y_test.values[0])

# Métricas de avaliação
r2 = r2_score(y_true, y_pred)
mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))

print(f'Métricas do modelo Random Forest (validação Leave-One-Out):')
print(f'R²: {r2:.3f}')
print(f'MAE: {mae:.3f} ton/ha')
print(f'RMSE: {rmse:.3f} ton/ha')

# 1. Gráfico real vs predito
plt.figure(figsize=(10, 6))
plt.plot(df_anual['Ano'], y_true, 'o-', label='Real', color='blue', linewidth=2)
plt.plot(df_anual['Ano'], y_pred, 's--', label='Predito', color='orange', linewidth=2)
plt.xlabel('Ano')
plt.ylabel('Produtividade (ton/ha)')
plt.title(f'Produtividade Real vs Predita (Random Forest)\nR² = {r2:.2f}, MAE = {mae:.2f}, RMSE = {rmse:.2f}')
plt.legend()
plt.grid(True)
plt.xticks(df_anual['Ano'])
plt.tight_layout()
plt.savefig('../resultados/produtividade_rf_real_vs_predito.png', dpi=300)
plt.close()

# 2. Análise de resíduos
residuos = np.array(y_true) - np.array(y_pred)
plt.figure(figsize=(10, 6))
plt.stem(df_anual['Ano'], residuos, 'r', markerfmt='ro', label='Resíduos')
plt.axhline(y=0, color='blue', linestyle='-')
plt.xlabel('Ano')
plt.ylabel('Resíduo (ton/ha)')
plt.title('Análise de Resíduos - Random Forest')
plt.grid(True, alpha=0.3)
plt.xticks(df_anual['Ano'])

# Anotar os valores dos resíduos
for ano, res in zip(df_anual['Ano'], residuos):
    plt.annotate(f'{res:.2f}', (ano, res), textcoords="offset points", 
                 xytext=(0,10), ha='center')

plt.tight_layout()
plt.savefig('../resultados/rf_anual_residuos.png', dpi=300)
plt.close()

# 3. Importância das variáveis
# Treinar o modelo com todos os dados
rf_modelo_final = RandomForestRegressor(n_estimators=100, random_state=42)
rf_modelo_final.fit(X, y)

importancias = rf_modelo_final.feature_importances_
indices = np.argsort(importancias)[::-1]
features = X.columns

# Converter para percentual
importancias_pct = importancias * 100

plt.figure(figsize=(10, 6))
sns.barplot(x=importancias_pct[indices], y=[features[i] for i in indices], palette='viridis')
plt.title('Importância das Variáveis - Random Forest', fontsize=14)
plt.xlabel('Importância Relativa (%)', fontsize=12)
plt.ylabel('Variável', fontsize=12)

# Adicionar valores percentuais nas barras
for i, v in enumerate(importancias_pct[indices]):
    plt.text(v + 0.5, i, f'{v:.1f}%', va='center')

plt.tight_layout()
plt.savefig('../resultados/rf_anual_importancia.png', dpi=300)
plt.close()

# 4. Gráfico de dispersão: valores reais vs. preditos
plt.figure(figsize=(8, 8))
plt.scatter(y_true, y_pred, c='blue', alpha=0.6, s=100)
plt.plot([min(y_true), max(y_true)], [min(y_true), max(y_true)], 'r--')
plt.xlabel('Produtividade Real (ton/ha)')
plt.ylabel('Produtividade Predita (ton/ha)')
plt.title('Dispersão: Valores Reais vs. Preditos')
plt.grid(True, alpha=0.3)

# Anotar os anos
for i, ano in enumerate(df_anual['Ano']):
    plt.annotate(str(ano), (y_true[i], y_pred[i]), textcoords="offset points", 
                 xytext=(5,5), ha='left')

plt.tight_layout()
plt.savefig('../resultados/rf_anual_dispersao.png', dpi=300)
plt.close()

# 5. Tabela de resultados detalhada
resultados_df = pd.DataFrame({
    'Ano': df_anual['Ano'],
    'Produtividade_Real': y_true,
    'Produtividade_Predita': y_pred,
    'Residuo': residuos,
    'Erro_Percentual': abs(residuos / np.array(y_true)) * 100
})

resultados_df.to_csv('../dados_processados/rf_resultados_detalhados.csv', index=False)
print("Resultados salvos em dados_processados/rf_resultados_detalhados.csv")
print("Visualizações salvas na pasta resultados/")

# Mostrar tabela de resultados
with pd.option_context('display.float_format', '{:.2f}'.format):
    print("\nTabela de resultados:")
    print(resultados_df)
    
# Salvar métricas em arquivo texto
with open('../dados_processados/rf_metricas.txt', 'w') as f:
    f.write(f'Métricas do modelo Random Forest (validação Leave-One-Out):\n')
    f.write(f'R²: {r2:.3f}\n')
    f.write(f'MAE: {mae:.3f} ton/ha\n')
    f.write(f'RMSE: {rmse:.3f} ton/ha\n')
    f.write(f'\nImportância das variáveis:\n')
    for i in indices:
        f.write(f"{features[i]}: {importancias[i]*100:.1f}%\n")
