"""
Script para modelagem preditiva da produtividade do milho em Sidrolândia-MS
Utiliza regressão linear/múltipla com variáveis NDVI, clima e produtividade.
Salva resultados e coeficientes em dados_processados/ e resultados/.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import os

# --- Modelagem ANUAL ---
# Carregar base integrada anual
df = pd.read_csv('../dados_processados/integrado_anual.csv')

# Selecionar variáveis explicativas e target
X = df[['Savitzky-Golay', 'Precipitacao_total_mm', 'Temp_media_C']]
y = df['Produtividade (ton/ha)']

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

r2 = r2_score(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)

# Salvar coeficientes
coefs = pd.DataFrame({'Variavel': X.columns, 'Coeficiente': model.coef_})
coefs.to_csv('../dados_processados/modelo_anual_coeficientes.csv', index=False)

# Salvar métricas
with open('../dados_processados/modelo_anual_metricas.txt', 'w') as f:
    f.write(f'R²: {r2:.2f}\nRMSE: {rmse:.2f}\nIntercepto: {model.intercept_:.2f}\n')

# Gráfico: Real vs Predito
plt.figure(figsize=(8,6))
plt.scatter(y, y_pred, color='blue', s=80)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel('Produtividade Real (ton/ha)')
plt.ylabel('Produtividade Predita (ton/ha)')
plt.title('Modelo Anual: Produtividade Real vs Predita')
plt.grid(True)
plt.tight_layout()
plt.savefig('../resultados/modelo_anual_real_vs_predito.png')
plt.close()

# --- Modelagem MENSAL (opcional, exemplo) ---
df_mensal = pd.read_csv('../dados_processados/integrado_mensal.csv')
X_m = df_mensal[['NDVI_medio', 'Precipitacao_total_mm', 'Temp_media_C']]
y_m = df_mensal['Produtividade (ton/ha)'] if 'Produtividade (ton/ha)' in df_mensal.columns else None

if y_m is not None:
    model_m = LinearRegression()
    model_m.fit(X_m, y_m)
    y_pred_m = model_m.predict(X_m)
    r2_m = r2_score(y_m, y_pred_m)
    mse_m = mean_squared_error(y_m, y_pred_m)
    rmse_m = np.sqrt(mse_m)
    # Salvar coeficientes
    coefs_m = pd.DataFrame({'Variavel': X_m.columns, 'Coeficiente': model_m.coef_})
    coefs_m.to_csv('../dados_processados/modelo_mensal_coeficientes.csv', index=False)
    # Salvar métricas
    with open('../dados_processados/modelo_mensal_metricas.txt', 'w') as f:
        f.write(f'R²: {r2_m:.2f}\nRMSE: {rmse_m:.2f}\nIntercepto: {model_m.intercept_:.2f}\n')
    # Gráfico
    plt.figure(figsize=(8,6))
    plt.scatter(y_m, y_pred_m, color='green', s=60)
    plt.plot([y_m.min(), y_m.max()], [y_m.min(), y_m.max()], 'r--')
    plt.xlabel('Produtividade Real (ton/ha)')
    plt.ylabel('Produtividade Predita (ton/ha)')
    plt.title('Modelo Mensal: Produtividade Real vs Predita')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('../resultados/modelo_mensal_real_vs_predito.png')
    plt.close()

print('Modelos anuais e mensais executados. Resultados e coeficientes salvos em dados_processados/ e resultados/.')
