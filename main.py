from __future__ import annotations
import pre_processing
import visualize_graph
import sys
from random import randint
from louvain import louvain_algorithm_init, graph_to_weighted_graph, get_weighted_graph

sys.setrecursionlimit(60000)  # change recursion limit so recursion error doesn't occur

graph, all_data_vertices = pre_processing.get_graph('fb-pages-artist-nodes.txt', 'fb-pages-artist-edges.txt')
# all_data_vertices: a dictionary mapping id (item for Vertex) to name of artist
# visualize_graph.visualize_graph(graph)

adjacent_matrix = graph.make_adjacent_matrix()

new_communities, modularity = louvain_algorithm_init(graph, adjacent_matrix)

new_communities = {i.item: new_communities[i] for i in new_communities}
print(new_communities)

weighted_init_graph = graph_to_weighted_graph(graph)

louvain_run_once = get_weighted_graph(graph, new_communities)

print(louvain_run_once)

print(new_communities)
