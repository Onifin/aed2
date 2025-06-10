
## LLM UTILIZADA: CLAUDE
### Prompt
Faça um gráfico de colunas desses comparando os valores dos três vetores usando matplotlib:

distancia_astar_kmeans = df_astar['distance_astar_kmeans']
distancia_djk_heap_kmeans = df_djk_heap['distance_dijkstra_heap_kmeans']
distancia_djk_kmeans = df_djk_1['distance_dijkstra_kmeans']


Ajuste para escala logarimica com matplotlib:

Calcular o tempo total

tempo_total_astar_kmeans = sum(tempo_astar_kmeans)
tempo_total_djk_heap_kmeans = sum(tempo_djk_heap_kmeans)
tempo_total_djk_kmeans = sum(tempo_djk_kmeans)

tempo_total_astar_kmeans_constrained = sum(tempo_astar_kmeans_constrained)
tempo_total_djk_heap_kmeans_constrained = sum(tempo_djk_heap_kmeans_constrained)
tempo_total_djk_kmeans_constrained = sum(tempo_djk_kmeans_constrained)



## LLM UTILIZADA - GEMINI

### Prompt
Faça uma busca de um algoritmo de clusters que consiga dividir a quantidade de pontos igualmente por cluster.



