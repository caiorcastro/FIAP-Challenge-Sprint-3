"""
Random Forest para Previsão de Produtividade Agrícola
Usando integrado_anual.csv
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import LeaveOneOut
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Importação dos dados
df = pd.read_csv('../dados_processados/integrado_anual.csv')

# 2. Seleção de variáveis
X = df[['Área Plantada (ha)', 'Área Colhida (ha)', 'Savitzky-Golay',
        'Precipitacao_total_mm', 'Temp_media_C', 'Umidade_media']]
y = df['Produtividade (ton/ha)']

# 3. Treinamento e Validação Leave-One-Out
loo = LeaveOneOut()
y_true, y_pred = [], []

for train_idx, test_idx in loo.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred.append(model.predict(X_test)[0])
    y_true.append(y_test.values[0])

# 4. Avaliação do modelo
r2 = r2_score(y_true, y_pred)
mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))

print(f'R²: {r2:.3f}')
print(f'MAE: {mae:.3f}')
print(f'RMSE: {rmse:.3f}')
print('Execução concluída com sucesso.')

# 5. Gráfico de comparação real vs predito
plt.figure(figsize=(8,5))
plt.plot(df['Ano'], y_true, label='Real', marker='o')
plt.plot(df['Ano'], y_pred, label='Predito', marker='s')
plt.xlabel('Ano')
plt.ylabel('Produtividade (ton/ha)')
plt.title('Produtividade Real vs Predita (Random Forest)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('../resultados/produtividade_rf_real_vs_predito.png', dpi=200)
plt.show()

# 6. Importância das variáveis
model_final = RandomForestRegressor(n_estimators=100, random_state=42)
model_final.fit(X, y)
importancias = model_final.feature_importances_
features = X.columns

plt.figure(figsize=(7,4))
sns.barplot(x=importancias, y=features, palette='viridis')
plt.title('Importância das Variáveis - Random Forest')
plt.xlabel('Importância')
plt.tight_layout()
plt.savefig('../resultados/produtividade_rf_importancia_variaveis.png', dpi=200)
plt.show()
