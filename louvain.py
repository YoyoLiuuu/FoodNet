from classes import Graph, WeightedGraph, _Vertex


def louvain_algorithm_init(graph: Graph, adjacency_matrix: dict[int, dict[int, int]]) -> (dict[_Vertex, int], float):
    """
    This function detects and forms communities using a modified version of the Louvain Algorithm
    """
    # initialize each vertex as its own community
    communities = {vertex: i for vertex in graph._vertices for i in range(len(graph._vertices))}
    curr_modularity = graph.calculate_modularity_graph(communities, adjacency_matrix)

    for vertex in graph._vertices.values():

        # merge communities based on modularity calculations
        communities, curr_modularity = find_best_communities_for_vertex(graph, vertex, communities,
                                                                           curr_modularity, adjacency_matrix)
        # get modularity of new communities

    return communities, curr_modularity


def find_best_communities_for_vertex(graph: Graph,v: _Vertex, communities: dict[_Vertex, int], init_modularity: float,
                                     adjacency_matrix: dict[int, dict[int, int]]) -> (dict[_Vertex, int], float):
    """
    xxx
    """
    best_community, best_modularity = communities[v], init_modularity
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
