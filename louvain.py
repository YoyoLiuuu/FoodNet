from classes import Graph, WeightedGraph, _Vertex, _WeightedVertex, _Community
from helper_functions import get_weighted_graph, get_edge_weights
from typing import Optional


def louvain_algorithm_init(graph: Graph, adjacency_matrix: dict[int, dict[int, int]]) -> (dict[_Vertex, int], float):
    """
    This function detects and forms communities using a modified version of the Louvain Algorithm
    """
    # initialize each vertex as its own community
    communities = {}
    i = 0
    for v in graph._vertices.values():
        communities[v] = i
        i += 1

    curr_modularity = graph.calculate_modularity_graph(communities, adjacency_matrix)

    for vertex in graph._vertices.values():

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
    docstring
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
    Edge weight always one
    """
    wg = WeightedGraph()
    for v in graph._vertices.values():
        wg.add_vertex(v.item)
        for u in v.neighbours:
            wg.add_vertex(u.item)
            wg.add_edge(u.item, v.item)

    return wg


def get_weighted_graph(g: WeightedGraph, communities: dict[int, int]) -> WeightedGraph:
    """
    Return the weighted graph given the dictionary of communites, where each community is one node

    The community id will be a tuple with the sum of edge weights in the community and an identifying integer

    >>> communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1}
    >>> g = WeightedGraph()
    >>> for i in range(1, 6):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> g.add_edge(3, 4)
    >>> g.add_edge(2, 5)
    >>> new_g = get_weighted_graph(g, communities)
    >>> new_g.get_weight(0, 1)
    2
    """
    communities_lst = g.make_community_dicts(communities)
    new_g = WeightedGraph()
    outer_edges = g.get_all_outer_edges(communities_lst)

    for c in communities_lst:
        inner_edge_weight = g.get_inner_edge_weights(c)
        new_g.add_community(get_comm_id(communities, c), inner_edge_weight, c)

    new_outer_edges = get_edge_weights(communities, outer_edges)

    for edges in new_outer_edges:
        weight = edges[1]
        comm_ids = edges[0]

        new_g.add_edge(comm_ids[0], comm_ids[1], weight)

    return new_g


def get_comm_id(all_communities: dict[int, int], community: [int, _Vertex]):
    """
    Return the id of a community
    """
    for c in community:
        return all_communities[c]