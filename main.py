from __future__ import annotations
import pre_processing
import visualize_graph
import sys
from random import randint

sys.setrecursionlimit(60000)  # change recursion limit so recursion error doesn't occur

graph, all_data_vertices = pre_processing.get_graph('test_nodes.txt', 'test_edges.txt')
# all_data_vertices: a dictionary mapping id (item for Vertex) to name of artist
# visualize_graph.visualize_graph(graph)

adjacent_matrix = graph.make_adjacent_matrix()

communities = {}


for vertex in graph._vertices.values():
    communities[vertex] = randint(9, 10)

score = graph.calculate_modularity_graph(communities, adjacent_matrix)

print(score)

# communities visualization 

def set_to_dict(communities:list[set]) -> dict:
    dct = {}
    for i in range(0, len(communities)):
        for node in communities[i]:
            dct[node] = i
    return dct

def test():
    """
    Test function
    """
    G = nx.karate_club_graph()  # load a default graph

    partition = community.best_partition(G)  # compute communities

    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.colormaps.get_cmap('RdYlBu'), node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw(G, with_labels=True)
    # plt.show(G)
    return G
