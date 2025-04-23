import kagglehub

from functions import *
from functions_plots import *
from functions_task2 import *

# DOWNLOAD LATEST VERSION
path = kagglehub.dataset_download("ian9090/co-autoria-ppgeec")
print("PATH TO DATASET FILES:", path)

n_d_list, n_n_list, n_e_list, a_d_list, d_d_list = compute_metrics(path)
#plot_metrics(n_d_list, n_n_list, n_e_list, a_d_list)
#plot_degree_distribution_grouped(d_d_list)

d_d_list = [dict(counter) for counter in d_d_list]
'''plot_ridgeline(d_d_list, n_e_list, years=None, figsize=(12, 8),
                   overlap=0, palette="viridis", alpha=1,
                   title="Distribuição de Frequências por Ano",
                   xlabel="Valor", ylabel="Ano")'''

print_graphs(path)

avaliacao_dir = os.path.join(path, "basedados", "avaliacao_geral")
print(os.listdir(avaliacao_dir))

graph = nx.read_gexf(os.path.join(avaliacao_dir, "2010-2025.gexf"))
print(graph.number_of_nodes())

graph.remove_nodes_from
graph.subgraph
print(graph.nodes['7004474343'])

graph.nodes(data=True)