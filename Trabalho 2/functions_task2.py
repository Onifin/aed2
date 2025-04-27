import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def print_graphs(path):
    """
    Desenha grafos com as seguintes especificações:
    - Tamanho do vértice proporcional ao número de vizinhos
    - Destaca os top 5 vértices com mais vizinhos
    - Cor da aresta: vermelha se ligação entre membros permanentes, preta caso contrário
    - Largura da aresta proporcional à quantidade de citações

    Parâmetros:
    - path: caminho para o diretório base
    """

    evaluation_files = [
        ("2010-2012", "2010-2012.gexf"),
        ("2013-2016", "2013-2016.gexf"),
        ("2017-2020", "2017-2020.gexf"),
        ("2021-2024", "2021-2024.gexf")
    ]

    avaliacao_dir = os.path.join(path, "basedados", "avaliacao_geral")

    output_dir = os.path.join(path, "graphs")
    os.makedirs(output_dir, exist_ok=True)

    for period_label, filename in tqdm(evaluation_files):
        filepath = os.path.join(avaliacao_dir, filename)

        if not os.path.exists(filepath):
            print(f"Arquivo não encontrado: {filepath}")
            continue

        try:
            graph = nx.read_gexf(filepath)
            print(f"Grafo carregado: {period_label}")
        except Exception as e:
            print(f"Erro ao carregar o grafo {filename}: {str(e)}")
            continue

        plt.figure(figsize=(14, 12))

        node_degrees = dict(graph.degree())

        top_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
        top_nodes_ids = [node[0] for node in top_nodes]

        node_size_dict = {node: 30 + 5 * deg for node, deg in node_degrees.items()}
        for node_id in top_nodes_ids:
            node_size_dict[node_id] = node_size_dict[node_id] * 1.5  

        node_sizes = [node_size_dict[node] for node in graph.nodes()]

        node_colors = ['red' if node in top_nodes_ids else 'skyblue' for node in graph.nodes()]

        edge_colors = []
        for u, v, data in graph.edges(data=True):
            is_u_permanent = graph.nodes[u].get('is_permanent', False)
            is_v_permanent = graph.nodes[v].get('is_permanent', False)

            if is_u_permanent and is_v_permanent:
                edge_colors.append('red')
            else:
                edge_colors.append('black')

        edge_widths = []
        for u, v, data in graph.edges(data=True):
            citation_num = data.get('citation_num', 1) 
            
            width = 0.5 + 0.5 * np.log1p(citation_num)  
            edge_widths.append(width)

        pos = nx.spring_layout(graph, seed=42) 

        nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
        nx.draw_networkx_edges(graph, pos, width=edge_widths, edge_color=edge_colors, alpha=0.6)

        labels = {node: node for node in top_nodes_ids}
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, font_weight='bold')

        plt.title(f"Rede de Autores - {period_label}", fontsize=16)
        plt.axis('off')  

        plt.legend(handles=[
            plt.Line2D([0], [0], color='red', lw=2, label='Ligação entre membros permanentes'),
            plt.Line2D([0], [0], color='black', lw=2, label='Outras ligações'),
            plt.scatter([0], [0], s=100, color='red', label='Top 5 autores'),
            plt.scatter([0], [0], s=100, color='skyblue', label='Outros autores')
        ], loc='upper right')

        output_file = os.path.join(r'\Users\minna\OneDrive\Área de Trabalho\AED II\IAN REPOSITÓRIO\Trabalho 2\TASK2', f"network_graph_{period_label}.png")
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Grafo salvo: {output_file}")

        plt.close()