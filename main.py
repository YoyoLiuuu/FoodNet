from __future__ import annotations
import pre_processing
import visualize_graph
import sys
from louvain import louvain_algorithm_init, graph_to_weighted_graph, get_weighted_graph

sys.setrecursionlimit(60000)  # change recursion limit so recursion error doesn't occur

# graph, all_data_vertices = pre_processing.get_graph('test_nodes.txt', 'test_edges.txt')
graph, all_data_vertices = pre_processing.get_graph('fb-pages-food-nodes.txt', 'fb-pages-food-edges.txt')
# all_data_vertices: a dictionary mapping id (item for Vertex) to name of artist
# visualize_graph.visualize_graph(graph)

print('graph done')

adjacent_matrix = graph.make_adjacent_matrix()

communities, modularity = louvain_algorithm_init(graph, adjacent_matrix)
new_communities = {i.item: communities[i] for i in communities}
the_communities = new_communities.copy()
sorted(new_communities.items(), key=lambda x: x[1])
weighted_init_graph = graph_to_weighted_graph(graph)
louvain_graph = graph

modularity_increase = 1

while abs(modularity_increase) > 0.001:
    prev_louvain_graph = louvain_graph
    louvain_graph = get_weighted_graph(louvain_graph, new_communities)
    adjacent_matrix = louvain_graph.make_adjacent_matrix()
    curr_modularity = modularity
    prev_communities = new_communities
    the_communities, modularity = louvain_algorithm_init(louvain_graph, adjacent_matrix)
    new_communities = {i.item: the_communities[i] for i in the_communities}
    modularity_increase = modularity - curr_modularity
    if modularity_increase < 0:
        new_communities = prev_communities
        louvain_graph = prev_louvain_graph

communities_to_members = []

for i in the_communities:
    communities_to_members.append({all_data_vertices[num] for num in i.members})

print(communities_to_members)

# visualize communities -> but no edges shown between communities
for vertex in graph._vertices:
    graph._vertices[vertex].item = all_data_vertices[vertex]

visualize_graph.visualize_graph_clusters(graph, communities_to_members)

