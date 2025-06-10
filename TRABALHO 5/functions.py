from libs import *
from algorithms import *


def find_nodes(G, clusters, df):
  coords = np.array(df[['Lat', 'Lon']].values)
  nodes = []
  for cluster in clusters:
    cluster_node = []
    lat_lon = coords[cluster]  # Coordenadas do grupo
    lats = lat_lon[:, 1]
    lons = lat_lon[:, 0]

    for i in range(len(lats)):
      cluster_node.append(ox.distance.nearest_nodes(G, X=lons[i], Y=lats[i]))
    nodes.append(cluster_node)
  return nodes


def calculate_path_distance(G, caminho):
    distancia_total = 0

    for u, v in zip(caminho[:-1], caminho[1:]):
        edge_data = G.get_edge_data(u, v)

        if edge_data is None:
            continue  # Ou você pode fazer: return None ou lançar um erro

        # Para grafos multigrafo, edge_data é um dicionário com 1 ou mais arestas
        # Ex: {0: {'length': x}, 1: {'length': y}}
        lengths = [d['length'] for d in edge_data.values() if 'length' in d]

        if lengths:
            distancia_total += min(lengths)  # Ou sum(lengths), dependendo da lógica
        else:
            continue  # Ou tratar com valor padrão

    return distancia_total


def find_route_per_groupe(G, orig_node, dest_nodes, alg="a*"):
    copy_orig_node = orig_node
    route = []        # Ordem dos destinos visitados
    route_path = []   # Caminho completo (nós percorridos)
    remaining_nodes = dest_nodes.copy()  # Cópia para não modificar a lista original
    total_distance = 0
    #tracker = EmissionsTracker() # Coletar pegada de carbono
    #tracker.start()
    start = time.time()

    while len(remaining_nodes) > 0:
        dists = []
        paths = []

        for node in remaining_nodes:

            if alg == "a*":
                path = nx.astar_path(G, orig_node, node, weight='length')
            elif alg == "dijkstra":
                path = dijkstra_traditional(G, orig_node, node)
            elif alg == "dijkstra_heap":
                path = dijkstra_with_heap(G, orig_node, node)
                if path is None:
                    print("Deu ruim")
                    continue
            else:
                raise ValueError("Algoritmo não suportado: use 'a*', 'dijkstra' ou 'dijkstra_heap'.")

            dist = calculate_path_distance(G, path)
            dists.append(dist)
            paths.append(path)

        if not dists:
            break  # Nenhum caminho válido encontrado

        # Escolhe o destino mais próximo
        min_index = dists.index(min(dists))
        nearest_node = remaining_nodes[min_index]
        best_path = paths[min_index]

        # Adiciona à rota final
        route.append(nearest_node)
        # Adiciona à distância ao total
        total_distance += min(dists)

        # Adiciona o caminho ao route_path, evitando repetir o nó inicial
        if not route_path:
            route_path.extend(best_path)
        else:
            route_path.extend(best_path[1:])  # evita repetição do último nó do trecho anterior

        # Atualiza o ponto de partida
        orig_node = nearest_node

        # Remove o destino já visitado da cópia
        remaining_nodes.pop(min_index)

    #calcula o retorno ao nó inicial
    if alg == "a*":
        path = nx.astar_path(G, orig_node, copy_orig_node, weight='length')
    elif alg == "dijkstra":
        path = dijkstra_traditional(G, orig_node, copy_orig_node)
    elif alg == "dijkstra_heap":
        path = dijkstra_with_heap(G, orig_node, copy_orig_node)
    else:
        raise ValueError("Algoritmo não suportado: use 'a*', 'dijkstra' ou 'dijkstra_heap'.")

    # Adiciona o caminho ao route_path, evitando repetir o nó inicial

    route_path.extend(path[1:])  # evita repetição do último nó do trecho anterior
    total_distance += calculate_path_distance(G, path)
    #emission = tracker.stop()
    end = time.time()
    tempo = end - start

    return route, route_path, total_distance, tempo


def find_all_goupe_routes(G, orig_node, grupe_nodes, alg="a*"):

  #Armazena a sequência de nós percorridos pelos grupos
  routes = []
  #Armazena todos os pontos do caminho percorridos pelos grupos
  routes_paths = []
  #Armazena a distância de cada grupo
  distances = []
  #Armazena as emissões de carbono
  emissions = []
  #Armazena tempo
  tempos = []

  for nodes in grupe_nodes:
    route, route_path, total_distance, tempo = find_route_per_groupe(G, orig_node, nodes, alg)
    routes.append((route, route_path))
    routes_paths.append(route_path)
    distances.append(total_distance)
    #emissions.append(emission)
    tempos.append(tempo)

  return routes, routes_paths, distances, tempos


def plot_points_in_graph(G, pontos):
    """
    Plota pontos (latitude, longitude) sobre o grafo G.
    """
    # Extrai as coordenadas dos nós do grafo
    fig, ax = ox.plot_graph(G, show=False, close=False)

    # Separa as listas de latitude e longitude
    lats = [lat for lat, lon in pontos]
    lons = [lon for lat, lon in pontos]

    # Plota os pontos sobre o grafo
    ax.scatter(lons, lats, c='red', s=50, marker='o', label='Pontos')

    plt.legend()
    plt.show()


def return_nodes_position(G, nodes):
    """
    Retorna as posições geográficas (latitude e longitude) de uma lista de nós do grafo G.
    """
    positions = []
    for node in nodes:
        if node in G.nodes:
            lat = G.nodes[node]['y']
            lon = G.nodes[node]['x']
            positions.append((lat, lon))
        else:
            print(f"Nó {node} não encontrado no grafo.")
    return positions