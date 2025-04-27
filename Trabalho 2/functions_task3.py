import os
import networkx as nx
import matplotlib.pyplot as plt

def visualizar_grafos(grafo_original, subgrafo, titulo_original="Grafo Original", titulo_subgrafo="Subgrafo"):
    """
    Visualiza o grafo original e o subgrafo lado a lado, sem mostrar rótulos nos nós.

    Parâmetros:
    grafo_original (networkx.Graph): O grafo original completo
    subgrafo (networkx.Graph): O subgrafo a ser visualizado
    titulo_original (str): Título para o grafo original
    titulo_subgrafo (str): Título para o subgrafo
    """
    plt.figure(figsize=(16, 8))

    plt.subplot(1, 2, 1)
    pos_original = nx.spring_layout(grafo_original, seed=42)

    node_colors_original = ['skyblue' if node in subgrafo.nodes() else 'lightgray'
                           for node in grafo_original.nodes()]

    nx.draw_networkx_nodes(grafo_original, pos_original, node_size=200,
                          node_color=node_colors_original, alpha=0.8)
    nx.draw_networkx_edges(grafo_original, pos_original, width=1.0, alpha=0.5)

    plt.title(titulo_original)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    pos_subgrafo = nx.spring_layout(subgrafo, seed=42)

    nx.draw_networkx_nodes(subgrafo, pos_subgrafo, node_size=300,
                          node_color='skyblue', alpha=0.8)
    nx.draw_networkx_edges(subgrafo, pos_subgrafo, width=1.5, alpha=0.7)

    plt.title(titulo_subgrafo)
    plt.axis('off')

    plt.tight_layout()
    plt.show()


def visualizar_rede_ego(ego_node, grafo, radius=1, titulo_subgrafo="REDE EGO DO PROFESSOR FIRMINO"):
    """
    Visualiza o subgrafo ego de um nó específico, destacando o nó central com cor e tamanho diferentes.
    
    Parâmetros:
    ego_node (str): O nó central da rede ego, que será destacado
    grafo (networkx.Graph): O grafo completo do qual o subgrafo ego será extraído
    radius (int): O raio da rede ego, ou seja, a distância máxima dos nós ao ego para inclusão no subgrafo
    titulo_subgrafo (str): Título para o subgrafo
    """
    
    subgrafo_ego = nx.ego_graph(grafo, ego_node, radius=radius)
    
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(subgrafo_ego, seed=42)

    node_colors = ['red' if node == ego_node else 'skyblue' for node in subgrafo_ego.nodes()]
    node_sizes = [600 if node == ego_node else 300 for node in subgrafo_ego.nodes()]

    nx.draw_networkx_nodes(subgrafo_ego, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(subgrafo_ego, pos, width=1.5, alpha=0.7)

    labels = {node: node for node in subgrafo_ego.nodes() if node == ego_node}
    nx.draw_networkx_labels(subgrafo_ego, pos, labels=labels, font_size=12, font_weight='bold', font_color='black')

    plt.title(titulo_subgrafo)
    plt.axis('off')

    plt.tight_layout()
    plt.show()

