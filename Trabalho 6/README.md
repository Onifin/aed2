# 🌐 Do Grão ao Grafo: Conectando Cafeterias com o Algoritmo de Kruskal

Este projeto demonstra a aplicação do algoritmo de Kruskal para gerar uma **Árvore Geradora Mínima (MST)** conectando cafeterias na cidade de **Natal — RN, Brasil**, utilizando dados do **OpenStreetMap** com a biblioteca **OSMNX**.

---

## 📌 Objetivo

Construir uma rota com o menor custo total possível (em metros), conectando os pontos de interesse (cafeterias), sem formar ciclos. Para isso, utilizamos o algoritmo guloso de Kruskal aplicado a grafos urbanos.

---

## 🧰 Tecnologias utilizadas

- Python 3
- [OSMNX](https://github.com/gboeing/osmnx)
- NetworkX
- OpenStreetMap (OSM)

---

## 🚀 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Onifin/aed2.git
   cd Trabalho\ 6
   ``` 

O script:

* Carrega o grafo viário de Natal-RN
* Localiza todas as cafeterias cadastradas no OSM
* Calcula rotas mínimas entre elas
* Constrói a MST conectando os pontos

---

## 📈 Resultado

A saída informa o comprimento total da **"Rota da Cafeína"**, ou seja, a árvore geradora mínima entre as cafeterias mapeadas.

## 🔗 Referências

* Artigo completo no Medium:
  📄 [Do Grão ao Grafo: Conectando Cafeterias com o Algoritmo de Kruskal](https://medium.com/@onifin/do-gr%C3%A3o-ao-grafo-conectando-cafeterias-com-o-algoritmo-de-kruskal-65a857c3dcfc)

* Episódio do podcast sobre o projeto:
  🎧 [NotebookLM Podcast](https://notebooklm.google.com/notebook/40f4d4a8-84d8-448e-91e9-4717b2a64458/audio)

