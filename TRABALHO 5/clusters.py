import osmnx as ox
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
from k_means_constrained import KMeansConstrained

ox.settings.use_cache = True
ox.settings.log_console = True


def create_clusters(df, n_clusters, alg="k-means"):
  coords = np.array(df[['Lat', 'Lon']].values)

  if(alg == "k-means"):
    # KMEANS CLUSTERING
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=n_clusters)
    labels = kmeans.fit_predict(coords)

  if(alg == "k-means-constrained"):
    # KMEANS CLUSTERING
    cluster_size = len(coords) // n_clusters

    kmeans = KMeansConstrained(
        n_clusters=n_clusters,
        size_min=cluster_size,
        size_max=cluster_size + 1,
        random_state=0
    )
    labels = kmeans.fit_predict(coords)

  if(alg == "random"):
    labels = np.random.randint(0, n_clusters, len(coords))

  # PARA CADA CLUSTER, VAMOS PEGAR OS ÍNDICES DOS PONTOS
  clusters = [[] for _ in range(10)]
  for idx, label in enumerate(labels):
      clusters[label].append(idx)

  return clusters


def plot_clusters(G, clusters, orig_coords, df):
  # EXTRAIR COORDENADAS DOS PONTOS
  coords = df[['Lat', 'Lon']].values  # OSMNX USA (LAT, LON)

  # GERAR CORES DIFERENTES PARA OS GRUPOS
  colors = list(mcolors.TABLEAU_COLORS.values())[:len(clusters)]

  # PLOTAR O GRAFO
  fig, ax = ox.plot_graph(G, show=False, close=False, figsize=(10, 10), node_size=0, edge_color='gray')

  ax.scatter(orig_coords[1], orig_coords[0], c='w', label='origem', s=50, alpha=0.8, edgecolors='k')

  # PARA CADA GRUPO, PLOTAR OS PONTOS
  for i, grupo in enumerate(clusters):
      lat_lon = coords[grupo]  # COORDENADAS DO GRUPO
      lats = lat_lon[:, 1]
      lons = lat_lon[:, 0]

      ax.scatter(lons, lats, c=colors[i], label=f'Grupo {i+1}', s=50, alpha=0.8, edgecolors='k')

  # CONFIGURAÇÕES DO GRÁFICO
  plt.legend()
  plt.title('Grupos no Grafo com OSMnx')
  plt.xlabel('Longitude')
  plt.ylabel('Latitude')
  plt.show()


def plot_clusters_and_routes(G, clusters, routes, orig_coords, df, title='Rotas e Clusters no Grafo'):
    # Extrair coordenadas (lat, lon) do dataframe
    coords = df[['Lat', 'Lon']].values

    # Cores distintas para até 10 clusters
    base_colors = list(mcolors.TABLEAU_COLORS.values())
    if len(clusters) > len(base_colors):
        cmap = cm.get_cmap('tab20', len(clusters))
        cluster_colors = [cmap(i) for i in range(len(clusters))]
    else:
        cluster_colors = base_colors[:len(clusters)]

    # Cores para as rotas (opcionalmente iguais às dos clusters)
    route_colors = cluster_colors

    # Plota o grafo com rotas
    fig, ax = ox.plot_graph_routes(
        G,
        routes,
        route_colors=route_colors,
        route_linewidth=3,
        node_size=0,
        show=False,
        close=False,
        figsize=(18, 18),
        edge_color='white'
    )

    # Plota a origem
    ax.scatter(orig_coords[1], orig_coords[0], c='white', label='Origem', s=60, alpha=0.9, edgecolors='k', zorder=3)

    # Plota cada grupo de cluster
    for i, grupo in enumerate(clusters):
        lat_lon = coords[grupo]  # Índices dos pontos
        lats = lat_lon[:, 1]
        lons = lat_lon[:, 0]

        ax.scatter(
            lons,
            lats,
            c=[cluster_colors[i]],
            label=f'Grupo {i+1}',
            s=50,
            alpha=0.9,
            edgecolors='k',
            zorder=3
        )

    # Configurações visuais
    plt.legend()
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()