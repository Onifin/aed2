<p align="center">
  <img src="IMGs/DCA.png" alt="Logo da UFRN" width=300/>
</p>

<h3 align="center"><strong>UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE</strong></h3>

<p align="center"> 
DEPARTAMENTO DE ENGENHARIA DE COMPUTAÇÃO E AUTOMAÇÃO 
<br> 
DCA3702 - ALGORITMOS E ESTRUTURAS DE DADOS II  
</p>

<h1 align="center"><strong>PROJETO 05 - EXPLORANDO O ALGORITMO A*</strong></h1>

<strong>DISCENTES:</strong>
- IAN ANTONIO FONSECA ARAÚJO 
- LUCAS GARCIA COSTA 
- MINNAEL CAMPELO DE OLIVEIRA  

<strong>DOCENTE:</strong> 
- IVANOVITCH MEDEIROS DANTAS DA SILVA 

**Natal/RN — 2025**

## <strong>1. PROBLEMÁTICA</strong>

<p align="justify">
No dia a dia do Centro de Controle de Zoonoses de Natal, 10 grupos precisam sair de uma estação central, visitar um conjunto de pontos espalhados pela cidade e retornar ao ponto de partida. No total, são 65 locais de visita divididos em quatro zonas da cidade, e todos devem ser atendidos. O desafio está em montar rotas inteligentes para cada grupo: que cubram todos os pontos, evitem caminhos desnecessários, reduzam o tempo total gasto e, de quebra, ajudem a economizar combustível e reduzir emissões de CO₂. Para isso, vamos aplicar algoritmos de busca de caminhos como A*, Dijkstra e Dijkstra com min-heap, utilizando mapas reais da cidade com bibliotecas como networkx e osmnx. O objetivo é comparar essas estratégias com uma abordagem aleatória e verificar qual entrega o melhor resultado, considerando:

- Tempo de execução
- Distância percorrida
- Impacto ambiental

Com isso, buscamos uma solução prática, eficiente e aplicável a situações reais de logística urbana, onde o planejamento de rotas pode fazer toda a diferença na produtividade e no uso consciente de recursos.
</p>


## <strong>2. DESENVOLVIMENTO</strong>

#### 2.1 MODELAGEM E ANÁLISE INICIAL
O desenvolvimento da solução teve início com a obtenção do grafo de ruas da cidade de Natal/RN, utilizando a biblioteca OSMnx, que fornece representações de redes viárias com base em dados do OpenStreetMap. A partir desse grafo, foi identificado o nó mais próximo da estação central, definido pelas coordenadas geográficas (-5.75326, -35.26269).
Em seguida, foi realizada a leitura de um conjunto de 65 pontos de coleta a partir de um arquivo CSV, contendo suas respectivas latitudes e longitudes. Esses pontos representam as residências ou locais que precisam ser visitados pelos colaboradores. Para organizar a distribuição dos pontos entre os 10 colaboradores, foi empregada a técnica de clusterização, permitindo dividir os pontos de coleta em grupos distintos. Três abordagens foram utilizadas:

- K-Means Tradicional:
Foi aplicado o algoritmo K-Means, com o número de clusters definido como 10. Essa abordagem distribui os pontos com base em similaridade espacial, sem restrição quanto ao número de elementos por grupo.

- K-Means Constrained:
Utilizou-se o algoritmo KMeansConstrained, que permite impor restrições de tamanho mínimo e máximo para os clusters. Cada grupo recebeu entre 6 e 7 pontos, o que garante uma distribuição mais uniforme entre os colaboradores.

- Distribuição Aleatória:
Uma abordagem não supervisionada foi implementada como base comparativa, onde os pontos foram atribuídos aleatoriamente aos grupos. Essa estratégia serve de benchmark para as demais técnicas otimizadas.

Cada cluster gerado representa a rota potencial de um colaborador. Para visualização, os grupos foram plotados sobre o grafo da cidade com a função plot_clusters(), destacando cada conjunto de pontos com uma cor diferente e indicando a estação central como ponto de partida comum. 

<p align="center">
  <img src="IMGs/KMEANS.png" width="330" height="430"/>
  <img src="IMGs/KMEANSRESTRICAO.png" width="330" height="430"/>
  <img src="IMGs/RANDOM.png" width="330" height="430"/>
</p>

Sendo assim, será apresentado o desenvolvimento relacionado as implementações dos algoritmos de roteamento interno para cada cluster. A ideia é, para cada grupo de pontos:

- Calcular a menor rota possível partindo e retornando à estação central;
- Utilizar algoritmos de caminho mínimo: Dijkstra, Dijkstra com Min-Heap e A*;
- Armazenar as métricas de tempo de execução, distância percorrida e estimativa de emissão de CO₂.

Esses algoritmos serão aplicados sobre o grafo G previamente carregado, garantindo que a otimização ocorra respeitando a malha urbana real da cidade. O código atual está estruturado de forma modular, com funções reutilizáveis para a criação de clusters e visualização, o que permitirá integração eficiente com as rotinas de roteamento.


#### 2.2 ROTAS E CLUSTERS NO GRAFO A*

<p align="center">
  <img src="IMGs/astar_kmeans.png" width="330" height="430"/>
  <img src="IMGs/astar_kmeans_constrained.png" width="330" height="430"/>
  <img src="IMGs/astar_random.png" width="330" height="430"/>
</p>


#### 2.3 ROTAS E CLUSTERS NO DIJKSTRA HEAP

<p align="center">
  <img src="IMGs/dijkstra_heap_kmeans.png" width="330" height="430"/>
  <img src="IMGs/dijkstra_heap_kmeans_constrained.png" width="335" height="430"/>
  <img src="IMGs/dijkstra_heap_random.png" width="330" height="430"/>
</p>


#### 2.4 ROTAS E CLUSTERS NO DIJKSTRA CONVENCIONAL

<p align="center">
  <img src="IMGs/dijkstra_kmeans.png" width="330" height="430"/>
  <img src="IMGs/dijkstra_kmeans_constrained.png" width="335" height="430"/>
  <img src="IMGs/dijkstra_random.png" width="335" height="430"/>
</p>

## <strong>3. RESULTADOS</strong>

#### 3.1 ANÁLISE DE TEMPO
A análise dos tempos totais mostra que o algoritmo Dijkstra convencional é significativamente mais lento que as outras abordagens, especialmente quando combinado com K-means ou Random, atingindo tempos superiores a 10.000 segundos. Em contraste, A* e Dijkstra com heap têm desempenhos muito superiores, com tempos na casa de dezenas de segundos, principalmente ao serem combinados com K-means Constrained. Isso demonstra a importância de utilizar estruturas de dados eficientes (como heaps) e heurísticas (como no A*) para acelerar a execução.

<p align="center">
  <img src="IMGs/tempos.png" alt="Logo da UFRN" width=1000/>
</p>

#### 3.2 ANÁLISE DE DISTÂNCIA
Em relação à distância total percorrida, os algoritmos baseados em Random são claramente os menos eficientes, superando os 500.000 m. Em contraste, todas as combinações que utilizam K-means ou K-means Constrained resultam em distâncias significativamente menores, próximas de 270.000–280.000 m. Isso indica que estratégias de agrupamento orientadas reduzem bastante o custo do percurso, melhorando a qualidade das rotas geradas.


<p align="center">
  <img src="IMGs/dist.png" alt="Logo da UFRN" width=1000/>
</p>

#### 3.3 ANÁLISE DA EMISSÃO DE CO2
Quanto às emissões de CO₂, o padrão segue o observado no tempo: algoritmos mais lentos geram mais emissões. As combinações Dijkstra + K-means e Dijkstra + Random são as mais poluentes, com emissões de carbono consideráveis. Já as abordagens mais rápidas, como A* + K-means Constrained e Dijkstra Heap + K-means Constrained, têm impacto ambiental muito reduzido, com emissões próximas a 10⁻⁴ kg de CO₂, mostrando que otimização algorítmicas também traz benefícios sustentáveis.

<p align="center">
  <img src="IMGs/emissoes.png" alt="Logo da UFRN" width=1000/>
</p>

De forma geral, as melhores escolhas combinam algoritmos eficientes (como A* ou Dijkstra com heap) com métodos inteligentes de agrupamento (especialmente K-means Constrained). Essas combinações oferecem ótimo desempenho em tempo, baixa emissão de CO₂ e rotas mais curtas. Já abordagens aleatórias ou o uso de Dijkstra sem otimizações devem ser evitadas, pois comprometem seriamente a performance e eficiência do sistema.


## <strong>4. CONCLUSÃO</strong>
O presente trabalho apresentou uma solução eficiente para o roteamento dos colaboradores do Centro de Controle de Zoonoses de Natal/RN, com base em 65 pontos de coleta distribuídos por toda a cidade. A estratégia adotada envolveu a clusterização dos pontos em 10 grupos, utilizando os métodos K-Means, K-Means Constrained e uma abordagem aleatória como base comparativa. A aplicação da clusterização com restrições demonstrou melhor equilíbrio na distribuição dos pontos entre os colaboradores. Em seguida, os algoritmos Dijkstra, Dijkstra com Min-Heap e A* foram utilizados para calcular rotas otimizadas dentro de cada cluster, sempre partindo e retornando à estação central, sobre o grafo viário real obtido com OSMnx. As métricas de distância, tempo de execução e estimativa de CO₂ permitiram comparar as abordagens, revelando que os métodos otimizados superam significativamente a distribuição aleatória em termos de eficiência operacional. Concluímos que a combinação de clusterização balanceada e algoritmos de caminho mínimo oferece uma solução prática, escalável e aplicável a diversos cenários de logística urbana.



## Vídeo Explicativo

[Link para o vídeo no YouTube ou Loom](https://youtu.be/hPSra4taCoQ)

## Informações Complementares

- Os prompts utilizados no projeto estão contidos na pasta [MD](https://github.com/Onifin/aed2/tree/main/TRABALHO%205/MD)
- Os arquivos jupyter notebook utilizados estão na pasta [JUPYTER](https://github.com/Onifin/aed2/tree/main/TRABALHO%205/JUPYTER)
