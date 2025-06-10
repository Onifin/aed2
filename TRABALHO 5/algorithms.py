from libs import *


def dijkstra_traditional(G, source, target):
    """Implementação tradicional do Dijkstra (sem min-heap)."""
    print("iniciou")
    unvisited = set(G.nodes)
    distances = {node: float('inf') for node in G.nodes}
    predecessors = {node: None for node in G.nodes}

    distances[source] = 0

    while unvisited:
        # Seleciona o nó com a menor distância entre os não visitados
        u = min((node for node in unvisited), key=lambda node: distances[node])

        if distances[u] == float('inf'):
            break  # Todos os nós restantes são inalcançáveis

        unvisited.remove(u)

        if u == target:
            # Reconstrói o caminho a partir dos predecessores
            path = []
            while u is not None:
                path.insert(0, u)
                u = predecessors[u]
            return path

        for v in G.successors(u):
            if v in unvisited:
                for key in G[u][v]:
                    length = G[u][v][key].get("length", 1)
                    alt = distances[u] + length
                    if alt < distances[v]:
                        distances[v] = alt
                        predecessors[v] = u

    return None  # Caso não encontre caminho

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