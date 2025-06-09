import pandas as pd
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm  

import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from scipy.spatial.distance import euclidean
from itertools import permutations
from k_means_constrained import KMeansConstrained
import heapq

import codecarbon as cc
ox.settings.use_cache = True
ox.settings.log_console = True


def find_all_routes(G, orig_node, clusters_nodes, alg="a*"):
  routes = []
  routes_paths = []
  for nodes in clusters_nodes:
    route, route_path = find_route(G, orig_node, nodes, alg)
    routes.append((route, route_path))
    routes_paths.append(route_path)

  return routes, routes_paths

def find_route(G, orig_node, dest_nodes, alg="a*"):
    route = []        # Ordem dos destinos visitados
    route_path = []   # Caminho completo (nós percorridos)
    remaining_nodes = dest_nodes.copy()  # Cópia para não modificar a lista original

    while len(remaining_nodes) > 0:
        dists = []
        paths = []

        for node in remaining_nodes:
            if alg == "a*":
                path = nx.astar_path(G, orig_node, node, weight='length')
            elif alg == "dijkstra":
                path = nx.dijkstra_path(G, orig_node, node, weight='length')
            elif alg == "dijkstra_heap":
                path = dijkstra_with_heap(G, orig_node, node)
                if path is None:
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

        # Adiciona o caminho ao route_path, evitando repetir o nó inicial
        if not route_path:
            route_path.extend(best_path)
        else:
            route_path.extend(best_path[1:])  # evita repetição do último nó do trecho anterior

        # Atualiza o ponto de partida
        orig_node = nearest_node

        # Remove o destino já visitado da cópia
        remaining_nodes.pop(min_index)

    return route, route_path

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

        if len(edge_data) > 1:
            distancia_total += min(d['length'] for d in edge_data.values())
        else:
            distancia_total += edge_data[0]['length']

    return distancia_total


def dijkstra_with_heap(G, source, target):
    """Implementação manual do Dijkstra com min-heap."""
    visited = set()
    min_heap = [(0, source, [])]  # (distância acumulada, nó atual, caminho)

    while min_heap:
        dist_u, u, path = heapq.heappop(min_heap)

        if u in visited:
            continue
        visited.add(u)
        path = path + [u]

        if u == target:
            return path

        for v in G.successors(u):
            if v not in visited:
                for key in G[u][v]:
                    length = G[u][v][key].get("length", 1)
                    heapq.heappush(min_heap, (dist_u + length, v, path))

    return None  # Caso não encontre caminho


