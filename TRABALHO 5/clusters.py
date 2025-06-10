from libs import *


def create_clusters(df, n_clusters, alg="k-means"):
  coords = np.array(df[['Lat', 'Lon']].values)

  if(alg == "k-means"):
    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=n_clusters)
    labels = kmeans.fit_predict(coords)

  if(alg == "k-means-constrained"):
    # KMeans clustering
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

  # Para cada cluster, vamos pegar os índices dos pontos
  clusters = [[] for _ in range(10)]
  for idx, label in enumerate(labels):
      clusters[label].append(idx)

  return clusters



def plot_clusters(G, clusters, orig_coords, df, title=""):
  # Extrair coordenadas dos pontos
  coords = df[['Lat', 'Lon']].values  # OSMnx usa (lat, lon)

  # Gerar cores diferentes para os grupos
  colors = list(mcolors.TABLEAU_COLORS.values())[:len(clusters)]
  #mudando cores
  colors[2] = "#3BE001"
  colors[7] = "#BDE6BB"

  # Plotar o grafo
  fig, ax = ox.plot_graph(G, show=False, close=False, figsize=(10, 10), node_size=0, edge_color='gray')

  ax.scatter(orig_coords[1], orig_coords[0], c='w', label='origem', s=50, alpha=0.8, edgecolors='k')

  # Para cada grupo, plotar os pontos
  for i, grupo in enumerate(clusters):
      lat_lon = coords[grupo]  # Coordenadas do grupo
      lats = lat_lon[:, 1]
      lons = lat_lon[:, 0]

      ax.scatter(lons, lats, c=colors[i], label=f'Grupo {i+1}', s=50, alpha=0.8, edgecolors='k')


  # Configurações do gráfico
  plt.legend()
  plt.title(title)
  plt.xlabel('Longitude')
  plt.ylabel('Latitude')
  plt.show()



def plot_clusters_and_routes(G, clusters, routes, orig_coords, df, title='Rotas e Clusters no Grafo', filename='rotas_clusters'):
    # Extrair coordenadas (lat, lon) do dataframe
    coords = df[['Lat', 'Lon']].values

    # Cores distintas para até 10 clusters
    base_colors = list(mcolors.TABLEAU_COLORS.values())
    base_colors[2] = "#3BE001"
    base_colors[7] = "#BDE6BB"

    if len(clusters) > len(base_colors):
        cmap = cm.get_cmap('tab20', len(clusters))
        cluster_colors = [cmap(i) for i in range(len(clusters))]
    else:
        cluster_colors = base_colors[:len(clusters)]

    route_colors = cluster_colors

    # Criar figura e eixo
    fig, ax = ox.plot_graph(G, show=False, close=False, figsize=(16, 16), edge_color='gray', node_size=0)

    # Plota rotas individualmente
    for route, color in zip(routes, route_colors):
        for u, v in zip(route[:-1], route[1:]):
            data = G.get_edge_data(u, v)
            if data is None:
                data = G.get_edge_data(v, u)
                if data is None:
                    continue

            edge = min(data.values(), key=lambda d: d.get("length", float("inf")))
            if "geometry" in edge:
                xs, ys = edge["geometry"].xy
            else:
                xs = [G.nodes[u]['x'], G.nodes[v]['x']]
                ys = [G.nodes[u]['y'], G.nodes[v]['y']]
            ax.plot(xs, ys, color=color, linewidth=3, alpha=0.7, zorder=2)

    # Plota a origem
    ax.scatter(orig_coords[1], orig_coords[0], c='white', label='Origem', s=60, alpha=0.9, edgecolors='k', zorder=3)

    # Plota clusters
    for i, grupo in enumerate(clusters):
        lat_lon = coords[grupo]
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
    plt.title(title, color='white')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Salvar como PNG e PDF
    plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
    plt.savefig(f"{filename}.pdf", bbox_inches='tight')
    plt.close(fig)
