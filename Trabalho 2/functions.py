import os
import networkx as nx
from collections import Counter


def network_density(graph):
  return nx.density(graph)

def network_number_of_nodes(graph):
  return nx.number_of_nodes(graph)

def network_number_of_edges(graph):
  return nx.number_of_edges(graph)

def average_degree(graph):
  return (sum([degree for _, degree in graph.degree()]) / network_number_of_nodes(graph))

def degree_distribution(graph):
  return Counter([degree for _, degree in graph.degree()])

def compute_metrics(path):

  n_d_list = []
  n_n_list = []
  n_e_list = []
  a_d_list = []
  d_d_list = []

  for i in range(10, len(os.listdir(path+"/basedados/anos"))+10):
    filepath = f"{path}/basedados/anos/20{i}_authors_network.gexf"
    graph = nx.read_gexf(filepath)

    n_d = network_density(graph)
    n_n = network_number_of_nodes(graph)
    n_e = network_number_of_edges(graph)
    a_d = average_degree(graph)
    d_d = degree_distribution(graph)

    n_d_list.append(n_d)
    n_n_list.append(n_n)
    n_e_list.append(n_e)
    a_d_list.append(a_d)
    d_d_list.append(d_d)

  return n_d_list, n_n_list, n_e_list, a_d_list, d_d_list