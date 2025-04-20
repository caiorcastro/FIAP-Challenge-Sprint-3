"""
Segmentação temporal NDVI a partir de gráfico SATVeg.
- Lê o arquivo 'satveg_grafico.png' (curva NDVI ao longo do tempo)
- Permite ao usuário marcar thresholds (ex: NDVI > 0.7)
- Destaca zonas de baixo, médio e alto NDVI
- Salva gráfico segmentado em 'resultados/satveg_segmentado.png'
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

# Função para detectar a linha preta e roxa por cor
# Espera-se que a linha preta (NDVI=0.7) seja preta pura (0,0,0) e a roxa (NDVI=0.4) seja próxima de (128,0,128)
def detectar_linhas(img):
    altura, largura = img.shape[0], img.shape[1]
    # Se imagem RGBA, descarta canal alpha
    if img.shape[2] == 4:
        img_rgb = img[:,:,:3]
    else:
        img_rgb = img
    # Normaliza para 0-255 se necessário
    if img_rgb.max() <= 1.0:
        img_rgb = (img_rgb*255).astype(np.uint8)
    # Detecta linha preta (NDVI=0.7)
    preto = np.array([0,0,0])
    roxo = np.array([128,0,128])
    # Calcula distância de cor para cada linha
    dist_preto = np.mean(np.linalg.norm(img_rgb-preto, axis=2), axis=1)
    dist_roxo = np.mean(np.linalg.norm(img_rgb-roxo, axis=2), axis=1)
    y_preto = np.argmin(dist_preto)
    y_roxo = np.argmin(dist_roxo)
    return y_preto, y_roxo, altura

# Caminho da imagem
grafico_path = '../satveg_grafico.png'
img = mpimg.imread(grafico_path)
y_preto, y_roxo, altura_px = detectar_linhas(img)

fig, ax = plt.subplots(figsize=(10,5))
ax.imshow(img)
ax.axis('off')
ax.set_title('SATVeg NDVI - Segmentação Temporal', fontsize=16, weight='bold')

# Preenche faixas NDVI alinhadas às linhas detectadas
# NDVI alto: acima da linha preta, médio: entre preta e roxa, baixo: abaixo da roxa
faixas = [
    (0, y_roxo, '#ffeeba', 'NDVI Baixo'),
    (y_roxo, y_preto, '#b7e4c7', 'NDVI Médio'),
    (y_preto, altura_px, '#90ee90', 'NDVI Alto')
]
for y1, y2, cor, label in faixas:
    ax.fill_betweenx(y=[y1, y2], x1=0, x2=img.shape[1], color=cor, alpha=0.3, label=label)

# Apenas uma legenda clara
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='lower left', fontsize=12, frameon=True)

plt.savefig('../resultados/satveg_segmentado.png', bbox_inches='tight', dpi=300)
plt.close()

print(f'Gráfico segmentado salvo em resultados/satveg_segmentado.png (Linhas detectadas: preto={y_preto}, roxo={y_roxo})')
