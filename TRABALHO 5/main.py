from libs import *
from clusters import *
from functions import *
from algorithms import *


left, bottom, right, top = -35.3150, -5.8850, -35.1700, -5.7000
# Importando o grafo a partir da bounding box
G = ox.graph_from_bbox(bbox = (left, bottom, right, top), network_type='drive')


# Estabelecimento da origem no grafo
orig_coords = (-5.753265931760308, -35.26269411137159) # Unidade de Vigilancia de Zoonoses Natal
orig_node = ox.distance.nearest_nodes(G, X=orig_coords[1], Y=orig_coords[0]) #Encontrando o nó mais próximo a unidade


# Substitua 'arquivo.csv' pelo caminho do seu arquivo
df = pd.read_csv('./db/centroid_filtered.csv')
# Mostrar as primeiras linhas do arquivo
df.head()





# ///////////// DEFINIÇÃO DOS CLUSTERS ///////////////////////
clusters_kmeans = create_clusters(df, 10, "k-means")
clusters_kmeans_constrained = create_clusters(df, 10, "k-means-constrained")
clusters_random = create_clusters(df, 10, "random")


# ////////////// PLOT DOS CLUSTERS ////////////////////////////
plot_clusters(G, clusters_kmeans, orig_coords, df, title="CLUSTERS K-MEANS")
plot_clusters(G, clusters_kmeans_constrained, orig_coords, df, title="CLUSTERS K-MEANS-CONSTRAINED")
plot_clusters(G, clusters_random, orig_coords, df, title="CLUSTERS ALEATÓRIOS")


# ///////////// DEFINIÇÃO DOS NODES PARA CADA TIPO ////////////
nodes_kmeans = find_nodes(G, clusters_kmeans, df)
nodes_kmeans_constrained = find_nodes(G, clusters_kmeans_constrained, df)
nodes_random = find_nodes(G, clusters_random, df)


# //////////////////  A*  /////////////////////
path = nx.astar_path(G, orig_node, nodes_kmeans[0][0] , weight='length')
points1, paths1, distances1, emissions1, times1 = find_all_goupe_routes(G, orig_node, nodes_kmeans, alg="a*")
points2, paths2, distances2, emissions2, times2 = find_all_goupe_routes(G, orig_node, nodes_kmeans_constrained, alg="a*")
points3, paths3, distances3, emissions3, times3 = find_all_goupe_routes(G, orig_node, nodes_random, alg="a*")

results = pd.DataFrame({
    'distance_astar_kmeans': distances1,
    'emission_astar_kmeans': emissions1,
    'time_astar_kmeans': times1,
    'distance_astar_kmeans_constrained': distances2,
    'emission_astar_kmeans_constrained': emissions2,
    'time_astar_kmeans_constrained': times2,
    'distance_astar_random': distances3,
    'emission_astar_random': emissions3,
    'time_astar_random': times3
})

results.to_csv('./db/dados_astar.csv', index=False)

print(results)


plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO A* PARA O CLUSTER K-MEANS", "astar_kmeans")
plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO A* PARA O CLUSTER K-MEANS CONSTRAINED", "astar_kmeans_constrained")
plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO A* PARA O CLUSTER ALEATÓRIO ", "astar_random")


# //////////////// DIJSKTRA MIN-HEAP //////////////////
points1, paths1, distances1, emissions1, times1 = find_all_goupe_routes(G, orig_node, nodes_kmeans, alg="dijkstra_heap")
points2, paths2, distances2, emissions2, times2 = find_all_goupe_routes(G, orig_node, nodes_kmeans_constrained, alg="dijkstra_heap")
points3, paths3, distances3, emissions3, times3 = find_all_goupe_routes(G, orig_node, nodes_random, alg="dijkstra_heap")

results = pd.DataFrame({
    'distance_dijkstra_heap_kmeans': distances1,
    'emission_dijkstra_heap_kmeans': emissions1,
    'time_dijkstra_heap_kmeans': times1,
    'distance_dijkstra_heap_kmeans_constrained': distances2,
    'emission_dijkstra_heap_kmeans_constrained': emissions2,
    'time_dijkstra_heap_kmeans_constrained': times2,
    'distance_dijkstra_heap_random': distances3,
    'emission_dijkstra_heap_random': emissions3,
    'time_dijkstra_heap_random': times3
})

results.to_csv('dados_dijkstra_heap.csv', index=False)

print(results)

plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO DIJKSTRA COM MIN-HEAP PARA O CLUSTER K-MEANS", "dijkstra_heap_kmeans")
plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO DIJKSTRA COM MIN-HEAP PARA O CLUSTER K-MEANS CONSTRAINED", "dijkstra_heap_kmeans_constrained")
plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO DIJKSTRA COM MIN-HEAP PARA O CLUSTER ALEATÓRIO ", "dijkstra_heap_random")



# //////////////// DIJSKTRA  //////////////////
points1, paths1, distances1, emissions1, times1 = find_all_goupe_routes(G, orig_node, nodes_kmeans, alg="dijkstra")
points2, paths2, distances2, emissions2, times2 = find_all_goupe_routes(G, orig_node, nodes_kmeans_constrained, alg="dijkstra")
points3, paths3, distances3, emissions3, times3 = find_all_goupe_routes(G, orig_node, nodes_random, alg="dijkstra")

results = pd.DataFrame({
    'distance_dijkstra_kmeans': distances1,
    'emission_dijkstra_kmeans': emissions1,
    'time_dijkstra_kmeans': times1,
    'distance_dijkstra_kmeans_constrained': distances2,
    'emission_dijkstra_kmeans_constrained': emissions2,
    'time_dijkstra_kmeans_constrained': times2,
    'distance_dijkstra_random': distances3,
    'emission_dijkstra_random': emissions3,
    'time_dijkstra_random': times3
})

results.to_csv('dados_dijkstra.csv', index=False)

print(results)

plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO DIJKSTRA PARA O CLUSTER K-MEANS", "dijkstra_kmeans")
plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO DIJKSTRA PARA O CLUSTER K-MEANS CONSTRAINED", "dijkstra_kmeans_constrained")
plot_clusters_and_routes(G, clusters_kmeans, paths1, orig_coords, df, "ROTAS DO ALGORITMO DIJKSTRA PARA O CLUSTER ALEATÓRIO ", "dijkstra_random")