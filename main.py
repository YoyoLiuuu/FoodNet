from __future__ import annotations
import pre_processing
import visualize_graph
import sys
from random import randint
from louvain import louvain_algorithm_init, graph_to_weighted_graph, get_weighted_graph

sys.setrecursionlimit(60000)  # change recursion limit so recursion error doesn't occur

graph, all_data_vertices = pre_processing.get_graph('fb-pages-food-nodes.txt', 'fb-pages-food-edges.txt')

# graph, all_data_vertices = pre_processing.get_graph('test_nodes.txt', 'test_edges.txt')
# all_data_vertices: a dictionary mapping id (item for Vertex) to name of artist
# visualize_graph.visualize_graph(graph)

print('graph done')

adjacent_matrix = graph.make_adjacent_matrix()

communities, modularity = louvain_algorithm_init(graph, adjacent_matrix)
new_communities = {i.item: communities[i] for i in communities}
sorted(new_communities.items(), key=lambda x: x[1])
weighted_init_graph = graph_to_weighted_graph(graph)
louvain_graph = graph

modularity_increase = 1

while modularity_increase > 0.01:
    louvain_graph = get_weighted_graph(louvain_graph, new_communities)
    adjacent_matrix = louvain_graph.make_adjacent_matrix()
    curr_modularity = modularity
    new_communities, modularity = louvain_algorithm_init(louvain_graph, adjacent_matrix)
    new_communities = {i.item: (i.members, new_communities[i]) for i in new_communities}
    modularity_increase = modularity - curr_modularity

    print(new_communities)

