# README

Este trabalho consiste em criar uma nova versão de um notebook Jupyter com uma introdução à biblioteca NetworkX, no estilo **"hands on"**. Para isso, utilizei o modelo de prompt criado por **Dan Mac (@daniel_mac8)** no X (antigo Twitter) passando como contexto o notebook anterior e trechos do livro texto com a teoria.

## O que foi feito?

- **Notebook Hands On:**  
  Foi criado um notebook que introduz conceitos de grafos, como:
  - Grafos simples (não direcionados, sem laços e sem arestas paralelas)
  - Grafos direcionados
  - Grafos ponderados

  Cada seção apresenta uma breve explicação teórica seguida de atividades práticas utilizando a biblioteca Python **NetworkX** e visualizações com **Matplotlib**.

  O netebook também foi traduzido para o português.

- **Integração da Teoria:**  
  A teoria utilizada foi extraída dos capítulos do livro *"The Atlas for the Aspiring Network Scientist"*, que foi enviado como um PDF. Os capítulos foram resumidos e organizados para serem apresentados nos momentos adequados do notebook, facilitando o entendimento e a aplicação prática dos conceitos.

- **Modelo de Prompt:**  
  ```plaintext
  Eu quero que você faça um notebook no estilo "Hands on" baseado no notebook enviado de anexo. Use o texto do pdf enviado que possui a teoria sobre grafos. O estilo hands-on é uma postura ativa, que envolve a participação direta em atividades, em vez de apenas coordenar ou gerenciar

  Retorne o notebook em uma formatação parecida com a do anexo jupyter.

  O notebook criado deve estar em português. A teoria deve estar escrita resumidamente em seu devido local no notebook.

  Contexto: Você possui um notebook jupyter e um arquivo pdf com a teoria.
  ```
