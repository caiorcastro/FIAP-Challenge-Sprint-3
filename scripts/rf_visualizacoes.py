"""
Gera visualizações para Random Forest:
- Importância das variáveis (anual e mensal)
- Gráficos de resíduos (real vs predito)
Salva em resultados/.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# --- ANUAL ---
df_anual = pd.read_csv('../dados_processados/integrado_anual.csv')
X_anual = df_anual[['Savitzky-Golay', 'Precipitacao_total_mm', 'Temp_media_C']]
y_anual = df_anual['Produtividade (ton/ha)']
rf_anual = RandomForestRegressor(n_estimators=100, random_state=42)
rf_anual.fit(X_anual, y_anual)
importances_anual = rf_anual.feature_importances_

plt.figure(figsize=(6,4))
plt.bar(X_anual.columns, importances_anual, color='forestgreen')
plt.title('Importância das Variáveis - Random Forest (Anual)')
plt.ylabel('Importância')
plt.tight_layout()
plt.savefig('../resultados/rf_anual_importancia.png')
plt.close()

# Gráfico de resíduos anual
y_pred_anual = rf_anual.predict(X_anual)
residuos_anual = y_anual - y_pred_anual
plt.figure(figsize=(6,4))
plt.scatter(y_pred_anual, residuos_anual, color='navy')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Produtividade Predita')
plt.ylabel('Resíduo')
plt.title('Resíduos do Random Forest - Anual')
plt.tight_layout()
plt.savefig('../resultados/rf_anual_residuos.png')
plt.close()

# --- MENSAL ---
df_mensal = pd.read_csv('../dados_processados/integrado_mensal.csv')
X_mensal = df_mensal[['Precipitacao_total_mm', 'Temp_media_C', 'Umidade_media']]
y_mensal = df_mensal['NDVI_medio']
rf_mensal = RandomForestRegressor(n_estimators=100, random_state=42)
rf_mensal.fit(X_mensal, y_mensal)
importances_mensal = rf_mensal.feature_importances_

plt.figure(figsize=(6,4))
plt.bar(X_mensal.columns, importances_mensal, color='darkorange')
plt.title('Importância das Variáveis - Random Forest (Mensal)')
plt.ylabel('Importância')
plt.tight_layout()
plt.savefig('../resultados/rf_mensal_importancia.png')
plt.close()

# Gráfico de resíduos mensal
y_pred_mensal = rf_mensal.predict(X_mensal)
residuos_mensal = y_mensal - y_pred_mensal
plt.figure(figsize=(6,4))
plt.scatter(y_pred_mensal, residuos_mensal, color='purple')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('NDVI Predito')
plt.ylabel('Resíduo')
plt.title('Resíduos do Random Forest - Mensal')
plt.tight_layout()
plt.savefig('../resultados/rf_mensal_residuos.png')
plt.close()

print('Visualizações Random Forest salvas em resultados/.')
