from __future__ import annotations
import pre_processing
import visualize_graph
import sys

sys.setrecursionlimit(60000)



graph, all_data_vertices = pre_processing.get_graph()
# all_data_vertices: a dictionary mapping id (item for Vertex) to name of artist
# visualize_graph.visualize_graph(graph)

print(graph.make_adjacent_matrix())