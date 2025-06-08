import pandas as pd
import osmnx as ox

from sklearn.cluster import KMeans
from k_means_constrained import KMeansConstrained

from clusters import create_clusters, plot_clusters  # FUNÇÕES PERSONALIZADAS PARA CLUSTERIZAÇÃO E PLOTAGEM



# =================================
# CONFIGURAÇÕES INICIAIS DO CÓDIGO
# =================================

# CONFIGURAÇÕES DO OSMNX PARA USAR CACHE E MOSTRAR LOGS NO CONSOLE
ox.settings.use_cache = True
ox.settings.log_console = True

G = ox.graph_from_place("Natal, Brazil", network_type="drive") # CRIA O GRAFO DE VIAS DA CIDADE DE NATAL/RN 
orig_coords = (-5.753265931760308, -35.26269411137159) # DEFINE PONTO DE ORIGEM

# ENCONTRA O NÓ DO GRAFO MAIS PRÓXIMO DO PONTO DE ORIGEM
orig_node = ox.distance.nearest_nodes(G, X=orig_coords[1], Y=orig_coords[0])

df = pd.read_csv('./centroid_filtered.csv') # CARREGA OS DADOS DE CENTRÓIDES A PARTIR DE UM ARQUIVO CSV
coords = df[['Lat', 'Lon']].to_numpy() # CONVERTE AS COLUNAS DE LATITUDE E LONGITUDE PARA UM ARRAY NUMÉRICO



# =============================================================
# REALIZA A CLUSTERIZAÇÃO DOS PONTOS USANDO MÉTODOS DIFERENTES
# =============================================================

# 1. KMEANS TRADICIONAL (SEM RESTRIÇÕES DE TAMANHO)
kmeans = KMeans(n_clusters=10, random_state=0, n_init=10)
labels_kmeans = kmeans.fit_predict(coords)  # RETORNA O RÓTULO DE CLUSTER PARA CADA PONTO

# 2. KMEANS COM RESTRIÇÕES DE TAMANHO MÍNIMO E MÁXIMO
# MAIOR TAMANHO É 7 E O MENOR TAMANHO É 6 PARA A CONSTRAINED
cluster_size = len(coords) // 10  # CALCULA O TAMANHO IDEAL DE CADA CLUSTER
kmeans_constrained = KMeansConstrained(
    n_clusters=10,
    size_min=cluster_size,
    size_max=cluster_size + 1,
    random_state=0
)
labels_constrained = kmeans_constrained.fit_predict(coords)  # CLUSTERIZA COM TAMANHOS BALANCEADOS

# 3. CLUSTERIZAÇÃO ALEATÓRIA (VIA FUNÇÃO PERSONALIZADA)
clusters_random = create_clusters(df, 10, "random")



# ==================================================================
# FUNÇÃO AUXILIAR PARA ORGANIZAR ÍNDICES DOS PONTOS EM CADA CLUSTER
# ==================================================================

def get_clusters_from_labels(labels, n_clusters):
    clusters = [[] for _ in range(n_clusters)]  # INICIALIZA LISTA DE CLUSTERS
    for idx, label in enumerate(labels):        # ATRIBUI CADA PONTO AO SEU CLUSTER
        clusters[label].append(idx)
    return clusters

# APLICA A FUNÇÃO PARA OBTER LISTAS DE ÍNDICES DOS PONTOS EM CADA CLUSTER
clusters_kmeans = get_clusters_from_labels(labels_kmeans, 10)
clusters_kmeans_constrained = get_clusters_from_labels(labels_constrained, 10)



# ========================================================
# VISUALIZA OS CLUSTERS NO MAPA USANDO OSMNX + MATPLOTLIB
# ========================================================

plot_clusters(G, clusters_kmeans, orig_coords, df)  # PLOTA SOMENTE OS CLUSTERS KMEANS














'''
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
'''