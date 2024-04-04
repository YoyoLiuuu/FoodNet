from __future__ import annotations
import pre_processing
import visualize_graph
from louvain import louvain_algorithm, graph_to_weighted_graph, get_weighted_graph
from helper_functions import get_all_members

# all_data_vertices is a dictionary that maps id (item for _Vertex instances) to name of the restaurant
# graph, all_data_vertices = pre_processing.get_graph('test_nodes.txt', 'test_edges.txt')
graph, all_data_vertices = pre_processing.get_graph('fb-pages-food-nodes.txt', 'fb-pages-food-edges.txt')

# make adjacency matrix
adjacent_matrix = graph.make_adjacent_matrix()

# initialize communities with running the louvain algorithm on original graph
# getting the new best communities and modularity
the_communities, modularity = louvain_algorithm(graph, adjacent_matrix)

# create new_communities such that the keys are integers value instead of _Vertex instances
new_communities = {i.item: the_communities[i] for i in the_communities}

# sort the new communities such that the dictionary is ordered -> needed for creating weighted graph
sorted(new_communities.items(), key=lambda x: x[1])

# transform graph to weighted graph for louvain algorithm iteration
louvain_graph = graph_to_weighted_graph(graph)

# initialize modularity increase to be 0 (minimum modularity) for the last 3 runs
# this case, each graph will run louvain algorithm at least 3 times before it stops
modularity_increases = [1, 1, 1]

# iterate while the absolute value of the modularity gain is greater than 0.01 for the past 3 runs
# this indicates that the past 3 runs have made significant changes to the graph
# which means:
# 1. better communities are forming or
# 2. the algorithm have not yet find a community partition that is close to the best community partition
while all({abs(modularity_gain) > 0.01 for modularity_gain in modularity_increases[-3:]}):
    # create new louvain graph with each community as a vertex, in the new graph:
    # inner_weight = 2 * num of edges exists in a community of previous graph, representing community connectedness
    # edge weight = num of edges between 2 communities of the previous graph, representing graph connectedness
    # we want to maximize inner_weight and minimize edge weight. Edges weight is stored implicitly through neighbours
    # inner_weight is twice the edge weight because each edge has two vertices connected
    louvain_graph = get_weighted_graph(louvain_graph, new_communities)
    # create new adjacency matrix for weighted graph, each element represent edge weight
    adjacent_matrix = louvain_graph.make_adjacent_matrix()
    # store previous modularity to calculate modularity gain
    prev_modularity = modularity
    # run louvain on new graph for new best communities and best modularity
    the_communities, modularity = louvain_algorithm(louvain_graph, adjacent_matrix)
    # make new mappings such that key is integer values instead of _Vertex instances
    new_communities = {i.item: the_communities[i] for i in the_communities}
    # calculate modularity gain and append it to list such that the last three run modularity is updated
    modularity_increases.append(modularity - prev_modularity)

# initialize a list mapping from the name of the restaurant to its community
vertex_to_community = {}

# for each community in community, get all members of the community
for community in the_communities:
    members = get_all_members(community)
    # for each vertex of the community, add restaurant name - community pair to dictionary
    for vertex_value in members:
        vertex_to_community[all_data_vertices[vertex_value]] = the_communities[community]

# for the original graph before louvain community detection,
# update each vertex such that its .item attribute is the name of the restaurant
# this is for visualization such that human can understand better
for vertex in graph.vertices:
    graph.vertices[vertex].item = all_data_vertices[vertex]

