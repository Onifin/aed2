import kagglehub

from functions import *
from functions_plots import *
from functions_task2 import *
from functions_task3 import *

# DOWNLOAD LATEST VERSION
path = kagglehub.dataset_download("ian9090/co-autoria-ppgeec")
print("PATH TO DATASET FILES:", path)

n_d_list, n_n_list, n_e_list, a_d_list, d_d_list = compute_metrics(path)
plot_metrics(n_d_list, n_n_list, n_e_list, a_d_list)
plot_degree_distribution_grouped(d_d_list)

d_d_list = [dict(counter) for counter in d_d_list]
plot_ridgeline(d_d_list, n_e_list, years=None, figsize=(12, 8),
                   overlap=0, palette="viridis", alpha=1,
                   title="Distribuição de Frequências por Ano",
                   xlabel="Valor", ylabel="Ano")

print_graphs(path)


avaliacao_dir = os.path.join(path, "basedados", "avaliacao_geral")
print(os.listdir(avaliacao_dir))

graph = nx.read_gexf(os.path.join(avaliacao_dir, "2010-2025.gexf"))
print(graph.number_of_nodes())

graph.remove_nodes_from
graph.subgraph
print(graph.nodes['7004474343'])

graph.nodes(data=True)

lista_de_professores_permanentes = [node for node, data in graph.nodes(data=True) if data.get('is_permanent', True)]

numero_de_arestas = [len(list(graph.neighbors(subject[0]))) for subject in graph.nodes(data=True) if not subject[1].get('is_permanent')]
numero_medio_de_arestas = sum(numero_de_arestas) / len(numero_de_arestas)
numero_medio_de_arestas

type(numero_medio_de_arestas)

nos_com_mais_vizinhos_que_media = [subject[0] for subject in graph.nodes(data=True) if len(list(graph.neighbors(subject[0]))) > numero_medio_de_arestas]

subgrafo = graph.subgraph(nos_com_mais_vizinhos_que_media)

print("Densidade do grafo: ", nx.density(graph))
print("Densidade do subgrafo: ", nx.density(subgrafo))

#visualizar_grafos(graph, subgrafo, titulo_original="Grafo Original", titulo_subgrafo="Subgrafo")

for professor in lista_de_professores_permanentes:
  print(graph.nodes[professor])
  print(len(list(graph.neighbors(professor))))


colaboradores_firmino = list(graph.neighbors('6603603627'))
for i in range(len(colaboradores_firmino)):
  print(graph.nodes[colaboradores_firmino[i]])

ego_node = '6603603627'  # O nó central da rede ego
visualizar_rede_ego(ego_node, graph, radius=1)
