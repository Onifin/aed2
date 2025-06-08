import pandas as pd
import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from itertools import permutations
from k_means_constrained import KMeansConstrained

ox.settings.use_cache = True
ox.settings.log_console = True

from clusters import *



# Criação do grafo de Natal
G = ox.graph_from_place("Natal, Brazil", network_type = "drive")


# Estabelecimento da origem no grafo
orig_coords = (-5.753265931760308, -35.26269411137159) # Unidade de Vigilancia de Zoonoses Natal
orig_node = ox.distance.nearest_nodes(G, X=orig_coords[1], Y=orig_coords[0]) #Encontrando o nó mais próximo a unidade


# Substitua 'arquivo.csv' pelo caminho do seu arquivo
df = pd.read_csv('./centroid_filtered.csv')
# Mostrar as primeiras linhas do arquivo
df.head()


clusters_kmeans = create_clusters(df, 10, "k-means")
clusters_kmeans_constrained = create_clusters(df, 10, "k-means-constrained")
clusters_random = create_clusters(df, 10, "random")


plot_clusters(G, clusters_kmeans, orig_coords, df)


coords = np.array(df[['Lat', 'Lon']].values)

# KMeans clustering
kmeans = KMeans(n_clusters=10, random_state=0, n_init=10)
labels = kmeans.fit_predict(coords)

# Para cada cluster, vamos pegar os índices dos pontos
clusters = [[] for _ in range(10)]
for idx, label in enumerate(labels):
    clusters[label].append(idx)



from k_means_constrained import KMeansConstrained

n_clusters = 10
cluster_size = len(coords) // n_clusters

kmeans = KMeansConstrained(
    n_clusters=n_clusters,
    size_min=cluster_size,
    size_max=cluster_size + 1,
    random_state=0
)

labels = kmeans.fit_predict(coords)

# Para cada cluster, vamos pegar os índices dos pontos
clusters_norm = [[] for _ in range(10)]
for idx, label in enumerate(labels):
    clusters_norm[label].append(idx)



print(labels)


clusters_norm


import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from scipy.spatial.distance import euclidean
from itertools import permutations

coords = np.array(df[['Lat', 'Lon']].values)

# KMeans clustering
kmeans = KMeans(n_clusters=10, random_state=0, n_init=10)
labels = kmeans.fit_predict(coords)

# Para cada cluster, vamos pegar os índices dos pontos
clusters = [[] for _ in range(10)]
for idx, label in enumerate(labels):
    clusters[label].append(idx)

# Opcional: ordenação dos índices em cada cluster para minimizar a distância
# Para pequenos grupos, podemos usar força bruta
def optimal_order(points_indices):
    if len(points_indices) <= 7:
        min_dist = float('inf')
        best_order = points_indices
        for perm in permutations(points_indices):
            dist = 0
            for i in range(len(perm) - 1):
                dist += euclidean(coords[perm[i]], coords[perm[i + 1]])
            if dist < min_dist:
                min_dist = dist
                best_order = perm
        return list(best_order)
    else:
        # Para clusters maiores, usar heurística: Nearest Neighbor
        remaining = points_indices.copy()
        current = remaining.pop(0)
        ordered = [current]
        while remaining:
            next_idx = min(remaining, key=lambda x: euclidean(coords[current], coords[x]))
            remaining.remove(next_idx)
            ordered.append(next_idx)
            current = next_idx
        return ordered

# Otimiza a ordem dos índices em cada cluster
optimized_clusters = [optimal_order(cluster) for cluster in clusters]

print("grupos = [")
# Mostra resultado
for i, cluster in enumerate(optimized_clusters):
    print(f"    {cluster},")
print("]")


# Extrair coordenadas dos pontos
print(coords)


plot_clusters(G, clusters, orig_coords, df)

# Exemplo: lista de grupos conforme gerado anteriormente, com modificações por vizualização e moficação manual
grupos = clusters

# Extrair coordenadas dos pontos
coords = df[['Lat', 'Lon']].values  # OSMnx usa (lat, lon)

# Gerar cores diferentes para os grupos
colors = list(mcolors.TABLEAU_COLORS.values())[:len(grupos)]

# Plotar o grafo
fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0, edge_color='gray')

ax.scatter(orig_coords[1], orig_coords[0], c='w', label='origem', s=50, alpha=0.8, edgecolors='k')

# Para cada grupo, plotar os pontos
for i, grupo in enumerate(grupos):
    lat_lon = coords[grupo]  # Coordenadas do grupo
    lats = lat_lon[:, 1]
    lons = lat_lon[:, 0]

    ax.scatter(lons, lats, c=colors[i], label=f'Grupo {i+1}', s=50, alpha=0.8, edgecolors='k')


# Configurações do gráfico
plt.legend()
plt.title('Grupos no Grafo com OSMnx')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()