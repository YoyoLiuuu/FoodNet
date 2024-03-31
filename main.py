from __future__ import annotations
import pre_processing
import visualize_graph
import sys

sys.setrecursionlimit(60000)  # change recursion limit so recursion error doesn't occur

graph, all_data_vertices = pre_processing.get_graph('test_nodes.txt', 'test_edges.txt')
# all_data_vertices: a dictionary mapping id (item for Vertex) to name of artist
# visualize_graph.visualize_graph(graph)

adjacent_matrix = graph.make_adjacent_matrix()

all_communities = graph.init_communities()

