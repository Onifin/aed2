import kagglehub

from functions import *
from functions_plots import *

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
