<p align="center">
  <img src="IMGs/DCA.png" alt="Logo da UFRN"/>
</p>

<p align="center"><strong>UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE</strong></p>

<p align="center"> 
DEPARTAMENTO DE ENGENHARIA DE COMPUTAÇÃO E AUTOMAÇÃO  
DCA3702 - ALGORITMOS E ESTRUTURAS DE DADOS II  
</p>

<h2 align="center"><strong>PROJETO 01</strong></h2>

**Discentes**: Ian Antonio Fonseca Araújo, Minnael Campelo de Oliveira  
**Docente**: Ivanovitch Medeiros Dantas da Silva  

**Natal/RN — 2025**

## 1. Problemática

Em centros urbanos, a eficiência na escolha de rotas para serviços de entrega é crucial para reduzir custos, economizar tempo e minimizar impactos ambientais. Este projeto visa avaliar o desempenho de diferentes algoritmos de menor caminho aplicados a um cenário realista de entrega por motoboys em Natal/RN.

O foco será comparar a performance de três algoritmos de menor caminho — a implementação do OSMnx, Dijkstra tradicional e Dijkstra com min-heap — considerando critérios como tempo de execução, semelhança nas rotas e pegada de carbono.

## 2. Desenvolvimento

O cenário escolhido para este projeto foi o de rotas de entrega realizadas por motoboys na cidade de Natal/RN. A simulação considera como ponto de partida a Avenida Prudente de Morais, uma das principais vias da cidade, em direção a três bairros distintos: Neópolis, Candelária e Capim Macio.

Para cada um desses três destinos, foram testadas rotas utilizando três algoritmos distintos de menor caminho. O objetivo principal foi simular situações reais de entrega e verificar quais algoritmos conseguem gerar caminhos mais rápidos e eficientes, considerando o tempo de execução, a qualidade da rota e o impacto ambiental gerado pelo processamento computacional.

Para garantir uma comparação justa, cada algoritmo foi aplicado exatamente às mesmas três rotas (Prudente de Morais → Neópolis, Candelária e Capim Macio), totalizando nove simulações no conjunto do experimento. Dessa forma, foi possível analisar o comportamento dos algoritmos sob condições semelhantes.

Adicionalmente, foi criada uma API que retorna o caminho atualizado em função de sua posição em determinado tempo. O código-fonte e instruções para utilização estão disponíveis no seguinte repositório: [link]

## 3. Resultados

### Mapas das rotas geradas  

<img src="results/rota_dijkstra_tradicional.png" alt="Rota Dijkstra Tradicional" width="600"/>
<img src="results/rota_dijkstra_heap.png" alt="Rota Dijkstra com Heap" width="600"/>
<img src="results/rota_osmnx.png" alt="Rota OSMnx" width="600"/>

### Tempo de Execução dos Algoritmos  

<img src="results/tempo_execucao.png" alt="Comparação de tempos de execução" width="600"/>

### Pegada de Carbono (em kgCO2eq)  

<img src="results/pegada_carbono.png" alt="Pegada de carbono dos algoritmos" width="600"/>

## 4. Conclusão

A avaliação mostrou que o algoritmo Dijkstra com minheap proporciona uma boa relação entre desempenho computacional e qualidade da rota. 

## Vídeo Explicativo

[Link para o vídeo no YouTube ou Loom](https://www.youtube.com/seuvideoaqui)
