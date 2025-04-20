"""
Validação cruzada dos modelos anuais e mensais usando múltiplos algoritmos:
- LinearRegression
- Ridge
- Lasso
- RandomForestRegressor

Apresenta métricas e explicações para cada modelo. Foco no anual (produtividade) e mensal (NDVI).
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import os

os.makedirs('../dados_processados', exist_ok=True)
os.makedirs('../resultados', exist_ok=True)

# --- Função para avaliação e explicação dos modelos ---
def avaliar_modelos(X, y, modelos, nome_saida, explicacao):
    resultados = []
    loo = LeaveOneOut()
    for nome, modelo in modelos.items():
        scores = cross_val_score(modelo, X, y, cv=loo, scoring='r2')
        modelo.fit(X, y)
        y_pred = modelo.predict(X)
        mse = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_pred)
        resultados.append({
            'Modelo': nome,
            'R2_treino': r2,
            'R2_LOO_medio': np.mean(scores),
            'RMSE': rmse
        })
    df_result = pd.DataFrame(resultados)
    df_result.to_csv(f'../dados_processados/{nome_saida}_validacao_modelos.csv', index=False)
    with open(f'../dados_processados/{nome_saida}_explicacao.txt', 'w') as f:
        f.write(explicacao)
        f.write('\nMétricas:\n')
        f.write(df_result.to_string(index=False))
    return df_result

# --- 1. Modelagem ANUAL (Produtividade) ---
df_anual = pd.read_csv('../dados_processados/integrado_anual.csv')
X_anual = df_anual[['Savitzky-Golay', 'Precipitacao_total_mm', 'Temp_media_C']]
y_anual = df_anual['Produtividade (ton/ha)']
modelos_anual = {
    'LinearRegression': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.01),
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
}
explicacao_anual = (
    'Validação cruzada leave-one-out com 4 algoritmos:\n'
    '- LinearRegression: modelo linear simples.\n'
    '- Ridge: regularização L2 para reduzir overfitting.\n'
    '- Lasso: regularização L1 para seleção de variáveis.\n'
    '- RandomForest: modelo não-linear, robusto a colinearidade.'
)
avaliar_modelos(X_anual, y_anual, modelos_anual, 'anual', explicacao_anual)

# --- 2. Modelagem MENSAL (NDVI ~ clima) ---
df_mensal = pd.read_csv('../dados_processados/integrado_mensal.csv')
X_mensal = df_mensal[['Precipitacao_total_mm', 'Temp_media_C', 'Umidade_media']]
y_mensal = df_mensal['NDVI_medio']
modelos_mensal = {
    'LinearRegression': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.01),
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
}
explicacao_mensal = (
    'Validação cruzada leave-one-out para prever NDVI mensal a partir do clima:\n'
    '- LinearRegression: modelo linear simples.\n'
    '- Ridge: regularização L2 para reduzir overfitting.\n'
    '- Lasso: regularização L1 para seleção de variáveis.\n'
    '- RandomForest: modelo não-linear, robusto a colinearidade.'
)
avaliar_modelos(X_mensal, y_mensal, modelos_mensal, 'mensal', explicacao_mensal)

print('Validação cruzada concluída. Resultados salvos em dados_processados/.')
