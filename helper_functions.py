from __future__ import annotations
from classes import WeightedGraph, _Vertex, _Community


def get_weighted_graph(g: WeightedGraph, communities: dict[int, int]) -> WeightedGraph:
    """
    Return the weighted graph given the dictionary of communites, where each community is one vertex

    The community id will be a tuple with the sum of edge weights in the community and an
    identifying integer

    >>> ex_communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1}
    >>> g = WeightedGraph()
    >>> for i in range(1, 6):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> g.add_edge(3, 4)
    >>> g.add_edge(2, 5)
    >>> a_new_g = get_weighted_graph(g, ex_communities)
    >>> a_new_g.get_weight(0, 1)
    2
    """
    communities_lst = g.make_community_dicts(communities)
    new_g = WeightedGraph()
    outer_edges = get_all_outer_edges(communities_lst)

    for c in communities_lst:
        inner_edge_weight = get_inner_edge_weights(c)
        new_g.add_community(get_comm_id(communities, c), inner_edge_weight, c)

    new_outer_edges = get_edge_weights(communities, outer_edges)

    for edges in new_outer_edges:
        weight = edges[1]
        comm_ids = edges[0]

        new_g.add_edge(comm_ids[0], comm_ids[1], weight)

    return new_g


def get_comm_id(all_communities: dict[int, int], community: [int, _Vertex]) -> int:
    """
    Return the id of a community
    """
    c = next(iter(community))
    return all_communities[c]


def get_all_outer_edges(communities_lst: list[dict[int, _Vertex]]) -> list[set]:
    """
    Return a list of all outer edges in a graph given a list of communities
    >>> g = WeightedGraph()
    >>> for i in range(1, 6):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> g.add_edge(3, 4)
    >>> g.add_edge(4, 5)
    >>> g.add_edge(5, 2)
    >>> community1 = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
    >>> community2 = {4: g.vertices[4], 5: g.vertices[5]}
    >>> lst = get_all_outer_edges([community1, community2])
    >>> lst == [{3, 4}, {5, 2}] or lst == [{2, 5}, {3, 4}]
    True
    """
    all_outer_edges = []

    for c in communities_lst:
        all_outer_edges.extend([edge for edge in get_outer_edges(c) if edge not in all_outer_edges])

    return all_outer_edges


def get_outer_edges(community: dict[int, _Vertex]) -> list[set]:
    """
    Returns a list of sets, where the sets are outer edges

    >>> g = WeightedGraph()
    >>> for i in range(1, 5):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> g.add_edge(3, 4)
    >>> community = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
    >>> get_outer_edges(community)
    [{3, 4}]
    """
    outer_edges = []
    edge_visited = []  # improve runtime?
    for v in community:
        vertex = community[v]
        for u in vertex.neighbours:
            if {vertex, u} not in edge_visited and u.item not in community:
                outer_edges.append({v, u.item})

            edge_visited.append({vertex, u})

    return outer_edges


def get_inner_edge_weights(community: dict[int, _Vertex]) -> int:
    """
    Return sum of edge weights in a given community set

    >>> g = WeightedGraph()
    >>> for i in range(1, 4):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> a_community = {1: g.vertices[1], 2: g.vertices[2]}
    >>> get_inner_edge_weights(a_community)
    1
    >>> a_community = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
    >>> get_inner_edge_weights(a_community)
    3
    >>> g.add_vertex(4)
    >>> g.add_edge(3, 4)
    >>> get_inner_edge_weights(community)
    3
    >>> a_community = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3], 4: g.vertices[4]}
    >>> get_inner_edge_weights(a_community)
    4
    """
    edges_sum = 0
    edge_visited = []  # improve runtime with dictionary?
    for v in community:
        vertex = community[v]
        for u in vertex.neighbours:
            if {vertex, u} not in edge_visited and u.item in community:
                edges_sum += 1

            edge_visited.append({vertex, u})

    return edges_sum


def get_edge_weights(communities: dict[int, int], outer_edges: list[set]) -> \
        (list)[tuple[list[int], int]]:
    """
    Return a dictionary of edges with their new community ids and weights.
    Within the tuple, the edges are represented as a list with each element being a
    vertices and the edge weight is
    represented as an integer.

    As follows: ([community1 id, community2 id], weight)

    Preconditions
        - list(communites.values()) == sorted(communites.values())
        - every e in outer edges is an existing edge in a graph

    >>> ex_communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2}
    >>> outer_e = [{5, 2}, {4, 3}]
    >>> get_edge_weights(ex_communities, outer_e)
    [([0, 2], 1), ([0, 1], 1)]
    >>> ex_communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1}
    >>> get_edge_weights(ex_communities, outer_e)
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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'allowed-io': [],
        'max-line-length': 120,
        'max-nested-blocks': 4
    })