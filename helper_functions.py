from classes import WeightedGraph
from __future__ import annotations
from typing import Optional
import csv

def set_to_dict(communities: list[set]) -> dict:
    dct = {}
    for i in range(0, len(communities)):
        for node in communities[i]:
            dct[node] = i
    return dct


"""def test():
    """
# Test
# function
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
"""


def get_graph(vertices: str, edges: str, max: Optional[int] = 600000) -> (WeightedGraph, dict[str, str]):
    """
    Create graph from the files
    """
    g = WeightedGraph()
    all_data_vertices = {}
    count = 0
    with open(vertices, mode='r', encoding='cp437') as file:
        reader = csv.reader(file)
        file.readline()
        for row in reader:
            all_data_vertices[int(row[2])] = row[1]
            g.add_vertex(int(row[2]))

            count += 1

            if count == max:
                break

    with open(edges, mode='r', encoding='cp437') as file:
        reader = csv.reader(file)
        valid_vertices = all_data_vertices.keys()

        for row in reader:
            v1 = int(row[0])
            v2 = int(row[1])
            if v1 in valid_vertices and v2 in valid_vertices:
                g.add_edge(v1, v2)

    return g, all_data_vertices, valid_vertices


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


def get_comm_id(all_communities: dict[int, int], community: [int, _Vertex]):
    """
    Return the id of a community
    """
    for c in community:
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
    >>> community1 = {1: g._vertices[1], 2: g._vertices[2], 3: g._vertices[3]}
    >>> community2 = {4: g._vertices[4], 5: g._vertices[5]}
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
    >>> community = {1: g._vertices[1], 2: g._vertices[2], 3: g._vertices[3]}
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
    >>> community = {1: g._vertices[1], 2: g._vertices[2]}
    >>> get_inner_edge_weights(community)
    1
    >>> community = {1: g._vertices[1], 2: g._vertices[2], 3: g._vertices[3]}
    >>> get_inner_edge_weights(community)
    3
    >>> g.add_vertex(4)
    >>> g.add_edge(3, 4)
    >>> get_inner_edge_weights(community)
    3
    >>> community = {1: g._vertices[1], 2: g._vertices[2], 3: g._vertices[3], 4: g._vertices[4]}
    >>> get_inner_edge_weights(community)
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
