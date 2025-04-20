"""
Segmentação automática por cor (K-means) na imagem satveg-sta-querencia.png
- Identifica zonas: vegetação ativa, solo exposto, vegetação nativa/pousio
- Destaca cada zona com cor/transparência diferente
- Salva resultado em resultados/satveg_segmentado_kmeans.png
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image

# Parâmetros
img_path = '../satveg-sta-querencia.png'
output_path = '../resultados/satveg_segmentado_kmeans.png'
n_clusters = 3  # Vegetação, solo, pousio/sombra

# Lê imagem
img = Image.open(img_path).convert('RGB')
img_np = np.array(img)

# Prepara para K-means
pixels = img_np.reshape(-1, 3)
kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(pixels)
labels = kmeans.labels_.reshape(img_np.shape[:2])
centers = kmeans.cluster_centers_.astype(np.uint8)

# Define cores para destacar zonas
# Verde escuro: cultivo ativo, Amarelo: solo exposto, Cinza: vegetação nativa/pousio
cores_dest = [np.array([34,139,34]), np.array([255, 255, 0]), np.array([160,160,160])]  # verde, amarelo, cinza

# Associa clusters às cores destino pela proximidade ao verde, amarelo e cinza
def cor_mais_proxima(centro):
    return np.argmin([np.linalg.norm(centro-c) for c in cores_dest])

mapa_clusters = [cor_mais_proxima(centro) for centro in centers]

# Gera imagem segmentada
img_segmentada = np.zeros_like(img_np)
for i, idx in enumerate(mapa_clusters):
    img_segmentada[labels == i] = cores_dest[idx]

# Transparência para sobrepor
alpha = 0.45
img_overlay = (alpha*img_segmentada + (1-alpha)*img_np).astype(np.uint8)

plt.figure(figsize=(10,10))
plt.imshow(img_overlay)
plt.axis('off')
plt.title('Segmentação K-means: Vegetação (verde), Solo exposto (amarelo), Pousio (cinza)')
plt.savefig(output_path, bbox_inches='tight', dpi=300)
plt.close()

print(f'Segmentação K-means salva em {output_path}')
