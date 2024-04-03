from __future__ import annotations
from classes import WeightedGraph, _Vertex

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


def get_edge_weights(communties: dict[int, int], outer_edges: list[set]) -> list[tuple[list[int], int]]:
    """
    Return a dictionary of edges with their new community ids and weights

    >>> communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2}
    >>> outer_edges = [{5, 2}, {4, 3}]
    >>> get_edge_weights(communities, outer_edges)
    [([0, 2], 1), ([0, 1], 1)]
    >>> communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1}
    >>> get_edge_weights(communities, outer_edges)
    [([0, 1], 2)]
    """
    edges_dict = {}
    for edge in outer_edges:
        edge_name = set()
        for v in edge:
            edge_name.add(communties[v])

        edge_name = frozenset(edge_name)

        if edge_name in edges_dict:
            edges_dict[edge_name] += 1
        else:
            edges_dict[edge_name] = 1

    return [(list(key), edges_dict[key]) for key in edges_dict]

