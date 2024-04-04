from classes import Graph, WeightedGraph, _Vertex, _WeightedVertex, _Community
from helper_functions import get_weighted_graph, get_edge_weights
from typing import Optional


def louvain_algorithm(graph: Graph, adjacency_matrix: dict[int, dict[int, int]]) -> (dict[_Vertex, int], float):
    """
    This function detects and forms communities using a modified version of the Louvain Algorithm.
    """
    # initialize each vertex as its own community
    communities = {}
    i = 0
    for v in graph.vertices.values():
        communities[v] = i
        i += 1

    curr_modularity = graph.calculate_modularity_graph(communities, adjacency_matrix)

    for vertex in graph.vertices.values():

        # merge communities based on modularity calculations
        communities, curr_modularity = find_best_community(graph, vertex, communities, curr_modularity,
                                                           adjacency_matrix)
        # get modularity of new communities

    # reassign community numbers - can ignore for larger values of vertices -> runtime

    community_curr_values = set(communities.values())
    old_to_new = {}
    i = 0
    for value in community_curr_values:
        old_to_new[value] = i
        i += 1

    for key in communities:
        communities[key] = old_to_new[communities[key]]

    sorted_communities = dict(sorted(communities.items(), key=lambda x: x[1]))

    return sorted_communities, curr_modularity


def find_best_community(graph: Graph, v: _Vertex, communities: dict[_Vertex, int], init_modularity: float,
                        adjacency_matrix: dict[int, dict[int, int]]) -> (dict[_Vertex, int], float):
    """
    This function takes a vertex and finds the best community it belongs for the modularity score to be the highest.
    It iterates through all neighbours of the vertex and place the vertex in those communities, finding the modularity
    of each and return the community that yields the highest modularity.
    """
    best_community, best_modularity = communities, init_modularity
    neighbours_community = {communities[u] for u in v.neighbours}

    # iterate through every neighbour of v
    for community in neighbours_community:
        # place v in community and calculate new modularity
        if community != best_community:
            new_communities = communities.copy()
            new_communities[v] = community
            new_modularity = graph.calculate_modularity_graph(new_communities, adjacency_matrix)
            if new_modularity > best_modularity:
                best_community, best_modularity = new_communities, new_modularity

    return best_community, best_modularity


def graph_to_weighted_graph(graph: Graph) -> WeightedGraph:
    """
    This function converts graph to a weighted graph. In the new graph, the edge weight is always one.
    """
    wg = WeightedGraph()

    for v in graph.vertices.values():
        wg.add_vertex(v.item)
        for u in v.neighbours:
            wg.add_vertex(u.item)
            wg.add_edge(u.item, v.item)

    return wg
