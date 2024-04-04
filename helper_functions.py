from __future__ import annotations
from classes import WeightedGraph, _Vertex, _Community


def get_weighted_graph(g: WeightedGraph, communities: dict[int, int]) -> WeightedGraph:
    """
    Return the weighted graph given the dictionary of communites, where each community is one node

    The community id will be a tuple with the sum of edge weights in the community and an identifying integer

    Preconditions:
        - list(communites.values()) == sorted(communites.values())

    >>> communities_dict = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1}
    >>> g0 = WeightedGraph()
    >>> for i in range(1, 6):
    ...     g0.add_vertex(i)
    >>> g0.add_edge(1, 2)
    >>> g0.add_edge(2, 3)
    >>> g0.add_edge(1, 3)
    >>> g0.add_edge(3, 4)
    >>> g0.add_edge(2, 5)
    >>> g1 = get_weighted_graph(g0, communities_dict)
    >>> g1.get_weight(0, 1)
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
    Return the id of a community.
    """
    for c in community:
        return all_communities[c]


def get_edge_weights(communities: dict[int, int], outer_edges: list[set]) -> list[tuple[list[int], int]]:
    """
    Return a dictionary of edges with their new community ids and weights

    >>> ex_communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2}
    >>> ex_outer_edges = [{5, 2}, {4, 3}]
    >>> get_edge_weights(ex_communities, outer_edges)
    [([0, 2], 1), ([0, 1], 1)]
    >>> ex_communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1}
    >>> get_edge_weights(ex_communities, outer_edges)
    [([0, 1], 2)]
    """
    edges_dict = {}
    for edge in outer_edges:
        edge_name = set()
        for v in edge:
            edge_name.add(communities[v])

        edge_name = frozenset(edge_name)

        if edge_name in edges_dict:
            edges_dict[edge_name] += 1
        else:
            edges_dict[edge_name] = 1

    return [(list(key), edges_dict[key]) for key in edges_dict]


def get_all_members(community: _Vertex) -> dict[int, _Vertex]:
    """
    Return a dictionary mapping the value a vertex store to the id of the community it is a part of.
    """
    if not isinstance(community, _Community):
        return {community.item: community}

    new_members = {}

    for member in community.members:
        new_members = new_members | get_all_members(community.members[member])

    return new_members
