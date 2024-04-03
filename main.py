from __future__ import annotations
import pre_processing
import visualize_graph
import sys
from louvain import louvain_algorithm, graph_to_weighted_graph, get_weighted_graph
from helper_functions import get_all_members

sys.setrecursionlimit(60000)  # change recursion limit so recursion error doesn't occur

graph, all_data_vertices = pre_processing.get_graph('test_nodes.txt', 'test_edges.txt')
# graph, all_data_vertices = pre_processing.get_graph('fb-pages-food-nodes.txt', 'fb-pages-food-edges.txt')
# all_data_vertices: a dictionary mapping id (item for Vertex) to name of artist
# visualize_graph.visualize_graph(graph)

print('graph done')

adjacent_matrix = graph.make_adjacent_matrix()

communities, modularity = louvain_algorithm(graph, adjacent_matrix)
new_communities = {i.item: communities[i] for i in communities}
the_communities = new_communities.copy()
sorted(new_communities.items(), key=lambda x: x[1])
weighted_init_graph = graph_to_weighted_graph(graph)
louvain_graph = graph

modularity_increases = [1, 1, 1]

while all({abs(modularity_gain) > 0.01 for modularity_gain in modularity_increases[-3:]}):
    print('hi')
    prev_louvain_graph = louvain_graph
    louvain_graph = get_weighted_graph(louvain_graph, new_communities)
    adjacent_matrix = louvain_graph.make_adjacent_matrix()
    curr_modularity = modularity
    prev_communities = new_communities
    the_communities, modularity = louvain_algorithm(louvain_graph, adjacent_matrix)
    new_communities = {i.item: the_communities[i] for i in the_communities}
    modularity_increases.append(modularity - curr_modularity)
    if modularity_increases[-1] < 0:
        new_communities = prev_communities
        louvain_graph = prev_louvain_graph

vertex_to_community = {}

for community in the_communities:
    members = get_all_members(community)
    for vertex_value in members:
        vertex_to_community[all_data_vertices[vertex_value]] = the_communities[community]

# visualize communities -> but no edges shown between communities
for vertex in graph._vertices:
    graph._vertices[vertex].item = all_data_vertices[vertex]

print(graph._vertices)

print(members, len(the_communities))
print(all_data_vertices)
