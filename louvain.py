from classes import Graph, WeightedGraph, _Vertex


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
        communities, curr_modularity = find_best_communities_for_vertex(graph, vertex, communities,
                                                                           curr_modularity, adjacency_matrix)
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

    return communities, curr_modularity


def find_best_communities_for_vertex(graph: Graph,v: _Vertex, communities: dict[_Vertex, int], init_modularity: float,
                                     adjacency_matrix: dict[int, dict[int, int]]) -> (dict[_Vertex, int], float):
    """
    xxx
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
