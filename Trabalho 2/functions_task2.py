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
    # Lista de períodos de avaliação e seus arquivos correspondentes
    evaluation_files = [
        ("2010-2012", "2010-2012.gexf"),
        ("2013-2016", "2013-2016.gexf"),
        ("2017-2020", "2017-2020.gexf"),
        ("2021-2024", "2021-2024.gexf")
    ]

    # Diretório contendo os grafos de avaliação
    avaliacao_dir = os.path.join(path, "basedados", "avaliacao_geral")

    # Criar diretório para salvar as imagens se não existir
    output_dir = os.path.join(path, "graphs")
    os.makedirs(output_dir, exist_ok=True)

    # Processar cada período de avaliação
    for period_label, filename in tqdm(evaluation_files):
        filepath = os.path.join(avaliacao_dir, filename)

        # Verificar se o arquivo existe
        if not os.path.exists(filepath):
            print(f"Arquivo não encontrado: {filepath}")
            continue

        # Ler o grafo
        try:
            graph = nx.read_gexf(filepath)
            print(f"Grafo carregado: {period_label}")
        except Exception as e:
            print(f"Erro ao carregar o grafo {filename}: {str(e)}")
            continue

        # Criar figura para o grafo atual
        plt.figure(figsize=(14, 12))

        # Calcular o número de vizinhos (grau) para cada vértice
        node_degrees = dict(graph.degree())

        # Encontrar os 5 vértices com maior grau
        top_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
        top_nodes_ids = [node[0] for node in top_nodes]

        # Criar uma lista de tamanhos de nós baseada no grau
        node_size_dict = {node: 30 + 5 * deg for node, deg in node_degrees.items()}
        for node_id in top_nodes_ids:
            node_size_dict[node_id] = node_size_dict[node_id] * 1.5  # Aumentar em 50%

        node_sizes = [node_size_dict[node] for node in graph.nodes()]

        # Definir cores dos nós (destacando os top 5)
        node_colors = ['red' if node in top_nodes_ids else 'skyblue' for node in graph.nodes()]

        # Definir cores das arestas (vermelha para ligação entre membros permanentes, preta caso contrário)
        edge_colors = []
        for u, v, data in graph.edges(data=True):
            is_u_permanent = graph.nodes[u].get('is_permanent', False)
            is_v_permanent = graph.nodes[v].get('is_permanent', False)

            if is_u_permanent and is_v_permanent:
                edge_colors.append('red')
            else:
                edge_colors.append('black')

        # Definir larguras das arestas baseadas no número de citações
        edge_widths = []
        for u, v, data in graph.edges(data=True):
            citation_num = data.get('citation_num', 1)  # Valor padrão: 1
            # Normalizar para evitar arestas muito finas ou muito grossas
            width = 0.5 + 0.5 * np.log1p(citation_num)  # log(1+x) para evitar log(0)
            edge_widths.append(width)

        # Calcular o layout (posicionamento dos nós)
        pos = nx.spring_layout(graph, seed=42)  # Seed para reprodutibilidade

        # Desenhar o grafo
        nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
        nx.draw_networkx_edges(graph, pos, width=edge_widths, edge_color=edge_colors, alpha=0.6)

        # Adicionar rótulos apenas para os top 5 nós
        labels = {node: node for node in top_nodes_ids}
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, font_weight='bold')

        # Adicionar título e outras configurações
        plt.title(f"Rede de Autores - {period_label}", fontsize=16)
        plt.axis('off')  # Desabilitar eixos

        # Adicionar legenda
        plt.legend(handles=[
            plt.Line2D([0], [0], color='red', lw=2, label='Ligação entre membros permanentes'),
            plt.Line2D([0], [0], color='black', lw=2, label='Outras ligações'),
            plt.scatter([0], [0], s=100, color='red', label='Top 5 autores'),
            plt.scatter([0], [0], s=100, color='skyblue', label='Outros autores')
        ], loc='upper right')

        # Salvar a figura
        output_file = os.path.join(r'\Users\minna\OneDrive\Área de Trabalho\AED II\IAN REPOSITÓRIO\Trabalho 2\TASK2', f"network_graph_{period_label}.png")
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Grafo salvo: {output_file}")

        plt.close()